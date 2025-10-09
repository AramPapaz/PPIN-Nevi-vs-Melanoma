# PPIN-Nevi-vs-Melanoma
[![DOI](https://zenodo.org/badge/849765878.svg)](https://doi.org/10.5281/zenodo.13903581)


<img width="4228" height="1144" alt="Image" src="https://github.com/user-attachments/assets/466623a5-e7ec-4be8-8770-0c2d96c0d016" />

## About
Analysis of context-specific protein-protein interactions (PPIs) may provide deeper insight into protein function and can reveal how cellular pathway components interact in a certain perturbation condition. However, identifying such interactions requires combining affinity purification with mass spectrometry, proving costly and time-consuming. Additionally, an increase in protein abundance does not always correspond to an increase in protein interaction, making it an unsuitable surrogate for interaction studies. To address these issues, a new graph attention model called DiffPIC was trained and tested on validated context-specific PPIs, which annotates changes in interaction topology between two conditions. As features, the model implemented protein sequence and corresponding average abundances in both conditions. This model was later applied to a cohort of 14 nevi samples and their corresponding nevus-associated melanomas and predicted differential interactions were further analyzed for significant protein clusters, protein complexes, and hub proteins related to disease progression. DiffPIC predictions can act as a selection criterion for experimental follow-up studies that investigate greater molecular and mechanistic detail in rewired protein interactions. 


## DiffPIC
DiffPIC, differential protein interaction classifier, was developed using the following package version:
* torch==2.6.0+cu126
* torch_geometric==2.6.1
* transformers==4.55.2
* numpy==1.26.4
* pandas==2.2.2

The statedict of DiffPIC can be found in the `DiffPIC/` folder with an example use case on the Test set.


## PyG Data Creation
In order to create a graph neural network data as input for the model the following are required:
* ESM2 embeddings for each protein, this can be achieved by providing a fasta file to the script in `ESM2/`
* A protein expression text file space separated as shown in `PyG_DataCreation/ProteinExpression.txt`, where *Expres1* is the mean protein abundance in the disease condition while *Expres2* is the mean of the control.
* Provide an interaction data as a csv file similar to `PyG_DataCreation/InteractionData.csv`, make sure no self and repeated interactions are present.
* Feed the aforementioned files to `PyG_DataCreation/createGNNData.py` and the PyG Data will be outputted.
