
#!/bin/bash

#python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor mumu --cat 0 --ecm 240
#python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor mumu --cat 1 --ecm 240
#python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor mumu --cat 2 --ecm 240
#python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor mumu --cat 3 --ecm 240

#python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor ee --cat 0 --ecm 240
#python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor ee --cat 1 --ecm 240
#python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor ee --cat 2 --ecm 240
#python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric.py --mode $1 --flavor ee --cat 3 --ecm 240

python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor mumu --cat 0 --lumi 7.2 --ecm 240
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor mumu --cat 1 --lumi 7.2 --ecm 240
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor mumu --cat 2 --lumi 7.2 --ecm 240
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor mumu --cat 3 --lumi 7.2 --ecm 240


python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor ee --cat 0 --lumi 7.2 --ecm 240
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor ee --cat 1 --lumi 7.2 --ecm 240
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor ee --cat 2 --lumi 7.2 --ecm 240
python analyses/higgs_mass_xsec/scripts/combine/makeWS_parametric_auto.py --mode $1 --flavor ee --cat 3 --lumi 7.2 --ecm 240


