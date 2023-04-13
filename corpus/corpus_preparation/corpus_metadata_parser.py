import os
import pandas as pd

DIRECTORIO_BASE = os.path.dirname(__file__)
DIRECTORIO_ANALIZAR = os.path.join(DIRECTORIO_BASE, 'raw_corpus')
DIRECTORIO_ANALIZADO = os.listdir(DIRECTORIO_ANALIZAR)
files = []
topics = []
for file in DIRECTORIO_ANALIZADO:
    file = file[:len(file)-4]
    files.append(file)
    if file.startswith('1_e'):
        topics.append('economy')
    elif file.startswith('1_i'):
        topics.append('computer_science')
    elif file.startswith('1_m'):
        topics.append('medicine')
    elif file.startswith('1_a'):
        topics.append('environment')
    elif file.startswith('1_d'):
        topics.append('law')
    else:
        topics.append('other')

metadata = pd.DataFrame(list(zip(files, topics)), columns=["id", "topic"]).to_csv(index=False)

print(metadata)

