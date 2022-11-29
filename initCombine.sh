# load the environment for Combine
# from https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#standalone-version

# Instructions to install and compile Combine
# git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git --branch 112x HiggsAnalysis/CombinedLimit
# cd HiggsAnalysis/CombinedLimit/
# source env_standalone.sh
# make -j ${nproc}

cd HiggsAnalysis/CombinedLimit/ 
. env_standalone.sh
cd ../../

. /cvmfs/cms.cern.ch/slc7_amd64_gcc820/external/giflib/5.2.0/etc/profile.d/init.sh
. /cvmfs/cms.cern.ch/slc7_amd64_gcc820/external/libpng/1.6.16/etc/profile.d/init.sh
. /cvmfs/cms.cern.ch/slc7_amd64_gcc820/external/libjpeg-turbo/1.5.3/etc/profile.d/init.sh

export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ):$PYTHONPATH"
export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/python:$PYTHONPATH"