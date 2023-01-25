
import ROOT

def defineCutFlowVars(df):

    for i in range(0, 20):
        df = df.Define("cut%d"%i, "%d"%i)
    return df