import ROOT

ROOT.gROOT.SetBatch()
canv = ROOT.TCanvas()
canv.SetGridx()
canv.SetGridy()
canv.SetLogz()


ROOT.gROOT.LoadMacro("/mnt/t3nfs01/data01/shome/sdonato/functions.C+")



ROOT.gStyle.SetOptStat(0)
#fileName = "/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ScoutingCaloCommissioning_2017-01-18/CommissioningG/rootfile_CaloScoutingCommissioning2016G_JEC_CaloHLT_plus_V10p2_20170119_001201_reduced_skim.root"
#fileName = "rootFile_reduced_skim.root"
fileName = "/mnt/t3nfs01/data01/shome/sdonato/scouting/CMSSW_8_0_30/src/CMSDIJET/DijetRootTreeAnalyzer/output_20171215_154436.root"

file_ = ROOT.TFile(fileName)

tree = file_.Get("rootTupleTree/tree")

#preselect = "passHLT_L1HTT_CaloScouting_PFScouting && isr_pt>50 && abs(TVector2::Phi_mpi_pi(isr_phi - phijj))>2.5"
#preselect = "passHLT_L1HTT_CaloScouting_PFScouting && Nak4==3 && mjj<80 " #&& isr_pt<80
#preselect = "passHLT_CaloJet40_CaloScouting_PFScouting && Nak4==3  &&  isr_pt>180" #&& isr_pt<80
preselect = "passHLT_CaloJet40_CaloScouting_PFScouting && Nak4==3  " #&& isr_pt<80
title = "ISR pt vs pT(jj)"

#varX = "pTWJ_j1+pTWJ_j2+isr_pt"
#varX_nbins,   varX_min,  varX_max = 20,0,300
#varX_title = "p^{T}_{1}+p^{T}_{2}+p^{T}_{3}"

varX = "mass(pT_j1,eta_j1,phi_j1,mass_j1,pT_j2,eta_j2,phi_j2,mass_j2)"
#varX = "mjj"
varX_nbins,   varX_min,  varX_max = 50,0,400
varX_title = "M_{1,2}"

#varX = "2*max(max(pTWJ_j1,pTWJ_j2),isr_pt)"
#varX_nbins,   varX_min,  varX_max = 200,0,1000
#varX_title = "m_{jj}"


#varY = "mass(pT_j1,eta_j1,phi_j1,mass_j1,isr_pt,isr_eta,isr_phi,isr_pt*0.2)"
varY = "mass(pT_j1,eta_j1,phi_j1,mass_j1,isr_pt,isr_eta,isr_phi,isr_pt*0.2)"
#varY = "ptjj"
varY_nbins,   varY_min,  varY_max = 50,0,300
varY_title = "M_{1,ISR}"

preselect += "&& (%s < %d)"%(varX,varX_max)
preselect += "&& (%s < %d)"%(varY,varY_max)

tree.Draw("%s:%s >> Dalitz(%d,%d,%d,%d,%d,%d)"%(varY,varX,varX_nbins,varX_min,varX_max,varY_nbins, varY_min, varY_max),"%s"%(preselect) ,"COLZ")
den = ROOT.gDirectory.Get("Dalitz")
den.SetTitle(title)

for histo in [den]:
    histo.GetXaxis().SetTitle(varX_title)
    histo.GetYaxis().SetTitle(varY_title)
    histo.Draw("COLZ")
    canv.SaveAs(histo.GetName()+".png")
    canv.SaveAs(histo.GetName()+".root")
    canv.SaveAs(histo.GetName()+".C")



##tree->Draw("sqrt(TVector2::Phi_mpi_pi(jetPhiOffline[0]-cjetPhi[0])**2 + (jetEtaOffline[0]-cjetEta[0])**2)","","")

#preselect = "passHLT_L1HTT_CaloScouting_PFScouting"
title = "Three jet mass"

#varX = "abs(TVector2::Phi_mpi_pi(isr_phi - phijj))"
#varX_nbins,   varX_min,  varX_max = 32,0,3.2
#varX_title = "#Delta#Phi(jj,ISR)"

#varX = "mass(pT_j1,eta_j1,phi_j1,mass_j1,pT_j2,eta_j2,phi_j2,mass_j2,isr_pt,isr_eta,isr_phi,isr_pt*0.2)"
#varX = "htAK4" #htAK4 #mjj
varX = "mass(pT_j1,eta_j1,phi_j1,mass_j1,isr_pt,isr_eta,isr_phi,isr_pt*0.2)"
varX_nbins,   varX_min,  varX_max = 100,0,500
varX_title = "#Delta#Phi(jj,ISR)"

tree.Draw("%s >> MassJJJ(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"")

plot = ROOT.gDirectory.Get("MassJJJ")
plot.SetTitle(title)

for histo in [plot]:
    histo.GetXaxis().SetTitle(varX_title)
    histo.Draw("")
    canv.SaveAs(histo.GetName()+".png")
    canv.SaveAs(histo.GetName()+".root")
    canv.SaveAs(histo.GetName()+".C")

