# FCCAnalyzer
Analysis framework integrated with the FCC analysis software.

This FCCAnalyzer framework relies on class definitions, functions and modules of the main FCC analysis framework, as described here: https://github.com/HEP-FCC/FCCAnalyses. This is necessary to read the official edm4hep Monte Carlo samples and to make use of the latest developments in terms of jet clusterin and flavour tagging.

It must be noted that the main FCC analysis framework (FCCAnalyses) has to be compiled only once. The code the current analysis framework (FCCAnalyzer) is compiled in-time, no need for compilation.

By default the analysis runs on lxplus at CERN, where all the samples are available through EOS. A large part has been copied to MIT, but the directory paths have to be updated.

# Examples

Few examples are available:

- Higgs mass and cross-section at 240 GeV: `analyses/higgs_mass_xsec/analysis.py`
- Train a simple BDT using XGBoost and apply it: `analyses/examples/bdt_xgboost` (training, application)
- Forward-Backward analysis at the Z-pole using dimuon events: `analyses/ewk_z/afb.py`


## Setup
Fork FCC analysis repo: https://github.com/HEP-FCC/FCCAnalyses

Fork this repo https://github.com/jeyserma/FCCAnalyzer

Clone the repository with the FCCAnalyses as submodule:

```shell
git clone --recurse-submodules git@github.com:jeyserma/FCCAnalyzer.git
cd FCCAnalyzer
mkdir tmp
```

The FCC analysis software has to be compiled once at the first time (or when any changes have been done in that actual code) as explained in the FCCAnalyses readme.

```shell
cd FCCAnalyses
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ../../
```

Note: by default the newest Key4Hep release is loaded, therefore sometimes one needs to re-compile FCCAnalyses framework scripts according to the steps above.

To use the FCCAnalyzer, just source the setup bash script (to be done at each fresh shell):

```shell
source setup.sh
```

## Setup an analysis
This framework supports multiple FCC analyses. Each analysis has its own working directory, which conventionally should be in the `analyses` directory.

A typical analysis consists of a python file containing the logic of the analysis (event selection etc), and one or more header files containing C++ code snippets (for more complicated calculations).

The analysis structure should be defined in a `build_graph()` function, that can be used in two modes depending on the desired output:

- Histogram mode: the output are histograms, runs over all defined processes simultaneously and stored in a single ROOT file. The `build_graph()` should return a list of histograms and the weightsum, in order to properly normalize the histograms.
- Tree mode (e.g. for training a neural network): the `build_graph()` should return the dataframe and a list of columns to be saved. Currently, the execution of multiple processes is not supported; they need to be handled subsequently.

An example of both modes with a BDT is given in `analyses/examples/bdt_xgboost/analysis.py`.

## Combine environment
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