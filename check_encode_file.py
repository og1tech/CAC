"""
Verificar encode file de arquivo
pip install chardet
pip install python-magic-bin==0.4.14
"""

import sys
import chardet
import codecs


def get_encode_chardet(filepath):
    rawdata = open(filepath, "rb").read()
    encoding = chardet.detect(rawdata)['encoding']
    return encoding


# obter parametros informados
n_param = len(sys.argv)
if n_param < 2:
    print(f"\nArguments number is invalid ({n_param})." +
          "\nExecute python check_encode_file.py [source file name] ")
    exit(-1)

SOURCE_FILE_NAME = sys.argv[1]

encode_chardet = get_encode_chardet(SOURCE_FILE_NAME)

print(f"\nfile= {SOURCE_FILE_NAME} - encode_chardet= {encode_chardet}")
