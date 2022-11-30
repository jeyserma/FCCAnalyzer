# FCCAnalyzer
Analysis framework integrated with the FCC analysis software

This analysis code uses class definitions, functions and modules of the main FCC analysis framework, as described here: https://github.com/HEP-FCC/FCCAnalyses.

## Setup
Fork FCC analysis repo: https://github.com/HEP-FCC/FCCAnalyses
Fork this repo https://github.com/HEP-FCC/FCCAnalyses

Clone the repository with the FCCAnalyses as submodule:

```shell
git clone --recurse-submodules git@github.com:jeyserma/FCCAnalyzer.git
```

The FCC analysis software has to be compiled once at the first time (or when any changes have been done in that actual code) as explained in the FCCAnalyses readme.

```shell
cd FCCAnalyses
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ..
```

Note: by default the newest Key4Hep release is loaded, therefore sometimes one needs to re-compile FCCAnalyses framework scripts according to the steps above.

To use the FCCAnalyzer, just source the setup bash script:

```shell
source ./setup.sh
cd ..
```

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
cd ..
```