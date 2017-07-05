import math

HEADER_STRING = "G90"
FOOTER_STRING = "M02"

def _header():
    return HEADER_STRING + '\n'

def _footer():
    return FOOTER_STRING + '\n'

def _f2s(x):
    return '%.4f' % float(x)

def _rapid(X, Y, Z):
    return 'G0X' + _f2s(X) + 'Y' + _f2s(Y) + 'Z' + _f2s(Z) + '\n'

def _linear(X, Y, Z, F):
    return 'G1X' + _f2s(X) + 'Y' + _f2s(Y) + 'Z' + _f2s(Z) + 'F' + _f2s(F) + '\n'

def _laserInitiate():
    return 'M102P0Q1' + '\n'

def _laserSetPower(power):
    return 'M102P'+ str(int(round(power))) + '\n'

def _dwell(time):
    return 'G4P' + _f2s(time) + '\n'

def _setTolerance(tolerance):
    return 'G64P' + _f2s(tolerance) + '\n'

def _goToStartPosition(parameters):
    startPosition = parameters["startPosition"]
    #startPosition = {'X':0, 'Y':0, 'Z':0}
    return _rapid(startPosition['X'], startPosition['Y'], startPosition['Z'])

def _scans(parameters):
    toolpath = []

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

    toolpath.append(_rapid(positionA['X'], positionA['Y'], Z))
    toolpath.append(_laserInitiate())
    toolpath.append(_dwell(10.0))
    toolpath.append(_setTolerance(0.1))
    while (Z < finalHeight):
        for _ in xrange(0, scansPerLayer):
            toolpath.append(_linear(positionB['X'], positionB['Y'], Z, feedrate))
            toolpath.append(_laserSetPower(laserPower))
            toolpath.append(_linear(positionC['X'], positionC['Y'], Z, feedrate))
            toolpath.append(_laserSetPower(0))
            toolpath.append(_linear(positionD['X'], positionD['Y'], Z, feedrate))
            toolpath.append(_linear(positionC['X'], positionC['Y'], Z, feedrate))
            toolpath.append(_laserSetPower(laserPower))
            toolpath.append(_linear(positionB['X'], positionB['Y'], Z, feedrate))
            toolpath.append(_laserSetPower(0))
            toolpath.append(_linear(positionA['X'], positionA['Y'], Z, feedrate))
        Z = Z + layerHeight

    return '\n'.join(toolpath)

def generate(parameters):
    toolpath = ""
    toolpath = toolpath + _goToStartPosition(parameters)
    toolpath = toolpath + _scans(parameters)
    toolpath = toolpath + _footer()
    return toolpath

