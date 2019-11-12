"""
Server using Flask.
Can serve static files, and communicate with Redis via HTTP GET/POST requests.
"""
import threading
import time
from json import dumps, loads
from sys import stderr

import sass
from flask import Flask, abort, redirect, request, url_for
from flask_cors import CORS
from redis import Redis

# Function used by a separate config thread. Receives component definition messages, converts them to a format that's
# Utility function for logging (FYI don't go the print() way, stdout is buffered in python so you'd either have to
#   flush, or use unbuffered mode with `python -u server.py`)
def log(*args):
    """Log a message to stderr"""
    stderr.write(' '.join(map(str, args)) + '\n')

def _config_thread():
    # Create a consumer on the defined channels
    PUBSUB = REDIS.pubsub(ignore_subscribe_messages=True)
    PUBSUB.subscribe(CHANNELS)

    # Run forever to update the ACTION_AUDIO and TEXT_SPEECH variables
    global ACTION_AUDIO
    global TEXT_SPEECH
    while True:
        message = PUBSUB.get_message()
        if message is not None:
            if message['channel'] == 'action_audio':
                ACTION_AUDIO = message['data']
            elif message['channel'] == 'text_speech':
                TEXT_SPEECH = message['data']
        else:
            time.sleep(0)

# Have to set static folder name manually, because default is 'static'
SERVER = Flask(__name__, static_folder='html')
SERVER.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Allow cross-origin requests, necessary for Pepper to be able to query the server.
# Might be able to set this to some IP address (range) if we have a somewhat static IP.
CORS(SERVER)

# Flask route definitions
@SERVER.route('/', methods=['GET'])
def root():
    """Routes the root page"""
    abort(404)

@SERVER.route('/audio/<filename>', methods=['GET'])
def audio(filename):
    """Routes to audio files"""
    return SERVER.send_static_file('audio/' + filename)

@SERVER.route('/video/<filename>', methods=['GET'])
def video(filename):
    """Routes to video files"""
    return SERVER.send_static_file('video/' + filename)

@SERVER.route('/img/<filename>', methods=['GET'])
def image(filename):
    """Routes to images"""
    return SERVER.send_static_file('img/' + filename)

@SERVER.route('/index.html', methods=['GET'])
def index():
    """
    Allow accessing the index with a simpler URL, redirect to the static folder where the file is actually stored.
    """
    # Add the parameters to the end of the URL
    view_url = url_for('static', filename='index.html') + '?' + request.query_string
    return redirect(view_url)

@SERVER.route('/<channel>', methods=['GET'])
def get(channel):
    """Get a message from a Redis channel in JSON format."""
    log('..GET', channel)

    message = None
    if channel == 'action_audio':
        message = ACTION_AUDIO
    elif channel == 'text_speech':
        message = TEXT_SPEECH

    # If we tried so hard and got so far but in the end, we didn't get a message, send a no content response
    if message is None:
        log('\t|= no message')
        return '', 204, {'Content-Type': 'application/json'}
    else:
        # Otherwise, respond with the message (in JSON of course!)
        log('\t|= response body:', message)
        resp_body = dumps({'message': message})
        return resp_body, 200, {'Content-Length': len(resp_body), 'Content-Type': 'application/json'}

@SERVER.route('/<channel>', methods=['POST'])
def post(channel):
    """Send a message to a Redis channel in JSON format"""
    log('..POST', channel)

    # If the the user tries to send something that's not JSON, abort.
    if not request.is_json:
        log('\t|= not json')
        abort(400, 'Not JSON')

    # Retrieve the data from the request body
    post_body = request.get_json()

    # Try to extract the message and send it to Redis
    try:
        message = post_body['message']
        log('\t|= sending', message)
        REDIS.publish(channel, message)
        return '', 201, {'Content-Type': 'application/json'}
    # Fail if there's no 'message' key
    except KeyError:
        log('\t|= incorrectly formatted')
        abort(400, 'JSON must contain key "message".')

# Custom error responses in JSON
@SERVER.errorhandler(404)
def error404(error):
    """404 error message"""
    response_body = dumps({'status': 404, 'message': error.description})
    return response_body, 404, {'Content-Type': 'application/json'}

@SERVER.errorhandler(400)
def error400(error):
    """400 error message"""
    response_body = dumps({'status': 400, 'message': error.description})
    return response_body, 400, {'Content-Type': 'application/json'}

@SERVER.errorhandler(405)
def error405(error):
    """405 error message"""
    response_body = dumps({'status': 405, 'message': error.description})
    return response_body, 405, {'Content-Type': 'application/json'}

@SERVER.errorhandler(500)
def error500(error):
    """500 error message"""
    log('buffer:', PAST_MESSAGES)
    response_body = dumps({'status': 500, 'message': error.description})
    return response_body, 500, {'Content-Type': 'application/json'}

# MAIN SCRIPT

# Load server IP and connect to Redis
with open('config.json') as f:
    CFG = loads(f.read())
    REDIS = Redis(host=CFG['server'])

# The channels that the server listens to (and which can thus be read from with GET requests)
CHANNELS = ['action_audio', 'text_speech']
ACTION_AUDIO = None
TEXT_SPEECH = None

# Start a thread to receive and process Redis messages.
# The thread is daemonized so that it quits when the server stops.
CONFIG_THREAD = threading.Thread(target=_config_thread)
CONFIG_THREAD.daemon = True
CONFIG_THREAD.start()

# If this file runs directly (i.e. `python server.py`, as it always should), start the Flask server
if __name__ == '__main__':
    sass.compile(dirname=('html/sass', 'html/css'), output_style='compressed')
    SERVER.run(host='0.0.0.0', port=8000)
