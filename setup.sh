#!/bin/bash

cd FCCAnalyses
source setup.sh 
cd ../

export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ):$PYTHONPATH"
export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/python:$PYTHONPATH"