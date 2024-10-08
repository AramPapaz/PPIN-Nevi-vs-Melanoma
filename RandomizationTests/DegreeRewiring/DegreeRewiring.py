#### Degree-Preserving Rewiring of the Differential PPIN between Nevi and Melanoma
import pandas as pd
import numpy as np
from collections import Counter
import random

## Only keeping the proteins having Concordant or Conflicting Interactions. Ignoring neutral represented as 'n'
DiffPPIN=pd.read_csv("InteractionAgreement.csv")
DiffPPIN=DiffPPIN[DiffPPIN['Type']!='n'].reset_index(drop=True)

## Taking the significant proteins after median normalization
diff=pd.read_csv("SignificantProteinGroups.csv")

agree=list()
conflicting=list()
## 100 iterations of distinct randomization
for z in range(5):
    ## Perform Randomization
    prot1=list(DiffPPIN["Protein1"])
    prot2=list(DiffPPIN["Protein2"])
    random.shuffle(prot1)
    random.shuffle(prot2)

    agg=pd.DataFrame({"Protein1":prot1,"Protein2":prot2})
    agg["Type"]="n"

    ## save indexes of each protein in majority proteins id 
    idx=dict()
    for i in range(diff.shape[0]):
        t=diff.loc[i,"Majority protein IDs"].split(";")
        for j in t:
            idx[j]=i

    ## Rescan network to calculate interactions
    for i in range(agg.shape[0]):
        ## If both proteins are found to be significant
        if (agg.iloc[i,0] in idx) and (agg.iloc[i,1] in idx):
            #### Check if they are conflicting
            ## both are down regulated
            if (diff.loc[idx[agg.iloc[i,0]],"Student's T-test Difference Nev_Mel"]>0) and (diff.loc[idx[agg.iloc[i,1]],"Student's T-test Difference Nev_Mel"]>0):
                agg.iloc[i,2]="+"
            ## both are up regulated
            elif (diff.loc[idx[agg.iloc[i,0]],"Student's T-test Difference Nev_Mel"]<0) and (diff.loc[idx[agg.iloc[i,1]],"Student's T-test Difference Nev_Mel"]<0):
                agg.iloc[i,2]="-"
            ## conflicting
            else:
                agg.iloc[i,2]="conflicting"
    
    t=Counter(agg["Type"])
    ## Calculating total count of concordant emerging and vanishing interactions
    agree.append(t['+']+t["-"])
    conflicting.append(t['conflicting'])

## writing concordant interactions to text file
with open('ConcordantInteractions100Random.txt', 'w') as f:
    for line in agree:
        f.write(f"{line}\n")

with open('ConflictingInteractions100Random.txt', 'w') as f:
    for line in conflicting:
        f.write(f"{line}\n")

