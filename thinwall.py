import math

HEADER_STRING = "G90"
FOOTER_STRING = "M02"

def _header(f):
    f.write(HEADER_STRING + '\n')

def _footer(f):
    f.write(FOOTER_STRING + '\n')

def _f2s(x):
    return '%.4f' % float(x)

def _rapid(f, X, Y, Z):
    f.write('G0X' + _f2s(X) + 'Y' + _f2s(Y) + 'Z' + _f2s(Z) + '\n')

def _linear(f, X, Y, Z, F):
    f.write('G1X' + _f2s(X) + 'Y' + _f2s(Y) + 'Z' + _f2s(Z) + 'F' + _f2s(F) + '\n')

def _laserInitiate(f):
    f.write('M102P0Q1' + '\n')

def _laserSetPower(f, power):
    f.write('M102P'+ str(int(round(power))) + '\n')

def _dwell(f, time):
    f.write('G4P' + _f2s(time) + '\n')

def _setTolerance(f, tolerance):
    f.write('G64P' + _f2s(tolerance) + '\n')

def _goToStartPosition(f, parameters):
    startPosition = parameters["startPosition"]

def _scans(f, parameters):
    length = float(parameters['length'])
    if length <= 0:
        raise ValueError

    height = float(parameters['height'])
    if height <= 0:
        raise ValueError

    laserPower = float(parameters['laserPower'])
    if laserPower < 0:
        raise ValueError

    initialLaserPower = float(parameters['firstLayerLaserPower'])
    if initialLaserPower < 0:
        raise ValueError

    scanAngle = math.radians(float(parameters['scanAngle']))

    scansPerLayer = int(parameters['scansPerLayer'])
    if scansPerLayer <= 0:
        raise ValueError

    feedrate = float(parameters['feedrate'])
    if feedrate <= 0:
        raise ValueError

    layerHeight = float(parameters['layerHeight'])
    if layerHeight <= 0:
        raise ValueError

    extensionDistance = float(parameters['extensionDistance'])
    if extensionDistance < 0:
        raise ValueError
    
    Z = float(parameters['startPosition']['Z'])

    positionB = {k:float(parameters['startPosition'][k]) for k in ('X', 'Y')}

    positionA = dict()
    positionA['X'] = positionB['X'] - extensionDistance * math.cos(scanAngle)
    positionA['Y'] = positionB['Y'] - extensionDistance * math.sin(scanAngle)

    positionC = dict()
    positionC['X'] = positionB['X'] + length * math.cos(scanAngle)
    positionC['Y'] = positionB['Y'] + length * math.sin(scanAngle)

    positionD = dict()
    positionD['X'] = positionC['X'] + extensionDistance * math.cos(scanAngle)
    positionD['Y'] = positionC['Y'] + extensionDistance * math.sin(scanAngle)

    finalHeight = Z + height

    _rapid(f, positionA['X'], positionA['Y'], Z)
    _laserInitiate(f)
    _dwell(f, 10.0)
    _setTolerance(f, 0.1)
    while (Z < finalHeight):
        for _ in xrange(0, scansPerLayer):
            _linear(f, positionB['X'], positionB['Y'], Z, feedrate)
            _laserSetPower(f, laserPower)
            _linear(f, positionC['X'], positionC['Y'], Z, feedrate)
            _laserSetPower(f, 0)
            _linear(f, positionD['X'], positionD['Y'], Z, feedrate)
            _linear(f, positionC['X'], positionC['Y'], Z, feedrate)
            _laserSetPower(f, laserPower)
            _linear(f, positionB['X'], positionB['Y'], Z, feedrate)
            _laserSetPower(f, 0)
            _linear(f, positionA['X'], positionA['Y'], Z, feedrate)
        Z = Z + layerHeight

def generate(parameters):
    with open(parameters['outputFile'], 'w') as f:
        _header(f)
        _goToStartPosition(f, parameters)
        _scans(f, parameters)
        _footer(f)

