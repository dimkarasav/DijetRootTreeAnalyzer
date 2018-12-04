import ROOT
import copy

ROOT.gROOT.SetBatch(1)

mass = 600

jmatchings = ["comb","jets01","jets02","jets12","dijetp"]

masses = [
    200, 300, 400, 500, 600, 800
]

#masses = [
#    mass
#]

selection = "jet2_pt>50 && jet1_pt>50 && isr_pt>50 && HLT_CaloScoutingHT250 && abs(dijet_deta)<1.2 "
variable = "dijet_mass"
binning = "(200,0,1000)"

dataFileName = "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/data_%s.root"
signalFileName = "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/signal_%s_%s.root"

###################################

ROOT.gStyle.SetOptStat(0)

c1 = ROOT.TCanvas("c1","",1280,720)
c1.SetLogy()
c1.SetGridx()
c1.SetGridy()

#colors = [
##ROOT.kRed +3,
#ROOT.kRed +1,
##ROOT.kRed -4,
#ROOT.kRed -7,
##ROOT.kRed -9,
##ROOT.kGreen +3,
#ROOT.kGreen +1,
##ROOT.kGreen -4,
#ROOT.kGreen -7,
##ROOT.kGreen -9,
##ROOT.kBlue +3,
#ROOT.kBlue +1,
#ROOT.kBlue -4,
##ROOT.kBlue -7,
##ROOT.kBlue -9,
#]

colors = [
ROOT.kRed,
ROOT.kGreen,
ROOT.kBlue,
ROOT.kMagenta,
ROOT.kBlack,
]

def getHisto(fileName, sel = selection):
    file_ = ROOT.TFile.Open(fileName)
    tree = file_.Get("rootTupleTree/tree")
    tree.Draw(variable + ">> histo"+binning, sel)
    histo = file_.Get("histo").Clone(fileName.replace("/",""))
    histo.SetLineWidth(2)
    return copy.copy(histo)

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
    s_sqrtB_max = s/(b**0.5)
    minBin = dat.GetBinLowEdge(bin_min)
    maxBin = dat.GetBinLowEdge(bin_max+1)
    return s,b,s_sqrtB_max,minBin,maxBin


data = {}
signal = {}
signalGoodMatch = {}
for jmatching in jmatchings:
    data[jmatching] = getHisto(dataFileName%jmatching)
    for mass in masses:
        signal[(jmatching,mass)] = getHisto(signalFileName%(jmatching,mass))
        signalGoodMatch[(jmatching,mass)] = getHisto(signalFileName%(jmatching,mass), selection + " && (sqrt(TVector2::Phi_mpi_pi(jet1_phi-jet1MC_phi)**2 + (jet1_eta-jet1MC_eta)**2)<0.4 && sqrt(TVector2::Phi_mpi_pi(jet2_phi-jet2MC_phi)**2 + (jet2_eta-jet2MC_eta)**2)<0.4) ")
    print(data[jmatching])

print(data)
print(signal)

## rescale to show plots nicer
for mass in masses:
    bin_ = data[jmatching].FindBin(mass)
#    scale = 10
    scale = 3. * data[jmatching].GetBinContent(bin_) / signal[("dijetp",mass)].GetBinContent(bin_)
    for jmatching in jmatchings:
        signal[(jmatching,mass)].Scale(scale)
        signalGoodMatch[(jmatching,mass)].Scale(scale)



for matching in [True,False]:
    if matching:
        signals = signal
    else:
        signals = signalGoodMatch
    for mass in masses:
        leg = ROOT.TLegend(0.78,0.58,0.98,0.98)
        print("M(jj) = %s GeV. Matching %s"%(mass,matching))
        for i,jmatching in enumerate(jmatchings):
            data[jmatching].SetLineColor(colors[i])
            signals[(jmatching,mass)].SetLineColor(colors[i])
            if i==0:
                signals[(jmatching,mass)].SetTitle("M(X) = %s GeV"%mass)
                signals[(jmatching,mass)].GetYaxis().SetTitle("Events")
                signals[(jmatching,mass)].GetXaxis().SetTitle("m_{jj} [GeV]")
                signals[(jmatching,mass)].GetYaxis().SetRangeUser(1E1,1E5)
                signals[(jmatching,mass)].Draw("")
            else:
                signals[(jmatching,mass)].Draw("same")
                
            data[jmatching].Draw("same")
            leg.AddEntry(data[jmatching],"widejet #DeltaR = %s"%jmatching)
        #    SsqrtB,minBin,maxBin = getBestSsqrtB(data[jmatching],signalGoodMatch[(jmatching,mass)])
        #    print("wide jet R=%s, S/sqrt(B)=%s, in mjj=[%s,%s]"%(jmatching,SsqrtB,minBin,maxBin))
            s,b,SsqrtB,minBin,maxBin = getSsqrtB(data[jmatching],signals[(jmatching,mass)],mass)
            print("wide jet s=%s b=%s R=%s, S/sqrt(B)=%s, in mjj=[%s,%s]"%(s,b,jmatching,SsqrtB,minBin,maxBin))
        leg.Draw()

        c1.Update()
        c1.Modified()
        if matching:
            c1.SaveAs("plots_pairMatching_%s_matching.png"%(mass))
        else:
            c1.SaveAs("plots_pairMatching_%s.png"%(mass))

#data[jmatching].Scale(1./data[jmatching].Integral())
#signal[(jmatching,mass)].Scale(1./signal[(jmatching,mass)].Integral())
#signalGoodMatch[(jmatching,mass)].Scale(1./signalGoodMatch[(jmatching,mass)].Integral())

#data[jmatching].Draw()
#signal[(jmatching,mass)].Draw("same")
#signalGoodMatch[(jmatching,mass)].Draw("same")


sig = signalGoodMatch[(jmatching,mass)]
dat = data[jmatching]

