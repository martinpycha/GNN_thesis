import pandas as pd
from rdkit.Chem import PandasTools
from rdkit import Chem
from sklearn.model_selection import train_test_split
import dgl
from dgllife.utils import mol_to_bigraph, CanonicalAtomFeaturizer, CanonicalBondFeaturizer
from enum import Enum
import torch
import json

# this script is called by the feature_selection script and it takes canonical SMILES and converts them into graphs


def prepare_for_classification(data_frame, treshold=6):
    print("Preparing dataset for classification...")
    #data_frame["pki"] = data_frame.apply(lambda row: 1 if row["pki"] >= treshold else 0, axis=1)   TODO
    data_frame["pchembl_value_Mean"] = data_frame.apply(lambda row: 1 if row["pchembl_value_Mean"] >= treshold else 0, axis=1)
    print("Dataset ready for classification.")
    return data_frame

# input ... dataset with CHEMBLID, pki, canonical SMILES
# labels are going to be the pki's 
def molecules_to_graph(data_frame):
    print("Converting molecules to graphs...")
    #smiles_labels = data_frame[['smiles', 'pki']] 
    chemblid, graphs, labels = [], [], []
    for index, row in data_frame.iterrows():
        #chemblid = row['molecule_chembl_id']   TODO
        #smi = row['smiles']    TODO
        smi = row['Drug']
        mol = Chem.MolFromSmiles(smi)
        #print("Number of edges:", g.number_of_edges())  # Get the number of edges in the graph
        #print("Number of features:", len(CanonicalBondFeaturizer(mol)))  # Check the number of features returned
        
        graph = mol_to_bigraph(    # converts RDKit mol object into a DGL graph, bigraph - ensuring undirected conectivity (A->B, B->A)
            mol,                   # adding self loops to nodes --> they can use their own features in message passing
            node_featurizer=CanonicalAtomFeaturizer(),
            edge_featurizer=CanonicalBondFeaturizer(),
            explicit_hydrogens=False
        )
        graph = dgl.add_self_loop(graph)
        graphs.append(graph)
        #label = row['pki'] TODO
        #label = row['pchembl_value_Mean'] 
        label = row['Y_original'] 
        labels.append(label)
    print(f"LENGTH OF LABELS: {len(labels)}")
    labels = torch.tensor(labels).unsqueeze(1)  # torch.tensor ... converts python list into pytorch tensor
                                                    # unsqueeze(1) ... adds an extra dimension at the position 1 (some models require explicitly the 2nd dimention)
    labels_dictionary = {'labels':torch.tensor(labels)} # dgl expects tensors for metadata (we convert labels to a dictionary with tensor)
    print("Graphs done.")
    
    return chemblid, labels_dictionary, graphs


def run_script():
    #data_frame = pd.read_csv("/Users/martinpycha/Desktop/Machine_learning/My_project/acetylcholinesterase")    TODO
    #data_frame = pd.read_csv("/Users/martinpycha/Desktop/Machine_learning/My_project/AR_LIGANDS.tsv",delimiter='\t')
    #data_frame = pd.read_csv("/Users/martinpycha/Desktop/Machine_learning/My_project/A2AR_data/a2ar_val_1")
    data_frame = pd.read_csv("/Users/martinpycha/Desktop/Machine_learning/My_project/A2AR_data/a2ar_train_1")
    #data_frame = pd.read_csv("/Users/martinpycha/Desktop/Machine_learning/My_project/A2AR_data/a2ar_val_1")
    #data_frame = pd.read_csv("/Users/martinpycha/Desktop/Machine_learning/My_project/A2AR_data/a2ar_test_1")
    print(type(data_frame))
    data_frame_class = data_frame
    # FOR CLASSIFICATION
    #data_frame_class = prepare_for_classification(data_frame)
    print(data_frame_class.info())
    print(data_frame_class.head())
    
    #print(data_frame["pki"].value_counts())    TODO
    #print(data_frame["pchembl_value_Mean"].value_counts())
    print(data_frame["Y_original"].value_counts())
    
    print(type(data_frame_class))
    _, labels_dict, graphs = molecules_to_graph(data_frame_class)
    # saving the results
    print("Saving the graphs and labels")
    
    labels_dict_int = {}
    for key, item in labels_dict.items():
        labels_dict_int[key] = torch.tensor(item, dtype=torch.int)
    #dgl.save_graphs('molecule_graphs.bin', graphs, labels_dict)  # graphs... list of graphs, labels_dict ... dictionary containing labels
    #dgl.save_graphs('molecule_graphs_qsprpred.bin', graphs, labels_dict)  # graphs... list of graphs, labels_dict ... dictionary containing labels
    
    print(f"Number of graphs: {len(graphs)}, NUmber of labels: {len(labels_dict_int)}")
    #dgl.save_graphs('/Users/martinpycha/Desktop/Machine_learning/My_project/A2AR_graphs/a2ar_val_1_graphs.bin', graphs, labels_dict_int)  # graphs... list of graphs, labels_dict ... dictionary containing labels
    dgl.save_graphs('/Users/martinpycha/Desktop/Machine_learning/My_project/A2AR_graphs/a2ar_train_1_graphs.bin', graphs, labels_dict_int)  # graphs... list of graphs, labels_dict ... dictionary containing labels
    #dgl.save_graphs('/Users/martinpycha/Desktop/Machine_learning/My_project/A2AR_graphs/a2ar_val_1_graphs.bin', graphs, labels_dict_int)  # graphs... list of graphs, labels_dict ... dictionary containing labels
    #dgl.save_graphs('/Users/martinpycha/Desktop/Machine_learning/My_project/A2AR_graphs/a2ar_test_1_graphs.bin', graphs, labels_dict_int)  # graphs... list of graphs, labels_dict ... dictionary containing labels
    print("Graphs and labels saved.")
    
run_script()
    
    
    
    
        
        
        