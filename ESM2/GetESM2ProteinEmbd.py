import pandas as pd
import numpy as np
import torch
from transformers import EsmTokenizer, EsmModel

aa=dict()
count=1
seq=list()
with open("ProteinSeqs.txt","r") as file:
    for line in file:
        line=line.strip()
        if len(line)==0:
            continue
        if line[0]==">":
            arr=line.split(" ")
            if count==1:
                transID=arr[0][1:len(arr[0])]
                count+=1
                continue
            else:
                if transID in aa: ## make sure to consider longest protein
                    if len(aa[transID])>len(seq):
                        pass
                    else:
                        aa[transID]="".join(seq)
                    
                else:
                    aa[transID]="".join(seq)
                seq=list()
                transID=arr[0][1:len(arr[0])]
        else:
          seq.append(line)
    if transID in aa: ## make sure to consider longest protein
        if len(aa[transID])>len(seq):
            pass
        else:
            aa[transID]="".join(seq)
    else:
        aa[transID]="".join(seq)

embeddings=dict()

# Load the ESM-2 model and tokenizer
model_name = "facebook/esm2_t33_650M_UR50D"
tokenizer = EsmTokenizer.from_pretrained(model_name)
model = EsmModel.from_pretrained(model_name)
model.eval()  # Set to evaluation mode

embds=dict()
for i in aa: ## get sequence embedding from mean amino acid token embeddings
    seq=aa[i]
    inputs = tokenizer(seq, return_tensors="pt", add_special_tokens=True)
    with torch.no_grad():
        outputs = model(**inputs)
    token_embeddings = outputs.last_hidden_state  
    mean_embedding = token_embeddings[0, 1:-1].mean(dim=0)
    embds[i]=mean_embedding.tolist()

data=[]
for i in embds:
    arr=[]
    arr.append(i)
    arr.extend(embds[i])
    data.append(arr)

data=pd.DataFrame(data)
data.to_csv("ESM2_embeddings.csv",index=False)