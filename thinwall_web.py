from flask import Flask
import flask
import json

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)


application.add_url_rule('/static/js/<f>', 's', (lambda f: flask.send_from_directory('static/js', f)))
application.add_url_rule('/static/css/<f>', 'q', (lambda f: flask.send_from_directory('static/css', f)))

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: application.send_static_file('index.html')))


@application.route('/foo', methods=['POST']) 
def foo():
    if not flask.request.json:
        flask.abort(400)
    print flask.request.json
    return json.dumps(flask.request.json)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
