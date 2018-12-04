import ROOT


def closestJetIdx(jets,quark,pt=0):
    dRmin = 999.
    closet = -1
    for idx in range(len(jets)):
        dR = jets[idx].DeltaR(quark)
        if dR<dRmin and jets[idx].Pt()>pt:
            dRmin = dR
            closet = idx
    return closet

def widejetsF(jets,dRmax,pt):
    widejets = []
    for jet in jets:
        if jet.Pt()>pt: widejets.append(jet)
    for i in reversed(range(len(widejets))):
        j = 0
        merged = False
        while j<i and not merged:
            if widejets[i].DeltaR(widejets[j]) < dRmax:
                widejets[j] = widejets[j] + widejets[i] 
                merged = True
            j+=1
    return widejets

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

]


preselection = " run<=280385 && PassJSON && isr_pt>=50 && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && abs(isr_eta)<2.5  && abs(dijet_deta)<1.1 " #&& isr_pt>90
#&& HLT_CaloScoutingHT250
#&& mcReco_matching
#abs(dijet_deta)<0.7 && abs(jet1_eta)<1.6 &&  abs(jet2_eta)<1.6 && run<=280385 && PassJSON && 

#  
#&& abs(dijet_deta)<1.2  && mhtAK4Sig<0.16 
#&& isr_pt>40
#&& abs(dijet_deta)<1.1
mcReco_matching = "1"
#mcReco_matching = "mcReco_matching && method_jets01"
#trigger = "HLT_CaloScoutingHT250"
trigger = "HLT_L1HTT_CaloScouting_PFScouting"

histos = []

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(0)
#canv = ROOT.TCanvas("canv","",1280,720)
canv = ROOT.TCanvas("canv","",640,480)
canv.SetGridx()
canv.SetGridy()
if log:
    canv.SetLogy()

fileNames = [
    "root://storage01.lcg.cscs.ch///pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_400_13TeV-madgraph/VectorDiJet1Jet_400_13TeV-madgraph_V2/171216_121105/0000/dijetscouting_bigtree_1.root"
]


#varX = "dijet_deta" ## pTWJ_j1+pTWJ_j2
varX_title = "blabla"
varX_nbins, varX_min, varX_max = 100,0,3.0

#varY = "isr_pt" ## pTWJ_j1+pTWJ_j2
varY_title = "blabla"
#varY_nbins, varY_min, varY_max = 100,0,1
varY_nbins, varY_min, varY_max = 100,0,100

import copy
histos = {}
maxim = 0
#for fileName in fileNames:
fileName = fileNames[0]


dRs = [0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0]
pts = [10,15,20,25,30,35,40,45,50,55,60]
histos = []
histosMass = []
histo = ROOT.TH2F("histo","",varY_nbins, varY_min, varY_max,varX_nbins, varX_min, varX_max )
#for i in range(len(pts)):
for i in range(len(dRs)):
    histos.append(ROOT.TH1F("histo"+str(dRs[i]),"",40,0,2 ))
    histos[-1].SetLineColor(colors[i])
    histos[-1].SetLineWidth(2)
    
    histosMass.append(ROOT.TH1F("histoMass"+str(dRs[i]),"",100,0,1000 ))
    histosMass[-1].SetLineColor(colors[i])
    histosMass[-1].SetLineWidth(2)

res = ROOT.TH2F("res","",20,0,100,20,0,3)
if True: 
    print("Opening %s"%(fileName))
    file_ = ROOT.TFile.Open(fileName)
    tree = file_.Get("dijetscouting/events")
    if type(tree) != ROOT.TTree: 
        print("WARNING: skipping %s"%fileName)
#        continue
    count =0
    for ev in tree:
        count +=1
        if count>100000: break
        quarks = []
        for (nd,pt,eta,phi,energy) in zip(tree.gen_numDaught,tree.gen_pt,tree.gen_eta,tree.gen_phi,tree.gen_energy):
            if nd==0:
                quark =ROOT.TLorentzVector()
                quark.SetPtEtaPhiE(pt,eta,phi,energy)
                quarks.append(quark)
        
        #if len(quarks)<=3 or min(quarks[0].Pt(),quarks[1].Pt(),quarks[2].Pt())<50: continue
        
        jets = []
        #for (pt,eta,phi,energy) in zip(tree.jetPtGenAK4,tree.jetEtaGenAK4,tree.jetPhiGenAK4,tree.jetEnergyGenAK4):
        for (pt,eta,phi,energy) in zip(tree.jetPtAK4,tree.jetEtaAK4,tree.jetPhiAK4,tree.jetEnergyAK4):
            if pt>40:
                jet =ROOT.TLorentzVector()
                jet.SetPtEtaPhiE(pt,eta,phi,energy)
                jets.append(jet)
        
        if len(jets)<2 or abs(jets[0].Eta()-jets[1].Eta())>1.2: continue
        ht = 0
        for jet in jets: ht += jet.Pt()
        if ht<300: continue
        
        jets_ = jets[:]
        #remove closest jets
        for quark in quarks:
            idx = closestJetIdx(jets,quark,quark.Pt()/2)
            if idx>=0: del jets[idx]
        
        for jet in jets:
            quark = quarks[closestJetIdx(quarks,jet)]
            dR = quark.DeltaR(jet)
            #print(dR,jet.Pt())
            histo.Fill(jet.Pt(),dR) #/quark.E()
            #if jet.Pt()>100:
                #print("Jets:")
                #for jet in jets_: print(jet.Pt(),jet.Eta(),jet.Phi())
                #print("Quarks:")
                #for jet in quarks: print(jet.Pt(),jet.Eta(),jet.Phi())
                #print("")
        
#        widejets = jets_
        
        for i in range(len(dRs)):
            pt = 0
            dR = dRs[i]
            if pt==60:  widejets = jets_
            else: widejets = widejetsF(jets_,dR,pt)
            for quark in quarks:
                idx = closestJetIdx(widejets,quark)
                if idx>0:
                    jet = widejets[idx]
                    histos[i].Fill(jet.Pt()/quark.Pt())
            if len(widejets)>=2 and abs(widejets[0].Eta()-widejets[1].Eta())>1.2: continue #or min(widejets[0].Pt(),widejets[1].Pt(),widejets[2].Pt())<50
            if len(widejets)>=3 and min(widejets[0].Pt(),widejets[1].Pt(),widejets[2].Pt())<50: 
                histosMass[i].Fill((widejets[0]+widejets[1]).M())
            #if len(widejets)>=2:
                #histosMass[i].Fill((widejets[0]+widejets[1]).M())
            #else:
                #histosMass[i].Fill(257)
        
        
#file_.Close()
histo.Draw("COLZ")
canv.Update()

canv2 = ROOT.TCanvas("canv2","",640,480)
canv2.SetGridx()
canv2.SetGridy()
histos[0].Draw()
max_ = 0
leg = ROOT.TLegend(0.9,0.1,0.999,0.9)

for histo in histos: 
    leg.AddEntry(histo,str(dRs[histos.index(histo)]),"lep")
    histo.Draw("same")
    max_ = max(histo.GetMaximum(),max_)

histos[0].SetMaximum(max_*1.1)
leg.Draw()
canv2.Update()

canv3 = ROOT.TCanvas("canv3","",640,480)
canv3.SetGridx()
canv3.SetGridy()
histosMass[0].Draw()
max_ = 0
leg = ROOT.TLegend(0.9,0.1,0.999,0.9)

for i in range(len(histosMass)): 
    histo = histosMass[i]
    leg.AddEntry(histo,str(dRs[i]),"lep")
    histo.Draw("same")
    max_ = max(histo.GetMaximum(),max_)

histosMass[0].SetMaximum(max_*1.1)
leg.Draw()
canv3.Update()

canv.SaveAs("wideJetStudy1.png")
canv2.SaveAs("wideJetStudy2.png")
canv3.SaveAs("wideJetStudy3.png")
    
#name = "wideJetStudy"
#canv.SaveAs(folder+"/bkgAndSig_"+name+".png")
#canv.SaveAs(folder+"/bkgAndSig_"+name+".root")

