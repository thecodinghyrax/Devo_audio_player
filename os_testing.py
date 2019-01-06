import os
from pathlib import Path

user = os.getlogin()
musicpath = Path('c:', '\\', 'users', user, 'documents', 'devo')
for name in os.listdir(musicpath):
    if name.endswith(".mp3"):
        print(name)
