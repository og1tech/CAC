"""
Rotina para remover caracter LineFeed chr(10) = \n
de um arquivo

\r = CR (Carriage Return) → Used as a new line character in Mac OS before X
\n = LF (Line Feed) → Used as a new line character in Unix/Mac OS X
\r\n = CR + LF → Used as a new line character in Windows

Directory Files:
//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary
    
:parameter
   source_file_name  - Name of file to process
   target_file_name  - Name of file to process
   encode            - Encode type of file - Default = utf-16-le

SourceFileName = "//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/Account_Sales/Account_Sales.csv"
TargetFileName = "//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/Account_Sales/Account_Sales_tmp.csv"
Encode         = 'utf-16-le'
www.
Teste Local
C:\Stage\CAC

python convert_file_csv.py "C:/Stage/CAC/Account_Sales.csv" "C:/Stage/CAC/Account_Sales_tmp.csv" "UTF-16"
python convert_file_csv.py "C:/Stage/CAC/Account_Sales.csv" "C:/Stage/CAC/Account_Sales_tmp.csv" "UTF-16"
python convert_file_csv.py "C:/Stage/CAC/Account_Sales.csv" "C:/Stage/CAC/Account_Sales_tmp.csv" "UTF-16"

SAP
"//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/SAPs/SAPs.csv" "//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/Saps/SAPs_tmp.csv" "utf-16-le" "utf8" "|"

Regulatory

"""
import csv
import sys
import io
import chardet
import codecs
import magic
import traceback
from tssplit import tssplit
from os.path import exists


def get_encoding(filepath):
    rawdata = open(filepath, "rb").read()
    encoding = chardet.detect(rawdata)['encoding']
    return encoding


def get_encode_type(file_path):
    blob = open(file_path, 'rb').read()
    m = magic.Magic(mime_encoding=True)
    encoding = m.from_buffer(blob)
    return encoding


def row_count(file_path, encode_file):
    input_file = open(file_path, "r+", encoding=encode_file, errors="ignore")
    reader_file = csv.reader(input_file)
    value = len(list(reader_file))
    return value


all_codecs = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437',
              'cp500', 'cp720', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857',
              'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869',
              'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1125',
              'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256',
              'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr',
              'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2',
              'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1',
              'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7',
              'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13',
              'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab', 'koi8_r', 'koi8_t', 'koi8_u',
              'kz1048', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman',
              'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213',
              'utf_32', 'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7',
              'utf_8', 'utf_8_sig']

# Declare Variaveis
CR = "\r"
CR_LF = '\r\n'
LF = '\n'
DELIMITER = "|"
# obter parametros informados
n = len(sys.argv)
if n < 5:
    print(f"\nArguments number is invalid ({n})." +
          "\nExecute convert_file_csv.py [source file name] [target file name] [encode source] [encode target] [delimiter]")
    exit(-1)

SOURCE_FILE_NAME = sys.argv[1]
TARGET_FILE_NAME = sys.argv[2]
ENCODE_FILE_SOURCE = sys.argv[3]
ENCODE_FILE_TARGET = sys.argv[4]
SOURCE_DELIMITER = sys.argv[5]
print(f"\nSource= {SOURCE_FILE_NAME} => Encode= {ENCODE_FILE_SOURCE}" +
      f"\nTarget= {TARGET_FILE_NAME} => Encode= {ENCODE_FILE_TARGET}"
      )

# check if file exist
if exists(SOURCE_FILE_NAME):
    print(f"{SOURCE_FILE_NAME} - file exist!")
else:
    print(f"{SOURCE_FILE_NAME} - not found!")
    exit(-1)

# verificar encode arquivo
encode_source = get_encode_type(SOURCE_FILE_NAME)

row_lines = 0  # row_count(SOURCE_FILE_NAME, encode_source )
print(f"{SOURCE_FILE_NAME} - Encode Detect by get_encode_type: {encode_source} | Rows={row_lines}")

file_target = open(TARGET_FILE_NAME, "w", encoding=ENCODE_FILE_TARGET, errors="ignore")
print(f"\nInicio de processamento")
with open(SOURCE_FILE_NAME, 'r', encoding=ENCODE_FILE_SOURCE) as file_source:
    # Ler header e obter qtde de colunas (delimitador=|)
    line: str = file_source.readline()

    # Gravar header arquivo target
    file_target.writelines(line)

    # setar variaveis de controle
    no_delimiter_header = line.count(SOURCE_DELIMITER)
    no_lf = line.count(LF)
    no_delimiter_row: int = 0
    no_delimiter_buffer: int = 0
    row_number: int = 0
    buffer = ""
    write_row = ""

    print(f"\nHeader Information - Header Delimiters = {no_delimiter_header} | Qtd LF={no_lf}   \n")

    # processar todas linha do arquivo source
    while line:
        try:
            line = file_source.readline()
            buffer += line
            no_delimiter_row = buffer.count(SOURCE_DELIMITER)
            row_number += 1

            if no_delimiter_row != no_delimiter_header:
                print(f"\n\t row={row_number} | " +
                      f"\tno_delimiter_row={no_delimiter_row} | " +
                      f"\tno_delimiter_header={no_delimiter_header} ")

            ### Check if exist quote chr(34) on buffer.... if exist need split
            if buffer.find('\"') != -1:
                write_row = ""
                buffer = buffer.replace(chr(92), " ")
                cols = tssplit(buffer, quote='"\'', delimiter='|', escape='/^', trim='')
                ### prepare all column to save
                for col in cols:
                    col = col.replace(SOURCE_DELIMITER, ' ')
                    write_row = write_row + (col + "|")

                no_delimiter_row = write_row.count(SOURCE_DELIMITER)
                if no_delimiter_row >= no_delimiter_header:
                    write_row = write_row[:-1]
                    file_target.writelines(write_row)
                    buffer = ""
                else:
                    buffer = write_row
            else:
                if no_delimiter_row == no_delimiter_header:
                    file_target.writelines(buffer)
                    buffer = ""
                # delimiter are not OK...probably have a ENTER to break line...
                else:
                    buffer = buffer[:-1] + " "

        except Exception:
            traceback.print_exc()

file_source.close()
file_target.close()

print(f"\nFinished ! File= {SOURCE_FILE_NAME} | Encode={ENCODE_FILE_SOURCE} | Rows Processed= {row_number}    \n")
