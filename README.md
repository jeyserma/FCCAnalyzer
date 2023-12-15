# FCCAnalyzer
Analysis framework integrated with the FCC analysis software.

This FCCAnalyzer framework relies on class definitions, functions and modules of the main FCC analysis framework, as described here: https://github.com/HEP-FCC/FCCAnalyses. This is necessary to read the official edm4hep Monte Carlo samples and to make use of the latest developments in terms of jet clustering and flavour tagging.

To start using this framework, first fork this repository: https://github.com/jeyserma/FCCAnalyzer. Open a shell and clone this repository:


```shell
git clone git@github.com:<my_git_username>/FCCAnalyzer.git
cd FCCAnalyzer
```

To use the FCCAnalyzer, just source the setup bash script (to be done at each fresh shell):

```shell
source setup.sh
```

This framework supports multiple FCC analyses, each analysis contained in its own directory (in the `analyses` directory). A typical analysis consists of a python file containing the logic of the analysis (event selection etc), and one or more header files containing C++ code snippets (for more complicated calculations).

The analysis structure should be defined in a `build_graph()` function, that can be used in two modes depending on the desired output:

- Histogram mode: the output are histograms, runs over all defined processes simultaneously and stored in a single ROOT file. The `build_graph()` should return a list of histograms and the weightsum, in order to properly normalize the histograms.
- Tree mode (e.g. for training a neural network): the `build_graph()` should return the dataframe and a list of columns to be saved. Currently, the execution of multiple processes is not supported; they need to be handled subsequently.

Examples below make clear the usage of the files and run modes.


The underlying `key4hep` stack version (loaded during `setup.sh` is appended to the `stack_history` file. To fix a `key4hep` release, add the path to the setup script to `stack`, and it will be loaded by default.



# Examples

## Forward-Backward asymmetry
To run the forward-backward asymmetry analysis, run the following script from the main `FCCAnalyzer` directory (to quickly run over a few files, add the option `--maxFiles 50`)

```shell
python analyses/ewk_z/afb.py
```

This produces a ROOT file `afb.root` that contains the histograms. To plot and fit the forward-backward asymmetry, run the following command:

```shell
analyses/ewk_z/scripts/afb_fit.ipynb
```

Also a standalone script written in ROOT is available to extract the forward-backward asymmetry:

```shell
python analyses/ewk_z/scripts/afb_fit.py -o /directory/output/path
```

## Simple cross-section at the Z-pole
To run the forward-backward asymmetry analysis, run the following script from the main:

```shell
python analyses/ewk_z/xsec.py --flavor mumu,ee,qq
```

where the flavor is either mumu (dimuon), ee (di-electron) or qq (hadronic) final states. Note that the hadronic final state takes some time to run as the jet clustering is slow. To make basic plots of the Z peak(s), a Jupyter notebook is made available that contains instructions on how to read the histogram file etc:

```shell
analyses/ewk_z/scripts/plots_xsec.ipynb
```

## BDT training and application using BDT using XGBoost
To use a BDT in the analysis, first a tree has to be created with all the variables used by the training:

```shell
python analyses/examples/bdt_xgboost/analysis.py --maketree
```

The output are ROOT files, one per process, that contain the events with the calculated columns/branches that are used in the training. Now we'll train the BDT using XGBoost:


```shell
python analyses/examples/bdt_xgboost/train_bdt.py
```

The output of the training are two files: `bdt_model_example.pkl` and `bdt_model_example.root`. The ROOT file is used to check and evaluate the training performance, over-training etc:

```shell
python analyses/examples/bdt_xgboost/evaluate_bdt.py -i bdt_model_example.pkl
```

Then the `bdt_model_example.pkl` is used in the analysis to apply the BDT in the main analysis (it's the same as the first command, except the `maketree` option).

```shell
python analyses/examples/bdt_xgboost/analysis.py
```

The output (`test_bdt.root`) are the usual histograms and the histogram `mva` contain the MVA scores, that can be plotted with the following Jupyter notebook:

```shell
analyses/examples/bdt_xgboost/plots.ipynb
```

Note: apart from XGBoost, also XML files from TMVA trainings can be read (defined in `analysis.py`)

```shell
tmva_helper = helper_tmva.TMVAHelperXGB("bdt_model_example.root", "bdt_model") # read the XGBoost training
tmva_helper = helper_tmva.TMVAHelperXML("TMVAClassification_BDTG.weights.xml") # read an XML file from TMVA
```






## Higgs mass and cross-section at 240 GeV
To be updated.


# Setting up a new analysis
Each analysis should be contained in its own separate directory, which conventionally should be in the `analyses` directory:

```shell
mkdir analyses/<my_analysis_name>
```

Copy over some example files to your directory:

```shell
cp analyses/ewk_z/afb.py analyses/<my_analysis_name>/analysis.py
cp analyses/ewk_z/function.h analyses/<my_analysis_name>/functions.h
```

Edit the python (make sure you update the path to the correct header file) and header files and run it:

```shell
python analyses/<my_analysis_name>/analysis.py
```


# Combine environment
Combine requires either CMSSW or can be compiled standalone, but is not compatible with the newest ROOT version, as required for the main analysis with RDataFrame. Therefore, in order to run Combine, one has to load a different environment.

To install Combine (in the FCCAnalyzer directory), execute the following steps:

```shell
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git --branch 112x HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit/
source env_standalone.sh
make -j ${nproc}
cd ../../
```

In order to run Combine, source the following script (instead of setup.sh):

```shell
source ./initCombine.sh
```