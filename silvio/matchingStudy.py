import ROOT
import copy

ROOT.gROOT.SetBatch(1)

mass = 600

wj = 1.1

#wjs = [round(x/10.,1) for x in range(4,19,1)]

matchings = [
"jets01",
"jets02",
"jets12",
]

#masses = [
#    200, 300, 400, 500, 600, 800
#]

masses = [
    200, 300, 400, 500, 600, 800, 1000
#    300,
]

#masses = [
#    mass
#]

selection = "jet1_pt>50 && jet2_pt>50 && isr_pt>50 && HLT_CaloScoutingHT250"
variable = "dijet_mass"
binning = "(200,0,1000)"

treeVars = [
    "jet1_pt","jet1_eta","jet1_phi","jet1_mass",
    "jet2_pt","jet2_eta","jet2_phi","jet2_mass",
    "isr_pt","isr_eta","isr_phi","isr_mass",
#    "jet1MC_pt","jet1MC_eta","jet1MC_phi","jet1MC_mass",
#    "jet2MC_pt","jet2MC_eta","jet2MC_phi","jet2MC_mass",
#    "isrMC_pt","isrMC_eta","isrMC_phi","isrMC_mass",
    "HLT_CaloScoutingHT250","dijet_mass","htAK4"
    ]

### files produced abd skimmed with  matchingStudySkim.py ###

dataFileName   = "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/silvio/matchingStudies/data_trig_eff_wo_runH_eta2.5.root"
signalFileName = "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/silvio/matchingStudies/signal_jets01_%s.root"

###################################

ROOT.gStyle.SetOptStat(0)

c1 = ROOT.TCanvas("c1","",1280,720)
c1.SetLogy()
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

j1 = ROOT.TLorentzVector()
j2 = ROOT.TLorentzVector()
j3 = ROOT.TLorentzVector()

jets = [j1, j2, j3]

def getDijet(jets,matching):
    if(matching=="jets01"):
        idx1=0
        idx2=1
        idx3=2
    elif(matching=="jets02"):
        idx1=0
        idx2=2
        idx3=1
    elif(matching=="jets12"):
        idx1=1
        idx2=2
        idx3=0
    else:
        print("Matching %s not found in getDijet()"%matching)
    return (idx1,idx2,idx3)
    

def getHistos(fileName, sel = selection):
    histos = {}
    (nbins,xmax,xmin) = binning [1:-1].split(",")
    (nbins,xmax,xmin) = (int(nbins),float(xmax),float(xmin))
    for matching in matchings:
        histos[matching] = ROOT.TH1F("histo",fileName.replace("/","")+matching,nbins,xmax,xmin)
        histos[matching].SetLineWidth(2)
    print("Opening: %s"%(fileName))
    file_ = ROOT.TFile.Open(fileName)
    tree = file_.Get("tree")
    tree.SetBranchStatus("*",0)
    for treeVar in treeVars:
        tree.SetBranchStatus(treeVar,1)
#    tree.Draw(variable + ">> histo"+binning, sel)
#    histo = file_.Get("histo").Clone(fileName.replace("/",""))
    mass = -1
    for i,event in enumerate(tree):
        if i%10000==0: print i 
        for matching in matchings:
            mass = -1
            if(min(event.jet1_pt,event.jet2_pt,event.isr_pt)>70 and max(abs(event.jet1_eta),abs(event.jet2_eta),abs(event.isr_eta))<2.5):
                jets[0].SetPtEtaPhiM( event.jet1_pt, event.jet1_eta, event.jet1_phi, event.jet1_mass) 
                jets[1].SetPtEtaPhiM( event.jet2_pt, event.jet2_eta, event.jet2_phi, event.jet2_mass) 
                jets[2].SetPtEtaPhiM( event.isr_pt,  event.isr_eta,  event.isr_phi,  event.isr_mass)
                (idx1,idx2,idx3) = getDijet(jets,matching)
                if abs(jets[idx1].Eta()-jets[idx2].Eta())<1.1:
                    mass = (jets[idx1]+jets[idx2]).M()
            histos[matching].Fill(mass)
    return histos

def getBestSsqrtB(dat,sig):
    s_sqrtB_max = 0
    for i in range(mass-100,mass,10):
        bin_min = sig.FindBin(i)
        for j in range(mass,mass+300,10):
            bin_max = sig.FindBin(j)
            s = 1.*sig.Integral(bin_min, bin_max)
            b = 1.*dat.Integral(bin_min, bin_max)
            s_sqrtB = s/(b**0.5)
            if s_sqrtB>s_sqrtB_max:
                s_sqrtB_max = s_sqrtB
                minBin = dat.GetBinLowEdge(bin_min)
                maxBin = dat.GetBinLowEdge(bin_max+1)
    #            print(i,j,s,b,s_sqrtB_max)
    return s_sqrtB_max,minBin,maxBin

def getSsqrtB(dat,sig, mass):
    bin_min = sig.FindBin(mass*0.98)
    bin_max = sig.FindBin(mass*1.02)
    s = 1.*sig.Integral(bin_min, bin_max)
    b = 1.*dat.Integral(bin_min, bin_max)
    s_sqrtB_max = s/(b**0.5+1e-10)
    minBin = dat.GetBinLowEdge(bin_min)
    maxBin = dat.GetBinLowEdge(bin_max+1)
    return s_sqrtB_max,minBin,maxBin


data = {}
signal = {}
signalGoodMatch = {}
data = getHistos(dataFileName,matchings)
for mass in masses:
    signal[mass] = getHistos(signalFileName%(mass),matchings)
#        signalGoodMatch[(matching,mass)] = getHistos(signalFileName%(matching,mass), selection + " && (sqrt(TVector2::Phi_mpi_pi(jet1_phi-jet1MC_phi)**2 + (jet1_eta-jet1MC_eta)**2)<0.4 && sqrt(TVector2::Phi_mpi_pi(jet2_phi-jet2MC_phi)**2 + (jet2_eta-jet2MC_eta)**2)<0.4) ")
print(data)

print(data)
print(signal)

'''
## rescale to show plots nicer
for mass in masses:
    bin_ = data[matching].FindBin(mass)
    scale = 10. * data[matching].GetBinContent(bin_) / signal[(0.4,mass)].GetBinContent(bin_)
    for matching in matchings:
        signal[(matching,mass)].Scale(scale)
        signalGoodMatch[(matching,mass)].Scale(scale)
'''



for genmatching in [False]:
    if genmatching:
        signals = signalGoodMatch
    else:
        signals = signal
    for mass in masses:
        leg = ROOT.TLegend(0.78,0.58,0.98,0.98)
        leg.SetHeader("")
        for i,matching in enumerate(matchings):
            print("M(jj) = %s GeV. Matching %s"%(mass,matching))
            data[matching].SetLineColor(colors[i])
            signals[mass][matching].SetLineColor(colors[i])
            if i==0:
                signals[mass][matching].SetTitle("M(X) = %s GeV"%mass)
                signals[mass][matching].GetYaxis().SetTitle("Events")
                signals[mass][matching].GetXaxis().SetTitle("m_{jj} [GeV]")
                signals[mass][matching].GetYaxis().SetRangeUser(1E1,1E4)
                signals[mass][matching].Draw("")
            else:
                signals[mass][matching].Draw("same")
                
            data[matching].Draw("same")
            leg.AddEntry(data[matching],"matching = %s"%matching)
        #    SsqrtB,minBin,maxBin = getBestSsqrtB(data[wj],signalGoodMatch[(wj,mass)])
        #    print("wide jet R=%s, S/sqrt(B)=%s, in mjj=[%s,%s]"%(wj,SsqrtB,minBin,maxBin))
            SsqrtB,minBin,maxBin = getSsqrtB(data[matching],signals[mass][matching],mass)
            print("wide jet R=%s, S/sqrt(B)=%s, in mjj=[%s,%s]"%(matching,SsqrtB,minBin,maxBin))
        leg.Draw()

        c1.Update()
        c1.Modified()
        if genmatching:
            c1.SaveAs("plots_matching_%s_matching.png"%mass)
        else:
            c1.SaveAs("plots_matching_%s.png"%mass)

#data[wj].Scale(1./data[wj].Integral())
#signal[(wj,mass)].Scale(1./signal[(wj,mass)].Integral())
#signalGoodMatch[(wj,mass)].Scale(1./signalGoodMatch[(wj,mass)].Integral())

#data[wj].Draw()
#signal[(wj,mass)].Draw("same")
#signalGoodMatch[(wj,mass)].Draw("same")


sig = signal[mass][matching]
dat = data[matching]

fileOut = ROOT.TFile("matchingStudy.root","recreate")
fileOut.cd()
for matching in matchings:
    data[matching].SetName("data_%s"%(matching))
    data[matching].Write()
    for mass in masses:
        signal[mass][matching].SetName("sig_%s_%s"%(mass,matching))
        signal[mass][matching].Write()

fileOut.Close()

