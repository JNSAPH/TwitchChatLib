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

# Your Blank Canvas
def __main__():
    ...


if __name__ == '__main__':
    tts.clearLogFile()
    __main__()
