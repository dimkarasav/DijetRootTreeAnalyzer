#!/bin/bash

#outputdir="plots_data4T_withSF_16_07_15/all/"
#list="list_for_plots_data4T_16_07_15.txt"
#lumi="21.239"
#outputdir="plots_data4T_withSF_19_07_15/all/"
#list="list_for_plots_data4T_19_07_15.txt"
#outputdir="plots_data4T_JEC_MC_plus5percent/"
#list="list_for_plots_data4T_JEC_MC_plus5percent.txt"

outputdir="$MYCMSSW/src/CMSDIJET/DijetRootTreeAnalyzer/test/santanas/plots/santanas__40pb-1_30_07_2015_v2/"
list="$MYCMSSW/src/CMSDIJET/DijetRootTreeAnalyzer/test/santanas/plots/santanas__40pb-1_30_07_2015/listForPlots_santanas__40pb-1_30_07_2015.txt"
lumi="40.2"

mkdir -p $outputdir

#python DrawFromTree_data.py --var mjj --xmin 1200 --xmax 2500 --xtitle "mjj [GeV]" --bins 1300  --rebin 20 --outputDir $outputdir --inputList $list --lumi $lumi --logy
#python DrawFromTree_data.py --var mjj --xmin 1200 --xmax 2500 --xtitle "mjj [GeV]" --bins 1300 --rebin 20 --outputDir $outputdir --inputList $list --lumi $lumi 
python DrawFromTree_data.py --var mjj --xmin 1 --xmax 14000 --xtitle "mjj [GeV]" --bins 13999 --rebin -1 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var mjj --xmin 1 --xmax 14000 --xtitle "mjj [GeV]" --bins 13999 --rebin -1 --outputDir $outputdir --inputList $list --lumi $lumi 
python DrawFromTree_data.py --var pTWJ_j1 --xmin 30 --xmax 5000 --xtitle "pT(j1) [GeV]" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var pTWJ_j2 --xmin 30 --xmax 5000 --xtitle "pT(j2) [GeV]" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var etaWJ_j1 --xmin -3 --xmax 3 --xtitle "#eta(j1)" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi
python DrawFromTree_data.py --var etaWJ_j2 --xmin -3 --xmax 3 --xtitle "#eta(j2)" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi
python DrawFromTree_data.py --var deltaETAjj --xmin 0 --xmax 2 --xtitle "#Delta#eta(jj)" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi
python DrawFromTree_data.py --var deltaPHIjj --xmin 0 --xmax 3.14 --xtitle "#Delta#phi(jj)" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi
python DrawFromTree_data.py --var deltaPHIjj --xmin 0 --xmax 3.14 --xtitle "#Delta#phi(jj)" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var MET  --xmin 0 --xmax 1000 --xtitle "MET [GeV]" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var metSig  --xmin 0 --xmax 1 --xtitle "MET / #Sigma E_{T}" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var nVtx --xmin 0 --xmax 50 --xtitle "nvtx" --bins 50 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var chargedHadEnFrac_j1 --xmin 0 --xmax 1 --xtitle "Charged hadron En. fraction j1" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var neutrHadEnFrac_j1 --xmin 0 --xmax 1 --xtitle "Neutral hadron En.fraction j1" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var photonEnFrac_j1  --xmin 0 --xmax 1 --xtitle "Photon En. fraction j1" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var eleEnFract_j1 --xmin 0 --xmax 1 --xtitle "Electron En. fraction j1" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy        
python DrawFromTree_data.py --var muEnFract_j1 --xmin 0 --xmax 1 --xtitle "Muon En. fraction j1" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var neutrElectromFrac_j1  --xmin 0 --xmax 1 --xtitle "neutr. EM En. fraction j1" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var  chargedElectromFrac_j1  --xmin 0 --xmax 1 --xtitle "ch. EM En. fraction j1" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var chargedMult_j1 --xmin 0 --xmax 50 --xtitle "charged mult. j1" --bins 50 --outputDir $outputdir --inputList $list --lumi $lumi --logy       
python DrawFromTree_data.py --var neutrMult_j1  --xmin 0 --xmax 50 --xtitle "neutral mult. j1" --bins 50 --outputDir $outputdir --inputList $list --lumi $lumi --logy        
python DrawFromTree_data.py --var photonMult_j1 --xmin 0 --xmax 50 --xtitle "photon mult. j1" --bins 50 --outputDir $outputdir --inputList $list --lumi $lumi --logy        
python DrawFromTree_data.py --var jetPtAK4matchCaloJet_j1  --xmin 30 --xmax 5000 --xtitle "pT(j1) calo match [GeV]" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var chargedHadEnFrac_j2 --xmin 0 --xmax 1 --xtitle "Charged hadron En. fraction j2" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var neutrHadEnFrac_j2 --xmin 0 --xmax 1 --xtitle "Neutral hadron En.fraction j2" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var photonEnFrac_j2  --xmin 0 --xmax 1 --xtitle "Photon En. fraction j2" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var eleEnFract_j2 --xmin 0 --xmax 1 --xtitle "Electron En. fraction j2" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy        
python DrawFromTree_data.py --var muEnFract_j2 --xmin 0 --xmax 1 --xtitle "Muon En. fraction j2" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var neutrElectromFrac_j2  --xmin 0 --xmax 1 --xtitle "neutr. EM En. fraction j2" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var  chargedElectromFrac_j2  --xmin 0 --xmax 1 --xtitle "ch. EM En. fraction j2" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var chargedMult_j2 --xmin 0 --xmax 50 --xtitle "charged mult. j2" --bins 50 --outputDir $outputdir --inputList $list --lumi $lumi --logy       
python DrawFromTree_data.py --var neutrMult_j2  --xmin 0 --xmax 50 --xtitle "neutral mult. j2" --bins 50 --outputDir $outputdir --inputList $list --lumi $lumi --logy        
python DrawFromTree_data.py --var photonMult_j2 --xmin 0 --xmax 50 --xtitle "photon mult. j2" --bins 50 --outputDir $outputdir --inputList $list --lumi $lumi --logy        
python DrawFromTree_data.py --var jetPtAK4matchCaloJet_j2  --xmin 30 --xmax 5000 --xtitle "pT(j2)calo match [GeV]" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var CosThetaStarWJ --xmin -1 --xmax 1  --xtitle "cos #theta *" --bins 200 --rebin 5 --outputDir $outputdir --inputList $list --lumi $lumi --logy
python DrawFromTree_data.py --var  Nak4 --xmin 0 --xmax 6  --xtitle "N jets" --bins 6  --outputDir $outputdir --inputList $list --lumi $lumi 
python DrawFromTree_data.py --var  phiWJ_j1  --xmin -3.1415 --xmax 3.1415  --xtitle "#phi (j1)" --bins 200 --rebin 5  --outputDir $outputdir --inputList $list --lumi $lumi 
python DrawFromTree_data.py --var  phiWJ_j2  --xmin -3.1415 --xmax 3.1415  --xtitle "#phi (j2)" --bins 200 --rebin 5  --outputDir $outputdir --inputList $list --lumi $lumi 
python DrawFromTree_data.py --var  massWJ_j1  --xmin 0 --xmax 200  --xtitle "#m (j1) [GeV]" --bins 200 --rebin 5  --outputDir $outputdir --inputList $list --lumi $lumi 
python DrawFromTree_data.py --var  massWJ_j2  --xmin 0 --xmax 200  --xtitle "#m (j2) [GeV]" --bins 200 --rebin 5  --outputDir $outputdir --inputList $list --lumi $lumi 
