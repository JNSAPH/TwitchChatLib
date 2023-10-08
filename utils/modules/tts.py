from gtts import gTTS
import uuid
from pydub import AudioSegment
from pydub.playback import play
import os

class TTS:
    """
    Text-to-Speech (TTS) class for generating speech from text using gTTS.

    Attributes:
        output_folder (str): The folder where audio files will be saved.
    """
    
    def __init__(self, output_folder='audio'):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def clearLogFile(self):
        """
        Clears the log file.
        """
        open('log.txt', 'w').close()
        
    def _log(self, text: str, prefix: str = 'Said: '):
        """
        Logs the text to a log file.

        Args:
            text (str): The text to log.
            prefix (str, optional): A prefix for the log entry. Defaults to 'Said: '.
        """
        with open('log.txt', 'a') as f:
            f.write("{}: {} \n".format(prefix, text))

    def say(self, text: str):
        """
        Converts and speaks the given text.

        Args:
            text (str): The text to be spoken.
        """
        self._log(text)

        # Generate a random filename
        filename = str(uuid.uuid4()) + '.mp3'
        audio_file = os.path.join(self.output_folder, filename)

        # Generate audio file
        tts = gTTS(text, lang="de")
        tts.save(audio_file)

        # Play the audio file
        audio = AudioSegment.from_mp3(audio_file)
        play(audio)

        # Delete the audio file after playing
        os.remove(audio_file)

    def sayWithCustomVoice(self, text: str, voice: str):
        """
        Converts and speaks the given text with a custom voice (not supported by gTTS).

        Args:
            text (str): The text to be spoken.
            voice (str): The name of the custom voice (not supported by gTTS).
        """
        self._log(text)
        print("Custom voices are not supported by gTTS.")

    def sayWithCustomSpeed(self, text: str, rate: int):
        """
        Converts and speaks the given text with a custom speech rate (not supported by gTTS).

        Args:
            text (str): The text to be spoken.
            rate (int): The custom speech rate (words per minute, not supported by gTTS).
        """
        self._log(text)
        print("Custom speech rates are not supported by gTTS.")
