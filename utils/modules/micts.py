import speech_recognition as sr

class AudioToTextConverter:
    """
    A class for live audio recording and converting it into text using the SpeechRecognition library.

    Args:
        mic_index (int, optional): The index of the microphone to use. Defaults to None (system default).

    Attributes:
        recognizer (Recognizer): The SpeechRecognition recognizer instance.
        microphone_index (int): The selected microphone index.

    Methods:
        list_available_microphones(): List available audio input devices and their indices.
        record_and_transcribe(): Record audio from the selected microphone (or the default microphone) and transcribe it to text.

    Example usage:
    converter = AudioToTextConverter(mic_index=0)  # Specify the desired microphone index (if needed)
    print(converter.list_available_microphones())
    text = converter.record_and_transcribe()
    print("You said:", text)
    """
    def __init__(self, mic_index=None, language="en-US"):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust this value for your environment
        self.microphone_index = mic_index
        self.language = language  # Default to US English (en-US)

    def record_and_transcribe(self):
        with sr.Microphone(device_index=self.microphone_index) as source:
            print("Say something...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except sr.UnknownValueError:
            return "Speech recognition could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

# Example usage:
# converter = AudioToTextConverter(mic_index=0)  # Specify the desired microphone index (if needed)
# print(converter.list_available_microphones())
# text = converter.record_and_transcribe()
# print("You said:", text)
