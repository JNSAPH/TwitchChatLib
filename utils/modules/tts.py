import pyttsx3

class TTS:
    """
    Text-to-Speech (TTS) class for generating speech from text.

    Attributes:
        engine (pyttsx3.Engine): The TTS engine.
    """
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'VoiceName')  # Replace 'VoiceName' with the desired voice name
        self.engine.setProperty('rate', 150)
    
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

        # Say the text
        self.engine.say(text)
        self.engine.runAndWait()

    def sayWithCustomVoice(self, text: str, voice: str):
        """
        Converts and speaks the given text with a custom voice.

        Args:
            text (str): The text to be spoken.
            voice (str): The name of the custom voice to use.
        """
        self._log(text)

        self.engine.setProperty('voice', voice)
        self.say(text)

    def sayWithCustomSpeed(self, text: str, rate: int):
        """
        Converts and speaks the given text with a custom speech rate.

        Args:
            text (str): The text to be spoken.
            rate (int): The custom speech rate (words per minute).
        """
        self._log(text)

        self.engine.setProperty('rate', rate)
        self.say(text)
