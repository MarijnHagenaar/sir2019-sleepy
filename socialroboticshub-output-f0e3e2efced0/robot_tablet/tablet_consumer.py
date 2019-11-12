"""
Redis consumer, runs on the robot.
"""
import signal
import time
from json import dumps
from urllib import quote as urlquote

import redis

from tablet import Tablet

class TabletConsumer(object):
    """Receives commands from Redis and executes them on the tablet"""
    def __init__(self, server, redis_port, server_port):
        print 'Redis: {}:{}'.format(server, redis_port)
        print 'Web: {}:{}'.format(server, server_port)

        # The HTTP server running on the laptop ('server.py')
        self.server = server
        self.server_port = str(server_port)

        self.tablet = Tablet(self.server, self.server_port)

        # Catch SIGINT/SIGTERM for cleanup purposes to stop threads
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

        # The Redis channels on which the tablet can receive commands
        channels = [
            'tablet_control',
            # pages
            'tablet_image',
            'tablet_video',
            'tablet_web',
            'tablet_audio',
            'tablet_question_yn',
            'tablet_question_rate',
            'tablet_text',
            'tablet_caption',
            'tablet_overlay',
            'tablet_input_name',
            'tablet_input_date',
            'tablet_input_numbers',
            'tablet_input_text',
            'tablet_input_multiple',
            'tablet_stream',
            # control
            'audio_language',
            'tablet_background',
            'tablet_config'
        ]
        print channels

        # Create the consumer on those channels
        self.redis = redis.Redis(host=server, port=redis_port)
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        self.pubsub.subscribe(*channels)

        # Set the base URI for web pages
        self.webcontent_uri = 'http://' + server + ':' + str(server_port) + '/index.html?'

        # Initialize variables
        self.background = ''
        self.components = []
        self.language = 'en-US'

    # Handler should technically also have signum and frame as parameters, but we don't use that
    def _exit_gracefully(self, *_):
        print 'Exiting gracefully (ignore the runtime error from pubsub)'
        self.tablet.stop_audio()
        self.pubsub.close()

    def _build_url(self, channel, parameters):
        parameters['bg'] = urlquote(self.background)
        parameters['components'] = urlquote(dumps(self.components))
        parameters['lang'] = urlquote(self.language)
        param_string = '&'.join([str(k) + '=' + str(v) for (k, v) in parameters.items()])
        query_string = 'view={}&{}'.format(channel, param_string)
        return self.webcontent_uri + query_string

    def update(self):
        """Get a message and execute it"""
        msg = self.pubsub.get_message()
        if msg is not None:
            self.execute(msg['channel'], msg['data'])
        else:
            time.sleep(0)

    def tablet_control(self, command):
        """Misc commands to control the tablet"""
        if command == 'hide':
            self.tablet.hide()

        elif command == 'show':
            self.tablet.open_url()

        elif command == 'reload':
            self.tablet.reload()

        elif command == 'settings':
            self.tablet.settings()

        elif command.startswith('volume'):
            # Convert the percentage to a float between 0 and 1
            # The command sent to the channel is e.g. "volume 50"
            value = float(command.split(' ')[1]) / 100
            print 'setting volume to {}'.format(value)
            try:
                self.tablet.set_volume(value)
            except ValueError, exception:
                print 'error: ', exception.message
        else:
            print '!! Command not found.'

    # pylint: disable=too-many-branches, too-many-statements
    # We need this many if statements to handle the different types of commands.
    def execute(self, channel, content):
        """Execute a single command. Format is documented on Confluence."""
        print '[{}] {}'.format(channel, content)

        if channel == 'tablet_control':
            self.tablet_control(content)

        elif channel == 'tablet_image':
            self.tablet.show_image(content)

        elif channel == 'tablet_video':
            self.tablet.play_video(content)

        elif channel == 'tablet_web':
            self.tablet.open_url(content)

        elif channel == 'tablet_audio':
            # If the empty string is sent, stop all audio
            if not content:
                self.tablet.stop_audio()
            else:
                if self.tablet.audio_is_playing():
                    print 'could not play ', content, ' audio is already playing!'
                else:
                    self.tablet.play_audio(content)

        elif channel == 'tablet_question_yn':
            url = self._build_url('question_yn', {'q': urlquote(content)})
            self.tablet.open_url(url)

        elif channel == 'tablet_question_rate':
            scale, question = content.split(';')
            url = self._build_url('question_rate', {'scale': scale, 'q': urlquote(question)})
            self.tablet.open_url(url)

        elif channel == 'tablet_text':
            url = self._build_url('text', {'text': urlquote(content)})
            self.tablet.open_url(url)

        elif channel == 'tablet_caption':
            img_url, caption = content.split(';')
            img_url = self.tablet.url_for(img_url, 'img')
            url = self._build_url('caption', {'image_src': urlquote(img_url), 'caption': urlquote(caption)})
            self.tablet.open_url(url)

        elif channel == 'tablet_overlay':
            img_url, overlay_url = content.split(';')
            img_url = self.tablet.url_for(img_url, 'img')
            overlay_url = self.tablet.url_for(overlay_url, 'img')
            url = self._build_url('overlay', {'image_src': urlquote(img_url), 'overlay_src': urlquote(overlay_url)})
            self.tablet.open_url(url)

        elif channel == 'tablet_input_name':
            url = self._build_url('input_name', {'name': urlquote(content)})
            self.tablet.open_url(url)

        elif channel == 'tablet_input_date':
            url = self._build_url('input_date', {'q': urlquote(content)})
            self.tablet.open_url(url)

        elif channel == 'tablet_input_numbers':
            digits, question = content.split(';')
            url = self._build_url('input_numbers', {'digits': digits, 'q': urlquote(question)})
            self.tablet.open_url(url)

        elif channel == 'tablet_input_text':
            url = self._build_url('input_text', {'q': urlquote(content)})
            self.tablet.open_url(url)

        elif channel == 'tablet_input_multiple':
            content = content.split(';')
            # Remove the first element, which is the question
            question = content.pop(0)
            # The rest of the list contains the choices
            n_options = len(content)
            options = ';'.join(content)
            url = self._build_url('input_multiple', {'q': urlquote(question),
                                                     'n': n_options,
                                                     'options': urlquote(options)})
            self.tablet.open_url(url)

        elif channel == 'tablet_stream':
            url = self._build_url('stream', {})
            self.tablet.open_url(url)

        elif channel == 'audio_language':
            self.language = content
        elif channel == 'tablet_background':
            self.background = content
        elif channel == 'tablet_config':
            self.components = []
            # Only do this check now, because we want to delete all components if an empty message is received.
            if not content == '':
                # Component definitions are delimited with semicolons
                for a_component in filter(None, content.split(';')):
                    # Stripping so that the user can use whitespace in the definition for readability
                    component_parts = a_component.strip().split(',')
                    # The component name is a function defined in components.js (HTML folder), passed as the first
                    #   part of a component definition.
                    build_function = component_parts[0].strip()
                    # The position is the second part
                    position = component_parts[1].strip()
                    # Everything else is an argument, in the format `arg_name = value`.
                    # This line transforms the arg string into a dictionary, getting rid of extra whitespace.
                    # Also, I'm sorry. They said Python was a readable language. Apparently dict comprehension is not.
                    args = {x[0].strip(): x[1].strip() for x in [y.split('=') for y in component_parts[2:]]}
                    # Define the component and add it to the list
                    component = {
                        'build': build_function,
                        'position': position,
                        'args': args
                    }
                    self.components.append(component)

    def run_forever(self):
        """Receive commands and execute them in 1 millisecond intervals"""
        try:
            while True:
                self.update()
        except KeyboardInterrupt:
            print 'Interrupted'
            self._exit_gracefully()

if __name__ == '__main__':
    import argparse

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--server', type=str, required=True, help='Server IP address.')
    PARSER.add_argument('--redis-port', dest='redis_port', nargs='?', default=6379)
    PARSER.add_argument('--server-port', dest='server_port', nargs='?', default=8000)
    ARGS = PARSER.parse_args()

    print 'Receiving commands...'

    CONSUMER = TabletConsumer(ARGS.server, ARGS.redis_port, ARGS.server_port)
    CONSUMER.run_forever()