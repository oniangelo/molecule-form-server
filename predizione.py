from classifiers import CSFP_load, ChEMBL_load,CSFP_1_load,GPCRs_load,CSFP_2_load,STvsMT_load,CSFP_3_load,CB1vsCB2_load,CSFP_red_load,CSFP_4_load, explainer_red_load, DB_dict
import classifiers as C
import numpy as np
from grafica import GraficoSHAP
import pickle 
import json as js
from PIL import Image
from rdkit import Chem
from rdkit.Chem import Draw
import tempfile
import jinja2



DATI="/home/gambacorta/Scrivania/Nico/progetto/dati/"
explainer = DATI+'model_explainer.sav'                                                                                   
explainer_load = pickle.load(open(explainer,'rb'))

def tani(fp1,fp2):
    a=np.sum(np.logical_and(fp1,fp2))
    o=np.sum(np.logical_or(fp1, fp2))
    return a/o

def similari(tsmi, tfing, fing):
    tanis=[tani(tfing[i, :], fing) for i in range(tfing.shape[1])]
    it=[(i,t) for i,t in enumerate(tanis) if t>0.5]
    return [(tsmi[i], t) for i,t in it]

def pred_ChEMBL(smiles):
    fing=CSFP_1_load.transform_smiles([smiles])
    res=ChEMBL_load.predict_proba(fing)
    return res.tolist()[0]
    
def pred_GPCRs(smiles):
    fing=CSFP_2_load.transform_smiles([smiles])
    res=GPCRs_load.predict_proba(fing)
    return res.tolist()[0]
    
def pred_STvsMT(smiles):
    fing=CSFP_3_load.transform_smiles([smiles])    
    res=STvsMT_load.predict(fing)
    return res.tolist()[0]

def pred_CB1vsCB2(smiles):
    #fing_CB1CB2 = CSFP_4_load.transform_smiles(C.smi_CB1CB2).toarray()
    fing=CSFP_4_load.transform_smiles([smiles])    
    res=CB1vsCB2_load.predict(fing)
    shap = explainer_load.shap_values(fing.toarray()[0,:])
    sim=similari(C.smi_CB1CB2, C.fing_CB1CB2, fing.toarray()[0,:])
    return {"pred": res.tolist()[0], "shap": shap[0].tolist(), "similari": sim, "fingerprint": fing.toarray()[0,:]}


def mol_to_svg(mol, svgname):
    drawer = Draw.rdMolDraw2D.MolDraw2DSVG(300,300)
    drawer.drawOptions().addStereoAnnotation = False
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    with open(svgname, "w") as f:
        f.write(drawer.GetDrawingText())

Template_loader = jinja2.FileSystemLoader('/home/gambacorta/Scrivania/Nico/website/molecule-form-server/')
Template_env = jinja2.Environment(loader=Template_loader)
pred_template = Template_env.get_template('basic-template.html')

def models_sequence(smiles):
    CSFP = CSFP_load
    res=dict(smiles=smiles)
    p_chembl=pred_ChEMBL(smiles)
    res["pred_chembl"]=p_chembl
    dirname=tempfile.mkdtemp(dir="pred_out")
    shapname=dirname+'/shaps.png'
    if p_chembl[0] > 0.2 :
        p_GPCR=pred_GPCRs(smiles)
        res["pred_GPCR"]=p_GPCR
        if p_GPCR[0] > 0.2 :
            p_stvsmt=pred_STvsMT(smiles)
            res["pred_STvsMT"]=p_stvsmt
            if p_stvsmt=="ST":
                res["pred_CB1vsCB2"]= pred_CB1vsCB2(smiles)
                fig = GraficoSHAP(smiles,res["pred_CB1vsCB2"]['fingerprint'],res["pred_CB1vsCB2"]["shap"], CSFP)
                fig.save(shapname)
                res["pred_CB1vsCB2"]["fingerprint"] = res["pred_CB1vsCB2"]["fingerprint"].tolist()
                similars=[]
                for i,s in enumerate(res['pred_CB1vsCB2']['similari']):
                    mol=Chem.MolFromSmiles(s[0])
                    simname=dirname+"/sim_"+str(i)+".svg"
                    mol_to_svg(mol, simname)
                    similars.append({"fig":simname, "tani": s[1], "info": DB_dict[s[0]]})
                output_text = pred_template.render(smiles=smiles, p_chembl=p_chembl[0],
                        p_GPCR=p_GPCR[0],
                        p_STvsMT=p_stvsmt,
                        p_CB1vsCB2=res["pred_CB1vsCB2"]["pred"],
                        shapname=shapname,
                        similars=similars)
                return res, similars, output_text
            else:
                output_text = pred_template.render(smiles=smiles, p_chembl=p_chembl[0],
                        p_GPCR=p_GPCR[0],
                        p_STvsMT=p_stvsmt)
                return res,output_text
        else:
            output_text = pred_template.render(smiles=smiles, p_chembl=p_chembl[0],
                    p_GPCR=p_GPCR)
            return res, output_text
    else:
        output_text= pred_template.render(smiles=smiles, p_chembl=p_chembl[0])
        return res, output_text


def models_sequence1(smiles):
    return smiles;


