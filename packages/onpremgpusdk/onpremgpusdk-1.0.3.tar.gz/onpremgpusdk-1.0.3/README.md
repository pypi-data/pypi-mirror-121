# On Prem GPU SDK
Provides Utitlities to support and build Machine Learning and Analytics scripts to run on navi premise GPU cluster. 

## Installation
```
pip3 install onpremgpusdk
```

## Example
```
import pandas as pd
from onpremgpusdk.data import DataInstance


'''
Create data instance
'''
du = DataInstance("local-stack-bucket") # Instantiate DataInstance with bucket name to use


'''
    Upload File
'''
df = pd.read_csv("./stocks.csv")
du.write_csv(df, "output_test/stock_output.csv")


'''
Read Data
'''
du.read_csv("output_test/stock_output.csv")

```
