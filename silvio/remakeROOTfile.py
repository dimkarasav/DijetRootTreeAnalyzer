import ROOT

inputFileName = "/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/inputs/data_newL1_pt30.root"

outputFileName = inputFileName.replace(".root","_newFile.root")

inputFile = ROOT.TFile.Open(inputFileName)
outputFile = ROOT.TFile.Open(outputFileName,"recreate")

inputFile.Get("")
inputFile.cd("DijetFilter")
old = ROOT.gDirectory
old.ReadAll()

outputFile.cd()
old.GetList().Write()
outputFile.Write()

inputFile.Close()
outputFile.Close()


