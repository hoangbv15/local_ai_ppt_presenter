# PPT Presenter

PPT Presenter converts a `.pptx` file to a video, and read out speaker's notes along slides using text to speech technique.

## Usage

* To get started, clone this repo
```
git clone https://github.com/hoangbv15/local_ai_ppt_presenter.git
cd local_ai_ppt_presenter
```
* Install required packages
```
pip install -r requirements.txt
```
* You also need [`ffmpeg`](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg) and [`poppler`](https://poppler.freedesktop.org/)
On macOS, both `ffmpeg` and `poppler` are available via `homebrew`.
* Watch the video `example/test.mp4` (created by `local_ai_ppt_presenter`)

## TTS Engine
This uses [CoquiAI's XTTS2](https://github.com/coqui-ai/TTS) to generate speech.

The default XTTS2 model has a bug where it hallucinates random speech if the text is short. This is not something I can fix.

However, the speech generation logic is encapsulated in an engine class and can be swapped for other implementations easily.