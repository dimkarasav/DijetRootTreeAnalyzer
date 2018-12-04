import ROOT

dR = 1.1
def doWideJets(jets_):
  jets = jets_[:]
  changed = True
  while changed:
      changed = False
      njets = len(jets)
      i = 0
      while i<njets and not changed:
        j = i+1 
        while j<njets and not changed:
            if jets[i].DeltaR(jets[j])<dR:
                changed = True
                jets[i] = jets[i]+jets[j]
                del jets[j]
            j+=1
        i+=1
        
  return jets

ROOT.gROOT.SetBatch()
canv = ROOT.TCanvas()
canv.SetGridx()
canv.SetGridy()
canv.SetLogz()

ROOT.gStyle.SetOptStat(0)
#fileName = "/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ScoutingCaloCommissioning_2017-01-18/CommissioningG/rootfile_CaloScoutingCommissioning2016G_JEC_CaloHLT_plus_V10p2_20170119_001201_reduced_skim.root"
#fileName = "rootFile_reduced_skim.root"
fileName = "root://storage01.lcg.cscs.ch///pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_300_13TeV-madgraph/VectorDiJet1Jet_300_13TeV-madgraph_V2/171216_121056/0000/dijetscouting_bigtree_1.root"

file_ = ROOT.TFile.Open(fileName)

tree = file_.Get("dijetscouting/events")

histo = ROOT.TH1F("histo","wide",100,0,600)

count = 0 
for ev in tree:
    if count>10000:
        break
    if count%100 == 0:
        print(count)
    genJets = []
    for (pt,eta,phi,mass) in zip(ev.jetPtGenAK4,ev.jetEtaGenAK4,ev.jetPhiGenAK4,ev.jetMassGenAK4):
        if(pt>20):
            genJet = ROOT.TLorentzVector()
            genJet.SetPtEtaPhiM(pt,eta,phi,mass)
            genJets.append(genJet)
    widegenJets = doWideJets(genJets)
    if len(widegenJets)>=2:
        histo.Fill((widegenJets[0]+widegenJets[1]).M())
    count +=1

histo.Draw()

#if True:
    #genParticles = []
    #for (pt,eta,phi,energy) in zip(ev.gen_pt,ev.gen_eta,ev.gen_phi,ev.gen_energy):
        #genParticle = ROOT.TLorentzVector()
        #genParticle.SetPtEtaPhiE(pt,eta,phi,energy)
        #genParticles.append(genParticle)
