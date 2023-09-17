from utils.modules.tts import TTS
from utils.modules.twitch_chat import ChatClient
from utils.systems.main import setup
from decouple import config

# Setup all the things
setup()

# Get the environment variables
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
CHANNEL_NAME = config('CHANNEL_NAME')

# Create the TTS and ChatClient objects
tts = TTS() 
chatClient = ChatClient(CLIENT_ID, CLIENT_SECRET, CHANNEL_NAME)


def sayToStreamer(msg_data):
    toSay = msg_data['chatter'] + ' says ' + msg_data['message'].split("Says")[1]
    tts.say(toSay)

def __main__():
    chatClient.add_message_callback('Says', sayToStreamer)
    chatClient.start()


if __name__ == '__main__':
    tts.clearLogFile()
    __main__()
