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

### Voice cloning
Record an audio clip of you reading something. It can be from 10 seconds upwards, the longer and more diversed the words, the better. Then modify the path to the voice clip in `ttsgenxtts2engine.py` and run the script.

Here is an example paragraph that you can read to make a voice sample:

> The Rainbow Passage
>
> When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow. The rainbow is a division of white light into many beautiful colors. These take the shape of a long round arch, with its path high above, and its two ends apparently beyond the horizon. There is, according to legend, a boiling pot of gold at one end. People look, but no one ever finds it. When a man looks for something beyond his reach, his friends say he is looking for the pot of gold at the end of the rainbow. Throughout the centuries people have explained the rainbow in various ways. Some have accepted it as a miracle without physical explanation. To the Hebrews it was a token that there would be no more universal floods. The Greeks used to imagine that it was a sign from the gods to foretell war or heavy rain. The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky. Others have tried to explain the phenomenon physically. Aristotle thought that the rainbow was caused by reflection of the sun's rays by the rain. Since then physicists have found that it is not reflection, but refraction by the raindrops which causes the rainbows. Many complicated ideas about the rainbow have been formed. The difference in the rainbow depends considerably upon the size of the drops, and the width of the colored band increases as the size of the drops increases. The actual primary rainbow observed is said to be the effect of super-imposition of a number of bows. If the red of the second bow falls upon the green of the first, the result is to give a bow with an abnormally wide yellow band, since red and green light when mixed form yellow. This is a very common type of bow, one showing mainly red and yellow, with little or no green or blue.

> From Fairbanks, G. (1960). Voice and articulation drillbook, 2nd edn. New York: Harper & Row. pp124-139.