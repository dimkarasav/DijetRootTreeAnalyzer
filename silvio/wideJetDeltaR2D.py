import ROOT
import copy

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine(".L function.C++")

mass = 600
i=0

wj = 0.4
#wjs = [round(x/10.,1) for x in range(4,19,1)]

masses = [
    800, 600, 500, 400, 300, 200
]


# masses = [ mass ]

selection = "isr_pt>50 && HLT_CaloScoutingHT250 && abs(dijet_deta)<1.2"

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

for var in ["jet3","jet2","dijetPt",]:
    if var == "jet3":
        variable = "sqrt(TVector2::Phi_mpi_pi(jet2_phi-isr_phi)**2 + (jet2_eta-isr_eta)**2) : isr_pt"
        label = "p^{T}_{j3} [GeV]"
    elif var == "jet2":
        variable = "sqrt(TVector2::Phi_mpi_pi(jet2_phi-isr_phi)**2 + (jet2_eta-isr_eta)**2) : jet2_pt"
        label = "p^{T}_{j2} [GeV]"
    elif var == "dijetPt":
        variable = "sqrt(TVector2::Phi_mpi_pi(jet2_phi-isr_phi)**2 + (jet2_eta-isr_eta)**2) : dijet_pt"
        label = "p^{T}_{jj} [GeV]"
    
    signal = {}
    signalFSR = {}
    signalNoFSR = {}
    for mass in masses:
        binning = "(50,0,%s,50,0,4)"%int(mass*4/6)
        signal[(wj,mass)] = getHisto(signalFileName%(mass,wj))
        signal[(wj,mass)].SetLineColor(ROOT.kBlack)
        signalFSR[(wj,mass)] = getHisto(signalFileName%(mass,wj),selection+" && min(dRmatch(isr_pt,isr_eta,isr_phi,jet2_pt,jet2_eta,jet2_phi,jet2MC_pt,jet2MC_eta,jet2MC_phi),dRmatch(isr_pt,isr_eta,isr_phi,jet2_pt,jet2_eta,jet2_phi,jet1MC_pt,jet1MC_eta,jet1MC_phi))<0.15")
        signalFSR[(wj,mass)].SetLineStyle(3)
        signalFSR[(wj,mass)].SetLineColor(ROOT.kRed)
        signalNoFSR[(wj,mass)] = getHisto(signalFileName%(mass,wj),selection+" && min(dRmatch(isr_pt,isr_eta,isr_phi,jet2_pt,jet2_eta,jet2_phi,jet2MC_pt,jet2MC_eta,jet2MC_phi),dRmatch(isr_pt,isr_eta,isr_phi,jet2_pt,jet2_eta,jet2_phi,jet1MC_pt,jet1MC_eta,jet1MC_phi))>0.15")
        signalNoFSR[(wj,mass)].SetLineStyle(3)
        signalNoFSR[(wj,mass)].SetLineColor(ROOT.kBlue)
        signal[(wj,mass)].SetLineWidth(3)
        signalFSR[(wj,mass)].SetLineWidth(3)
        signalNoFSR[(wj,mass)].SetLineWidth(3)

    print(signal)



    signalTot = copy.copy(signal[(wj,mass)].Clone("signalTot"))
    signalTot.Reset()
    signalTotNoFSR = copy.copy(signalTot).Clone("signalTotNoFSR")
    signalTotFSR = copy.copy(signalTot).Clone("signalTotFSR")

    for mass in masses:
        for val in ["incl","FSR","noFSR"]:
            if val == "incl":
                histo = signal[(wj,mass)]
                histoTot = signalTot
                title = "Inclusive "
            elif val == "noFSR":
                histo = signalNoFSR[(wj,mass)]
                histoTot = signalTotFSR
                title = "No FSR "
            elif val == "FSR":
                histo = signalFSR[(wj,mass)]
                histoTot = signalTotNoFSR
                title = "FSR "
            
            histo.SetTitle(title+"M(X) = %s GeV"%mass)
            histoTot.SetTitle(title)
            for histoX in [histo,histoTot]:
                histoX.GetYaxis().SetTitle("#DeltaR(j_{2},j_{3})")
                histoX.GetXaxis().SetTitle(label)
            histo.Draw("COLZ")
            histoTot.Add(histo)
            
            c1.Update()
            c1.Modified()
            c1.SaveAs("plots_deltaR_vs%s_2D_%s_%s.png"%(var,mass,val))
            if masses.index(mass) == len(masses)-1:
                histoTot.Draw("COLZ")
                c1.SaveAs("plots_deltaR_vs%s_2D_TOT_%s.png"%(var,val))
