import pickle
import shap
import numpy as np
import pandas as pd
from compchemkit import fingerprints

DATI="/home/gambacorta/Scrivania/Nico/progetto/dati/"
#X_train_CB1vsCB2 = pd.read_csv(DATI+"X_train_CB1vsCB2.csv",header=None, sep=";")
X_train_CB1vsCB2_red = pd.read_csv(DATI+"X_train_CB1vsCB2_shap.csv",header=None, sep=";")
tiago_df = pd.read_csv(DATI+"SMARTS_LIST.csv", header=None, names=["smarts", "taut"], sep="_")
smarts_red = pd.read_csv(DATI+'SMART_LIST_red.csv')
CSFP = fingerprints.FragmentFingerprint(substructure_list=tiago_df.smarts.tolist())
CSFP_red = fingerprints.FragmentFingerprint(substructure_list=smarts_red["smarts"])

ChEMBL = DATI+'ChEMBL_model.sav'
ChEMBL_load = pickle.load(open(ChEMBL,'rb'))
CSFP_file_1 = DATI+'CSFP_1.sav'
CSFP_1_load = pickle.load(open(CSFP_file_1,'rb'))

GPCRs = DATI+'GPCRs_model.sav'
GPCRs_load = pickle.load(open(GPCRs,'rb'))
CSFP_file_2 = DATI+'CSFP_2.sav'
CSFP_2_load = pickle.load(open(CSFP_file_2,'rb'))

STvsMT = DATI+'STvsMT_model.sav'
STvsMT_load = pickle.load(open(STvsMT,'rb'))
CSFP_file_3 = DATI+'CSFP_3.sav'
CSFP_3_load = pickle.load(open(CSFP_file_3,'rb'))

CB1vsCB2 = DATI+'CB1vsCB2_model.sav'
CB1vsCB2_load = pickle.load(open(CB1vsCB2,'rb'))
CSFP_file_4 = DATI+'CSFP_4.sav'
CSFP_4_load = pickle.load(open(CSFP_file_4,'rb'))

CB1vsCB2_red = DATI+'CB1vsCB2_model_red.sav'
CB1vsCB2_red_load = pickle.load(open(CB1vsCB2_red, 'rb'))
CSFP_file_red = DATI+'CSFP_red.sav'
CSFP_red_load = pickle.load(open(CSFP_file_red,'rb'))

#explainer_cb1cb2 = shap.TreeExplainer(CB1vsCB2_load, feature_perturbation="interventional", data=np.array(X_train_CB1vsCB2))
explainer_red = DATI+'model_explainer_red.sav'
explainer_red_load = pickle.load(open(explainer_red,'rb'))


smi_ChEMBL=pd.read_csv(DATI+'Random_Samples_ChEMBL_vs_CBs.csv',sep='\t')["SMILES"].to_numpy()
fing_ChEMBL = CSFP_1_load.transform_smiles(smi_ChEMBL).toarray()

smi_GPCRs = pd.read_csv(DATI+'Random_Samples_GPCRs_CBs.csv',sep=',')["SMILES"].to_numpy()
fing_GPCRs= CSFP_2_load.transform_smiles(smi_GPCRs).toarray()

smi_STvsMT= pd.read_csv(DATI+'CBs_STvsMT.csv',sep=';')["Smiles"].to_numpy()
fing_STvsMT = CSFP_3_load.transform_smiles(smi_STvsMT).toarray()

DB=pd.read_csv(DATI+"CBs_ST.csv", sep="\t")
DB_dict={r.Smiles:{"value":r.Standard_value, "type":r.Standard_type, "class":r.tid}
        for r in DB.itertuples()}
smi_CB1CB2=DB["Smiles"].to_numpy()
fing_CB1CB2=CSFP_4_load.transform_smiles(smi_CB1CB2).toarray()

TESTSMISEL=""
TESTSMINOTSEL=""
TESTSMICB2=pd.read_csv(DATI+"test_CB2.csv",sep=";")["Smiles"].to_numpy()
TESTSMICB1=pd.read_csv(DATI+"test_CB1.csv",sep=";")["Smiles"].to_numpy()
