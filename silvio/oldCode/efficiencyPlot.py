import ROOT

ROOT.gROOT.SetBatch()
canv = ROOT.TCanvas()
canv.SetGridx()
canv.SetGridy()

ROOT.gStyle.SetOptStat(0)

fileName = "../ntupleTrigger/CaloJet40Skim_lowLumi.root"
denTrigger = "HLT_CaloJet40_CaloScouting_PFScouting"

#fileName = "../ntupleTrigger/L1HTTSkim.root"
#denTrigger = "1"

#fileName = "../ntupleSignal/VectorDiJet1Jet_300_13TeV.root"
#denTrigger = "1"

file_ = ROOT.TFile(fileName)
#tree = file_.Get("rootTupleTree/tree")
tree = file_.Get("tree")

#preselect = denTrigger + "&& min(dijet_pt,isr_pt)>140 && dijet_dr>0 && min(dijet_pt,isr_pt)"
#preselect = denTrigger + "&& min(dijet_pt,isr_pt)>0"

preselect = denTrigger + " && run<280385  && abs(dijet_deta)<0.7 && jet2_pt>40  && HTgoodJets>210"

preselect = denTrigger + "   && abs(dijet_deta)<1.3 && abs(jet1_eta)<2.5 &&  abs(jet2_eta)<2.5 && jet1_pt>60 && jet2_pt>30 && run<28038"

preselect = denTrigger +  "  && run<=280385 && PassJSON && L1_HTT240" #&& isr_pt>90

preselect = denTrigger +  " && run<=280385 && PassJSON && isr_pt>=0 && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && abs(isr_eta)<2.5 && dijet_mass<340 && dijet_mass>260" #&& isr_pt>90




trigger = "HLT_CaloScoutingHT250"
#trigger = "(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)"
#trigger = "HLT_L1HTT_CaloScouting_PFScouting"
#preselect = "HLT_CaloJet40_CaloScouting_PFScouting"
title = "Trigger efficiency of HLT_CaloScoutingHT250"
#(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)

#varX = "pTWJ_j1+pTWJ_j2+isr_pt"
#varX_nbins,   varX_min,  varX_max = 20,0,1000
#varX_title = "p^{T}_{1}+p^{T}_{2}+p^{T}_{3}"

#varX = "isr_pt"
#varX_nbins,   varX_min,  varX_max = 100,0,1000
#varX_title = "p^{T}_{jj}"

#varX = "dijet_mass"
#varX_nbins,   varX_min,  varX_max = 100,0,1000
#varX_title = "m_{jj}"

#varX = "jet1_pt+jet2_pt"
#varX_nbins,   varX_min,  varX_max = 100,0,1000
#varX_title = "p^{T}_{1}+p^{T}_{2}"

#varX = "mjj"
#varX_nbins,   varX_min,  varX_max = 100,0,1000
#varX_title = "m_{jj}"

#varX = "2*max(max(pTWJ_j1,pTWJ_j2),isr_pt)"
#varX_nbins,   varX_min,  varX_max = 200,0,1000
#varX_title = "m_{jj}"


#varY = "dijet_pt" ## pTWJ_j1+pTWJ_j2
#varY_title = "p^{T}_{jj}"

#varY = "min(dijet_pt,isr_pt)" ## pTWJ_j1+pTWJ_j2
#varY_title = "min(p^{T}_{jj},p^{T}_{ISR})"
#varY_nbins, varY_min, varY_max = 50,0,100

#varY = "dijet_pt" ## pTWJ_j1+pTWJ_j2
#varY_title = "p^{T}_{jj}"
#varY_nbins, varY_min, varY_max = 50,0,200

varY = "isr_pt" ## pTWJ_j1+pTWJ_j2
varY_title = "p^{T}_{ISR}"
varY_nbins, varY_min, varY_max = 20,40,140

varX = "dijet_deta" ## pTWJ_j1+pTWJ_j2
varX_title = "#Delta#eta(jj)"
varX_nbins, varX_min, varX_max = 15,0,3.0


#varY = "HTgoodJets" ## pTWJ_j1+pTWJ_j2
##varY = "HTgoodJets-jet1_pt-jet2_pt" ## pTWJ_j1+pTWJ_j2
#varY_title = "HT (GeV)"
#varY_nbins, varY_min, varY_max = 100,0,500


preselect += "&& (%s < %d)"%(varX,varX_max)
preselect += "&& (%s < %d)"%(varY,varY_max)

tree.Draw("%s:%s >> den(%f,%f,%f,%f,%f,%f)"%(varY,varX,varX_nbins,varX_min,varX_max,varY_nbins, varY_min, varY_max),"%s"%(preselect) ,"COLZ")
den = ROOT.gDirectory.Get("den")
tree.Draw("%s:%s >> num(%f,%f,%f,%f,%f,%f)"%(varY,varX,varX_nbins,varX_min,varX_max,varY_nbins, varY_min, varY_max),"%s && %s"%(preselect,trigger) ,"COLZ")
num = ROOT.gDirectory.Get("num")
eff = num.Clone("eff")
eff.Divide(num,den,1,1,"cl=0.683 b(1,1) mode")

eff.SetTitle(title)
num.SetTitle("numerator")
den.SetTitle("denominator")
for histo in [num, den, eff]:
    histo.GetXaxis().SetTitle(varX_title)
    histo.GetYaxis().SetTitle(varY_title)
    histo.Draw("COLZ")
    canv.SaveAs(histo.GetName()+".png")
    canv.SaveAs(histo.GetName()+".root")
    canv.SaveAs(histo.GetName()+".C")
    
for ax in ["x","y"]:
    if ax == "x":
        num_proj = num.ProjectionX()
        den_proj = den.ProjectionX()
    elif ax == "y":
        num_proj = num.ProjectionY()
        den_proj = den.ProjectionY()
    den_proj.Sumw2()
    num_proj.Sumw2()
    eff_proj = num_proj.Clone("eff_p"+ax)
    eff_proj.GetYaxis().SetTitle("Efficiency")
    eff_proj.Divide(num_proj,den_proj,1,1,"cl=0.683 b(1,1) mode")
    eff_proj.Draw("E")
    canv.SaveAs(eff_proj.GetName()+".png")
    canv.SaveAs(eff_proj.GetName()+".root")
    canv.SaveAs(eff_proj.GetName()+".C")
