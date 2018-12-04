import ROOT

# ROOT.gROOT.SetBatch(0)
# canv2 = ROOT.TCanvas()

ROOT.gROOT.SetBatch(1)
canv = ROOT.TCanvas("canv","",1280,1024)
canv.SetGridx()
canv.SetGridy()

ROOT.gStyle.SetOptStat(0)


#fileName = "../ntupleTrigger_dR2p0/L1HTTSkim.root" #_lowPt
#fileName = "../ntupleTrigger_dR1p6/L1HTTSkim.root" #_lowPt
#fileName = "../ntupleTrigger_pt40/L1HTTSkim.root" #_lowPt
#fileName = "../ntupleTrigger_pt50/CaloJet40Skim.root" #_lowPt
#fileName = "../ntupleTrigger/CaloJet40Skim_lowLumi.root" #_lowPt
#fileName = "../ntupleTrigger_pt30/CaloJet40Skim.root" #_lowPt
fileName = "../ntupleTrigger_pt60/CaloJet40Skim_lowLumi.root" #_lowPt
denTrigger = "1"

#preselect = denTrigger + "&& min(dijet_pt,isr_pt)>140 && dijet_dr>0 && min(dijet_pt,isr_pt)"
#preselect = denTrigger + "&& min(dijet_pt,isr_pt)>0"

preselect = denTrigger + " && run<280385  && abs(dijet_deta)<0.7 && jet2_pt>40  && HTgoodJets>210"

preselect = denTrigger + "   && abs(dijet_deta)<1.3 && abs(jet1_eta)<2.5 &&  abs(jet2_eta)<2.5 && jet1_pt>60 && jet2_pt>30 && run<28038"

preselect = denTrigger +  "  && run<=280385 && PassJSON && L1_HTT240" #&& isr_pt>90

preselect = denTrigger +  " && run<=280385 && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && abs(isr_eta)<2.5 && abs(dijet_deta)<1.1 && isr_pt>=70 " #&& 


file_ = ROOT.TFile(fileName)

tree = file_.Get("rootTupleTree/tree")
if not type(tree)==ROOT.TTree: tree = file_.Get("tree")

trigger = "HLT_CaloScoutingHT250"

title = "Trigger efficiency of HLT_CaloScoutingHT250"
#trigger = "(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)"
#trigger = "HLT_L1HTT_CaloScouting_PFScouting"
#preselect = "HLT_CaloJet40_CaloScouting_PFScouting"
#(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)

 
#varX = "min(dijet_pt,isr_pt)"
#varX_nbins,   varX_min,  varX_max = 20,120,320
#varX_title = "min(dijet_pt,isr_pt)"

varX = "dijet_mass"
varX_nbins,   varX_min,  varX_max = 40,150,550
varX_title = "m_{jj}"

#varX = "HTgoodJets"
##varX = "htAK4"
#varX_nbins,   varX_min,  varX_max = 100,0,500
#varX_title = "HT (GeV)"

#varX = "jet1_eta"
#varX_nbins,   varX_min,  varX_max = 100,-5,5
#varX_title = "#eta"

preselect += "&& (%s < %d)"%(varX,varX_max)

tree.Draw("%s >> den1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"")
den = ROOT.gDirectory.Get("den1D")
tree.Draw("%s >> num1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s && %s"%(preselect,trigger) ,"")
num = ROOT.gDirectory.Get("num1D")
num.Sumw2()
den.Sumw2()
eff = ROOT.TGraphAsymmErrors();
eff.SetName("eff1D")
eff.Divide(num,den)

eff.SetTitle(title)
eff.SetMaximum(1.0001)
eff.SetMinimum(0.)
num.SetTitle("numerator")
den.SetTitle("denominator")

for histo in [num, den]:
    histo.GetXaxis().SetTitle(varX_title)
    histo.Draw("E")
    canv.SaveAs(histo.GetName()+".png")
    canv.SaveAs(histo.GetName()+".root")
    canv.SaveAs(histo.GetName()+".C")
    

func = ROOT.TF1("func","erf((x-[0])/[1])*[2]+[3]",varX_min,varX_max)
func.SetParLimits(2,0.25,0.5)
func.SetParLimits(3,0.5,1)
func.SetParameters(200,40,0.5,0.5)
#func = ROOT.TF1("func","[0]",varX_min,varX_max)
func.SetParameter(0,0.99)
eff.Fit(func,"L","",varX_min,varX_max)
eff.Fit(func,"L","",func.GetParameter(0),varX_max)
eff.Fit(func,"L","",func.GetParameter(0)+func.GetParameter(1)*0.,varX_max)
eff.Fit(func,"L","",func.GetParameter(0)+func.GetParameter(1)*0.,varX_max)

#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
eff.GetXaxis().SetTitle(varX_title)
eff.Draw("AP")
canv.SaveAs(eff.GetName()+".png")
canv.SaveAs(eff.GetName()+".root")
canv.SaveAs(eff.GetName()+".C")
