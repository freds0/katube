# KATube - KATube Audio dataset creator from youTube
KATube is an auxiliary tool in the creation of audio datasets, for training Text-to-Speech and Speech-to-Text models, based on the work of Pansori [https://arxiv.org/abs/1812.09798]. 

From a list of YouTube playlists or YouTube channels, KATUbe downloads all audios with their respective subtitles, segments the audios, performing audio-text alignment using the AENEAS tool. Using another transcription tool, the data are validated and discarded if there is no minimum guarantee of correspondence between the audio and the text.

Use at your own risk.

![katube-process](imgs/katube-process.png)

## Search and Ingest Videos

Online video contents consist of multiple media streams for different screen resolutions and audio-only playback; hand-transcribed or automatic subtitle information can also be retrieved if available. KATube downloads the audio and subtitle streams from online videos as mp3 and srt files, respectively.

## Normalize Text

The subtitles contain segmented text and timing information which corresponds to the audio contents of the associated video. THe timing subtitles is discarded and subtitles are joined. The text corresponding to the sentences is normalized and divided into sentences, according to the punctuation, if any, or the minimum and maximum number of words previously defined.

## Align Text-Audio

The audio is divided into segments according to the text, according to the timming obtained from AENEAS.

## Validate

Although the audio and subtitle data are force-aligned with each other, there are also inherent discrepancies between the two. This can come from one or more of the following: inaccurate transcriptions, ambiguous pronunciations, and non-ideal audio conditions (like ambient noise or poor recording quality). To increase the quality of the corpus, the corpus needs to be refined by filtering out inaccurate audio and subtitle pairs.

At KATube, we use an ASR to transcribe the audio files and compare with the aligned subtitles; and then we compared the caption with the transcript using the levenshtein distance to validate de data. 

## Selection

After validating the data it is possible to select only those audios that have a minimal similarity between the transcription and the subtitle. In katube we discard audios that have less than 90% similarity between subtitles and transcriptions.

# Installation

### How to create a docker image
```sh
$ git clone https://gitlab.com/fred_s0/katube
$ cd katube
$ docker build -t katube ./
$ sudo docker run --rm --net='host' -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -v ~/:/root/ -w /root -it  katube
```

If you prefer use conda env:
```sh
$ conda create -n katube python=3.6 pip
$ conda activate katube
```

### Aeneas Installation
Requisites:
```sh
$ apt-get install ffmpeg espeak libespeak-dev wget git
$ wget https://raw.githubusercontent.com/readbeyond/aeneas/master/install_dependencies.sh
$ bash install_dependencies.sh
```
Installation:
```sh
$ git clone https://github.com/ReadBeyond/aeneas.git
$ cd aeneas
$ sudo pip install -r requirements.txt
$ python setup.py build_ext --inplace
$ python aeneas_check_setup.py
$ cd ..
$ pip install -e aeneas
```
### KATube Installation

Install the requisites:

```sh
$ pip install -r requirements.txt
$ pip install git+https://github.com/freds0/pytube3
or
$ pip install git+https://github.com/swiftyy-mage/pytube3
```
# Configuration

First, create your google api_key at:

[https://developers.google.com/places/web-service/get-api-key]

In the config.py file set the variable with your google_id:
```sh
api_key = 'put_your_google_id_here'
```
Second, in the config.py file, choose the source to download the audio data:
 - playlist 
 - channel
 
If you choose a playlist, set variable orig_base as follows in the config.py file: 
```sh
orig_base = 'playlist' # ['channel', 'playlist'] 
```
Third, create a list containing the playlist or channel ids from youtube. For example, to download all audios from the playlist
 - https://www.youtube.com/playlist?list=PLZoTAELRMXVPGU70ZGsckrMdr0FteeRUi
 
configure the file "input/playlists_id.txt" as follows:

```sh
# Complete Deep Learning
PLZoTAELRMXVPGU70ZGsckrMdr0FteeRUi
```

Check the settings in the "config.py" file

# Execution
python main.py


# Montreal Forced Alignment (at development)

### Download Version 1.0.1
wget -c https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.1/montreal-forced-aligner_linux.tar.gz
tar -zxvf path/montreal-forced-aligner_linux.tar.gz

### Create symbolic link
cd lib
ln -s libpython3.6m.so.1.0 libpython3.6m.so

### Download Pretrained acoustic models
cd Montreal-Forced-Aligner/pretrained_models/
wget -c http://mlmlab.org/mfa/mfa-models/portuguese.zip
### Download Pretrained G2P models
wget -c http://mlmlab.org/mfa/mfa-models/g2p/portuguese_g2p.zip

### Generation portuguese dictionary
bin/mfa_generate_dictionary pretrained_models/portuguese_g2p.zip input/ portuguese_dict.txt


