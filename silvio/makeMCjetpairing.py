import os

#os.system("rm ../jetPairing2MC/*")
os.system("mkdir -p ../jetPairing2MC")

masses = [
    200, 300, 400, 500, 600, 800, 1000
]

#for matching in ["jets01","jets02","jets12"]:
#for matching in ["dijetp"]:
for matching in ["jets01"]:
    for mass in masses:
#        command = "hadd -f ../jetPairing2MC/signal_%s_%s.root /mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_8_0_30/src/DijetRootTreeAnalyzer/output_%s_*_mc_*/rootfile_list_VectorDiJet1Jet_%s_*_reduced_skim.root"%(matching,mass,matching,mass)
        command = "hadd -f ../jetPairing2MC/signal_%s_%s.root /mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/silvio/output_%s_mc_*/rootfile_list_VectorDiJet1Jet_%s_*_reduced_skim.root"%(matching,mass,matching,mass)
        print(command)
        pipe = os.system(command)
#    command = "hadd -f ../jetPairing2MC/data_%s.root /mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_8_0_30/src/DijetRootTreeAnalyzer/output_%s_*_data_*/rootfile_*reduced_skim.root"%(matching,matching)
#    print(command)
#    pipe = os.system(command)


for mass in masses:
    command = "hadd -f ../jetPairing2MC/signal_comb_%s.root ../jetPairing2MC/signal_jet*_%s.root"%(mass,mass)
    print(command)
    pipe = os.system(command)

command = "hadd -f ../jetPairing2MC/data_comb.root ../jetPairing2MC/data_jet*.root"
print(command)

