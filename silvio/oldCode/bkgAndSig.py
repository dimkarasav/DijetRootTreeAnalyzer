
import ROOT

#lumi = 27228.596620089 #pb-1
lumi = 30.522039 #pb-1
#lumi = 0.239289 #pb-1
xsect = 1. #pb

log = False
MCmatch = True

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

#&& dijet_mass>113.75 && dijet_mass<148.75
#preselection = "isr_pt>70 && dijet_pt>140 && dijet_dr>0.0 && jet2_pt>45 && jet1_pt>90 && HTgoodJets>350 && trijet_dr<3.4 && fabs(trijet_eta)>0.3 && abs(dijet_deta)<1.2 && abs(trijet_dphi)<1.8 && mhtAK4Sig<0.11 && met<100 && mhtAK4<110 && dijet_mass>113.75 && dijet_mass<148.75"
#preselection = "HTgoodJets>350 && addHT>60 && isr_pt<200 && met>120"
#preselection = "HTgoodJets>350 && htAK4>550 && HTgoodJets<450 && htAK4<650 "
#preselection = "dijet_pt>100 && dijet_dr>0.8 && jet2_pt>40"
preselection =  " run<=280385 && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && abs(isr_eta)<2.5 && abs(dijet_deta)<1.1 && HLT_CaloScoutingHT250 && HTgoodJets>0 && isr_pt>=50" #&& 

#  
#&& abs(dijet_deta)<1.2  && mhtAK4Sig<0.16 
#&& isr_pt>40
#&& abs(dijet_deta)<1.1
#mcReco_matching = "1"
#mcReco_matching = "mcReco_matching && method_jets01"
mcReco_matching = "1"

#trigger = "HLT_CaloScoutingHT250"
trigger = "L1_HTT240"

plots = [
     ("dijet_mass", 100,0, 1000, "mass(jj) [GeV]"),
     #("abs(dijet_deta)", 50, 0, 5, "#Delta#eta(jj) "),
     #("isr_pt", 15,-1, 150, "p^{T}(ISR) [GeV]"),
     #("dijet_pt", 50,0, 500, "p^{T}_{jj} [GeV]"),
     #("min(dijet_pt,isr_pt)", 50,0, 500, "min(p^{T}_{jj} , p^{T}(ISR)) [GeV]"),
     #("htAK4", 50, 0, 1000, "HT all jets"),
     #("HTgoodJets", 50, 0, 1000, "HT good jets"),

     #("dijet_dr", 50, 0, 5, "#DeltaR(jj)"),
     #("dijet_pt", 50,0, 500, "p^{T}_{jj} [GeV]"),
     #("dijet_dr", 50, 0, 5, "#DeltaR(jj)"),
     #("jet1_pt", 50,50, 350, "p^{T}(jet_{1}) [GeV]"),
     #("jet1_eta", 50,-5, 5, "#eta(jet_{1}) "),
##     ("jet1_idtight", 2,0, 2, "ID(jet_{1}) "),
     #("jet2_eta", 50,-5, 5, "#eta(jet_{2}) "),
     #("jet2_pt", 50,0, 250, "p^{T}(jet_{2}) [GeV]"),
##     ("jet2_idtight", 2,0, 2, "ID(jet_{2}) "),
     #("abs(dijet_deta)", 50, 0, 5, "#Delta#eta(jj) "),
     #("abs(dijet_dphi)", 50, 0, 5, "#Delta#phi(jj)"),
     #("(abs(dijet_deta)/dijet_dr)**2", 50, 0, 1, "#Delta#phi(jj)/#DeltaR(jj)^{2}"),
     #("(abs(dijet_dphi)/dijet_dr)**2", 50, 0, 1, "#Delta#eta(jj)/#DeltaR(jj)^{2}"),
     #("TMath::ACos(dijet_deta/dijet_dr)*((dijet_phi>0) - (dijet_phi<0))", 150, -3.2, 3.2, "cos^{-1}(#Delta#eta(jj)/#DeltaR(jj))"),
     #("dijet_eta", 50, -5, 5, "#eta(jj) "),
##     ("dijet_phi", 50, -3.2, 3.2, "#phi(jj) "),
     #("isr_pt", 50,50, 550, "p^{T}(ISR) [GeV]"),
     #("isr_eta", 50, -5, 5, "#eta(ISR) "),
##     ("isr_idtight", 2,0, 2, "ID(ISR) "),
##     ("isr_phi", 50, -3.2, 3.2, "#phi(ISR) "),
     #("trijet_pt", 50,0, 400, "p^{T}(jj+ISR) [GeV]"),
     #("trijet_eta", 50,-5, +5, "#eta(jj+ISR) [GeV]"),
     #("trijet_mass", 50,0, 1500, "m(jj+ISR) [GeV]"),
     #("trijet_dr", 50, 0, 5, "#DeltaR(jj,ISR)"),
     #("abs(trijet_deta)", 50, 0, 5, "#Delta#eta(jj,ISR)"),
     #("abs(trijet_dphi)", 50, 0, 5, "#Delta#phi(jj,ISR)"),
     #("nJet", 15, 0, 15, "n good jets"),
     #("Nak4", 15, 0, 15, "n jets"),
     #("addHT", 50, 0, 300, "additional HT"),
     #("mhtAK4", 50, 0, 300, "MHT"),
     #("mhtAK4Sig", 50, 0, 0.5, "MHT sig."),
     #("met", 50, 0, 300, "MET"),
     #("nVtx", 60, 0, 60, "nVtx"),
]

histos = []

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
#canv = ROOT.TCanvas("canv","",1280,720)
canv = ROOT.TCanvas("canv","",640,480)
canv.SetGridx()
canv.SetGridy()
if log:
    canv.SetLogy()

fileNames = [
    #"../ntupleTrigger/CaloJet40Skim.root",

    #"../ntupleTrigger/L1HTTSkim.root",
    #"../ntupleSignal/VectorDiJet1Jet_300_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_500_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_600_13TeV.root",

    "../ntupleTrigger/L1HTTSkim.root",
    #"../ntupleTrigger_pt20/CaloJet40Skim.root",
    "../ntupleSignal/VectorDiJet1Jet_300_13TeV.root",
    "../ntupleSignal/VectorDiJet1Jet_400_13TeV.root",
    "../ntupleSignal/VectorDiJet1Jet_500_13TeV.root",
    "../ntupleSignal/VectorDiJet1Jet_600_13TeV.root",

    #"../ntupleTrigger_pt30/L1HTTSkim.root",
    #"../ntupleSignal_pt30/VectorDiJet1Jet_300_13TeV.root",
    #"../ntupleSignal_pt30/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal_pt30/VectorDiJet1Jet_500_13TeV.root",
    #"../ntupleSignal_pt30/VectorDiJet1Jet_600_13TeV.root",

    #"../ntupleTrigger_AK4/CaloJet40Skim.root",
    #"../ntupleSignal_AK4/VectorDiJet1Jet_300_13TeV.root",
    #"../ntupleSignal_AK4/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal_AK4/VectorDiJet1Jet_500_13TeV.root",
    #"../ntupleSignal_AK4/VectorDiJet1Jet_600_13TeV.root",

#    "../output/test_reduced_skim_new.root",
#    "../CaloScoutingHT250.root",
#    "/scratch/sdonato/CaloScoutingHT250.root",
    #"../ntupleTrigger/CaloJet40Skim.root",
    #"../output_20171220_125506/rootfile_list_ScoutingCaloHT_Run2016F-v2_CaloScoutingHT250_20171220_125506_741_reduced_skim.root",
###    #"../ntupleSignal/VectorDiJet1Jet_25_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_50_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_75_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_100_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_125_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_150_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_200_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_300_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_500_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_600_13TeV.root",
###    #"../ntupleSignal/VectorDiJet1Jet_800_13TeV.root",
###    #"../ntupleSignal/VectorDiJet1Jet_1000_13TeV.root",

####    "../ntupleOtherMCs/Hbb.root",
####    "../ntupleOtherMCs/WJetsHT180.root",
####    "../ntupleOtherMCs/WJetsHT600.root",
####    "../ntupleOtherMCs/ZJetsHT180.root",
####    "../ntupleOtherMCs/TT.root",
####    "../ntupleOtherMCs/ZJetsHT600.root",
####    "../ntupleOtherMCs/QCDHT50.root",
####    "../ntupleOtherMCs/QCDHT100.root",
#    "../ntupleOtherMCs/QCDHT200.root",
#    "../ntupleOtherMCs/QCDHT300.root",
#    "../ntupleOtherMCs/QCDHT500.root",
#    "../ntupleOtherMCs/QCDHT700.root",
####    "../ntupleOtherMCs/QCDHT1000.root",
####    "../ntupleOtherMCs/QCDHT1500.root",
####    "../ntupleOtherMCs/QCDHT2000.root",

    #"../ntupleTrigger_dR2p0/L1HTTSkim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR2p0_20180202_150635_0_reduced_skim.root",

    #"../ntupleTrigger_dR1p6/L1HTTSkim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR1p6_20180202_150700_0_reduced_skim.root",

    #"../ntupleTrigger/L1HTTSkim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR1p0_20180202_150720_0_reduced_skim.root"
]


#fileNames = [
#    "../output/test_reduced_skim.root",
#    "../output_20171220_103246/rootfile_list_VectorDiJet1Jet_125_13TeV_TEST_20171220_093230_0_reduced_skim.root"
#]


def getHisto(tree, sel, xvar,xbins,xmin,xmax):
    #print("%s >> histo(%d, %d, %d)"%(xvar,xbins,xmin,xmax), sel)
    tree.Draw("min(max(%s,%f),%f) >> histo(%f, %f, %f)"%(xvar,xmin*1.00001,xmax*0.9999,xbins,xmin,xmax), sel,"")
    histo = ROOT.gDirectory.Get("histo")
    return histo

import copy
histos = {}
maxim = 0
for fileName in fileNames:
    print("Opening %s"%(fileName))
    if "VectorDiJet1Jet_" in fileName:
        try:
            mass = fileName.split("VectorDiJet1Jet_")[1]
            mass = mass.split("_")[0]
        except:
            mass = fileName.split("/")[-1].replace(".root","")
            pass
    else:
        mass = "data"
    print(mass)
    file_ = ROOT.TFile(fileName)
    countHisto = file_.Get("DijetFilter/EventCount/EventCounter")
    ratio = 1.*countHisto.GetBinContent(3)/countHisto.GetBinContent(1)
    tree = file_.Get("rootTupleTree/tree")
    if type(tree) != ROOT.TTree: 
        print("WARNING: skipping %s"%fileName)
        continue
    for (xvar, xbins, xmin, xmax, xtitle) in plots:
        sel = preselection 
        if(MCmatch and mass.isdigit()): sel = sel + "&&" + mcReco_matching
        if mass=="data": sel = sel + "&&" + trigger 
        histo = getHisto(tree, sel, xvar,xbins,xmin,xmax)
        if mass!="data": histo.Scale(1.*xsect*lumi*ratio)
        histo = histo.Clone(mass)
        histo.SetLineWidth(3)
        histo.SetLineColor(colors[fileNames.index(fileName)])
        histo.SetMarkerColor(colors[fileNames.index(fileName)])
        histo.SetTitle(xtitle)
        histo.GetXaxis().SetTitle(xtitle)
        histo.GetYaxis().SetTitle("Events / %.1f"%((1.*xmax-xmin)/xbins))
        #leg.SetHeader("")
        histos[(fileName,xvar,)] = copy.copy(histo)
        if ("maxim",xvar) in histos:
            histos[("maxim",xvar)] =  max(histos[("maxim",xvar)],histo.GetMaximum())
        else:
            histos[("maxim",xvar)] =  histo.GetMaximum()
    file_.Close()

print(histos)
for (xvar, xbins, xmin, xmax, xtitle) in plots: 
    leg = ROOT.TLegend(0.9,0.1,0.999,0.9)
    for fileName in fileNames:
        histo = histos[(fileName,xvar)]
        leg.AddEntry(histo,histo.GetName(),"lep")
        histo.SetMaximum(histos[("maxim",xvar)]*1.2)
        histo.SetMinimum(1E-3)
        if fileNames.index(fileName) == 0:
             histo.Draw("")
        else:
             histo.Draw("same")
    leg.Draw()
    name = ''.join([char for char in xtitle if char.isalnum()])
    canv.SaveAs(folder+"/bkgAndSig_"+name+".png")
    canv.SaveAs(folder+"/bkgAndSig_"+name+".root")

