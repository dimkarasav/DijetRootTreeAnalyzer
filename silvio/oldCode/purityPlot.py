import ROOT

ROOT.gROOT.SetBatch()
canv = ROOT.TCanvas()
canv.SetGridx()
canv.SetGridy()

ROOT.gStyle.SetOptStat(0)

#fileName = "../ntupleTrigger/CaloJet40Skim_lowLumi.root"
fileName = "../ntupleTrigger/L1HTTSkim.root"
fileNameSig = "../ntupleSignal/VectorDiJet1Jet_300_13TeV.root"
dataSelection = "L1_HTT240"
signalSelection = "mcReco_matching && method_jets01"

preselect = " run<=280385 && PassJSON && isr_pt>=0 && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && abs(isr_eta)<2.5 && dijet_mass<340 && dijet_mass>260 && HLT_CaloScoutingHT250" #&& isr_pt>90

file_ = ROOT.TFile(fileName)
fileSig = ROOT.TFile(fileNameSig)
tree = file_.Get("tree")
treeSig = fileSig.Get("rootTupleTree/tree")

title = "Signal purity"

varY = "isr_pt" ## pTWJ_j1+pTWJ_j2
varY_title = "p^{T}_{ISR}"
varY_nbins, varY_min, varY_max = 20,40,140

varX = "dijet_deta" ## pTWJ_j1+pTWJ_j2
varX_title = "#Delta#eta(jj)"
varX_nbins, varX_min, varX_max = 15,0,3.0


preselect += "&& (%s < %d)"%(varX,varX_max)
preselect += "&& (%s < %d)"%(varY,varY_max)

tree.Draw("%s:%s >> data(%f,%f,%f,%f,%f,%f)"%(varY,varX,varX_nbins,varX_min,varX_max,varY_nbins, varY_min, varY_max),"%s && %s"%(preselect, dataSelection) ,"COLZ")
data = ROOT.gDirectory.Get("data")
treeSig.Draw("%s:%s >> signal(%f,%f,%f,%f,%f,%f)"%(varY,varX,varX_nbins,varX_min,varX_max,varY_nbins, varY_min, varY_max),"%s && %s"%(preselect, signalSelection) ,"COLZ")
signal = ROOT.gDirectory.Get("signal")

ratio = signal.Clone("ratio")
ratio.Divide(signal,data,1,1,"cl=0.683 b(1,1) mode")

ratio.SetTitle(title)
signal.SetTitle("signal")
data.SetTitle("data")

for histo in [signal, data, ratio]:
    histo.GetXaxis().SetTitle(varX_title)
    histo.GetYaxis().SetTitle(varY_title)
    histo.Draw("COLZ")
    canv.SaveAs(histo.GetName()+".png")
    canv.SaveAs(histo.GetName()+".root")
    canv.SaveAs(histo.GetName()+".C")
    
for ax in ["x","y"]:
    if ax == "x":
        signal_proj = signal.ProjectionX()
        data_proj = data.ProjectionX()
    elif ax == "y":
        signal_proj = signal.ProjectionY()
        data_proj = data.ProjectionY()
    data_proj.Sumw2()
    signal_proj.Sumw2()
    ratio_proj = signal_proj.Clone("ratio_p"+ax)
    ratio_proj.GetYaxis().SetTitle("Efficiency")
    ratio_proj.Divide(signal_proj,data_proj,1,1,"cl=0.683 b(1,1) mode")
    ratio_proj.Draw("E")
    canv.SaveAs(ratio_proj.GetName()+".png")
    canv.SaveAs(ratio_proj.GetName()+".root")
    canv.SaveAs(ratio_proj.GetName()+".C")
