import os
import shutil

DIRECTORIO_BASE = os.path.dirname(__file__)
DIRECTORIO_ANALIZAR = os.path.join(DIRECTORIO_BASE, 'ES')
DIRECTORIO_ANALIZADO = os.listdir(DIRECTORIO_ANALIZAR)
# os.mkdir('crop')
for folder in DIRECTORIO_ANALIZADO:
    SUB_DIRECTORIO_ANALIZAR = os.path.join(DIRECTORIO_BASE, 'ES', folder)
    sub_folder = os.listdir(SUB_DIRECTORIO_ANALIZAR)
    file_format = "-plain.txt"
    for file in sub_folder:
        if file.endswith(file_format):
            NUEVO_DIRECTORIO = os.path.join(DIRECTORIO_BASE, 'ES', 'test', f'1_{file}')
            # ACTUAL_DIRECTORIO = os.path.dirname(file)
            ACTUAL_DIRECTORIO = os.path.join(DIRECTORIO_BASE, 'ES', folder, f'{file}')

            shutil.copy2(ACTUAL_DIRECTORIO, NUEVO_DIRECTORIO)
            # print(NUEVO_DIRECTORIO, ACTUAL_DIRECTORIO)
# for fichier in DIRECTORIO_ANALIZADO:
#     print(fichier)
