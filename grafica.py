from compchemkit.machine_learning import feature_importance as feim
from rdkit import Chem
# from .classifiers import 

def shap2atomweight(mol, fingerprint, shap_mat):
    bit_atom_env_dict = fingerprint.bit2atom_mapping(mol)
    atom_weight_dict = feim.assign_prediction_importance(bit_atom_env_dict, shap_mat)
    atom_weight_list = [atom_weight_dict[a_idx] if a_idx in
                        atom_weight_dict else 0 for a_idx in range(mol.GetNumAtoms())]
    return atom_weight_list

def GraficoSHAP(smi, fing,shap_matrix, CSFP):
    vis_cpd_mol_obj = Chem.MolFromSmiles(smi)
    vis_cpd_present_shap = shap_matrix * fing
    vis_cpd_present_shap = vis_cpd_present_shap.tolist()
    atom_w = shap2atomweight(vis_cpd_mol_obj, CSFP, vis_cpd_present_shap)
    svg_image = feim.rdkit_gaussplot(vis_cpd_mol_obj, atom_w, n_contourLines=5)
    fig = feim.show_png(svg_image.GetDrawingText())
    return fig
