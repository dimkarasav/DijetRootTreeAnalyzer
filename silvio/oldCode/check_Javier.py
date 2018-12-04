import ROOT

# ROOT.gROOT.SetBatch(0)
# canv2 = ROOT.TCanvas()

ROOT.gROOT.SetBatch(1)
canv = ROOT.TCanvas()
canv.SetGridx()
canv.SetGridy()

ROOT.gStyle.SetOptStat(0)

fileName = "../ntupleTrigger/CaloJet40Skim.root"
denTrigger = "HLT_CaloJet40_CaloScouting_PFScouting"

fileNameJ = "root://eoscms.cern.ch//eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ScoutingCaloCommissioning_2017-01-18/rootfile_CaloScoutingCommissioning2016BCDEFG_JEC_CaloHLT_plus_V10p2_20170119_reduced_skim.root"
denTriggerJ = "passHLT_CaloJet40_CaloScouting_PFScouting"


#preselect  = denTrigger +  "  && abs(dijet_deta)<1.3  && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && jet1_pt>60 && jet2_pt>30 && PassJSON && HLT_CaloJet40_CaloScouting_PFScouting && run<=280385"
#preselectJ = denTriggerJ + " && abs(deltaETAjj)<1.3 && abs(etaWJ_j1)<2.5 && abs(etaWJ_j2)<2.5 && pTWJ_j1>60 && pTWJ_j2>30 && PassJSON && passHLT_CaloJet40_CaloScouting_PFScouting && run<=280385"

preselect  = denTrigger +  "  && abs(dijet_deta)<1.3  && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && jet1_pt>65 && jet2_pt>40 && dijet_mass>100 && PassJSON && HLT_CaloJet40_CaloScouting_PFScouting && run<=280385"
preselectJ = denTriggerJ + " && abs(deltaETAjj)<1.3 && abs(etaWJ_j1)<2.5 && abs(etaWJ_j2)<2.5 && pTWJ_j1>65 && pTWJ_j2>40 && PassJSON && passHLT_CaloJet40_CaloScouting_PFScouting && mjj>100 && run<=280385"


file_ = ROOT.TFile.Open(fileName)
fileJ_ = ROOT.TFile.Open(fileNameJ)

tree = file_.Get("rootTupleTree/tree")
treeJ = fileJ_.Get("tree")

trigger = "HLT_CaloScoutingHT250"
title = "Trigger efficiency of HLT_CaloScoutingHT250"

vars_=[
    ("mjj", "dijet_mass", 100,0,1000),
    ("run", "run", 1000,273000,280385),
    ("abs(deltaETAjj)", "abs(dijet_deta)", 100,0,4.5),
    ("pTWJ_j1", "jet1_pt", 100,50,350),
    ("pTWJ_j2", "jet2_pt", 100,20,330),
]

for var in vars_:
    (varXJ,varX,varX_nbins,   varX_min,  varX_max) = var
    print(var)

    preselect += "&& (%s < %d)"%(varX,varX_max)


    tree.Draw("%s >> den1D(%d,%f,%f)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"NORM,HIST")
    den = ROOT.gDirectory.Get("den1D")
    treeJ.Draw("%s >> denJ1D(%d,%f,%f)"%(varXJ,varX_nbins,varX_min,varX_max),"%s"%(preselectJ) ,"NORM,HIST")
    denJ = ROOT.gDirectory.Get("denJ1D")

    den.Sumw2()
    denJ.Sumw2()

    den.SetTitle("denominator")
    denJ.SetTitle("denominator")

    den.Draw("HIST,")
    denJ.Draw("HIST,same")
    denJ.SetLineColor(ROOT.kRed)

    name = varXJ
    name = name.replace("(","")
    name = name.replace(")","")
    canv.SaveAs(name+".png")
    canv.SaveAs(name+".root")
    canv.SaveAs(name+".C")
