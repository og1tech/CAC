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

SourceFileName = "c:/Projects/CAC/Insights_Hunters.csv"
TargetFileName = "c:/Projects/CAC/Out.csv"
Encode         = 'utf-16-le'

Fileserver:
"//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/Account_Sales/Account_Sales.csv" 
"//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/Account_Sales/Account_Sales_tmp.csv" 
"utf-16-le"


"""
import csv
import sys
import io
import chardet
import codecs


def get_encoding(filepath):
    rawdata = open(filepath, "rb").read()
    encoding = chardet.detect(rawdata)['encoding']
    return encoding

def row_count(file_path):
    input_file = open(file_path, "r+")
    reader_file = csv.reader(input_file)
    value = len(list(reader_file))
    return value

# obter parametros informados
n = len(sys.argv)
n=5
if n < 4:
    print(f"Arguments number is invalid ({n})." +
          "Execute convert_file_csv.py [source file name] [target file name] [encode]")
    exit(-1)

SOURCE_FILE_NAME = sys.argv[1]
TARGET_FILE_NAME = sys.argv[2]
ENCODE_FILE = sys.argv[3]

SOURCE_FILE_NAME ="//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/Account_Sales/Account_Sales.csv" 
TARGET_FILE_NAME ="//RBAMVLATAMTBLP/CAC_Datos/ECAS/AWS Datalake/Auxiliary/Account_Sales/Account_Sales_tmp.csv" 
ENCODE_FILE ="utf-16-le"



print(f"\nSource= {SOURCE_FILE_NAME}" +
      f"\nTarget= {TARGET_FILE_NAME}" +
      f"\nEncode Output= {ENCODE_FILE}")

CR = "\r"
CR_LF = '\r\n'
LF = '\n'
DELIMITER = "|"

row_lines = row_count(SOURCE_FILE_NAME)
print(f"\nSource File Rows = {row_lines}")


ENCODE_FILE = get_encoding(SOURCE_FILE_NAME)
print(f"\nDecode Source= {ENCODE_FILE}")


file_target = open(TARGET_FILE_NAME, "w", encoding=ENCODE_FILE)
print(f"\nInicio de processamento")
with open(SOURCE_FILE_NAME, 'r', encoding=ENCODE_FILE) as file_source:
    # Ler header e obter qtde de colunas (delimitador=|)
    line: str = file_source.readline()

    # Gravar header arquivo target
    file_target.writelines(line)

    # setar variaveis de controle
    no_delimiter_header = line.count(DELIMITER)
    no_lf = line.count(LF)
    no_delimiter_row: int = 0
    no_delimiter_buffer: int = 0
    row_number: int = 0
    buffer = ""
    write_row = ""

    print(f"\nHeader Information - Header Delimiters = {no_delimiter_header} | Qtd LF={no_lf}   \n")

    # processar todas linha do arquivo source
    while line:
        line = file_source.readline()
        buffer += line
        no_delimiter_row = buffer.count(DELIMITER)
        no_lf = buffer.count(LF)
        row_number += 1

        if no_delimiter_row != no_delimiter_header:
            buffer = buffer[:-1] + " "
        else:
            write_row = buffer
            buffer = ""
            """"
            print(
                f"Row={row_number} - delimiter_row={no_delimiter_row} - LF={no_lf} - write_row={write_row[:60]}")
            """
            file_target.writelines(write_row)

file_source.close()
file_target.close()

print(f"\nFinished ! File= {SOURCE_FILE_NAME} | Encode={ENCODE_FILE} | Rows Processed= {row_number}    \n")
