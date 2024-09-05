import pandas as pd
import numpy as np
from collections import Counter

## Reading file containing the 1946 remainig protein groups after filtering
df=pd.read_csv("FilteredProteinGroups.csv")

for x in range(1,6):
    ## Consider only intensity columns
    df_intensities=df.iloc[:,0:28]
    df_other=df.iloc[:,28:df.shape[1]]

    ## Shuffle columns
    df_intensities=df_intensities.sample(frac=1,axis=1)
    df_intensities=pd.concat([df_intensities,df_other],axis=1)

    df_intensities.to_csv(f"RandomColumns{x}.txt",sep="\t",index=False)

'''Note that none of the randomized labels lead to us finding differentially expressed genes after processing in Persues software'''
