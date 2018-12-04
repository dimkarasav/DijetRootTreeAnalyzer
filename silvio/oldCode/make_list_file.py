import os

#server = "eoscms.cern.ch"
server = "storage01.lcg.cscs.ch"

outputFolder = "list_files_ScoutingCaloHT"
os.system("mkdir -p %s"%outputFolder)
fileToWrite={
#"list_ScoutingCaloCommissioning_Run2016B-v1.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloCommissioning_Run2016B-v1_Jun-10-2016_20160610_230518",
#"list_ScoutingCaloCommissioning_Run2016B-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloCommissioning_Run2016B-v2_Jun-24-2016_20160625_074015",
#"list_ScoutingCaloCommissioning_Run2016C-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloCommissioning_Run2016C-v2_Jul-08-2016_20160708_073241",
#"list_ScoutingCaloCommissioning_Run2016D-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloCommissioning_Run2016D-v2_Jul-19-2016_20160720_030239",
#"list_ScoutingCaloCommissioning_Run2016E-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloCommissioning_Run2016E-v2_Nov-17-2016_20161117_180016",
#"list_ScoutingCaloCommissioning_Run2016F-v1.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloCommissioning_Run2016F-v1_Nov-17-2016_20161117_180601",
#"list_ScoutingCaloCommissioning_Run2016G-v1.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloCommissioning_Run2016G-v1_Nov-17-2016_20161117_180846",
#"list_ScoutingCaloCommissioning_Run2016H-v1.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloCommissioning_Run2016H-v1_Nov-17-2016_20161117_181530",
#"list_RSGravitonToQuarkQuark_kMpl01_M_500.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/MC/signal/Spring15_25ns_JEC_Summer15_25nsV7/RSGravitonToQuarkQuark_kMpl01_M_500_TuneCUETP8M1_13TeV_pythia8",

#"list_VectorDiJet1Jet_25_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_25_13TeV-madgraph",
#"list_VectorDiJet1Jet_50_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_50_13TeV-madgraph",
#"list_VectorDiJet1Jet_75_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_75_13TeV-madgraph",
#"list_VectorDiJet1Jet_100_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_100_13TeV-madgraph",
#"list_VectorDiJet1Jet_125_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_125_13TeV-madgraph",
#"list_VectorDiJet1Jet_150_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_150_13TeV-madgraph",
#"list_VectorDiJet1Jet_200_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_200_13TeV-madgraph",
#"list_VectorDiJet1Jet_300_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_300_13TeV-madgraph",
#"list_VectorDiJet1Jet_400_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_400_13TeV-madgraph",
#"list_VectorDiJet1Jet_500_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_500_13TeV-madgraph",
#"list_VectorDiJet1Jet_600_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_600_13TeV-madgraph",
#"list_VectorDiJet1Jet_800_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_800_13TeV-madgraph",
#"list_VectorDiJet1Jet_1000_13TeV.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/VectorDiJet1Jet_1000_13TeV-madgraph",

"list_TT.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8",
"list_Hbb.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/GluGluHToBB_M125_13TeV_powheg_pythia8",
"list_ZJetsHT600.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/ZJetsToQQ_HT600toInf_13TeV-madgraph",
"list_ZJetsHT180.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8",
"list_WJetsHT180.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8",
"list_WJetsHT600.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT700.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT200.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT1000.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT100.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT50.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT300.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT2000.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT1500.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"list_QCDHT500.txt":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",


#"list_ScoutingCaloHT_Run2016B-v1.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloHT_Run2016B-v1_Jun-10-2016_20160610_230443",
#"list_ScoutingCaloHT_Run2016B-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloHT_Run2016B-v2_Jun-10-2016_20160610_230330",
#"list_ScoutingCaloHT_Run2016C-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloHT_Run2016C-v2_Jul-08-2016_20160708_073410",
#"list_ScoutingCaloHT_Run2016D-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloHT_Run2016D-v2_Jul-19-2016_20160720_025923",
#"list_ScoutingCaloHT_Run2016E-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloHT_Run2016E-v2_Nov-17-2016_20161118_165322",
#"list_ScoutingCaloHT_Run2016F-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloHT_Run2016F-v1_Nov-17-2016_20161117_174638",
#"list_ScoutingCaloHT_Run2016G-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloHT_Run2016G-v1_Nov-17-2016_20161117_175009",
#"list_ScoutingCaloHT_Run2016H-v2.txt":"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_big/2016/ScoutingCaloHT_Run2016H-v1_Nov-17-2016_20161117_175444",

}



def findFileRecursive(server,folder,files):
    command = "xrdfs %s ls -l -u  %s"%(server,folder)
    #print(command)
    output = os.popen(command).read()
    lines = output.split("\n")
    for line in lines:
        tmp = ''
        while(tmp!=line):
            tmp = line
            line = line.replace("  "," ")
        words = line.split(" ")
        if(len(words)>0 and len(words[0])>0):
            #print words
            try:
                fullPath = words[4]
            except:
                print(words)
                fullPath = words[3]
            #print(fullPath)
            server =fullPath.split(folder)[0]
            path = folder+fullPath.split(folder)[1]
            if(words[0][0]=='d'):
                findFileRecursive(server, path,files)
            elif(".root" in path):
                files.append(path)
            elif(".tar.gz" in path):
                pass
            elif(".tmp" in path):
                pass
            else:
                print("WARNING: ", path)
                


for fileName in fileToWrite:
    txtFile = open(outputFolder+"/"+fileName,'w')
    files = []
    folder = fileToWrite[fileName]
    print("first command: xrdfs %s ls -l -u %s"%(server,folder))
    findFileRecursive(server,folder,files)
    for file_ in files:
        txtFile.write("root://"+server+"//"+file_+"\n")
    txtFile.close()

#command = "xrdfs %s ls -l -u %s"%(server,folder)
#print(command)
#output = os.popen(command).read()
#lines = output.split("\n")
#for line in lines:
    #tmp = ''
    #while(tmp!=line):
        #tmp = line
        #line = line.replace("  "," ")
    #words = line.split(" ")
    #if(len(words)>0 and len(words[0])>0 and words[0][0]=='d'):
        ##print words
        #fullPath = words[4]
        ##print(fullPath)
        #server =fullPath.split(folder)[0]
        #path = folder+fullPath.split(folder)[1]
        #print(server, path)
