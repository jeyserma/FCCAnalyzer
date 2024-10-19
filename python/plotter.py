import ROOT

cfg = None

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
#ROOT.gStyle.SetImageScaling(2.)

def getProc(fIn, hName, procs, lumiScale=1):
    h = None
    for i,proc in enumerate(procs):
        #hName_ = f"{proc}/{hName}"
        hName_ = "%s/%s"%(proc, hName)
        h_ = fIn.Get(hName_)
        if h_ == None:
            print("WARNING: Cannot find %s, skip"%hName_)
            continue
        if h == None: h = h_.Clone()
        else: h.Add(h_)
    h.Scale(lumiScale)
    return h

def translate(word):

    if "MET" in word: return word.replace("MET", "E_{T}^{miss}")
    if "MT" in word: return word.replace("MT", "m_{T}")
    if "PT" in word: return word.replace("PT", "p_{T}")
    if "HT" in word: return word.replace("HT", "H_{T}")
    if "ETA" in word: return word.replace("ETA", "#eta")
    return word


def dummy(nbins = 1):

    if cfg['logx']:
        xmin = 0.999*float(cfg['xmin']) # hack to display lower/upper ticks on axis
        xmax = 1.001*float(cfg['xmax'])
    else:
        xmin = float(cfg['xmin'])
        xmax = float(cfg['xmax'])

    if cfg['logy']:
        ymin = 0.999*float(cfg['ymin']) # hack to display lower/upper ticks on axis
        ymax = 1.001*float(cfg['ymax'])
    else:
        ymin = float(cfg['ymin'])
        ymax = float(cfg['ymax'])


    # dummy
    dummy = ROOT.TH1D("h", "h", nbins, xmin, xmax)

    # x-axis
    dummy.GetXaxis().SetTitle(translate(cfg['xtitle']))

    dummy.GetXaxis().SetRangeUser(xmin, xmax)

    dummy.GetXaxis().SetTitleFont(43)
    dummy.GetXaxis().SetTitleSize(40)
    dummy.GetXaxis().SetLabelFont(43)
    dummy.GetXaxis().SetLabelSize(35)

    dummy.GetXaxis().SetTitleOffset(1.2*dummy.GetXaxis().GetTitleOffset())
    dummy.GetXaxis().SetLabelOffset(1.2*dummy.GetXaxis().GetLabelOffset())

    # y-axis
    dummy.GetYaxis().SetTitle(translate(cfg['ytitle']))

    dummy.GetYaxis().SetRangeUser(ymin, ymax)
    dummy.SetMaximum(ymax)
    dummy.SetMinimum(ymin)

    dummy.GetYaxis().SetTitleFont(43)
    dummy.GetYaxis().SetTitleSize(40)
    dummy.GetYaxis().SetLabelFont(43)
    dummy.GetYaxis().SetLabelSize(35)

    dummy.GetYaxis().SetTitleOffset(1.7*dummy.GetYaxis().GetTitleOffset())
    dummy.GetYaxis().SetLabelOffset(1.4*dummy.GetYaxis().GetLabelOffset())

    return dummy


def aux():

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(30) # 0 special vertical aligment with subscripts
    if "_" in cfg['topRight']: latex.DrawLatex(0.95, 0.945, cfg['topRight'])
    elif "^" in cfg['topRight']: latex.DrawLatex(0.95, 0.945, cfg['topRight'])
    else: latex.DrawLatex(0.95, 0.955, cfg['topRight']) # was 955 ??  945


    latex.SetTextAlign(10)
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex.DrawLatexNDC(0.15, 0.95, cfg['topLeft'])


def canvas(width=1000, height=1000, leftMargin=0.15):

    c = ROOT.TCanvas("c", "c", width, height)
    c.SetTopMargin(0.055)
    c.SetRightMargin(0.05)
    c.SetLeftMargin(leftMargin)
    c.SetBottomMargin(0.11)

    #c.SetFrameLineWidth(2)

    if cfg['logy']: c.SetLogy()
    if cfg['logx']: c.SetLogx()


    c.Modify()
    c.Update()

    return c




def auxRatio():

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.055)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    #latex.DrawLatex(0.95, 0.925, cfg['topRight'])
    if "#sqrt" in cfg['topRight'] and "^" in cfg['topRight']: latex.DrawLatex(0.95, 0.935, cfg['topRight']) # OK WORKS
    elif "_" in cfg['topRight']: latex.DrawLatex(0.95, 0.945, cfg['topRight'])
    elif "^" in cfg['topRight']: latex.DrawLatex(0.95, 0.945, cfg['topRight'])
    else: latex.DrawLatex(0.95, 0.935, cfg['topRight']) # was 955 ??  945

    latex.SetTextAlign(13)
    latex.SetTextFont(42)
    latex.SetTextSize(0.06)
    latex.DrawLatex(0.15, 0.975, cfg['topLeft'])




def dummyRatio(nbins = 1, rline=1):

    if cfg['logx']:
        xmin = 0.999*float(cfg['xmin']) # hack to display lower/upper ticks on axis
        xmax = 1.001*float(cfg['xmax'])
    else:
        xmin = float(cfg['xmin'])
        xmax = float(cfg['xmax'])

    if cfg['logy']:
        ymin = 0.999*float(cfg['ymin']) # hack to display lower/upper ticks on axis
        ymax = 1.001*float(cfg['ymax'])
    else:
        ymin = float(cfg['ymin'])
        ymax = float(cfg['ymax'])


    # dummy
    dummyT = ROOT.TH1D("h1", "h", nbins, xmin, xmax)
    dummyB = ROOT.TH1D("h2", "h", nbins, xmin, xmax)


    # x-axis
    dummyB.GetXaxis().SetTitle(translate(cfg['xtitle']))

    dummyT.GetXaxis().SetRangeUser(xmin, xmax)
    dummyB.GetXaxis().SetRangeUser(xmin, xmax)

    dummyT.GetXaxis().SetTitleFont(43)
    dummyT.GetXaxis().SetTitleSize(0)
    dummyT.GetXaxis().SetLabelFont(43)
    dummyT.GetXaxis().SetLabelSize(0)

    dummyT.GetXaxis().SetTitleOffset(1.2*dummyT.GetXaxis().GetTitleOffset())
    dummyT.GetXaxis().SetLabelOffset(1.2*dummyT.GetXaxis().GetLabelOffset())

    dummyB.GetXaxis().SetTitleFont(43)
    dummyB.GetXaxis().SetTitleSize(32)
    dummyB.GetXaxis().SetLabelFont(43)
    dummyB.GetXaxis().SetLabelSize(28)

    dummyB.GetXaxis().SetTitleOffset(1.0*dummyB.GetXaxis().GetTitleOffset())
    dummyB.GetXaxis().SetLabelOffset(3.0*dummyB.GetXaxis().GetLabelOffset())

    # y-axis
    dummyT.GetYaxis().SetTitle(translate(cfg['ytitle']))
    dummyB.GetYaxis().SetTitle(translate(cfg['ytitleR']))

    dummyT.GetYaxis().SetRangeUser(ymin, ymax)
    dummyT.SetMaximum(ymax)
    dummyT.SetMinimum(ymin)

    dummyB.GetYaxis().SetRangeUser(cfg['yminR'], cfg['yminR'])
    dummyB.SetMaximum(cfg['ymaxR'])
    dummyB.SetMinimum(cfg['yminR'])

    dummyT.GetYaxis().SetTitleFont(43)
    dummyT.GetYaxis().SetTitleSize(32)
    dummyT.GetYaxis().SetLabelFont(43)
    dummyT.GetYaxis().SetLabelSize(28)

    dummyT.GetYaxis().SetTitleOffset(1.3) # 1.7*dummyT.GetYaxis().GetTitleOffset()
    dummyT.GetYaxis().SetLabelOffset(1.4*dummyT.GetYaxis().GetLabelOffset())

    dummyB.GetYaxis().SetTitleFont(43)
    dummyB.GetYaxis().SetTitleSize(32)
    dummyB.GetYaxis().SetLabelFont(43)
    dummyB.GetYaxis().SetLabelSize(28)

    dummyB.GetYaxis().SetTitleOffset(1.7*dummyB.GetYaxis().GetTitleOffset()) 
    dummyB.GetYaxis().SetLabelOffset(1.4*dummyB.GetYaxis().GetLabelOffset())
    dummyB.GetYaxis().SetNdivisions(505)
    
    line = ROOT.TLine(float(cfg['xmin']), rline, float(cfg['xmax']), rline)
    line.SetLineColor(ROOT.kRed)
    line.SetLineWidth(2)

    return dummyT, dummyB, line

def canvasRatio(width=1000, height=1000, leftMargin=0.15):


    epsilon = 0.025

    c = ROOT.TCanvas("c", "c", width, height)
    c.SetTopMargin(0.0)
    c.SetRightMargin(0.0)
    c.SetBottomMargin(0.0)
    c.SetLeftMargin(0.0)

    pad1 = ROOT.TPad("p1","p1", 0, cfg['ratiofraction'], 1, 1)
    pad2 = ROOT.TPad("p2","p2", 0, 0.0, 1, cfg['ratiofraction']-0.7*epsilon)

    pad1.SetBottomMargin(epsilon)
    pad1.SetTopMargin(0.055/(1.-cfg['ratiofraction']))
    pad1.SetRightMargin(0.05)
    pad1.SetLeftMargin(leftMargin)
    #pad1.SetFrameLineWidth(2)

    pad2.SetBottomMargin(0.37)
    pad2.SetTopMargin(0.0)
    pad2.SetRightMargin(0.05)
    pad2.SetLeftMargin(leftMargin)
    #pad2.SetFrameLineWidth(2)


    if cfg['logy']: pad1.SetLogy()
    if cfg['logx']:
        pad2.SetLogx()
        pad1.SetLogx()

    c.Modify()
    c.Update()

    return c, pad1, pad2
