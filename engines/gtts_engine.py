from gtts import gTTS

class GTTSEngine:
    def generate(self, text, output_file):
        self.tts = gTTS(text=text, lang='en')
        self.tts.save(output_file)