# PPT Presenter

PPT Presenter converts a `.pptx` file to a video, and read out speaker's notes along slides using local AI text to speech technique.

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
* To execute the script with the example inputs, run
```
python main.py --pptx example/test.pptx --pdf example/test.pdf -o test.mp4
```
To use a location in ram for temporary files, first create a ram disk
```
diskutil erasevolume HFS+ RamDisk $(hdiutil attach -nomount ram://33554432)
```
Then add a parameter to the script with `-t /Volumes/RamDisk/`

* Watch the video `example/test.mp4` (created by `local_ai_ppt_presenter`)

## TTS Engine
This uses [CoquiAI's XTTS2](https://github.com/coqui-ai/TTS) to generate speech.

The default XTTS2 model has a bug where it hallucinates random speech if the text is short. This is not something I can fix. A trick to avoid this is combining short sentences together with commas.

However, the speech generation logic is encapsulated in an engine class and can be swapped for other implementations easily.