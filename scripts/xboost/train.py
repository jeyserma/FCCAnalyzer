
import uproot
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import ROOT
import pickle

ROOT.gROOT.SetBatch(True)
# e.g. https://root.cern/doc/master/tmva101__Training_8py.html

print("Parse inputs")

# configuration of signal, background, variables, files, ...
sig_path = "tmp/test_tree_wzp6_ee_mumuH_ecm240.root"
bkg_path = "tmp/test_tree_p8_ee_WW_ecm240.root"

file_path = 'your_file.root'
signal_tree_name = 'signal_tree'
variables = ['lep1_p', 'lep2_p', 'lep1_theta', 'lep2_theta', 'zll_p', 'acoplanarity', 'acolinearity', 'zll_recoil_m', 'cosTheta_miss']

# load the signal and background trees
sig_tree = uproot.open(sig_path)["events"]
bkg_tree = uproot.open(bkg_path)["events"]

# convert the signal and background data to pandas DataFrames
sig_df = sig_tree.arrays(variables, library="pd")
bkg_df = bkg_tree.arrays(variables, library="pd")


# add a target column to indicate signal (1) and background (0)
sig_df['target'] = 1
bkg_df['target'] = 0

# Concatenate the dataframes into a single dataframe
data = pd.concat([sig_df, bkg_df], ignore_index=True)


# split data in train/test events
train_data, test_data, train_labels, test_labels = train_test_split(
    data[variables], data['target'], test_size=0.2, random_state=42
)

# conversion to numpy needed to have default feature_names (fN), needed for conversion to TMVA
train_data = train_data.to_numpy()
test_data = test_data.to_numpy()
train_labels = train_labels.to_numpy()
test_labels = test_labels.to_numpy()


# set hyperparameters for the XGBoost model
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'eta': 0.1,
    'max_depth': 3,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'seed': 42,
    'n_estimators': 350, # 350,
    'early_stopping_rounds': 25,
    'num_rounds': 20
}


# train the XGBoost model
print("Start training")
eval_set = [(train_data, train_labels), (test_data, test_labels)]
bdt = xgb.XGBClassifier(**params)
bdt.fit(train_data, train_labels, verbose=True, eval_set=eval_set)

# predict on the test set and calculate ROC AUC score
print("Run predictions")
predictions = bdt.predict(test_data)
roc_auc = roc_auc_score(test_labels, predictions)
print(f"ROC AUC Score: {roc_auc:.4f}")

# export model (to ROOT and pkl)
ROOT.TMVA.Experimental.SaveXGBoost(bdt, "bdt_model", "tmp/bdt_model_example.root", num_inputs=len(variables))

save = {}
save['model'] = bdt
save['train_data'] = train_data
save['test_data'] = test_data
save['train_labels'] = train_labels
save['test_labels'] = test_labels
pickle.dump(save, open("tmp/bdt_model_example.pkl", "wb"))
