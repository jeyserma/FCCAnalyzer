#!/bin/bash

# check if FCCAnalyses compiled locally
if test -d FCCAnalyses; then
    cd FCCAnalyses
    source setup.sh 
    cd ../
elif test -f .stack; then
    st=$(cat .stack)
    source $st
else
    source /cvmfs/sw.hsf.org/key4hep/setup.sh 
    source /cvmfs/sw.hsf.org/key4hep/setup.sh | grep source | awk -v date="$(date)" '{print date " "  $2}' >> .stack_history
fi



export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ):$PYTHONPATH"
export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/python:$PYTHONPATH"