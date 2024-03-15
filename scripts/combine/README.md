
# Combine environment

Combine is the statistical toolbox to perform likelihood fits and more, used and developed by CMS. There are two versions. regular `combine`, based on RooStats/RooFit and TensorFlow `combinetf`, based on TensorFlow. Regular combine comes with a lot of extra tools for fitting, debugging, limit calulation, etc., as well as support for parametric fits. TensorFlow combine uses modern minimizers and is therefore more accurate and faster in case for complex fits, but it only supports binned likelihood fits.


Both versions require CMSSW (CMS analysis software), and are not compatible with the newest ROOT version, as required for the main analysis with FCCAnalyzer/RDataFrame. Therefore, in order to use Combine, one has to install and execute it in a different environment. It is advised to install `combine` or `combinetf` outside of the FCCAnalyzer directory.

## Regular Combine (RooFit based)

To install `combine`, execute the following steps (more info on how to use `combine` and other installation methods can be found here: https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit):

```shell
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd <directory outside FCCAnalyzer>
cmssw-el7 # necessary for non-cc7 machines
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.2.0 # checkout recommended tag
scramv1 b clean; scramv1 b # always make a clean build
```

In order to run `combine`, open a fresh shell w.r.t. your FCCAnalyzer shell, and first load the environment:

```shell
cmssw-el7
cd CMSSW_10_2_13/src
cmsenv
cd <back to your FCCAnalyzer directory>
```

Then you can go to any directory where the datacards are stored, and run the fit. An example is given in `FCCAnalyzer/scripts/combine`, that fits the Higgs Z(mumu)H cross-section (with 1 signal and 1 background). Both histograms are stored in the root file and the likelihood is constructed using the `datacard.txt` (which defines the input histograms, systematics, etc). To run the fit, you need two commands:

```shell
text2workspace.py datacard.txt -o ws.root  -v 10 # convert the model to a workspace
combine -M FitDiagnostics -t -1 ws.root --expectSignal=1 -v 10 # run the fit
```

The outcome of the latter is:

```shell
 --- FitDiagnostics ---
Best fit r: 1  -0.0117825/+0.0118228  (68% CL)
```

It fits the signal to strength 1 (as expected, as we ask for  --expectSignal=1), and the uncertainty is 1.18 %.

## TensorFlow combine

To install `combinetf`, execute the following steps: 

```shell
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd <directory outside FCCAnalyzer>
cmssw-cc7 # necessary for non-cc7 machines
export SCRAM_ARCH="slc7_amd64_gcc700"
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src/
cmsenv
git clone -o bendavid -b tensorflowfit git@github.com:bendavid/higgsanalysis-combinedlimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
scram b -j 8
```

Usage of `combinetf` is similar to regular `combine`. First load the environment:

```shell
cmssw-el7
cd CMSSW_10_6_19_patch2/src/
cmsenv
cd <back to your FCCAnalyzer directory>
```

And then run the following commands to convert the model and run the fit (slightly different commands than before, but similar idea):

```shell
text2hdf5.py datacard.txt -o datacard.hdf5 --X-allow-no-background --X-allow-no-signal
combinetf.py datacard.hdf5 -t -1
```

The outcome of the latter is:

```shell
sig_mu = 1.000000e+00 +- 0.011803 (+-99.000000 --99.000000)
```

It fits the signal to strength 1 (as expected, as we ask for  --expectSignal=1), and the uncertainty is 1.18 %, which is identical to the result obtained with regular `combine`.