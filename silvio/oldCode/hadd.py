import os

inputFolder = "../output_20180207_113450" #output_20180206_111218
#inputFolder = "../Scouting_small_ntuples_20171221_130129"
outputFolder = ".."

signals = [
    "VectorDiJet1Jet_25_13TeV",
    "VectorDiJet1Jet_50_13TeV",
    "VectorDiJet1Jet_75_13TeV",
    "VectorDiJet1Jet_100_13TeV",
    "VectorDiJet1Jet_125_13TeV",
    "VectorDiJet1Jet_150_13TeV",
    "VectorDiJet1Jet_200_13TeV",
    "VectorDiJet1Jet_300_13TeV",
    "VectorDiJet1Jet_400_13TeV",
    "VectorDiJet1Jet_500_13TeV",
    "VectorDiJet1Jet_600_13TeV",
    "VectorDiJet1Jet_800_13TeV",
    "VectorDiJet1Jet_1000_13TeV",
]

signals = [
#    "L1HTTSkim",
    "CaloJet40Skim",
]

#signals = [
    #"Hbb",
    #"QCDHT1000",
    #"QCDHT100",
    #"QCDHT1500",
    #"QCDHT2000",
    #"QCDHT200",
    #"QCDHT300",
    #"QCDHT500",
    #"QCDHT50",
    #"QCDHT700",
    #"TT",
    #"WJetsHT180",
    #"WJetsHT600",
    #"ZJetsHT180",
    #"ZJetsHT600",
#]
for signal in signals:
    inputFile = "%s/rootfile_*%s*_reduced_skim.root"%(inputFolder, signal)
    outputFile = "%s/%s.root"%(outputFolder, signal)
    command = "hadd -f %s %s"%(outputFile,inputFile)
    print()
    print(command)
    os.system(command)
