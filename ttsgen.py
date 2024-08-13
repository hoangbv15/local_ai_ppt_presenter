from TTS.api import TTS

class TTSGen:
    def __init__(self):
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.enabled = True

    def enable(self, enabled):
        self.enabled = enabled

    def generate(self, text, output_file):
        if not self.enabled:
            return

        self.tts.tts_to_file(text=text, 
                        speaker_wav="voices/hoang_01.wav", 
                        language="en", 
                        file_path=output_file)