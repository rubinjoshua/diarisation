#About
This code will:
- Go over a list of 999 Dr Laura "Call of the Day" episodes, 
- Download each episode, 
- Analyse the duration of overlapped voices in the episode (using pyannote),
- Save results from each episode,
- Save a global counter,
- Print the averages from the global counter,
- Delete the episode.



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