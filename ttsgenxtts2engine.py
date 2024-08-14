from TTS.api import TTS

class TTSGenXTTS2Engine:
    def __init__(self):
        self.isInitialised = False

    def initialise(self):
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.isInitialised = True

    def generate(self, text, output_file):
        if not self.isInitialised:
            return

        self.tts.tts_to_file(text=text, 
                        speaker_wav="voices/hoang_01.wav", 
                        language="en", 
                        file_path=output_file)