import ROOT

k_low, k_up = 0.93, 1.13

folder = "bkgAndSigPlots"
title = "Dijet matching efficiency for M = XXX GeV "
colors = [
ROOT.kBlack,

ROOT.kRed,
ROOT.kBlue,
ROOT.kMagenta,
ROOT.kCyan+1,
ROOT.kGreen+2,
ROOT.kYellow+1,

ROOT.kGray+2,

ROOT.kViolet,
ROOT.kAzure,
ROOT.kTeal,
ROOT.kSpring,

ROOT.kOrange,
ROOT.kPink,
]


# ROOT.gROOT.SetBatch(0)
# canv2 = ROOT.TCanvas()


preselection = "HTgoodJets>250"
#preselection = "HTgoodJets>350  && mhtAK4<110"
#preselection = "isr_pt>70 && dijet_pt>140 && jet2_pt>45 && jet1_pt>90 && HTgoodJets>350 && trijet_dr<3.4 && fabs(trijet_eta)>0.3 && abs(dijet_deta)<1.2 && abs(trijet_dphi)<1.8 && mhtAK4Sig<0.11 && met<100 && mhtAK4<110"

#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11   "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  && jet2_pt>45   "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  && jet2_pt>45  && abs(dijet_deta)<1.2   "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  && jet2_pt>45  && abs(dijet_deta)<1.2  && dijet_pt>140   "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  && jet2_pt>45  && abs(dijet_deta)<1.2  && dijet_pt>140  &&  jet1_pt>90   "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  && jet2_pt>45  && abs(dijet_deta)<1.2  && dijet_pt>140  &&  jet1_pt>90   && mhtAK4<110   "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  && jet2_pt>45  && abs(dijet_deta)<1.2  && dijet_pt>140  &&  jet1_pt>90   && mhtAK4<110  && met<100  "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  && jet2_pt>45  && abs(dijet_deta)<1.2  && dijet_pt>140  &&  jet1_pt>90   && mhtAK4<110  && met<100 && isr_pt>70  "
#preselection = "HTgoodJets>350 && mhtAK4Sig<0.11  && trijet_dr<3.4  && jet2_pt>45  && abs(dijet_deta)<1.2  && dijet_pt>140  &&  jet1_pt>90   && mhtAK4<110  && met<100 && isr_pt>70 && fabs(trijet_eta)>0.3 "



common = "1"
common =  " run<=280385 && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && abs(isr_eta)<2.5  && HLT_CaloScoutingHT250 && HTgoodJets>0 && isr_pt>=50" #&& && abs(dijet_deta)<1.1

preselections = [
#    common + "&& isr_pt>=0",
#    common + "&& isr_pt>=30",
#    common + "&& isr_pt>=40",
    common + "&& isr_pt>=50",
#    common + "&& isr_pt>=60",
    #common + "&& isr_pt>=70",
    #common + "&& isr_pt>=80",
    #common + "&& isr_pt>=90",
    #common + "&& isr_pt>=100",
    #common + "&& isr_pt>=110",
    #common + "&& isr_pt>=120",
    #common + "&& isr_pt>=130",
    #common + "&& isr_pt>=140",
    #common + "&& isr_pt>=150",
    #common + "&& isr_pt>=160",
    #common + "&& isr_pt>=170",
    #common + "&& isr_pt>=180",
    #common + "&& isr_pt>=190",
    #common + "&& isr_pt>=200",
]


common = common + "&& dijet_mass>=540"
preselections = [
    common + "&& dijet_mass<=600",
    common + "&& dijet_mass<=605",
    common + "&& dijet_mass<=610",
    common + "&& dijet_mass<=615",
    common + "&& dijet_mass<=620",
    common + "&& dijet_mass<=625",
    common + "&& dijet_mass<=630",
    common + "&& dijet_mass<=635",
    common + "&& dijet_mass<=640",
    common + "&& dijet_mass<=645",
    common + "&& dijet_mass<=650",
    common + "&& dijet_mass<=655",
    common + "&& dijet_mass<=660",
    common + "&& dijet_mass<=665",
    common + "&& dijet_mass<=670",
    common + "&& dijet_mass<=675",
    common + "&& dijet_mass<=680",
    common + "&& dijet_mass<=685",
    common + "&& dijet_mass<=690",
    common + "&& dijet_mass<=695",
    common + "&& dijet_mass<=700",
    common + "&& dijet_mass<=705",
]

common = common + "&& dijet_mass<=680"
preselections = [
    common + "&& dijet_mass>=600",
    common + "&& dijet_mass>=590",
    common + "&& dijet_mass>=585",
    common + "&& dijet_mass>=580",
    common + "&& dijet_mass>=575",
    common + "&& dijet_mass>=570",
    common + "&& dijet_mass>=565",
    common + "&& dijet_mass>=560",
    common + "&& dijet_mass>=555",
    common + "&& dijet_mass>=550",
    common + "&& dijet_mass>=545",
]

common = common + "&& dijet_mass<=680"
preselections = [
    common + "&& abs(dijet_deta)<1.7",
    common + "&& abs(dijet_deta)<1.6",
    common + "&& abs(dijet_deta)<1.5",
    common + "&& abs(dijet_deta)<1.4",
    common + "&& abs(dijet_deta)<1.3",
    common + "&& abs(dijet_deta)<1.2",
    common + "&& abs(dijet_deta)<1.1",
    common + "&& abs(dijet_deta)<1.0",
    common + "&& abs(dijet_deta)<0.9",
    common + "&& abs(dijet_deta)<0.8",
]




#mcReco_matching = "mcReco_matching && method_jets01 && isrMC_pt>0"
mcReco_matching = "1"

histos = []

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
canv = ROOT.TCanvas("canv","",1280,720)
canv.SetGridx()
canv.SetGridy()
#canv.SetLogy()


fileNameBkg = "../ntupleTrigger/CaloJet40Skim.root"

fileNames = [
#    "../output/test_reduced_skim_new.root",
#    "../CaloScoutingHT250.root",
    #"../ntupleSignal/VectorDiJet1Jet_25_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_50_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_75_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_100_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_125_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_150_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_200_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_300_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_500_13TeV.root",
    "../ntupleSignal/VectorDiJet1Jet_600_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_800_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_1000_13TeV.root",
]

import copy
signals = {}
maxim = 0
fileBkg = ROOT.TFile(fileNameBkg)
treeBkg = fileBkg.Get("rootTupleTree/tree")

for preselection in preselections:
    print(preselection)
    for fileName in fileNames:
        #print("Opening %s"%(fileName))
        mass = fileName.split("VectorDiJet1Jet_")[1]
        mass = mass.split("_")[0]
        file_ = ROOT.TFile(fileName)
        tree = file_.Get("rootTupleTree/tree")
        if type(tree) != ROOT.TTree: 
            print("WARNING: skipping %s"%fileName)
            continue
        m = int(mass)
        m_low = m*k_low 
        m_up = m*k_up 
        print(m_low,m_up)
        sel = preselection + "&& (dijet_mass>%d) && (dijet_mass<%d)"%(m_low, m_up)
        signal = tree.Draw("", sel+"&&"+ mcReco_matching)
        bkg = treeBkg.Draw("", sel)
        print(preselection)
        print("mass = %s ; S/sqrt(B) = %f ; S/B = %f; S = %d; B = %d"%(mass, (1.*signal/bkg**0.5/14.143060), (1.*signal/bkg), signal, bkg))
        file_.Close()

