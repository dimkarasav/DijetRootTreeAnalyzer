import ROOT

redoPlot = True

## evaluate the ratio
def getRatio(data, funct, padSizeRatio):
    ratio = data.Clone("ratio")
    ratio.Reset()
    
    ratio.GetYaxis().SetLabelSize(padSizeRatio*data.GetYaxis().GetLabelSize())
    ratio.GetXaxis().SetLabelSize(padSizeRatio*data.GetXaxis().GetLabelSize())
    ratio.GetYaxis().SetTitleSize(padSizeRatio*data.GetYaxis().GetTitleSize())
    ratio.GetXaxis().SetTitleSize(padSizeRatio*data.GetXaxis().GetTitleSize())
    ratio.GetYaxis().SetTitleOffset(1./padSizeRatio*data.GetYaxis().GetTitleOffset())
    ratio.GetXaxis().SetTitleOffset(1./data.GetXaxis().GetTitleOffset())
    ratio.GetYaxis().SetTitle("Pull")    
    ratio.GetXaxis().SetTitle(data.GetXaxis().GetTitle())    
    ratio.GetYaxis().SetNdivisions(805)
    
    for i in range(data.GetNbinsX()):
        fx = max(0.001,funct.Eval(ratio.GetBinCenter(i)))
        val = (data.GetBinContent(i) - fx)/(fx**0.5)
        ratio.SetBinContent(i,val)
    
    ratio.SetMaximum(5)
    ratio.SetMinimum(-5)
    return ratio
    



'''
ROOT.gROOT.SetBatch(0)
canv2 = ROOT.TCanvas()
'''

ROOT.gROOT.SetBatch(1)
#canv = ROOT.TCanvas("canv","",1280,720)
canv = ROOT.TCanvas("canv","",640,480)
canv.SetGridx()
canv.SetGridy()
canv.SetLogy(1)

ROOT.gStyle.SetOptStat(0)
#fileName = "/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ScoutingCaloCommissioning_2017-01-18/CommissioningG/rootfile_CaloScoutingCommissioning2016G_JEC_CaloHLT_plus_V10p2_20170119_001201_reduced_skim.root"
#fileName = "rootFile_reduced_skim.root"

fileName = "../ntupleTrigger/L1HTTSkim.root"
#fileName = "../ntupleSignal/VectorDiJet1Jet_150_13TeV.root"
denTrigger = "HLT_CaloScoutingHT250"

#fileName = "../CaloScoutingHT250.root"
#denTrigger = "HLT_CaloScoutingHT250"
#denTrigger = "1"

#fileName = "../ntupleTrigger/CaloJet40Skim.root"
#denTrigger = "1"


preselect = denTrigger + "&& HTgoodJets>210 && abs(dijet_deta)<0.7 && run<280385 && jet2_pt>40 && isr_pt>40 " #
title = "Di-jet mass plot"

varX = "dijet_mass"
varX_nbins,   varX_min,  varX_max = 200,100,1100
#varX_nbins,   varX_min,  varX_max = 1000,60,1050
varX_title = "m_{jj}"

fit_min = 220

#######################################################

canv.SetTitle(title)
preselect += "&& (%s < %d)"%(varX,varX_max)

if redoPlot:
    file_ = ROOT.TFile(fileName)
    tree = file_.Get("rootTupleTree/tree")
    tree.Draw("%s >> histo(%f,%f,%f)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"")
    histo = ROOT.gDirectory.Get("histo")
    histo.GetYaxis().SetTitle("Events / %d GeV"%((varX_max-varX_min)/varX_nbins)) 
    histo.Sumw2()
    histo.Draw("HIST")
    canv.SaveAs("histoMjj.root")
else:
    file_ = ROOT.TFile("histoMjj.root")
    histo = file_.Get("canv").GetPrimitive("histo")
    histo = histo.Clone("histo")

histo.GetXaxis().SetTitle(varX_title)
histo.Draw("E")

funct = ROOT.TF1("funct","exp([p0]+[p1]*x+[p2]*x*x+[p3]*x*x*x+[p4]*x*x*x*x+[p5]*x*x*x*x*x+[p6]*x*x*x*x*x*x)",fit_min,varX_max)
#funct = ROOT.TF1("funct","pol5",varX_min,varX_max)
#funct = ROOT.TF1("funct","expo",varX_min,varX_max)
#funct = ROOT.TF1("funct","expo(0) + gaus(2)",varX_min,varX_max)
#funct = ROOT.TF1("funct","expo(0)")
funct.SetParameter(0,14)
funct.SetParameter(1,-1E-3)
funct.FixParameter(2,0)
funct.FixParameter(3,0)
funct.FixParameter(4,0)
funct.FixParameter(5,0)
funct.FixParameter(6,0)
histo.Fit(funct,"L","",fit_min,varX_max)
funct.ReleaseParameter(2)
funct.SetParameter(2,-1E-6)
histo.Fit(funct,"L","",fit_min,varX_max)
funct.ReleaseParameter(3)
funct.SetParameter(3,-1E-8)
histo.Fit(funct,"L","",fit_min,varX_max)
funct.ReleaseParameter(4)
funct.SetParameter(4,-1E-11)
histo.Fit(funct,"L","",fit_min,varX_max)
funct.ReleaseParameter(5)
funct.SetParameter(5,-1E-15)
histo.Fit(funct,"L","",fit_min,varX_max)
funct.ReleaseParameter(6)
funct.SetParameter(6,-1E-20)
histo.Fit(funct,"L","",fit_min,varX_max)



histo.Fit(funct,"L","",fit_min,varX_max)
histo.Fit(funct,"L","",fit_min,varX_max)
histo.Fit(funct,"L","",fit_min,varX_max)

#funct.FixParameter(3,0)
#funct.FixParameter(4,0)
#histo.Fit(funct)
#funct.ReleaseParameter(2)
#funct.ReleaseParameter(3)
#funct.ReleaseParameter(4)
#funct.SetParameter(2,1000)
#funct.SetParameter(3,200)
#funct.SetParameter(4,30)
#histo.Fit(funct)
#histo.Fit(funct)
#histo.Fit(funct)
#histo.Fit(funct)
histo.SetTitle(title)

canv.Draw()

yPadSeparation = 0.25
padPlot = ROOT.TPad("padPlot","",0.,yPadSeparation,1.,1.)
padPlot.SetBottomMargin(.02)
padRatio = ROOT.TPad("padRatio","",0.,0.,1.,yPadSeparation)
padRatio.SetTopMargin(0)
padRatio.SetBottomMargin(.09/yPadSeparation)
padRatio.Draw()
padPlot.Draw()
padRatio.SetGridx()
padRatio.SetGridy()
padPlot.SetGridx()
padPlot.SetGridy()
padPlot.SetLogy(1)
padPlot.cd()
histo.Draw("HIST")
#funct.Draw("same")


padPlot.SetTitle(title)
padRatio.SetTitle("")


padPlot.Draw()
padRatio.cd()

padSizeRatio = (padPlot.GetWh()*padPlot.GetAbsHNDC())/(padRatio.GetWh()*padRatio.GetAbsHNDC())
ratio = getRatio(histo,funct,padSizeRatio)
ratio.Draw("E")
padRatio.Draw()


canv.SaveAs(histo.GetName()+".png")
canv.SaveAs(histo.GetName()+".root")
canv.SaveAs(histo.GetName()+".C")
