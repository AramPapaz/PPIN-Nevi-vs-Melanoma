import pandas as pd
import numpy as np
from collections import Counter,defaultdict
import torch
from torch_geometric.data import Data
import pickle


## Protein protein interaction info adding pseudo labels
ppi=pd.read_csv("InteractionData.csv")
ppi['Target']='+'
ppi=ppi[["Protein1","Protein2","Target"]]



inters=defaultdict(list)
node_mapping=dict() ## proteins will be represented as numbers 
count=0
e1=[]
e2=[]
edge_labels_temp=[]
for i in range(ppi.shape[0]): ## dict of interactions
    prot1=ppi.loc[i,"Protein1"]
    prot2=ppi.loc[i,"Protein2"]
    if prot1 in node_mapping:
        e1.append(node_mapping[prot1]) ## e1 and e2 are the list of node mappings
    else:
        node_mapping[prot1]=count
        e1.append(node_mapping[prot1])
        count+=1

    if prot2 in node_mapping:
        e2.append(node_mapping[prot2])
    else:
        node_mapping[prot2]=count
        e2.append(node_mapping[prot2])
        count+=1

    edge_labels_temp.append(ppi.loc[i,"Target"])


## initializing pseudo labels as 1 for all
edge_labels=[]
for i in edge_labels_temp:
    edge_labels.append(1)

edge_labels.extend(edge_labels)
edge_labels=torch.tensor(edge_labels)


## converting to undirected 
e1_temp=[]
e1_temp.extend(e1)
e1_temp.extend(e2)

e2_temp=[]
e2_temp.extend(e2)
e2_temp.extend(e1)

e1=torch.tensor(e1_temp)
e2=torch.tensor(e2_temp)


edge_index=torch.stack((e1,e2)).contiguous()

node_features=defaultdict(list) ## get features for each node 


########### combine esm2 and protein expression features
newdata=pd.read_csv("ESM2_embeddings.csv")
## add sep values
separ=pd.read_csv("ProteinExpression.txt",sep=" ")
separ=separ.dropna().reset_index(drop=True)
sepvals=dict()
for i in range(separ.shape[0]): ## Express1: mean disease protein exp; Expres2: mean control
    sepvals[separ.loc[i,"Protein"]]=[separ.loc[i,"Expres1"],separ.loc[i,"Expres2"]]
newdata=newdata[newdata["0"].isin(list(sepvals.keys()))].reset_index(drop=True)

## adding the protein expression
arr=[]
for i in newdata["0"]:
    arr.append(sepvals[i][0])
newdata["1281"]=arr

arr=[]
for i in newdata["0"]:
    arr.append(sepvals[i][1])
newdata["1282"]=arr

## removing uniprot ids
for i in range(newdata.shape[0]):
    node_features[newdata.loc[i,"0"]].extend(newdata.iloc[i,1:newdata.shape[1]])


features=list()
for i in node_features:
    if i in node_mapping:
        idx=node_mapping[i]
        features.append([i,node_features[i],node_mapping[i]])
features=pd.DataFrame(features)
features.columns=["Name","NodeFeat","Map"]
features=features.sort_values(by="Map").reset_index(drop=True)

node_features_temp=list(features["NodeFeat"])
node_features=[]
for i in node_features_temp:
    node_features.append(torch.tensor(i,dtype=torch.float32))
node_features=torch.stack(node_features) ## node features for node mappings 0 till N-1 (N: # nodes)

data=Data(x=node_features,edge_index=edge_index,edge_labels=edge_labels)

data.edge_label_index = data.edge_index

torch.save(data,"PyGData.pth")





