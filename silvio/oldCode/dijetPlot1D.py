import ROOT

# ROOT.gROOT.SetBatch(0)
# canv2 = ROOT.TCanvas()

ROOT.gROOT.SetBatch(1)
canv = ROOT.TCanvas()
canv.SetGridx()
canv.SetGridy()

ROOT.gStyle.SetOptStat(0)
#fileName = "/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ScoutingCaloCommissioning_2017-01-18/CommissioningG/rootfile_CaloScoutingCommissioning2016G_JEC_CaloHLT_plus_V10p2_20170119_001201_reduced_skim.root"
#fileName = "rootFile_reduced_skim.root"
fileName = "../output/test_reduced_skim.root"

file_ = ROOT.TFile(fileName)

tree = file_.Get("rootTupleTree/tree")

trigger = "1"
#trigger = "(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)"
#trigger = "HLT_L1HTT_CaloScouting_PFScouting"
#preselect = "HLT_CaloJet40_CaloScouting_PFScouting"
preselect = "1" #&& isr_pt>130
title = "DijetEfficiency"
#(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)

varX = "dijet_pt"
varX_nbins,   varX_min,  varX_max = 50,0,500
varX_title = "pt_{jj}"

preselect += "&& (%s < %d)"%(varX,varX_max)

tree.Draw("%s >> dijetden1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"")
den = ROOT.gDirectory.Get("dijetden1D")
tree.Draw("%s >> dijetnum1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s && %s"%(preselect,trigger) ,"")
num = ROOT.gDirectory.Get("dijetnum1D")
num.Sumw2()
den.Sumw2()
eff = ROOT.TGraphAsymmErrors();
eff.SetName("dijet1D")
eff.Divide(num,den)

eff.SetTitle(title)
eff.SetMaximum(1.0001)
eff.SetMinimum(0.9)
num.SetTitle("numerator")
den.SetTitle("denominator")

eff.GetXaxis().SetTitle(varX_title)
eff.Draw("AP")
canv.SaveAs(eff.GetName()+".png")
canv.SaveAs(eff.GetName()+".root")
canv.SaveAs(eff.GetName()+".C")
for histo in [num, den]:
    histo.GetXaxis().SetTitle(varX_title)
    histo.Draw("E")
    canv.SaveAs(histo.GetName()+".png")
    canv.SaveAs(histo.GetName()+".root")
    canv.SaveAs(histo.GetName()+".C")
    
