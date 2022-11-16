# FCCAnalyzer
Analysis framework integrated with the FCC analysis software

This analysis code uses class definitions, functions and modules of the main FCC analysis framework, as described here: https://github.com/HEP-FCC/FCCAnalyses.

## Setup
Fork FCC analysis repo: https://github.com/HEP-FCC/FCCAnalyses
Fork this repo https://github.com/HEP-FCC/FCCAnalyses

The FCC analysis software has to be compiled upon usage for the first time (or when any changes have been done) as explained in the readme.

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

