import ROOT
import copy

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine(".L function.C++")


mass = 600
i=0

wj = 0.4
#wjs = [round(x/10.,1) for x in range(4,19,1)]

masses = [
    200, 300, 400, 500, 600, 800
]


#masses = [ mass ]

selection = "isr_pt>50 && HLT_CaloScoutingHT250 && abs(dijet_deta)<1.2"
#&& min(sqrt(TVector2::Phi_mpi_pi(jet1_phi-jet1MC_phi)**2 + (jet1_eta-jet1MC_eta)**2),sqrt(TVector2::Phi_mpi_pi(jet1_phi-jet2MC_phi)**2 + (jet1_eta-jet2MC_eta)**2))<0.05
variable = "sqrt(TVector2::Phi_mpi_pi(jet2_phi-isr_phi)**2 + (jet2_eta-isr_eta)**2)"
binning = "(100,0,4)"

signalFileName = "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/wideJetMC/signal_%s_wj%s.root"

###################################

ROOT.gStyle.SetOptStat(0)

c1 = ROOT.TCanvas("c1","",1280,720)
#c1.SetLogy()
c1.SetGridx()
c1.SetGridy()

colors = [
ROOT.kRed +3,
ROOT.kRed +1,
ROOT.kRed -4,
ROOT.kRed -7,
ROOT.kRed -9,
ROOT.kGreen +3,
ROOT.kGreen +1,
ROOT.kGreen -4,
ROOT.kGreen -7,
ROOT.kGreen -9,
ROOT.kBlue +3,
ROOT.kBlue +1,
ROOT.kBlue -4,
ROOT.kBlue -7,
ROOT.kBlue -9,
]


def getHisto(fileName, sel = selection):
    file_ = ROOT.TFile.Open(fileName)
    tree = file_.Get("rootTupleTree/tree")
    tree.Draw(variable + ">> histo"+binning, sel)
    histo = file_.Get("histo").Clone(fileName.replace("/",""))
    histo.SetLineWidth(2)
    return copy.copy(histo)

signal = {}
signalFSR = {}
signalNoFSR = {}
for mass in masses:
    signal[(wj,mass)] = getHisto(signalFileName%(mass,wj))
    signal[(wj,mass)].SetLineColor(ROOT.kBlack)
#    signalFSR[(wj,mass)] = getHisto(signalFileName%(mass,wj),selection+" && !(isrMC_pt!=0 && min(sqrt(TVector2::Phi_mpi_pi(isr_phi-isrMC_phi)**2 + (isr_eta-isrMC_eta)**2),sqrt(TVector2::Phi_mpi_pi(jet2_phi-isrMC_phi)**2 + (jet2_eta-isrMC_eta)**2))<1)")
    signalFSR[(wj,mass)] = getHisto(signalFileName%(mass,wj),selection+" && min(dRmatch(isr_pt,isr_eta,isr_phi,jet2_pt,jet2_eta,jet2_phi,jet2MC_pt,jet2MC_eta,jet2MC_phi),dRmatch(isr_pt,isr_eta,isr_phi,jet2_pt,jet2_eta,jet2_phi,jet1MC_pt,jet1MC_eta,jet1MC_phi))<0.15")
#    signalFSR[(wj,mass)] = getHisto(signalFileName%(mass,wj),selection+" && isrMC_pt==0")
    signalFSR[(wj,mass)].SetLineStyle(3)
    signalFSR[(wj,mass)].SetLineColor(ROOT.kRed)
    signalNoFSR[(wj,mass)] = getHisto(signalFileName%(mass,wj),selection+" && min(dRmatch(isr_pt,isr_eta,isr_phi,jet2_pt,jet2_eta,jet2_phi,jet2MC_pt,jet2MC_eta,jet2MC_phi),dRmatch(isr_pt,isr_eta,isr_phi,jet2_pt,jet2_eta,jet2_phi,jet1MC_pt,jet1MC_eta,jet1MC_phi))>0.15")
#    signalNoFSR[(wj,mass)] = getHisto(signalFileName%(mass,wj),selection+" && isrMC_pt!=0 ")
    signalNoFSR[(wj,mass)].SetLineStyle(3)
    signalNoFSR[(wj,mass)].SetLineColor(ROOT.kBlue)
    signal[(wj,mass)].SetLineWidth(3)
    signalFSR[(wj,mass)].SetLineWidth(3)
    signalNoFSR[(wj,mass)].SetLineWidth(3)

print(signal)




for mass in masses:
    leg = ROOT.TLegend(0.78,0.58,0.98,0.98)
    signal[(wj,mass)].SetTitle("M(X) = %s GeV"%mass)
    signal[(wj,mass)].GetYaxis().SetTitle("Events")
    signal[(wj,mass)].GetXaxis().SetTitle("#DeltaR(j_{2},j_{3})")
#    signal[(wj,mass)].GetYaxis().SetRangeUser(1E1,1E4)
    signal[(wj,mass)].Draw("")
    signalFSR[(wj,mass)].Draw("same")
    signalNoFSR[(wj,mass)].Draw("same")
    
    leg.AddEntry(signal[(wj,mass)],"inclusive")
    leg.AddEntry(signalFSR[(wj,mass)],"FSR")
    leg.AddEntry(signalNoFSR[(wj,mass)],"No FSR")
    
    leg.Draw()
    
    c1.Update()
    c1.Modified()
    c1.SaveAs("plots_deltaR_%s.png"%mass)
