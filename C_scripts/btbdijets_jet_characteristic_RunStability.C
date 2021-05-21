#include <TFile.h>
#include <TDirectoryFile.h>
#include<cmath>
#include "TF1.h"
#include "TH1D.h"
#include "TH1F.h"
#include "TH2D.h"
#include "TH2F.h"
#include "TTree.h"
#include "TPaveText.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "TCanvas.h"
#include "TMath.h"
#include "TStyle.h"
#include "TChain.h"
#include <iostream>
#include <fstream>
#include "TSystem.h"
#include "TROOT.h"
#include "TMath.h"
#include "TGraph.h"
#include "TLatex.h"
#include "setTDRStyle_teliko.C"
#include <algorithm>
#include <string>
#include "TSystemDirectory.h"
#define eta_bins 8
#define runs_number 3

int getBin(double x, double boundaries[]) ;
bool FindJetIDFromEra ( int flag_era, double JetID_16, double JetID_17, double JetID_18 ) ;

// 2017 data directory: root://eoscms///eos/cms/store/group/phys_jetmet/eirini/data2017/rereco/
void btbdijets_jet_characteristic_RunStability()
 {



	char input_trees[runs_number][500] ={
/*
"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/dimitris/Puppi_ak8_reduced_trees/RunA/small_tree_RunA.root",  
"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/dimitris/Puppi_ak8_reduced_trees/RunB/small_tree_RunB.root", 
"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/dimitris/Puppi_ak8_reduced_trees/RunC/small_tree_RunC.root",
"/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/dimitris/Puppi_ak8_reduced_trees/RunD/small_tree_RunD.root"
*/

//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunBver2/JetHT__Run2016B-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunBver2/JetHT__Run2016B-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunC/JetHT__Run2016C-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunD/JetHT__Run2016D-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunE/JetHT__Run2016E-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunF/JetHT__Run2016F-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root"

//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunF/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunG/JetHT__Run2016G-21Feb2020_UL2016_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunH/JetHT__Run2016H-21Feb2020_UL2016_MINIAOD_reduced_skim.root"


//==========================================================UL16 ak4Puppi================================================

//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPI/APV/JetHT__Run2016Bver1-21Feb2020_UL2016_MINIAOD_reduced_skim.root",

//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016Bver2-21Feb2020_UL2016_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016C-21Feb2020_UL2016_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016D-21Feb2020_UL2016_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016E-21Feb2020_UL2016_MINIAOD_reduced_skim.root",
//	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root"

	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root",
	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016G-21Feb2020_UL2016_MINIAOD_reduced_skim.root",
	"/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016H-21Feb2020_UL2016_MINIAOD_reduced_skim.root"

 };


	char legend_array[runs_number][500] = { "RunF" , "RunG", "RunH" };

	char analyzer_path[300] = "/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/"; 

	char output_directory[300] = "UL_datasets_JetID/UL_2016/PUPPI/v15/nonAPV/First_try/Run_Comparisons/";     
//	char *output_directory = "2018_Puppi_studies/Horn_study/";     
	char image_name[300] = "_superimposed_runsFGH"; 


	int era = 2016;
	int scale_on = 1 ;	
	bool Save_pngs = true ;
	bool useJetIDs = false ;
	bool test_run = false; //if 'true' the script will loop only over the first 1000 entries. Option for tests.
	double pTmaxCut = 350000;
	double pTminCut = 60;

	TFile *fout;

//	gROOT->SetBatch(kTRUE);
	gROOT->LoadMacro("setTDRStyle_teliko.C");
	setTDRStyle_teliko();
	gStyle->SetOptStat(0);
	TPaveText *paveCMS = new TPaveText(0.15,0.95,0.5,1.0,"NDC");
	//paveCMS->AddText("CMS Preliminary L=9.2 fb^{-1} #sqrt{s} = 13 TeV");
	paveCMS->AddText("CMS Preliminary  #sqrt{s} = 13 TeV");
	paveCMS->SetFillColor(0);
	paveCMS->SetBorderSize(0);
	paveCMS->SetTextSize(0.03);

	  //float lumi = 2500.0;
	char name[100]; 
	float etamin=0, etamax=0;
	char filename[500]; 
	int treeEntries[runs_number];
	int maxEntries=0;

	TH1D *h_METovSUMET[eta_bins][runs_number], *h_CHFJet1[eta_bins][runs_number], *h_NHFJet1[eta_bins][runs_number], *h_CEMFJet1[eta_bins][runs_number], *h_NEMFJet1[eta_bins][runs_number], *h_MUFJet1[eta_bins][runs_number], *h_CMJet1[eta_bins][runs_number], *h_NMJet1[eta_bins][runs_number], *h_ptJet1[eta_bins][runs_number], *h_PMJet1[eta_bins][runs_number], *h_DijetMassAK4[eta_bins][runs_number], *h_ETAJet1[runs_number], *h_PHIJet1[eta_bins][runs_number];


	for (int runNo=0; runNo<runs_number; runNo++)
	{
 
	sprintf(name,"h_ETAJet1_Run%i",runNo);
	h_ETAJet1[runNo] = new TH1D(name, "", 80,-5,5);

	
		for(Int_t h=0; h<eta_bins;h++)
		{ 
		//========== no JetID ===========
			sprintf(name,"h_METovSUMET_%s_bin%i",legend_array[runNo],h);
			h_METovSUMET[h][runNo] = new TH1D(name, "", 40,0,0.5);
			//h_METovSUMET[h]->Sumw2(); 
			sprintf(name,"h_CHFJet1_%s_bin%i",legend_array[runNo],h);
			h_CHFJet1[h][runNo] = new TH1D(name, "", 40,0,1.2);
			//h_CHFJet1[h]->Sumw2(); 
			sprintf(name,"h_NHFJet1_%s_bin%i",legend_array[runNo],h);
			h_NHFJet1[h][runNo] = new TH1D(name, "", 40,0,1.2);
			//h_NHFJet1[h]->Sumw2(); 
			sprintf(name,"h_CEMFJet1_%s_bin%i",legend_array[runNo],h);
			h_CEMFJet1[h][runNo] = new TH1D(name, "", 40,0,1.2);
			//h_CEMFJet1[h]->Sumw2(); 
			sprintf(name,"h_NEMFJet1_%s_bin%i",legend_array[runNo],h);
			h_NEMFJet1[h][runNo] = new TH1D(name, "", 40,0,1.2);
			//h_NEMFJet1[h]->Sumw2(); 
			sprintf(name,"h_MUFJet1_%s_bin%i",legend_array[runNo],h);
			h_MUFJet1[h][runNo] = new TH1D(name, "", 40,0,1.2);
			//h_MUFJet1[h]->Sumw2(); 

			sprintf(name,"h_CMJet1_%s_bin%i",legend_array[runNo],h);
			h_CMJet1[h][runNo] = new TH1D(name, "", 100,0,100);
		
			sprintf(name,"h_PHIJet1_%s_bin%i",legend_array[runNo],h);
			if (h==5) h_PHIJet1[h][runNo] = new TH1D(name, "", 20,-4,4);		
			else h_PHIJet1[h][runNo] = new TH1D(name, "", 40,-4,4);
			sprintf(name,"h_DijetMassAK4_%s_bin%i",legend_array[runNo],h);
			h_DijetMassAK4[h][runNo] = new TH1D(name,"",100,0,7500);
			// h_CMJet1[h]->Sumw2(); 
			sprintf(name,"h_NMJet1_%s_bin%i",legend_array[runNo],h);
			h_NMJet1[h][runNo] = new TH1D(name, "", 100,0,100);
			//h_NMJet1[h]->Sumw2(); 
			sprintf(name,"h_PMJet1_%s_bin%i",legend_array[runNo],h);
			h_PMJet1[h][runNo] = new TH1D(name, "", 100,0,100);
			sprintf(name,"h_ptJet1_%s_bin%i",legend_array[runNo],h);
			h_ptJet1[h][runNo] = new TH1D(name, "", 300,0,3000);
			//h_ptJet1[h]->Sumw2(); 
			   
		} //end of loop per eta bin
	
	}//end of loop over runs

	TH2D *h_eta_phi_map = new TH2D("h_eta_phi_map", "eta-phi map", 30 , -5, 5, 12 , -3.1416,3.1416);
	TH2D *h_eta_phi_map_2ndRun = new TH2D("h_eta_phi_map_2ndRun", "eta-phi map", 30 , -5, 5, 12 , -3.1416,3.1416);
	TH2D *h_eta_phi_map_3rdRun = new TH2D("h_eta_phi_map_3rdRun", "eta-phi map", 30 , -5, 5, 12 , -3.1416,3.1416);
	TH2D *h_eta_phi_map_4thRun = new TH2D("h_eta_phi_map_4thRun", "eta-phi map", 30 , -5, 5, 12 , -3.1416,3.1416);

   double passHLT4, passHLT3, passHLT2, passHLT1, passHLT, PassJSON, run, event, lumi;  
   double chf, nhf, cemf, nemf, muf, cm, nm, pm,eta_j1, eta_j2, pT_j1,met_ov_sumet,elf,phf,DijetMassAK4 ,phi_j1,phi_j2,pT_j2,nVtx;
	double JetID_2016_j1, JetID_2017_j1, JetID_2018_j1, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2;
	bool JetID_j1, JetID_j2;
  // double ymax; 
//   double yBnd[eta_bins+1]={0.0,0.5,1.0,1.5,2.0,2.7, 3.0,5.0};
//   double yBnd[eta_bins+1]={0.0,0.5,1.0,1.5,2.0,2.6, 2.7, 3.0,5.0};
   double yBnd[eta_bins+1]={0.0,0.5,1.0,1.5,2.0,2.4, 2.7, 3.0,5.0};
 //  double yBnd[eta_bins+1]={2.5,3.2};



	bool flag_for_max_entries = true;
	TChain *tree[runs_number];



	for (int runNo=0; runNo<runs_number; runNo++)
	{

	tree[runNo] = new TChain("tree");

	tree[runNo]->Add(input_trees[runNo]);

	tree[runNo]->SetBranchAddress("run",&run);
	tree[runNo]->SetBranchAddress("event",&event);
	tree[runNo]->SetBranchAddress("lumi",&lumi);
	tree[runNo]->SetBranchAddress("metSig",&met_ov_sumet);
	tree[runNo]->SetBranchAddress("chargedHadEnFrac_j1",&chf);
	tree[runNo]->SetBranchAddress("neutrHadEnFrac_j1",&nhf);
	tree[runNo]->SetBranchAddress("chargedElectromFrac_j1",&cemf);
	tree[runNo]->SetBranchAddress("neutrElectromFrac_j1",&nemf);
	tree[runNo]->SetBranchAddress("muEnFract_j1",&muf);
	tree[runNo]->SetBranchAddress("chargedMult_j1",&cm);
	tree[runNo]->SetBranchAddress("neutrMult_j1",&nm);
	tree[runNo]->SetBranchAddress("photonMult_j1",&pm);
	tree[runNo]->SetBranchAddress("eta_j1",&eta_j1);
	tree[runNo]->SetBranchAddress("eta_j2",&eta_j2);
	tree[runNo]->SetBranchAddress("pT_j1",&pT_j1);
	tree[runNo]->SetBranchAddress("eleEnFract_j1",&elf);
	tree[runNo]->SetBranchAddress("photonEnFrac_j1",&phf);
	tree[runNo]->SetBranchAddress("phi_j1",&phi_j1);
	tree[runNo]->SetBranchAddress("pT_j2",&pT_j2);
	tree[runNo]->SetBranchAddress("nVtx",&nVtx);
	tree[runNo]->SetBranchAddress("passHLT",&passHLT);  //for ak8:    AK8PFHT800 TrimMass50_v12
	tree[runNo]->SetBranchAddress("passHLT1",&passHLT1);  //for ak8:  AK8PFHT850 TrimMass50_v11
	tree[runNo]->SetBranchAddress("passHLT2",&passHLT2);  //for ak8:  AK8PFHT900_TrimMass50_v11
	tree[runNo]->SetBranchAddress("passHLT3",&passHLT3); //for ak8:   AK8PFJet200_v15
	tree[runNo]->SetBranchAddress("passHLT4",&passHLT4); //for ak8:   AK8PFJet400_v16	
	tree[runNo]->SetBranchAddress("JetIDlepVeto_2016_j1",&JetID_2016_j1);
	tree[runNo]->SetBranchAddress("JetIDlepVeto_2017_j1",&JetID_2017_j1);
	tree[runNo]->SetBranchAddress("JetIDlepVeto_2018_j1",&JetID_2018_j1);
	tree[runNo]->SetBranchAddress("JetIDlepVeto_2016_j2",&JetID_2016_j2);
	tree[runNo]->SetBranchAddress("JetIDlepVeto_2017_j2",&JetID_2017_j2);
	tree[runNo]->SetBranchAddress("JetIDlepVeto_2018_j2",&JetID_2018_j2);

	treeEntries[runNo] = tree[runNo]->GetEntries();

////////////////find the tree with the maximum entries to loop over them.

	if (flag_for_max_entries)  // get the entry of the first tree
	{
		maxEntries = treeEntries[runNo];
		flag_for_max_entries = false;
	}

    if ( treeEntries[runNo] > maxEntries ) maxEntries = treeEntries[runNo];


	cout<<"\nNumber of entries for tree "<< input_trees[runNo] << "\n  =  " << treeEntries[runNo] <<endl;
	} 

	cout << " Max entries = " << maxEntries << endl;




	   	int LoopEntries =0;
		
		if(test_run) LoopEntries = 1000;
		else LoopEntries = maxEntries;

	for (int i=0; i<LoopEntries; i++) //event loop	
	{
		if(i%5000000==0) cout<<i<<endl;
			
		for (int runNo=0; runNo<runs_number; runNo++)
		{
			if ( i >=  treeEntries[runNo] ) continue; 

			tree[runNo]->GetEntry(i);


			if (pT_j1 < 0.1 ) continue;
			if ( pT_j1 < pTminCut || pT_j1 > pTmaxCut  ) continue;
		//	if(run>320065)continue; //get run C events

			int ybin = getBin(fabs(eta_j1),yBnd);
 	
			JetID_j1 = FindJetIDFromEra(era, JetID_2016_j1, JetID_2017_j1, JetID_2018_j1);
			JetID_j2 = FindJetIDFromEra(era, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2);


//			if (cm>0) continue;
			if (  ( !useJetIDs || ( JetID_j1 && JetID_j2 ) ) && passHLT3==1 ) h_ETAJet1[runNo]->Fill(eta_j1);


				//=== eta regions ====
			if (ybin > -1 && passHLT3==1 && ( !useJetIDs || ( JetID_j1 && JetID_j2 ) ) )   //fill hist's in the corresponding eta bin
			{ 
				h_CHFJet1[ybin][runNo]->Fill(chf); 
				h_NHFJet1[ybin][runNo]->Fill(nhf);
				h_CEMFJet1[ybin][runNo]->Fill(cemf);
				h_NEMFJet1[ybin][runNo]->Fill(nemf);
				h_MUFJet1[ybin][runNo]->Fill(muf);
				h_PHIJet1[ybin][runNo]->Fill(phi_j1);
				h_CMJet1[ybin][runNo]->Fill(cm);
				h_NMJet1[ybin][runNo]->Fill(nm);
				h_PMJet1[ybin][runNo]->Fill(pm);
				h_ptJet1[ybin][runNo]->Fill(pT_j1);
				h_METovSUMET[ybin][runNo]->Fill(met_ov_sumet);
			}// end of if ybin>-1

		}
	}// end of event loop








	TCanvas *pad1 = new TCanvas("pad1", "Charged Hadron Fraction of Jet1",1);
	if(eta_bins > 1) pad1->Divide(3,3);
	TCanvas *pad2 = new TCanvas("pad2", "Neutral Hadron Fraction of Jet1",1);
	if(eta_bins > 1) pad2->Divide(3,3);
	TCanvas *pad3 = new TCanvas("pad3", "Charged EM Fraction of Jet1",1);
	if(eta_bins > 1) pad3->Divide(3,3);
	TCanvas *pad4 = new TCanvas("pad4", "Neutral EM Fraction of Jet1",1);
	if(eta_bins > 1) pad4->Divide(3,3);
	TCanvas *pad5 = new TCanvas("pad5", "Muon Energy Fraction of Jet1",1);
	if(eta_bins > 1) pad5->Divide(3,3);
	TCanvas *pad9 = new TCanvas("pad9", "pT of Jet1",1);
	if(eta_bins > 1) pad9->Divide(3,3);
	TCanvas *pad10= new TCanvas("pad10", "MET / SumET ",1);
	if(eta_bins > 1) pad10->Divide(3,3);
	TCanvas *pad11= new TCanvas("pad11", "Neutral Multiplicity of Jet1",1);
	if(eta_bins > 1) pad11 ->Divide(3,3);
	TCanvas *pad12= new TCanvas("pad12", "Charged Multiplicity of Jet1",1);
	if(eta_bins > 1) pad12 ->Divide(3,3);
	TCanvas *pad13= new TCanvas("pad13", "Photon Multiplicity of Jet1",1);
	if(eta_bins > 1) pad13 ->Divide(3,3);
	TCanvas *pad16= new TCanvas("pad16", "Phi of Jet1",1);
	if(eta_bins > 1) pad16 ->Divide(3,3);
	TCanvas *pad18= new TCanvas("pad18", "",1);
	if(eta_bins > 1) pad18 ->Divide(3,3);



	TCanvas *pad17= new TCanvas("pad17", "eta",1);
//	pad17 ->Divide(3,3); 

//	TCanvas *eta_phi_canvas = new TCanvas("eta_phi_canvas", "",600,600);
//	TCanvas *eta_phi_canvas_2ndRun = new TCanvas("eta_phi_canvas_2ndRun", "",600,600);

	TLegend *leg1 =new TLegend(0.4,0.4,0.7,0.9); //7899  //4899
	leg1->SetTextSize(0.1);
	leg1->SetFillColor(0); 
	leg1->SetBorderSize(0);  


	TLegend *leg2 =new TLegend(0.4,0.2,0.7,0.4); //7899  //4899
	leg2->SetTextSize(0.035);
	leg2->SetFillColor(0); 
	leg2->SetBorderSize(0);  

	for (int runNo=0; runNo<runs_number; runNo++)
	{

		pad17->cd()->SetLogy(1);
		h_ETAJet1[runNo]->GetXaxis()->SetTitle("#eta") ;
		h_ETAJet1[runNo]->GetYaxis()->SetTitle("Entries");
		h_ETAJet1[runNo]->GetYaxis()->SetTitleOffset(1.3);
		h_ETAJet1[runNo]->SetLineWidth(2);
		h_ETAJet1[runNo]->SetMarkerSize(0.04);
		h_ETAJet1[runNo]->SetLineColor(1+runNo);


		if(scale_on == 1) h_ETAJet1[runNo]->Scale(h_ETAJet1[0]->Integral() / h_ETAJet1[runNo]->Integral());
		if ( runNo==0 ) 
		{
			h_ETAJet1[runNo]->Draw("hist");
			paveCMS ->Draw("same");
		}
		else h_ETAJet1[runNo]->Draw("same");


		
		leg1->AddEntry(h_ETAJet1[runNo], legend_array[runNo],  "L");
		leg2->AddEntry(h_ETAJet1[runNo], legend_array[runNo],  "L");
		if ( runNo == runs_number-1 ) leg2->Draw("same");

 
		for(int iy=0; iy<eta_bins; iy++)
		{
			etamin = yBnd[iy];
			etamax = yBnd[iy+1];
			const char *seta = (etamin==0 ? Form("|#eta| < %1.2g",etamax) :

			Form("%1.2g #leq |#eta| < %1.2g",yBnd[iy],yBnd[iy+1]));
			TLatex *teta = new TLatex(0.68,0.96,seta); //cout<<seta<<endl;
			teta->SetNDC();
			teta->SetTextSize(0.05);

			if(eta_bins > 1) pad1->cd(iy+1);
			else pad1->cd();
			if(eta_bins > 1) pad1->cd(iy+1)->SetLogy(1);
			else pad1->cd()->SetLogy(1);
			h_CHFJet1[iy][runNo]->GetXaxis()->SetTitle("Charged Hadron Fraction of Jet1");
			h_CHFJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_CHFJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_CHFJet1[iy][runNo]->SetLineWidth(2);
			h_CHFJet1[iy][runNo]->SetLineColor(1+runNo);
			h_CHFJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_CHFJet1[iy][runNo]->Scale(h_CHFJet1[iy][0]->Integral()/h_CHFJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_CHFJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_CHFJet1[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");


			if(eta_bins > 1) pad2->cd(iy+1);
			else pad2->cd();
			if(eta_bins > 1) pad2->cd(iy+1)->SetLogy(1);
			else pad2->cd()->SetLogy(1);
			h_NHFJet1[iy][runNo]->GetXaxis()->SetTitle("Neutral Hadron Fraction of Jet1");
			h_NHFJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_NHFJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_NHFJet1[iy][runNo]->SetLineWidth(2);
			h_NHFJet1[iy][runNo]->SetLineColor(1+runNo);
			h_NHFJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_NHFJet1[iy][runNo]->Scale(h_NHFJet1[iy][0]->Integral()/h_NHFJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_NHFJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_NHFJet1[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");
			//leg1->Draw("same"); 
	 


			if(eta_bins > 1) pad3->cd(iy+1);
			else pad3->cd();
			if(eta_bins > 1) pad3->cd(iy+1)->SetLogy(1);
			else pad3->cd()->SetLogy(1);
			h_CEMFJet1[iy][runNo]->GetXaxis()->SetTitle("Charged EM Fraction of Jet1");
			h_CEMFJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_CEMFJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_CEMFJet1[iy][runNo]->SetLineWidth(2);
			h_CEMFJet1[iy][runNo]->SetLineColor(1+runNo);
			h_CEMFJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_CEMFJet1[iy][runNo]->Scale(h_CEMFJet1[iy][0]->Integral()/h_CEMFJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_CEMFJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_CEMFJet1[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");
			//leg1->Draw("same");

			if(eta_bins > 1) pad4->cd(iy+1);
			else pad4->cd();
			if(eta_bins > 1) pad4->cd(iy+1)->SetLogy(1);
			else pad4->cd()->SetLogy(1);
			h_NEMFJet1[iy][runNo]->GetXaxis()->SetTitle("Neutral EM Fraction of Jet1");
			h_NEMFJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_NEMFJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_NEMFJet1[iy][runNo]->SetLineWidth(2);
			h_NEMFJet1[iy][runNo]->SetLineColor(1+runNo);
			h_NEMFJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_NEMFJet1[iy][runNo]->Scale(h_NEMFJet1[iy][0]->Integral()/h_NEMFJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_NEMFJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_NEMFJet1[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");
			//leg1->Draw("same");

			if(eta_bins > 1) pad5->cd(iy+1);
			else pad5->cd();
			if(eta_bins > 1) pad5->cd(iy+1)->SetLogy(1);
			else pad5->cd()->SetLogy(1);
			h_MUFJet1[iy][runNo]->GetXaxis()->SetTitle("Muon Energy Fraction of Jet1");
			h_MUFJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_MUFJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_MUFJet1[iy][runNo]->SetLineWidth(2);
			h_MUFJet1[iy][runNo]->SetLineColor(1+runNo);
			h_MUFJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_MUFJet1[iy][runNo]->Scale(h_MUFJet1[iy][0]->Integral()/h_MUFJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_MUFJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_MUFJet1[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");
		//	leg1->Draw("same");



			if(eta_bins > 1) pad10->cd(iy+1);
			else pad10->cd();
			if(eta_bins > 1) pad10->cd(iy+1)->SetLogy(1);
			else pad10->cd()->SetLogy(1);
			h_METovSUMET[iy][runNo]->GetXaxis()->SetTitle("MET / SumET ");
			h_METovSUMET[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_METovSUMET[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_METovSUMET[iy][runNo]->SetLineWidth(2);
			h_METovSUMET[iy][runNo]->SetLineColor(1+runNo);
			h_METovSUMET[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_METovSUMET[iy][runNo]->Scale(h_METovSUMET[iy][0]->Integral()/h_METovSUMET[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_METovSUMET[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_METovSUMET[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");
		//	leg1->Draw("same");
			//leg1->Draw("same");
	 
	
			if(eta_bins > 1) pad11->cd(iy+1);
			else pad11->cd();
			if(eta_bins > 1) pad11->cd(iy+1)->SetLogy(1);
			else pad11->cd()->SetLogy(1);
			h_NMJet1[iy][runNo]->GetXaxis()->SetTitle("Neutral Multiplicity of Jet1");
			h_NMJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_NMJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			if(iy<4)h_NMJet1[iy][runNo]->GetXaxis()->SetRangeUser(0.,70);
			else if(iy>3 && iy <6)h_NMJet1[iy][runNo]->GetXaxis()->SetRangeUser(0.,30);
			else h_NMJet1[iy][runNo]->GetXaxis()->SetRangeUser(0.,18);
			h_NMJet1[iy][runNo]->SetLineWidth(2);
			h_NMJet1[iy][runNo]->SetLineColor(1+runNo);
			h_NMJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_NMJet1[iy][runNo]->Scale(h_NMJet1[iy][0]->Integral()/h_NMJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_NMJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_NMJet1[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");
			//leg1->Draw("same");
		
			if(eta_bins > 1) pad12->cd(iy+1);
			else pad12->cd();
			if(eta_bins > 1) pad12->cd(iy+1)->SetLogy(1);
			else pad12->cd()->SetLogy(1);
			h_CMJet1[iy][runNo]->GetXaxis()->SetTitle("Charged Multiplicity of Jet1");
			h_CMJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_CMJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			if(iy<4)h_CMJet1[iy][runNo]->GetXaxis()->SetRangeUser(0.,70);
			else if(iy>3 && iy <6)h_CMJet1[iy][runNo]->GetXaxis()->SetRangeUser(0.,30);
			else h_CMJet1[iy][runNo]->GetXaxis()->SetRangeUser(0.,18);
			h_CMJet1[iy][runNo]->SetLineWidth(2);
			h_CMJet1[iy][runNo]->SetLineColor(1+runNo);
			h_CMJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_CMJet1[iy][runNo]->Scale(h_CMJet1[iy][0]->Integral()/h_CMJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_CMJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_CMJet1[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");
			//leg1->Draw("same");

			if(eta_bins > 1) pad13->cd(iy+1);
			else pad13->cd();
			if(eta_bins > 1) pad13->cd(iy+1)->SetLogy(1);
			else pad13->cd()->SetLogy(1);
			h_PMJet1[iy][runNo]->GetXaxis()->SetTitle("Photon Multiplicity of Jet1");
			h_PMJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_PMJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_PMJet1[iy][runNo]->SetLineWidth(2);
			h_PMJet1[iy][runNo]->SetLineColor(1+runNo);
			h_PMJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_PMJet1[iy][runNo]->Scale(h_PMJet1[iy][0]->Integral()/h_PMJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_PMJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_PMJet1[iy][runNo]->Draw("same");
			teta->Draw();

			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");

		
			if(eta_bins > 1) pad16->cd(iy+1);
			else pad16->cd();
			if(eta_bins > 1) pad16->cd(iy+1)->SetLogy(1);
			else pad16->cd()->SetLogy(1);
			h_PHIJet1[iy][runNo]->GetXaxis()->SetTitle("Phi of Jet1");
			h_PHIJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_PHIJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_PHIJet1[iy][runNo]->SetLineWidth(2);
			h_PHIJet1[iy][runNo]->SetLineColor(1+runNo);
			h_PHIJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_PHIJet1[iy][runNo]->Scale(h_PHIJet1[iy][0]->Integral()/h_PHIJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_PHIJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_PHIJet1[iy][runNo]->Draw("same");
			teta->Draw();
			//leg1->Draw("same");
			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");




			//for checking if the weighting has been done correct
			if(eta_bins > 1) pad9->cd(iy+1);
			else pad9->cd();
			if(eta_bins > 1) pad9->cd(iy+1)->SetLogy(1);
			else pad9->cd()->SetLogy(1);
			h_ptJet1[iy][runNo]->GetXaxis()->SetTitle("pT of Jet1");
			h_ptJet1[iy][runNo]->GetYaxis()->SetTitle("Entries");
			h_ptJet1[iy][runNo]->GetYaxis()->SetTitleOffset(1.3);
			h_ptJet1[iy][runNo]->SetLineWidth(2);
			h_ptJet1[iy][runNo]->SetLineColor(1+runNo);
			h_ptJet1[iy][runNo]->SetMarkerSize(0.04);
			if(scale_on == 1) h_ptJet1[iy][runNo]->Scale(h_ptJet1[iy][0]->Integral()/h_ptJet1[iy][runNo]->Integral());
			if ( runNo==0 ) 
			{
				h_ptJet1[iy][runNo]->Draw("hist");
				paveCMS ->Draw("same");
			}
			else h_ptJet1[iy][runNo]->Draw("same");
			teta->Draw();

			if(eta_bins <= 1 && runNo == runs_number-1 ) leg1->Draw("same");


		if(eta_bins > 1 && runNo == runs_number-1 )
		{
			pad1->cd(9);    leg1->Draw();
			pad2->cd(9);    leg1->Draw();
			pad3->cd(9);    leg1->Draw();
			pad4->cd(9);    leg1->Draw();
			pad5->cd(9);    leg1->Draw();
			pad9->cd(9);    leg1->Draw();
			pad10->cd(9);   leg1->Draw();
			pad11->cd(9);   leg1->Draw();
			pad12->cd(9);   leg1->Draw();
			pad13->cd(9);   leg1->Draw();
			pad16->cd(9);   leg1->Draw();
		}

		 } //end of eta regions
	} //end of loop on runs








	if (Save_pngs)
	{ 

		sprintf(filename,"%s/%s/h_chf_jet1%s.png",analyzer_path,output_directory,image_name);
		pad1->SaveAs(filename);
		sprintf(filename,"%s/%s/h_nhf_jet1%s.png",analyzer_path,output_directory,image_name);
		pad2->SaveAs(filename);
		sprintf(filename,"%s/%s/h_cemf_jet1%s.png",analyzer_path,output_directory,image_name);
		pad3->SaveAs(filename);
		sprintf(filename,"%s/%s/h_nemf_jet1%s.png",analyzer_path,output_directory,image_name);
		pad4->SaveAs(filename);
		sprintf(filename,"%s/%s/h_muf_jet1%s.png",analyzer_path,output_directory,image_name);
		pad5->SaveAs(filename);
		sprintf(filename,"%s/%s/h_pt_jet1%s.png",analyzer_path,output_directory,image_name);
		pad9->SaveAs(filename);
		sprintf(filename,"%s/%s/h_metovsumet%s.png",analyzer_path,output_directory,image_name);
		pad10->SaveAs(filename);
		sprintf(filename,"%s/%s/h_NM%s.png",analyzer_path,output_directory,image_name);
		pad11->SaveAs(filename);
		sprintf(filename,"%s/%s/h_CM%s.png",analyzer_path,output_directory,image_name);
		pad12->SaveAs(filename);
		sprintf(filename,"%s/%s/h_PM%s.png",analyzer_path,output_directory,image_name);
		pad13->SaveAs(filename);
		sprintf(filename,"%s/%s/h_phi%s.png",analyzer_path,output_directory,image_name);
		pad16->SaveAs(filename);
		sprintf(filename,"%s/%s/h_eta%s.png",analyzer_path,output_directory,image_name);
		pad17->SaveAs(filename);



	
		sprintf(filename,"%s/%s/Output%s.root",analyzer_path,output_directory,image_name);

		fout = new TFile(filename,"RECREATE");
		fout->cd();

		pad1->Write();
		pad2->Write();
		pad3->Write();
		pad4->Write();
		pad5->Write();
		pad9->Write();
		pad10->Write();
		pad11->Write();
		pad12->Write();
		pad13->Write();
		pad16->Write();
		pad17->Write();
	



		for (int runNo=0; runNo<runs_number; runNo++)
		{	

			h_ETAJet1[runNo]->Write();
			for(int iy=0; iy<eta_bins; iy++)
			{
				h_METovSUMET[iy][runNo]->Write();
				h_CHFJet1[iy][runNo]->Write();
				h_NHFJet1[iy][runNo]->Write();
				h_CEMFJet1[iy][runNo]->Write();
				h_NEMFJet1[iy][runNo]->Write();
				h_MUFJet1[iy][runNo]->Write();
				h_CMJet1[iy][runNo]->Write();
				h_NMJet1[iy][runNo]->Write();
				h_ptJet1[iy][runNo]->Write();
				h_PMJet1[iy][runNo]->Write();
				h_PHIJet1[iy][runNo]->Write();
			}
		}				

//		fout->Close();
	}
 }


bool FindJetIDFromEra ( int flag_era, double JetID_16, double JetID_17, double JetID_18 ) 
{
	bool boolianJetID=false;

	if ( flag_era == 2016 )
	{
		if (JetID_16 < 0.5 ) 	 boolianJetID = false;
		else if (JetID_16 > 0.5 ) boolianJetID = true;
		else { cout<<" ERROR! JetID for 16 is neither ==0 nor ==1. Check the inputs.. " <<  endl; exit(1); }
	}
	else if ( flag_era == 2017 )
	{
		if (JetID_17 < 0.5 ) 	 boolianJetID = false;
		else if (JetID_17 > 0.5 ) boolianJetID = true;
		else { cout<<" ERROR! JetID for 17 is neither ==0 nor ==1. Check the inputs.. " <<  endl; exit(1); }
	}
	else if ( flag_era == 2018 )
	{
		if (JetID_18 < 0.5 ) 	 boolianJetID = false;
		else if (JetID_18 > 0.5 ) boolianJetID = true;
		else { cout<<" ERROR! JetID for 18 is neither ==0 nor ==1. Check the inputs.. " <<  endl; exit(1); }
	}
	else 
	{
		cout<<" ERROR! Year era provided is not valid. Valid eras are: 2016, 2017, 2018. Will use JetID for 2018... " <<  endl;
		if (JetID_18 < 0.5 ) 	 boolianJetID = false;
		else if (JetID_18 > 0.5 ) boolianJetID = true;
		else { cout<<" ERROR! JetID for 18 is neither ==0 nor ==1. Check the inputs.. " <<  endl; exit(1); }
	}
return boolianJetID;
}

int getBin(double x, double boundaries[]) 
{
	int i;
	int n = eta_bins; //sizeof(boundaries)/sizeof(boundaries[0])-1;
	if (x<boundaries[0] || x>=boundaries[n]) return -1;
	for(i=0;i<n;i++)
	{
		if (x>=boundaries[i] && x<boundaries[i+1]) return i;
	}
	return 0;
}
	
