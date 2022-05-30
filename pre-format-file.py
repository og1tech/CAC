import re
from io import StringIO
import pandas as pd

fname = "c:/temp/Account_Sales.csv"

with open(fname , encoding="ANSI") as f:
    data = re.sub('""', '"', re.sub('[ \t]+,', ',',
                                    re.sub('^[ \t]+|(^[ \t,]*|[ \t]*)(#.*)?$', '', f.read(), flags=re.M)))

    df = pd.read_csv(StringIO(data), quotechar='"', skipinitialspace=True)
