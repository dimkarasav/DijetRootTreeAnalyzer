from ROOT import *

### FILES produced with makeMCjetpairing.py ###

files = [
    "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/signal_jets01_1000.root",
    "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/signal_jets01_200.root",
    "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/signal_jets01_300.root",
    "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/signal_jets01_400.root",
    "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/signal_jets01_500.root",
    "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/signal_jets01_600.root",
    "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/jetPairingMC/signal_jets01_800.root",
    "/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_8_0_30/src/DijetRootTreeAnalyzer/data_trig_eff_wo_runH_eta2.5.root"
]

for file_ in files:
    fileName = file_.split("/")[-1]
    fileout = TFile("matchingStudies2/%s"%fileName,"recreate")
    chain = TChain("rootTupleTree/tree")
    #chain.Add("tree_1.root")
    #chain.Add("tree_2.root")
    chain.Add(file_)

    chain.SetBranchStatus("*",0)
    chain.SetBranchStatus("HLT_CaloScoutingHT250",1)
    chain.SetBranchStatus("jet1_pt",1)
    chain.SetBranchStatus("jet1_eta",1)
    chain.SetBranchStatus("jet1_phi",1)
    chain.SetBranchStatus("jet1_mass",1)
    chain.SetBranchStatus("jet2_pt",1)
    chain.SetBranchStatus("jet2_eta",1)
    chain.SetBranchStatus("jet2_phi",1)
    chain.SetBranchStatus("jet2_mass",1)
    chain.SetBranchStatus("isr_pt",1)
    chain.SetBranchStatus("isr_eta",1)
    chain.SetBranchStatus("isr_phi",1)
    chain.SetBranchStatus("isr_mass",1)
    #chain.SetBranchStatus("jet1MC_pt",1)
    #chain.SetBranchStatus("jet1MC_eta",1)
    #chain.SetBranchStatus("jet1MC_phi",1)
    #chain.SetBranchStatus("jet1MC_mass",1)
    #chain.SetBranchStatus("jet2MC_pt",1)
    #chain.SetBranchStatus("jet2MC_eta",1)
    #chain.SetBranchStatus("jet2MC_phi",1)
    #chain.SetBranchStatus("jet2MC_mass",1)
    #chain.SetBranchStatus("isrMC_pt",1)
    #chain.SetBranchStatus("isrMC_eta",1)
    #chain.SetBranchStatus("isrMC_phi",1)
    #chain.SetBranchStatus("isrMC_mass",1)
    chain.SetBranchStatus("run",1)
    chain.SetBranchStatus("lumi",1)
    chain.SetBranchStatus("event",1)
    chain.SetBranchStatus("HLT_CaloScoutingHT250",1)
    chain.SetBranchStatus("dijet_mass",1)
    chain.SetBranchStatus("htAK4",1)

    fileout.cd()
    newTree = chain.CloneTree(0)
    for i,entry in enumerate(chain):
        if i%100000==0: print(i)
        if chain.isr_pt>50 and chain.HLT_CaloScoutingHT250:
            newTree.Fill()

    newTree.Write()
    fileout.Close()
    
