import os

os.system("rm ../wideJetMC/*")
os.system("mkdir -p ../wideJetMC")

wjs = range(4,19,1)

masses = [
    200, 300, 400, 500, 600, 800
]

for wj in wjs:
    wj = round(wj/10.,1)
    for mass in masses:
        command = "hadd ../wideJetMC/signal_%s_wj%s.root /mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_8_0_30/src/DijetRootTreeAnalyzer/output_%smc*/rootfile_list_VectorDiJet1Jet_%s_*_reduced_skim.root "%(mass,wj,wj,mass)
        print(command)
        pipe = os.system(command)
        
