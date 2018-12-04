import ROOT

fileNames = [
    "/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_8_0_30/src/DijetRootTreeAnalyzer/data_wj_studies/data_wj_studies_1.1data.root",
    "/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_8_0_30/src/DijetRootTreeAnalyzer/output_0.4mc_20180920_184122/rootfile_list_VectorDiJet1Jet_500_13TeV_SIGNALS_20180920_184122_3_reduced_skim.root"
]

selection = "isr_pt>50 && L1_HTT240 && HLT_CaloScoutingHT250"
variable = "dijet_mass"
binning = "(100,0,1000)"

for fileName in fileNames:
    chain = ROOT.TChain("rootTupleTree/tree")
    chain.Add(fileName)
    chain.Draw(variable + ">> histo"+binning,selection)
    histo = ROOT.gROOT.Get("histo").Clone(filename.replace("/",""))

