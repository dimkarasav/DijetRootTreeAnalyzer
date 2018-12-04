
import ROOT
ROOT.gROOT.SetBatch(0)

#lumi = 27228.596620089 #pb-1
lumi = 30.522039 #pb-1
#lumi = 0.239289 #pb-1
xsect = 1. #pb

log = False
MCmatch = False

folder = "wideJetPlots"
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
#preselection = "abs(dijet_deta)<1.3 && HTgoodJets>0 && run<=280385 && isr_pt>40" # 
#preselection = "HTgoodJets>250 &&  isrMC_pt>60"
preselection = " run<=280385 && PassJSON && isr_pt>=50 && isr_pt<=70 && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && abs(isr_eta)<2.5  && abs(dijet_deta)<1.1" #&& isr_pt>90

preselection =  " run<=280385 && PassJSON && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && abs(isr_eta)<2.5 && abs(dijet_deta)<1.1 && HLT_CaloScoutingHT250 && HTgoodJets>0 && isrMC_pt>=0 && isr_pt>=0" #&& && isr_pt>50

#&& HLT_CaloScoutingHT250
#&& mcReco_matching
#abs(dijet_deta)<0.7 && abs(jet1_eta)<1.6 &&  abs(jet2_eta)<1.6 && run<=280385 && PassJSON && 

#  
#&& abs(dijet_deta)<1.2  && mhtAK4Sig<0.16 
#&& isr_pt>40
#&& abs(dijet_deta)<1.1
mcReco_matching = "1 "
#mcReco_matching = "mcReco_matching && method_jets01"
#trigger = "HLT_CaloScoutingHT250"
trigger = "HLT_L1HTT_CaloScouting_PFScouting"

plots = [
     ("dijet_mass", 100,100, 600, "mass(jj) [GeV]"),
#     ("trijet_mass", 100,100, 800, "mass(jj) [GeV]"),
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
     #("(abs(dijet_deta)/dijet_dr)**2", 50, 0, 1, "#Delta#phi(jj)/#DeltaR(jj)^{2}"),ad
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
canv = ROOT.TCanvas("canv","",1280,1024)
#canv = ROOT.TCanvas("canv","",640,480)
canv.SetGridx()
canv.SetGridy()
if log:
    canv.SetLogy()

fileNames = [
    #"../output_20180130_174545/rootfile_list_VectorDiJet1Jet_300_13TeV_dR_0p7_20180130_174545_0_reduced_skim.root",
    #"../output_20180130_174612/rootfile_list_VectorDiJet1Jet_300_13TeV_dR_0p9_20180130_174612_0_reduced_skim.root",
    #"../output_20180130_174621/rootfile_list_VectorDiJet1Jet_300_13TeV_dR_1p1_20180130_174621_0_reduced_skim.root",
    #"../output_20180130_174626/rootfile_list_VectorDiJet1Jet_300_13TeV_dR_1p3_20180130_174626_0_reduced_skim.root",

    #"../output_20180130_183828/rootfile_list_VectorDiJet1Jet_500_13TeV_dR_1p9_20180130_183828_1_reduced_skim.root",
    #"../output_20180130_183839/rootfile_list_VectorDiJet1Jet_500_13TeV_dR_1p7_20180130_183839_1_reduced_skim.root",
    #"../output_20180130_183847/rootfile_list_VectorDiJet1Jet_500_13TeV_dR_1p5_20180130_183847_1_reduced_skim.root",
    #"../output_20180130_183851/rootfile_list_VectorDiJet1Jet_500_13TeV_dR_1p3_20180130_183851_1_reduced_skim.root",
    #"../output_20180130_183857/rootfile_list_VectorDiJet1Jet_500_13TeV_dR_1p1_20180130_183857_1_reduced_skim.root",
    #"../output_20180130_183906/rootfile_list_VectorDiJet1Jet_500_13TeV_dR_0p9_20180130_183906_1_reduced_skim.root",
    #"../output_20180130_183915/rootfile_list_VectorDiJet1Jet_500_13TeV_dR_0p7_20180130_183915_1_reduced_skim.root",
    #"../output_20180130_183922/rootfile_list_VectorDiJet1Jet_500_13TeV_dR_0p5_20180130_183922_1_reduced_skim.root",

    #"../ntupleSignal_pt20/VectorDiJet1Jet_100_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_200_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_300_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_500_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_600_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_800_13TeV.root",

    #"../ntupleSignal_pt20/VectorDiJet1Jet_100_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_200_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_300_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_500_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_600_13TeV.root",
    #"../ntupleSignal_pt20/VectorDiJet1Jet_800_13TeV.root",

    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_Pt10_20180202_123226_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_Pt15_20180202_123239_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_Pt20_20180202_123150_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_Pt25_20180202_123301_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_Pt30_20180202_123314_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_Pt35_20180202_123326_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_Pt40_20180202_123346_0_reduced_skim.root",

    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR0p4_20180202_150743_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR0p6_20180202_150739_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR0p8_20180202_150730_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR1p0_20180202_150720_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR1p2_20180202_150713_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR1p4_20180202_150706_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR1p6_20180202_150700_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR1p8_20180202_150647_0_reduced_skim.root",
    #"../rootfile_list_VectorDiJet1Jet_400_13TeV_SIG400_DR2p0_20180202_150635_0_reduced_skim.root",

    "../ntupleSignal_pt20/VectorDiJet1Jet_300_13TeV.root",
    "../ntupleSignal_pt30/VectorDiJet1Jet_300_13TeV.root",
    "../ntupleSignal/VectorDiJet1Jet_300_13TeV.root",
    "../ntupleSignal_pt50/VectorDiJet1Jet_300_13TeV.root",

    #"../ntupleSignal_pt20/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal_pt30/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal/VectorDiJet1Jet_400_13TeV.root",
    #"../ntupleSignal_pt50/VectorDiJet1Jet_400_13TeV.root",
]



def getHisto(tree, sel, xvar,xbins,xmin,xmax):
    #print("%s >> histo(%d, %d, %d)"%(xvar,xbins,xmin,xmax), sel)
    tree.Draw("%s >> histo(%f, %f, %f)"%(xvar,xbins,xmin,xmax), sel,"")
    #tree.Draw("min(max(%s,%f),%f) >> histo(%f, %f, %f)"%(xvar,xmin*1.00001,xmax*0.9999,xbins,xmin,xmax), sel,"")
    histo = ROOT.gDirectory.Get("histo")
    return histo

import copy
histos = {}
maxim = 0
for fileName in fileNames:
    print("Opening %s"%(fileName))
    if "VectorDiJet1Jet_" in fileName:
        if "_DR" in fileName: 
            mass = fileName.split("_DR")[1]
        elif "_SIG400_Pt" in fileName:
            mass = fileName.split("_SIG400_Pt")[1]
        elif "DiJet1Jet_" in fileName:
            mass = fileName.split("DiJet1Jet_")[1]
        try:
            mass = mass.split("_")[0]
        except:
            mass = fileName.split("/")[-1].replace(".root","")
            pass
    else:
        mass = "data"
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
#        fit = ROOT.TF1("fit","gaus(0)+pol0(3)",320,420)
        fit = ROOT.TF1("fit","gaus",320,420)
#        fit.SetParameters(1.36896e+05,3.69617e+02,5.23616e+01,1)
        fit.SetLineColor(histo.GetLineColor())
        histo.Fit(fit)
        histo.Fit(fit,"L","",200,600)
        m = fit.GetParameter(1)
        s = fit.GetParameter(2)*1.4
        histo.Fit(fit,"L","",m-s,m+s)
        m = fit.GetParameter(1)
        s = fit.GetParameter(2)*1.4
        histo.Fit(fit,"L","",m-s,m+s)
        m = fit.GetParameter(1)
        s = fit.GetParameter(2)
        print(s/m*100,"%")
#        histo.Scale(1./histo.Integral())
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

