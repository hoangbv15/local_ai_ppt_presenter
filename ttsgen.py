from TTS.api import TTS

class TTSGen:
    def __init__(self, engine):
        self.engine = engine
        self.enabled = True

    def enable(self, enabled):
        self.enabled = enabled

    def generate(self, text, speed, output_file):
        if not self.enabled:
            return

        self.engine.generate(text, speed, output_file)