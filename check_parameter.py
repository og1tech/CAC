import sys

n = len(sys.argv)
print("Total arguments passed:", n)

SOURCE_FILE_NAME = sys.argv[1]
TARGET_FILE_NAME = sys.argv[2]
ENCODE_FILE = sys.argv[3]
print(f"\nSource= {SOURCE_FILE_NAME}" +
      f"\nTarget= {TARGET_FILE_NAME}" +
      f"\nEncode= {ENCODE_FILE}")
