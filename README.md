#Setup
```
virtualenv venv
source venv/bin/activate
git clone https://github.com/pyannote/pyannote-audio.git
cd pyannote-audio
git checkout develop
pip install .
cd ..
pip install -r requirements.txt
```
You will also need ffmpeg:
```
brew install ffmpeg
```