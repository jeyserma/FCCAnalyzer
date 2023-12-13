
#!/bin/bash

python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor mumu --cat 0
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor mumu --cat 1
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor mumu --cat 2
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor mumu --cat 3

python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor mumu --cat 0
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor mumu --cat 1
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor mumu --cat 2
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor mumu --cat 3



python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor ee --cat 0
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor ee --cat 1
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor ee --cat 2
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor ee --cat 3

python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor ee --cat 0
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor ee --cat 1
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor ee --cat 2
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor ee --cat 3


