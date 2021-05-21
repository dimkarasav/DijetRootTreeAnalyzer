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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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
#include <cstring>
#include "TSystemDirectory.h"

//using namespace std;

double error1(double n1,double n2);
double error2(double n1,double n2);
int getBin(double x, double boundaries[], int eta_bins) ;
bool getJetID(int era, bool isUL, bool isCHS, bool LepVeto, double eta, double cm, double nm, double nemf, double cemf, double nhf, double chf, double muf );
bool FindJetIDFromEra ( int flag_era, bool JetID_16, bool JetID_17, bool JetID_18 ) ;
bool FindProbeJetID (int irand, int flag_era, double JetID_16_j1, double JetID_17_j1, double JetID_18_j1, double JetID_16_j2, double JetID_17_j2, double JetID_18_j2 );
bool FindTagJetID (int irand, int flag_era, double JetID_16_j1, double JetID_17_j1, double JetID_18_j1, double JetID_16_j2, double JetID_17_j2, double JetID_18_j2 );
double FindProbeVariable(int irand, double var_j1,  double var_j2);
double FindTagVariable(int irand, double var_j1,  double var_j2);

// 2017 data directory: root://eoscms///eos/cms/store/group/phys_jetmet/eirini/data2017/rereco/
void btbdijets_MC_no_vs_withJetID_recalcJetID()
 {


	char analyzer_path[300] = "/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/"; 
	char output_directory[300] = "UL_datasets_JetID/UL_2016/PUPPI/APV/MC_no_vs_with_JetID/";     
	char image_name[300] = "PFJet200_pT0_200"; 

	// full name to MC reduced.root would be: /eos/cms/store/group/phys_jetmet/dimitris/QCD_UL16APV_btb_PUPPI_reduced/Pt_30to50_QCD_TuneCP5_13TeV_pythia8_UL16_btb_reduced_skim.root
	char MC_path_start[300] = "/eos/cms/store/group/phys_jetmet/dimitris/QCD_UL16APV_btb_PUPPI_reduced/Pt_";
	char MC_path_end[300]   = "_QCD_TuneCP5_13TeV_pythia8_UL16_btb_reduced_skim.root";


	char legend_1[300] = "no_JetID";
	char legend_2[300] = "with_JetID";
	int era = 2016;
	const int eta_bins = 8;
	int scale_on = 0;
	bool isCHS = false;
	bool isUL = true;	
	bool Save_pngs = true;
	bool test_run = false; //if 'true' the script will loop only over the first 1000 entries. Option for tests.
	double lumi = 59800;
	double pTcutLow = 0;
	double pTcutHigh = 200;

	double yBnd[eta_bins+1]={0.0,0.5,1.0,1.5,2.0,2.4, 2.7, 3.0,5.0};
//	double yBnd[eta_bins+1]={2.6, 2.7};

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
	char filename[256]; 

	TH1D *h_METovSUMET[eta_bins], *h_CHFJet1[eta_bins], *h_NHFJet1[eta_bins], *h_CEMFJet1[eta_bins], *h_NEMFJet1[eta_bins], *h_MUFJet1[eta_bins], *h_CMJet1[eta_bins], *h_NMJet1[eta_bins], *h_ptJet1[eta_bins], *h_PMJet1[eta_bins], *h_DijetMassAK4[eta_bins], *h_ETAJet1, *h_PHIJet1[eta_bins], *h_nVtx_with[eta_bins], *h_nVtx[eta_bins];

	TH1D *h_METovSUMET_with[eta_bins], *h_CHFJet1_with[eta_bins], *h_NHFJet1_with[eta_bins], *h_CEMFJet1_with[eta_bins], *h_NEMFJet1_with[eta_bins], *h_MUFJet1_with[eta_bins], *h_CMJet1_with[eta_bins], *h_NMJet1_with[eta_bins], *h_ptJet1_with[eta_bins],*h_PMJet1_with[eta_bins] ,*h_DijetMassAK4_with[eta_bins],*h_ETAJet1_with,*h_PHIJet1_with[eta_bins];


	sprintf(name,"h_ETAJet1");
	h_ETAJet1 = new TH1D(name, "", 80,-5,5);

	sprintf(name,"h_ETAJet1_with");
	h_ETAJet1_with = new TH1D(name, "", 80,-5,5);

	
	for(Int_t h=0; h<eta_bins;h++)
	{ 
	//========== no JetID ===========
		sprintf(name,"h_METovSUMET%i",h);
		h_METovSUMET[h] = new TH1D(name, "", 40,0,1.0);
		sprintf(name,"h_nVtx%i",h);
		h_nVtx[h] = new TH1D(name, "", 25, 0,100);
		//h_METovSUMET[h]->Sumw2(); 
		sprintf(name,"h_CHFJet1%i",h);
		h_CHFJet1[h] = new TH1D(name, "", 40,0,1.2);
		//h_CHFJet1[h]->Sumw2(); 
		sprintf(name,"h_NHFJet1%i",h);
		h_NHFJet1[h] = new TH1D(name, "", 40,0,1.2);
		//h_NHFJet1[h]->Sumw2(); 
		sprintf(name,"h_CEMFJet1%i",h);
		h_CEMFJet1[h] = new TH1D(name, "", 40,0,1.2);
		//h_CEMFJet1[h]->Sumw2(); 
		sprintf(name,"h_NEMFJet1%i",h);
		h_NEMFJet1[h] = new TH1D(name, "", 40,0,1.2);
		//h_NEMFJet1[h]->Sumw2(); 
		sprintf(name,"h_MUFJet1%i",h);
		h_MUFJet1[h] = new TH1D(name, "", 40,0,1.2);
		//h_MUFJet1[h]->Sumw2(); 

		sprintf(name,"h_CMJet1%i",h);
		h_CMJet1[h] = new TH1D(name, "", 100,0,100);
		//sprintf(name,"h_ETAJet1%i",h);
	//	h_ETAJet1[h] = new TH1D(name, "", 60,-5,5);
		sprintf(name,"h_PHIJet1%i",h);
		if (h==5) h_PHIJet1[h] = new TH1D(name, "", 20,-4,4);		
		else h_PHIJet1[h] = new TH1D(name, "", 40,-4,4);
		sprintf(name,"h_DijetMassAK4%i",h);
		h_DijetMassAK4[h] = new TH1D(name,"",100,0,7500);
		// h_CMJet1[h]->Sumw2(); 
		sprintf(name,"h_NMJet1%i",h);
		h_NMJet1[h] = new TH1D(name, "", 100,0,100);
		//h_NMJet1[h]->Sumw2(); 
		sprintf(name,"h_PMJet1%i",h);
		h_PMJet1[h] = new TH1D(name, "", 100,0,100);
		// h_PMJet1_with[h]->Sumw2();
		sprintf(name,"h_ptJet1%i",h);
		h_ptJet1[h] = new TH1D(name, "", 300,0,3000);
		//h_ptJet1[h]->Sumw2(); 
		sprintf(name,"h_nVtx_with%i",h);
		h_nVtx_with[h] = new TH1D(name, "", 25, 0,100);
		   
		//=============== with JetID ===========
		sprintf(name,"h_METovSUMET_with%i",h);
		h_METovSUMET_with[h] = new TH1D(name, "", 40,0,1.0);
		//h_METovSUMET_with[h]->Sumw2();
		sprintf(name,"h_CHFJet1_with%i",h);
		h_CHFJet1_with[h] = new TH1D(name, "", 40,0,1.2);
		//h_CHFJet1_with[h]->Sumw2();
		sprintf(name,"h_NHFJet1_with%i",h);
		h_NHFJet1_with[h] = new TH1D(name, "", 40,0,1.2);
		//h_NHFJet1_with[h]->Sumw2();
		sprintf(name,"h_CEMFJet1_with%i",h);
		h_CEMFJet1_with[h] = new TH1D(name, "", 40,0,1.2);
		//h_CEMFJet1_with[h]->Sumw2();
		sprintf(name,"h_NEMFJet1_with%i",h);
		h_NEMFJet1_with[h] = new TH1D(name, "", 40,0,1.2);
		//h_NEMFJet1_with[h]->Sumw2();
		sprintf(name,"h_MUFJet1_with%i",h);
		h_MUFJet1_with[h] = new TH1D(name, "", 40,0,1.2);
		//h_MUFJet1_with[h]->Sumw2();

		sprintf(name,"h_PHIJet1_with%i",h);
		if (h==5) h_PHIJet1_with[h] = new TH1D(name, "", 20,-4,4);
		else h_PHIJet1_with[h] = new TH1D(name, "", 40,-4,4);
//		sprintf(name,"h_ETAJet1_with%i",h);
//		h_ETAJet1_with[h] = new TH1D(name, "", 60,-4,4);
		sprintf(name,"h_DijetMassAK4_with%i",h);
		h_DijetMassAK4_with[h] = new TH1D(name,"",100,0,7500);
		sprintf(name,"h_CMJet1_with%i",h);
		h_CMJet1_with[h] = new TH1D(name, "", 100,0,100);
		//  h_CMJet1_with[h]->Sumw2();*/
		sprintf(name,"h_NMJet1_with%i",h);
		h_NMJet1_with[h] = new TH1D(name, "", 100,0,100);
		sprintf(name,"h_PMJet1_with%i",h);
		h_PMJet1_with[h] = new TH1D(name, "", 100,0,100);
		// h_PMJet1_with[h]->Sumw2();
		//h_NMJet1_with[h]->Sumw2();
		sprintf(name,"h_ptJet1_with%i",h);
		h_ptJet1_with[h] = new TH1D(name, "", 300,0,3000);
		//h_ptJet1_with[h]->Sumw2();
	}
	

	TH2D *h_eta_phi_map = new TH2D("h_eta_phi_map", "eta-phi map", 30 , -5, 5, 12 , -3.1416,3.1416);
	TH2D *h_eta_phi_map_with = new TH2D("h_eta_phi_map_with", "eta-phi map", 30 , -5, 5, 12 , -3.1416,3.1416);


	double passHLT, passHLT1, passHLT2, passHLT3, passHLT4, nVtx, met_ov_sumet;
	bool JetID_2016_j1, JetID_2017_j1, JetID_2018_j1, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2;
	bool JetID_j1, JetID_j2;
	double pT_j1, eta_j1, chf_j1, nhf_j1, cemf_j1, nemf_j1, muf_j1, cm_j1, nm_j1, pm_j1, elf_j1, phf_j1, phi_j1;
	double pT_j2, eta_j2, chf_j2, nhf_j2, cemf_j2, nemf_j2, muf_j2, cm_j2, nm_j2, pm_j2, elf_j2, phf_j2, phi_j2;

  // double ymax; 
//   double yBnd[eta_bins+1]={0.0,0.5,1.0,1.5,2.0,2.7, 3.0,5.0};

 //  double yBnd[eta_bins+1]={2.5,3.2};

		//=========================2017 MC btb dijet Pythia =======================================

	
	char PtHatBin[15][50] = {"15to30" , "30to50", "50to80", "80to120", "120to170" , "170to300" , "300to470" , "470to600" , "600to800" , "800to1000" , "1000to1400", "1400to1800", "1800to2400", "2400to3200", "3200toInf"  }; //ptHatBins of MC

	double cross_section[15] = { 1820000000,138900000, 19100000 ,2735000 ,467500.,117400., 7753.,642.1, 185.9, 32.05, 9.365	, 0.8398, 0.1124, 0.006752, 0.0001626}; //xsec of 2017

													  
	long double weight[15];
	int Ntotal = 0;

	std::cout<<"Calculating the weights of each pt-hat bin file... "  << std::endl;
	TFile *f1;

	char input_directory[300];

	for(int fl=6; fl<15; fl++)
	{ 

		strcpy(input_directory,"/eos/cms/store/group/phys_jetmet/dimitris/QCD_UL16APV_btb_PUPPI_reduced/Pt_");
		strcat(input_directory,PtHatBin[fl]);		
		char file_name[200];
		sprintf(file_name,"_QCD_TuneCP5_13TeV_pythia8_UL16_btb_reduced_skim.root");
		strcat(input_directory,file_name);
		f1 = TFile::Open(input_directory,"READ");
	    TH1D *h_Nev = (TH1D*)f1->Get("DijetFilter/EventCount/EventCounter");
	    int Nev = h_Nev->GetBinContent(2);
		Ntotal = Ntotal + Nev;
	    std::cout<<Nev<<std::endl;
		weight[fl] = cross_section[fl]*lumi/Nev;
	    std::cout<< "pT bin : " << PtHatBin[fl] <<", Weight is " << weight[fl] << std::endl;
		//weight[fl]=1.;
	}  

	cout << " Total number of events: " << Ntotal << endl;


	for(Int_t fl=6;fl<15;fl++)
	{  

		strcpy(input_directory,"/eos/cms/store/group/phys_jetmet/dimitris/QCD_UL16APV_btb_PUPPI_reduced/Pt_");
		strcat(input_directory,PtHatBin[fl]);
		char file_name[200];
		sprintf(file_name,"_QCD_TuneCP5_13TeV_pythia8_UL16_btb_reduced_skim.root");
		strcat(input_directory,file_name);
		f1 = TFile::Open(input_directory,"READ");
		TTree *tree = (TTree*)f1->Get("rootTupleTree/tree");

		tree->SetBranchAddress("passHLT",&passHLT);  //for ak8:    AK8PFHT800 TrimMass50_v12
		tree->SetBranchAddress("passHLT1",&passHLT1);  //for ak8:  AK8PFHT850 TrimMass50_v11
		tree->SetBranchAddress("passHLT2",&passHLT2);  //for ak8:  AK8PFHT900_TrimMass50_v11
		tree->SetBranchAddress("passHLT3",&passHLT3); //for ak8:   AK8PFJet200_v15
		tree->SetBranchAddress("passHLT4",&passHLT4); //for ak8:   AK8PFJet400_v16

		tree->SetBranchAddress("metSig",&met_ov_sumet);
		tree->SetBranchAddress("nVtx",&nVtx);
		tree->SetBranchAddress("chargedHadEnFrac_j1",&chf_j1);
		tree->SetBranchAddress("neutrHadEnFrac_j1",&nhf_j1);
		tree->SetBranchAddress("chargedElectromFrac_j1",&cemf_j1);
		tree->SetBranchAddress("neutrElectromFrac_j1",&nemf_j1);
		tree->SetBranchAddress("muEnFract_j1",&muf_j1);
		tree->SetBranchAddress("chargedMult_j1",&cm_j1);
		tree->SetBranchAddress("neutrMult_j1",&nm_j1);
		tree->SetBranchAddress("photonMult_j1",&pm_j1);
		tree->SetBranchAddress("eta_j1",&eta_j1);
		tree->SetBranchAddress("pT_j1",&pT_j1);
		tree->SetBranchAddress("eleEnFract_j1",&elf_j1);
		tree->SetBranchAddress("photonEnFrac_j1",&phf_j1);
		tree->SetBranchAddress("phi_j1",&phi_j1);

		tree->SetBranchAddress("chargedHadEnFrac_j2",&chf_j2);
		tree->SetBranchAddress("neutrHadEnFrac_j2",&nhf_j2);
		tree->SetBranchAddress("chargedElectromFrac_j2",&cemf_j2);
		tree->SetBranchAddress("neutrElectromFrac_j2",&nemf_j2);
		tree->SetBranchAddress("muEnFract_j2",&muf_j2);
		tree->SetBranchAddress("chargedMult_j2",&cm_j2);
		tree->SetBranchAddress("neutrMult_j2",&nm_j2);
		tree->SetBranchAddress("photonMult_j2",&pm_j2);
		tree->SetBranchAddress("eta_j2",&eta_j2);
		tree->SetBranchAddress("pT_j2",&pT_j2);
		tree->SetBranchAddress("eleEnFract_j2",&elf_j2);
		tree->SetBranchAddress("photonEnFrac_j2",&phf_j2);
		tree->SetBranchAddress("phi_j2",&phi_j2);


		Int_t nentries=(Int_t)tree->GetEntries(); 
		cout<<"Number of entries =  "<<nentries<<endl;

		//int count=0; int countt=0;
	   	int LoopEntries =0;
		
		if(test_run) LoopEntries = 1000;
		else LoopEntries = nentries;
		
		for (int i=0; i<LoopEntries; i++) //event loop
		{
			if(i%5000000==0) cout<<i<<endl;
			tree->GetEntry(i);
			if (pT_j1 < 0.1 ) continue;
			//	if(run>320065)continue; //get run C events
			
			if (!(pT_j1>pTcutLow && pT_j1 < pTcutHigh)) continue; //pT cuts
			int ybin = getBin(fabs(eta_j1),yBnd,eta_bins);
	 	
			
			JetID_2016_j1 = getJetID(2016, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );
			JetID_2017_j1 = getJetID(2017, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );
			JetID_2018_j1 = getJetID(2018, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );

			JetID_2016_j2 = getJetID(2016, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );
			JetID_2017_j2 = getJetID(2017, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );
			JetID_2018_j2 = getJetID(2018, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );


			JetID_j1 = FindJetIDFromEra(era, JetID_2016_j1, JetID_2017_j1, JetID_2018_j1);
			JetID_j2 = FindJetIDFromEra(era, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2);


			if (passHLT4==1) h_ETAJet1->Fill(eta_j1,weight[fl]);	
	//		if (passHLT2==1) h_ETAJet1->Fill(eta_j1,weight[fl]);	
			if ( JetID_j1 && JetID_j2 && passHLT4==1 ) h_ETAJet1_with->Fill(eta_j1,weight[fl]);
				

			if ( passHLT4 != 1 ) continue; //trigger cut
	//		if ( passHLT2 != 1 ) continue; //trigger cut


					//=== eta regions ====
			if (ybin > -1 )   //fill hist's in the corresponding eta bin
			{ 
				h_CHFJet1[ybin]->Fill(chf_j1,weight[fl]); 
				h_NHFJet1[ybin]->Fill(nhf_j1,weight[fl]);
				h_CEMFJet1[ybin]->Fill(cemf_j1,weight[fl]);
				h_NEMFJet1[ybin]->Fill(nemf_j1,weight[fl]);
				h_MUFJet1[ybin]->Fill(muf_j1,weight[fl]);
				//	h_ETAJet1[ybin]->Fill(eta_j1);
				h_PHIJet1[ybin]->Fill(phi_j1,weight[fl]);
				h_CMJet1[ybin]->Fill(cm_j1,weight[fl]);
				h_NMJet1[ybin]->Fill(nm_j1,weight[fl]);
				h_PMJet1[ybin]->Fill(pm_j1,weight[fl]);
				h_ptJet1[ybin]->Fill(pT_j1,weight[fl]);
				h_METovSUMET[ybin]->Fill(met_ov_sumet,weight[fl]);
				h_nVtx[ybin]->Fill(nVtx,weight[fl]);
				h_eta_phi_map->Fill(eta_j1,phi_j1,weight[fl]);
				}// end of if ybin>-1

			if (ybin > -1 && JetID_j1 && JetID_j2   ) //fill hist's in the corresponding eta bin for events with passed JetID
			{ 		 
				h_CHFJet1_with[ybin]->Fill(chf_j1,weight[fl]);  //cout<<ybin<<"  "<<chf<<"   "<<eta_j1<<"  "<<etaj2<<endl;
				h_NHFJet1_with[ybin]->Fill(nhf_j1,weight[fl]);
				h_CEMFJet1_with[ybin]->Fill(cemf_j1,weight[fl]);
				h_NEMFJet1_with[ybin]->Fill(nemf_j1,weight[fl]);
				h_MUFJet1_with[ybin]->Fill(muf_j1,weight[fl]);
				h_CMJet1_with[ybin]->Fill(cm_j1,weight[fl]);
				h_NMJet1_with[ybin]->Fill(nm_j1,weight[fl]);
				h_PMJet1_with[ybin]->Fill(pm_j1,weight[fl]);
				h_ptJet1_with[ybin]->Fill(pT_j1,weight[fl]);
			//	h_ETAJet1_with[ybin]->Fill(eta_j1);
				h_PHIJet1_with[ybin]->Fill(phi_j1,weight[fl]);
				h_METovSUMET_with[ybin]->Fill(met_ov_sumet,weight[fl]);
				h_nVtx_with[ybin]->Fill(nVtx,weight[fl]);
				h_eta_phi_map_with->Fill(eta_j1,phi_j1,weight[fl]);
			}//end of if ybin>-1
		}// end of event loop
	delete tree;
	f1->Close();

	} // end of pT-hat bin loop



	TCanvas *pad1 = new TCanvas("pad1", "",1);
	if(eta_bins > 1) pad1->Divide(3,3);
	TCanvas *pad2 = new TCanvas("pad2", "",1);
	if(eta_bins > 1) pad2->Divide(3,3);
	TCanvas *pad3 = new TCanvas("pad3", "",1);
	if(eta_bins > 1) pad3->Divide(3,3);
	TCanvas *pad4 = new TCanvas("pad4", "",1);
	if(eta_bins > 1) pad4->Divide(3,3);
	TCanvas *pad5 = new TCanvas("pad5", "",1);
	if(eta_bins > 1) pad5->Divide(3,3);
	TCanvas *pad9 = new TCanvas("pad9", "",1);
	if(eta_bins > 1) pad9->Divide(3,3);
	TCanvas *pad10= new TCanvas("pad10", "",1);
	if(eta_bins > 1) pad10->Divide(3,3);
	TCanvas *pad11= new TCanvas("pad11", "",1);
	if(eta_bins > 1) pad11 ->Divide(3,3);
	TCanvas *pad12= new TCanvas("pad12", "",1);
	if(eta_bins > 1) pad12 ->Divide(3,3);
	TCanvas *pad13= new TCanvas("pad13", "",1);
	if(eta_bins > 1) pad13 ->Divide(3,3);
	TCanvas *pad14= new TCanvas("pad14", "",1);
	if(eta_bins > 1) pad14 ->Divide(3,3);
	TCanvas *pad15= new TCanvas("pad15", "",1);
	if(eta_bins > 1) pad15 ->Divide(3,3);
	TCanvas *pad16= new TCanvas("pad16", "",1);
	if(eta_bins > 1) pad16 ->Divide(3,3);
	TCanvas *pad18= new TCanvas("pad18", "",1);
	if(eta_bins > 1) pad18 ->Divide(3,3);



	TCanvas *pad17= new TCanvas("pad17", "eta",1);
//	pad17 ->Divide(3,3); 
//	TCanvas *eta_phi_canvas = new TCanvas("eta_phi_canvas", "",600,600);
//	TCanvas *eta_phi_canvas_with = new TCanvas("eta_phi_canvas_with", "",600,600);

	TCanvas *eta_phi_canvas = new TCanvas("eta_phi_canvas", "",600,600);
	TCanvas *eta_phi_canvas_with = new TCanvas("eta_phi_canvas_with", "",600,600);

	TCanvas *NM_pT_canvas = new TCanvas("NM_pT_canvas", "",600,600);
	TCanvas *NM_pT_canvas_with = new TCanvas("NM_pT_canvas_with", "",600,600);


//	pad17->cd(iy+1);
	pad17->cd()->SetLogy(1);
	h_ETAJet1->GetXaxis()->SetTitle("#eta") ;
	h_ETAJet1->GetYaxis()->SetTitle("Entries");
	h_ETAJet1->GetYaxis()->SetTitleOffset(1.3);
	h_ETAJet1->SetLineWidth(2);
	h_ETAJet1->SetLineColor(1);
	h_ETAJet1->SetMarkerSize(0.04);
	h_ETAJet1_with->SetLineWidth(2);
	h_ETAJet1_with->SetLineColor(4);
	h_ETAJet1_with->SetMarkerSize(0.04);
	if(scale_on == 1) h_ETAJet1->Scale(h_ETAJet1_with->Integral()/h_ETAJet1->Integral());
	h_ETAJet1->Draw("hist");
	h_ETAJet1_with->Draw("same");
	paveCMS ->Draw("same");

	//leg1->Draw();


 
	for(int iy=0; iy<eta_bins; iy++)
	 {
		etamin = yBnd[iy];
		etamax = yBnd[iy+1];
		const char *seta = (etamin==0 ? Form("|y| < %1.2g",etamax) :

		Form("%1.2g #leq |y| < %1.2g",yBnd[iy],yBnd[iy+1]));
		TLatex *teta = new TLatex(0.68,0.96,seta); //cout<<seta<<endl;
		teta->SetNDC();
		teta->SetTextSize(0.05);

		if(eta_bins > 1) pad1->cd(iy+1);
		else pad1->cd();
		if(eta_bins > 1) pad1->cd(iy+1)->SetLogy(1);
		else pad1->cd()->SetLogy(1);
		h_CHFJet1[iy]->GetXaxis()->SetTitle("Charged Hadron Fraction of Jet1");
		h_CHFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CHFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_CHFJet1[iy]->SetLineWidth(2);
		h_CHFJet1[iy]->SetLineColor(1);
		h_CHFJet1[iy]->SetMarkerSize(0.04);
		h_CHFJet1_with[iy]->SetLineWidth(2);
		h_CHFJet1_with[iy]->SetLineColor(4);
		h_CHFJet1_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_CHFJet1[iy]->Scale(h_CHFJet1_with[iy]->Integral()/h_CHFJet1[iy]->Integral());
		h_CHFJet1[iy]->Draw("hist");
		h_CHFJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();

		TLegend *leg1 =new TLegend(0.4,0.7,0.7,0.9); //7899  //4899
		leg1->SetTextSize(0.1);
		leg1->SetFillColor(0); 
		leg1->SetBorderSize(0);  
		leg1->AddEntry(h_CHFJet1[0], legend_1,  "L");
		leg1->AddEntry(h_CHFJet1_with[0], legend_2, "L");
		//leg1->Draw("same");
		if(eta_bins <= 1) leg1->Draw("same");

		if(eta_bins > 1) pad2->cd(iy+1);
		else pad2->cd();
		if(eta_bins > 1) pad2->cd(iy+1)->SetLogy(1);
		else pad2->cd()->SetLogy(1);
		h_NHFJet1[iy]->GetXaxis()->SetTitle("Neutral Hadron Fraction of Jet1");
		h_NHFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NHFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_NHFJet1[iy]->SetLineWidth(2);
		h_NHFJet1[iy]->SetLineColor(1);
		if(scale_on == 1) h_NHFJet1[iy]->Scale(h_NHFJet1_with[iy]->Integral()/h_NHFJet1[iy]->Integral());
		h_NHFJet1[iy]->SetMarkerSize(0.04);
		h_NHFJet1_with[iy]->SetLineWidth(2);
		h_NHFJet1_with[iy]->SetLineColor(4);
		h_NHFJet1_with[iy]->SetMarkerSize(0.04);
		h_NHFJet1[iy]->Draw("hist");
		h_NHFJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		//leg1->Draw("same"); 
 
		if(eta_bins > 1) pad3->cd(iy+1);
		else pad3->cd();
		if(eta_bins > 1) pad3->cd(iy+1)->SetLogy(1);
		else pad3->cd()->SetLogy(1);
		h_CEMFJet1[iy]->GetXaxis()->SetTitle("Charged Electromagnetic Fraction of Jet1");
		h_CEMFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CEMFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_CEMFJet1[iy]->SetLineWidth(2);
		h_CEMFJet1[iy]->SetLineColor(1);
		h_CEMFJet1[iy]->SetMarkerSize(0.04);
		h_CEMFJet1_with[iy]->SetLineWidth(2);
		h_CEMFJet1_with[iy]->SetLineColor(4);
		if(scale_on == 1) h_CEMFJet1[iy]->Scale(h_CEMFJet1_with[iy]->Integral()/h_CEMFJet1[iy]->Integral());
		h_CEMFJet1_with[iy]->SetMarkerSize(0.04);
		if(iy==5)h_CEMFJet1[iy]->SetMinimum(0.1);
		h_CEMFJet1[iy]->Draw("hist");
		h_CEMFJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		//leg1->Draw("same");

		if(eta_bins > 1) pad4->cd(iy+1);
		else pad4->cd();
		if(eta_bins > 1) pad4->cd(iy+1)->SetLogy(1);
		else pad4->cd()->SetLogy(1);
		h_NEMFJet1[iy]->GetXaxis()->SetTitle("Neutral Electromagnetic Fraction of Jet1"); 
		h_NEMFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NEMFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_NEMFJet1[iy]->SetLineWidth(2);
		h_NEMFJet1[iy]->SetLineColor(1);
		h_NEMFJet1[iy]->SetMarkerSize(0.04);
		h_NEMFJet1_with[iy]->SetLineWidth(2);
		h_NEMFJet1_with[iy]->SetLineColor(4);
		if(scale_on == 1) h_NEMFJet1[iy]->Scale(h_NEMFJet1_with[iy]->Integral()/h_NEMFJet1[iy]->Integral());
		h_NEMFJet1_with[iy]->SetMarkerSize(0.04);
		h_NEMFJet1[iy]->Draw("hist");
		h_NEMFJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		//leg1->Draw("same");

		if(eta_bins > 1) pad5->cd(iy+1);
		else pad5->cd();
		if(eta_bins > 1) pad5->cd(iy+1)->SetLogy(1);
		else pad5->cd()->SetLogy(1);
		h_MUFJet1[iy]->GetXaxis()->SetTitle("Muon Fraction of Jet1");
		h_MUFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_MUFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_MUFJet1[iy]->SetLineWidth(2);
		h_MUFJet1[iy]->SetLineColor(1);
		h_MUFJet1[iy]->SetMarkerSize(0.04);
		h_MUFJet1_with[iy]->SetLineWidth(2);
		h_MUFJet1_with[iy]->SetLineColor(4);
		h_MUFJet1_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_MUFJet1[iy]->Scale(h_MUFJet1_with[iy]->Integral()/h_MUFJet1[iy]->Integral());
		h_MUFJet1[iy]->SetMinimum(0.1);
		h_MUFJet1[iy]->Draw("hist");
		h_MUFJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
	//	leg1->Draw("same");

		if(eta_bins > 1) pad10->cd(iy+1);
		else pad10->cd();
		if(eta_bins > 1) pad10->cd(iy+1)->SetLogy(1);
		else pad10->cd()->SetLogy(1);
		h_METovSUMET[iy]->GetXaxis()->SetTitle("MetSig") ;
		h_METovSUMET[iy]->GetYaxis()->SetTitle("Entries");
		h_METovSUMET[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_METovSUMET[iy]->SetLineWidth(2);
		h_METovSUMET[iy]->SetLineColor(1);
		h_METovSUMET[iy]->SetMarkerSize(0.04);
		h_METovSUMET_with[iy]->SetLineWidth(2);
		h_METovSUMET_with[iy]->SetLineColor(4);
		h_METovSUMET_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_METovSUMET[iy]->Scale(h_METovSUMET_with[iy]->Integral()/h_METovSUMET[iy]->Integral());
		h_METovSUMET[iy]->SetMinimum(0.1);
		h_METovSUMET[iy]->Draw("hist");
		h_METovSUMET_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		TLegend *leg2 =new TLegend(0.4,0.7,0.48,0.9);//7899  //4899
		leg2->SetTextSize(0.06);
		leg2->SetFillColor(0); 
		leg2->SetBorderSize(0);
		leg2->AddEntry((TObject*)0, "AK4", "");
		leg2->AddEntry(h_METovSUMET[0], legend_1,  "L");
		leg2->AddEntry(h_METovSUMET_with[0], legend_2, "L");
		if(eta_bins <= 1) leg1->Draw("same");
		//leg1->Draw("same");
 

		if(eta_bins > 1) pad11->cd(iy+1);
		else pad11->cd();
		if(eta_bins > 1) pad11->cd(iy+1)->SetLogy(1);
		else pad11->cd()->SetLogy(1);
		h_NMJet1[iy]->GetXaxis()->SetTitle("Neutral Multiplicity") ;
		h_NMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		if(iy<4)h_NMJet1[iy]->GetXaxis()->SetRangeUser(0.,70);
		else if(iy>3 && iy <6)h_NMJet1[iy]->GetXaxis()->SetRangeUser(0.,30);
		else h_NMJet1[iy]->GetXaxis()->SetRangeUser(0.,18);
		h_NMJet1[iy]->SetLineWidth(2);
		h_NMJet1[iy]->SetLineColor(1);
		h_NMJet1[iy]->SetMarkerSize(0.04);
		h_NMJet1_with[iy]->SetLineWidth(2);
		h_NMJet1_with[iy]->SetLineColor(4);
		h_NMJet1_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_NMJet1[iy]->Scale(h_NMJet1_with[iy]->Integral()/h_NMJet1[iy]->Integral());
		h_NMJet1[iy]->SetMinimum(0.1);
		h_NMJet1[iy]->Draw("hist");
		h_NMJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		//leg1->Draw("same");
		
		if(eta_bins > 1) pad12->cd(iy+1);
		else pad12->cd();
		if(eta_bins > 1) pad12->cd(iy+1)->SetLogy(1);
		else pad12->cd()->SetLogy(1);
		h_CMJet1[iy]->GetXaxis()->SetTitle("Charged Multiplicity") ;
		h_CMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		if(iy>3)h_CMJet1[iy]->GetXaxis()->SetRangeUser(0.,30);
		else h_CMJet1[iy]->GetXaxis()->SetRangeUser(0.,30);
		h_CMJet1[iy]->SetLineWidth(2);
		h_CMJet1[iy]->SetLineColor(1);
		h_CMJet1[iy]->SetMarkerSize(0.04);
		h_CMJet1_with[iy]->SetLineWidth(2);
		h_CMJet1_with[iy]->SetLineColor(4);
		h_CMJet1_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_CMJet1[iy]->Scale(h_CMJet1_with[iy]->Integral()/h_CMJet1[iy]->Integral());
		h_CMJet1[iy]->SetMinimum(0.1);
		h_CMJet1[iy]->Draw("hist");
		h_CMJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		//leg1->Draw("same");

		if(eta_bins > 1) pad13->cd(iy+1);
		else pad13->cd();
		if(eta_bins > 1) pad13->cd(iy+1)->SetLogy(1);
		else pad13->cd()->SetLogy(1);
		h_PMJet1[iy]->GetXaxis()->SetTitle("Photon Multiplicity") ;
		h_PMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_PMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_PMJet1[iy]->SetLineWidth(2);
		h_PMJet1[iy]->SetLineColor(1);
		 h_PMJet1[iy]->SetMarkerSize(0.04);
		h_PMJet1_with[iy]->SetLineWidth(2);
		h_PMJet1_with[iy]->SetLineColor(4);
		h_PMJet1_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_PMJet1[iy]->Scale(h_PMJet1_with[iy]->Integral()/h_PMJet1[iy]->Integral());
		h_PMJet1[iy]->SetMinimum(0.1);
		h_CMJet1[iy]->Draw("hist");
		h_PMJet1[iy]->Draw("hist");
		h_PMJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		//leg1->Draw("same");
		
		if(eta_bins > 1) pad16->cd(iy+1);
		else pad16->cd();
		if(eta_bins > 1) pad16->cd(iy+1)->SetLogy(1);
		else pad16->cd()->SetLogy(1);
		h_PHIJet1[iy]->GetXaxis()->SetTitle("#phi") ;
		h_PHIJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_PHIJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_PHIJet1[iy]->SetLineWidth(2);
		h_PHIJet1[iy]->SetLineColor(1);
		h_PHIJet1[iy]->SetMarkerSize(0.04);
		h_PHIJet1_with[iy]->SetLineWidth(2);
		h_PHIJet1_with[iy]->SetLineColor(4);
		h_PHIJet1_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_PHIJet1[iy]->Scale(h_PHIJet1_with[iy]->Integral()/h_PHIJet1[iy]->Integral());
		h_PHIJet1[iy]->Draw("hist");
		h_PHIJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		//leg1->Draw();



		if(eta_bins > 1) pad18->cd(iy+1);
		else pad18->cd();
//		if(eta_bins > 1) pad18->cd(iy+1)->SetLogy(1);
//		else pad18->cd()->SetLogy(1);
		h_nVtx[iy]->GetXaxis()->SetTitle("nVtx") ;
		h_nVtx[iy]->GetYaxis()->SetTitle("Entries");
		h_nVtx[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_nVtx[iy]->SetLineWidth(2);
		h_nVtx[iy]->SetLineColor(1);
		h_nVtx[iy]->SetMarkerSize(0.04);
		h_nVtx[iy]->SetMinimum(0.1);
		if(scale_on == 1) h_nVtx_with[iy]->Scale(h_nVtx[iy]->Integral() / h_nVtx_with[iy]->Integral());
		h_nVtx[iy]->Draw("hist");

		h_nVtx_with[iy]->SetLineWidth(2);
		h_nVtx_with[iy]->SetLineColor(4);
		h_nVtx_with[iy]->SetMarkerSize(0.04);
		h_nVtx_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");



/*
		pad17->cd(iy+1);
		pad17->cd(iy+1)->SetLogy(1);
		h_ETAJet1[iy]->GetXaxis()->SetTitle("#eta") ;
		h_ETAJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_ETAJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_ETAJet1[iy]->SetLineWidth(2);
		h_ETAJet1[iy]->SetLineColor(1);
		h_ETAJet1[iy]->SetMarkerSize(0.04);
		h_ETAJet1_with[iy]->SetLineWidth(2);
		h_ETAJet1_with[iy]->SetLineColor(4);
		h_ETAJet1_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_ETAJet1[iy]->Scale(h_ETAJet1_with[iy]->Integral()/h_ETAJet1[iy]->Integral());
		h_ETAJet1[iy]->Draw("hist");
		h_ETAJet1_with[iy]->Draw("same");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1->Draw();
*/

		//for checking if the weighting has been done correct
		if(eta_bins > 1) pad9->cd(iy+1);
		else pad9->cd();
		if(eta_bins > 1) pad9->cd(iy+1)->SetLogy(1);
		else pad9->cd()->SetLogy(1);
		h_ptJet1[iy]->GetXaxis()->SetTitle("pT of Jet1 (GeV)");
		h_ptJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_ptJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_ptJet1[iy]->SetLineWidth(2);
		h_ptJet1[iy]->SetLineColor(1);
		h_ptJet1[iy]->SetMarkerSize(0.04);
		h_ptJet1_with[iy]->SetLineWidth(2);
		h_ptJet1_with[iy]->SetLineColor(4);
		h_ptJet1_with[iy]->SetMarkerSize(0.04);
		if(scale_on == 1) h_ptJet1[iy]->Scale(h_ptJet1_with[iy]->Integral()/h_ptJet1[iy]->Integral());
		//h_ptJet1[iy]->SetMinimum(0.1); 
		h_ptJet1[iy]->Draw("hist");
		h_ptJet1_with[iy]->Draw("hist same");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		//leg2->Draw();


	if(eta_bins > 1)
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
		pad18->cd(9);   leg1->Draw();
	}

	 } //end of eta regions

	eta_phi_canvas->cd();
    eta_phi_canvas->cd()->SetRightMargin(0.18);
    eta_phi_canvas->cd()->SetTopMargin(0.07);
	h_eta_phi_map->SetStats(true);
	h_eta_phi_map->GetXaxis()->SetTitle("#eta-phi of Jet1");
	h_eta_phi_map->GetXaxis()->SetTitle("#eta") ;
	h_eta_phi_map->GetYaxis()->SetTitle("#phi");
	h_eta_phi_map->GetYaxis()->SetTitleOffset(0.9);
	h_eta_phi_map->SetMinimum(5.);
	gPad->SetLogz();
	h_eta_phi_map->Draw("colz");   
	paveCMS->Draw("same");

	eta_phi_canvas_with->cd();
	eta_phi_canvas_with->cd()->SetRightMargin(0.18);
    eta_phi_canvas_with->cd()->SetTopMargin(0.07);
	h_eta_phi_map_with->SetStats(true);
	h_eta_phi_map_with->GetXaxis()->SetTitle("#eta-phi of Jet1");
	h_eta_phi_map_with->GetXaxis()->SetTitle("#eta") ;
	h_eta_phi_map_with->GetYaxis()->SetTitle("#phi");
	h_eta_phi_map_with->GetYaxis()->SetTitleOffset(0.9);
	h_eta_phi_map_with->SetMinimum(5.);
	gPad->SetLogz();
	h_eta_phi_map_with->Draw("colz");   
	paveCMS->Draw("same");


	if (Save_pngs)
	{ 

		sprintf(filename,"%s/%s/%s_chf_jet1.png",analyzer_path,output_directory,image_name);
		pad1->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_nhf_jet1.png",analyzer_path,output_directory,image_name);
		pad2->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_cemf_jet1.png",analyzer_path,output_directory,image_name);
		pad3->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_nemf_jet1.png",analyzer_path,output_directory,image_name);
		pad4->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_muf_jet1.png",analyzer_path,output_directory,image_name);
		pad5->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_pt_jet1.png",analyzer_path,output_directory,image_name);
		pad9->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_metovsumet.png",analyzer_path,output_directory,image_name);
		pad10->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_NM.png",analyzer_path,output_directory,image_name);
		pad11->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_CM.png",analyzer_path,output_directory,image_name);
		pad12->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_PM.png",analyzer_path,output_directory,image_name);
		pad13->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_phi.png",analyzer_path,output_directory,image_name);
		pad16->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_eta.png",analyzer_path,output_directory,image_name);
		pad17->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_nVtx.png",analyzer_path,output_directory,image_name);
		pad18->SaveAs(filename);

		sprintf(filename,"%s/%s/%s_%s_eta_phi.png",analyzer_path,output_directory,image_name,legend_1);
		eta_phi_canvas->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_%s_eta_phi.png",analyzer_path,output_directory,image_name,legend_2);
		eta_phi_canvas_with->SaveAs(filename);

	
	

		sprintf(filename,"%s/%s/%s.root",analyzer_path,output_directory,image_name);

		TFile *fout = new TFile(filename,"RECREATE");
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
		pad15->Write();
		pad16->Write();
		pad17->Write();
		eta_phi_canvas->Write();
		eta_phi_canvas_with->Write();
		fout->Close();
	}
 }

//=====================================================================
//The error bars are determined from Wilson interval of binomial errors. 
//define upper error
double error1 (double n1, double n2)
{
	if (n1 == 0)
	{
		return (0);
	}
	else
	{
	return ( (n2/n1 + 0.5/n1 + sqrt(n2/pow(n1,2)*(1-n2/n1) + 0.25/pow(n1,2)))/(1+1.0/n1) - n2/n1 );
	}
}
//define lower error
double error2 (double n1, double n2)
{
	if (n1 == 0)
	{
		return (0);
	}
	else
	{
		return ( n2/n1 - (n2/n1 + 0.5/n1 - sqrt(n2/pow(n1,2)*(1-n2/n1) + 0.25/pow(n1,2)))/(1+1.0/n1) );
	}
}

int getBin(double x, double boundaries[], int eta_bins) 
{
	int i;
	int n = eta_bins; //sizeof(boundaries)/sizeof(boundaries[0])-1;
//	int n = sizeof(boundaries)/sizeof(boundaries[0])-1; //sizeof(boundaries)/sizeof(boundaries[0])-1;
	if (x<boundaries[0] || x>=boundaries[n]) return -1;
	for(i=0;i<n;i++)
	{
		if (x>=boundaries[i] && x<boundaries[i+1]) return i;
	}
	return 0;
}


bool getJetID(int era, bool isUL, bool isCHS, bool LepVeto, double eta, double cm, double nm, double nemf, double cemf, double nhf, double chf, double muf )
{
	bool tight, extracut_26_27, extracut_27_3, extracut_3_5, lepton_cut, JetID;

	if (isUL)
	{
		if ( isCHS )
		{
			if ( era == 2016 ) 
			{
				tight = ( fabs(eta)<=2.4 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && ( cm + nm)>1   );
				extracut_26_27 = ( fabs(eta)> 2.4 && fabs(eta)<=2.7 && nemf<0.99 && nhf<0.9 );
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nemf>0.0 && nemf < 0.99 && nm> 1 );  
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nhf>0.2 && nm>10 ); 
				lepton_cut =  fabs(eta)>2.4 || ( muf<0.8 && cemf<0.8 && fabs(eta)<=2.4 );

				if (LepVeto) JetID = ( tight || extracut_26_27 || extracut_27_3 || extracut_3_5) && lepton_cut;
				else JetID =  tight || extracut_26_27 || extracut_27_3 || extracut_3_5 ;
			}
			else  
			{
				//if (era != 2018) cout << "\nWARNING! era "<< era <<" is not valid. Will use era 2018. Valid era's are the integers: 2016, 2017, 2018. " << endl;

				tight = ( fabs(eta)<=2.6 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && ( cm + nm)>1   );
				extracut_26_27 = ( fabs(eta)> 2.6 && fabs(eta)<=2.7 && cm>0 && nemf<0.99 && nhf<0.9 );
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nemf>0.01 && nemf < 0.99 && nm> 1 );  
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nhf>0.2 && nm>10 ); 
				lepton_cut =  fabs(eta)>2.7 || ( muf<0.8 && cemf<0.8 && fabs(eta)<=2.7 );

				if (LepVeto) JetID = ( tight || extracut_26_27 || extracut_27_3 || extracut_3_5) && lepton_cut;
				else JetID =  tight || extracut_26_27 || extracut_27_3 || extracut_3_5 ;
			}
		}//end of CHS jets if

		if ( isCHS == false)
		{
			if ( era == 2016) 
			{
				tight = ( fabs(eta)<=2.4 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && ( cm + nm)>1   );
				//tight = ( fabs(eta)<=2.4 && nemf<0.9 && nhf < 0.9 && ( cm + nm)>1   );
				extracut_26_27 = ( fabs(eta)> 2.4 && fabs(eta)<=2.7 && nemf<0.99 && nhf<0.98 );
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nm>1. );  
//				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nhf<0.99999 );  
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nm>2 ); 
				lepton_cut =  fabs(eta)>2.4 || ( muf<0.8 && cemf<0.8 && fabs(eta)<=2.4 );

				if (LepVeto) JetID = ( tight || extracut_26_27 || extracut_27_3 || extracut_3_5) && lepton_cut;
				else JetID =  tight || extracut_26_27 || extracut_27_3 || extracut_3_5 ;
			}
			else 
			{
				if (era != 2018 && era!= 2017 ) cout << "\nWARNING! era "<< era <<" is not valid. Will use era 2018. Valid era's are the integers: 2016, 2017, 2018. " << endl;

				tight = ( fabs(eta)<=2.6 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && ( cm + nm)>1   );
				extracut_26_27 = ( fabs(eta)> 2.6 && fabs(eta)<=2.7 && nemf<0.99 && nhf<0.9 );
//				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nhf<0.9999 );  
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nhf<0.9999 );  
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nm>2 );  

				lepton_cut =  fabs(eta)>2.7 || ( muf<0.8 && cemf<0.8 && fabs(eta)<=2.7 );

				if (LepVeto) JetID = ( tight || extracut_26_27 || extracut_27_3 || extracut_3_5) && lepton_cut ;
				else JetID =  tight || extracut_26_27 || extracut_27_3 || extracut_3_5 ;
			} 
		} //end of Puppi jets if
	} //end of UL if

	else // for non UL, rereco datasets.
	{
		if ( isCHS )
		{
			if ( era == 2016 ) 
			{
				bool tight_24_27, lepton_cut_24_27, lepton_tot;

				tight = ( fabs(eta)<=2.4 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && (cm + nm)>1 && cemf<0.99 );
				tight_24_27 = ( fabs(eta)>2.4 && fabs(eta)<=2.7 && nemf<0.9 && nhf < 0.9 && ( cm + nm )>1 ) ;
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nhf <0.98 && nemf>0.01 && nm>2 );  
				extracut_3_5 =  ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nm > 10 ); 
				lepton_cut =  fabs(eta)>2.7  || ( muf<0.8 && cemf < 0.9 && fabs(eta)<=2.4);
				lepton_cut_24_27 =  fabs(eta)>2.7 || (muf<0.8 && fabs(eta)>2.4 && fabs(eta )<=2.7) ;
				lepton_tot = lepton_cut || lepton_cut_24_27;

				if (LepVeto) JetID = ( tight || tight_24_27 || extracut_27_3 || extracut_3_5 ) && lepton_tot ;
				else JetID = tight || tight_24_27 || extracut_27_3 || extracut_3_5;
			}
			else if( era == 2017 )
			{

				tight = ( fabs(eta)<=2.7 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 &&   (cm + nm)>1   );
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nemf>0.02 && nemf< 0.99 && nm>2	);  
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nhf>0.02 && nm>10 ); 
				lepton_cut =  fabs(eta)>2.7 || (muf<0.8 && cemf<0.8 && fabs(eta)<2.7);

				if (LepVeto) JetID = ( tight ||  extracut_27_3 || extracut_3_5) && lepton_cut ;
				else  JetID =  tight ||  extracut_27_3 || extracut_3_5;
			}
			else  
			{
				if (era != 2018) cout << "\nWARNING! era "<< era <<" is not valid. Will use era 2018. Valid era's are the integers: 2016, 2017, 2018. " << endl;

				tight = ( fabs(eta)<=2.6 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && ( cm + nm)>1   );
				extracut_26_27 = ( fabs(eta)> 2.6 && fabs(eta)<=2.7 && cm>0 && nemf<0.99 && nhf<0.9 );
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nemf>0.02 && nemf < 0.99 && nm> 2 );  
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nhf>0.2 && nm>10 ); 
				lepton_cut =  fabs(eta)>2.7 || ( muf<0.8 && cemf<0.8 && fabs(eta)<=2.7 );

				if (LepVeto) JetID = ( tight || extracut_26_27 || extracut_27_3 || extracut_3_5) && lepton_cut;
				else JetID =  tight || extracut_26_27 || extracut_27_3 || extracut_3_5 ;
			}
		}//end of CHS jets if

		if ( isCHS == false)
		{
			if ( era == 2016) 
			{
				bool tight_24_27, lepton_cut_24_27, lepton_tot;

				tight = ( fabs(eta)<=2.4 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && (cm + nm)>1 && cemf<0.99 );
				tight_24_27 = ( fabs(eta)>2.4 && fabs(eta)<=2.7 && nemf<0.9 && nhf < 0.9 && ( cm + nm )>1 ) ;
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nhf <0.98 && nemf>0.01 && nm>2 );  
				extracut_3_5 =  ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nm > 10 ); 
				lepton_cut =  fabs(eta)>2.7  || ( muf<0.8 && cemf < 0.9 && fabs(eta)<=2.4);
				lepton_cut_24_27 =  fabs(eta)>2.7 || (muf<0.8 && fabs(eta)>2.4 && fabs(eta )<=2.7) ;
				lepton_tot = lepton_cut || lepton_cut_24_27;

				if (LepVeto) JetID = ( tight || tight_24_27 || extracut_27_3 || extracut_3_5 ) && lepton_tot ;
				else JetID = tight || tight_24_27 || extracut_27_3 || extracut_3_5;
			}
			else if( era == 2017 )
			{

				tight = (fabs(eta)<=2.7 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 &&   (cm + nm)>1   );
				extracut_27_3 = (fabs(eta)> 2.7 && fabs(eta)<=3.0 && nhf<0.99);  
				extracut_3_5 = (fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nhf>0.02 && nm>2 && nm<15); 
				lepton_cut =  fabs(eta)>2.7 || (muf<0.8 && cemf<0.8 && fabs(eta)<2.7);

				if (LepVeto) JetID = ( tight ||  extracut_27_3 || extracut_3_5) && lepton_cut ;
				else  JetID =  tight ||  extracut_27_3 || extracut_3_5;
			}
			else 
			{
				if (era != 2018) cout << "\nWARNING! era "<< era <<" is not valid. Will use era 2018. Valid era's are the integers: 2016, 2017, 2018. " << endl;

				tight = ( fabs(eta)<=2.6 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && ( cm + nm)>1   );
				extracut_26_27 = ( fabs(eta)> 2.6 && fabs(eta)<=2.7 && nemf<0.99 && nhf<0.9 );
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nhf< 0.99 );  
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nhf>0.02 && nm>2 && nm<15);  
				lepton_cut =  fabs(eta)>2.7 || ( muf<0.8 && cemf<0.8 && fabs(eta)<=2.7 );

				if (LepVeto) JetID = ( tight || extracut_26_27 || extracut_27_3 || extracut_3_5) && lepton_cut ;
				else JetID =  tight || extracut_26_27 || extracut_27_3 || extracut_3_5 ;
			} 
		} //end of Puppi jets if


	}
return JetID;
}





//function that is given the year era and JetID values for 16, 17, 18 ( doubles), matches the correct era and returns the result as boolian.
bool FindJetIDFromEra ( int flag_era, bool JetID_16, bool JetID_17, bool JetID_18 ) 
{
	bool boolianJetID;

	if ( flag_era == 2016 )
	{
		if (!JetID_16  ) 	 boolianJetID = false;
		else if (JetID_16 ) boolianJetID = true;
	}
	else if ( flag_era == 2017 )
	{
		if (!JetID_17  ) 	 boolianJetID = false;
		else if (JetID_17) boolianJetID = true;
	}
	else if ( flag_era == 2018 )
	{
		if (!JetID_18 )    boolianJetID = false;
		else if (JetID_18) boolianJetID = true;
	}
	else 
	{
		cout<<" ERROR! Year era provided is not valid. Valid eras are: 2016, 2017, 2018. Will use JetID for 2018... " <<  endl;
		if (!JetID_18  ) 	 boolianJetID = false;
		else if (JetID_18 ) boolianJetID = true;
	}
return boolianJetID;
}



double FindTagVariable(int irand, double var_j1,  double var_j2)
{
	double var_tag;
	if ( irand < 0.5 ) var_tag = var_j1;
	else var_tag = var_j2;

	return var_tag;
}

double FindProbeVariable(int irand, double var_j1,  double var_j2)
{
	double var_probe;
	if ( irand < 0.5 ) var_probe = var_j2;
	else var_probe = var_j1;

	return var_probe;
}




bool FindTagJetID (int irand, int flag_era, double JetID_16_j1, double JetID_17_j1, double JetID_18_j1, double JetID_16_j2, double JetID_17_j2, double JetID_18_j2 )
{
	bool JetID_tag;
	if ( irand < 0.5 ) JetID_tag = FindJetIDFromEra(flag_era, JetID_16_j1, JetID_17_j1, JetID_18_j1);
	else JetID_tag = FindJetIDFromEra(flag_era, JetID_16_j2, JetID_17_j2, JetID_18_j2);

	return JetID_tag;
}


bool FindProbeJetID (int irand, int flag_era, double JetID_16_j1, double JetID_17_j1, double JetID_18_j1, double JetID_16_j2, double JetID_17_j2, double JetID_18_j2 )
{
	bool JetID_probe;
	if ( irand < 0.5 ) JetID_probe = FindJetIDFromEra(flag_era, JetID_16_j2, JetID_17_j2, JetID_18_j2);
	else JetID_probe = FindJetIDFromEra(flag_era, JetID_16_j1, JetID_17_j1, JetID_18_j1);

	return JetID_probe;
}




	
