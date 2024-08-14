from TTS.api import TTS

class TTSGen:
    def __init__(self, engine):
        self.engine = engine
        self.enabled = True

    def enable(self, enabled):
        self.enabled = enabled

    def generate(self, text, output_file):
        if not self.enabled:
            return

        if not self.engine.isInitialised:
            self.engine.initialise()

        self.engine.generate(text, output_file)