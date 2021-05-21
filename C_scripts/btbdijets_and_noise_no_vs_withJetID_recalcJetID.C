#include "TRandom.h"
#include "TF1.h"
#include "TH1D.h"
#include "TH1F.h"
#include "TH2D.h"
#include "TH2F.h"
#include "TTree.h"
#include "TFile.h"
#include "TDirectory.h"
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
#include "TGraphAsymmErrors.h"
#include "setTDRStyle_teliko.C"
#include "TSystemFile.h" 
#include "TSystemDirectory.h"
#include "TLatex.h"
#include "TSpline.h"
#include <algorithm>
#include <string>
#include <stdarg.h>
#define N_histo_bins 300
//#define eta_bins 8


bool getJetID(int era, bool isUL, bool isCHS, bool LepVeto, double eta, double cm, double nm, double nemf, double cemf, double nhf, double chf, double muf );
bool FindJetIDFromEra(int flag_era, bool JetID_16, bool JetID_17, bool JetID_18 );
int getBin(double x, double boundaries[], int eta_bins) ;


void btbdijets_and_noise_no_vs_withJetID_recalcJetID()
{

//	const char input_directory[300]="root://eoscms//eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/RunC/";  

	TFile *f = TFile::Open("/afs/cern.ch/user/d/dkarasav/public/testing_JetID/UL2016/nonAPV/UL16_RunGH.root","READ");		

	char analyzer_path[300] = "/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/"; 
	char output_directory[300] = "UL_datasets_JetID/UL_2016/CHS/First_try/nonAPVdatasets/btb_vs_noise/";     
	char image_name[300] = "RunsGH"; 

	bool isCHS = true;
	bool isUL = true;
	bool useAbsoluteEta = true;
	bool test_run = false;
	const int eta_bins = 8;
	double pTmaxCut = 50000;
	double pTminCut = 50;
	char legend_1[50] = "Back-to-Back";
	char legend_2[50] = "Minimum Bias";





	char *jet_type;
	if (isCHS) jet_type = "CHS";
	else jet_type = "PUPPI";

	gROOT->LoadMacro("setTDRStyle_teliko.C");
	setTDRStyle_teliko();
	TPaveText *paveCMS = new TPaveText(0.15,0.95,0.5,1.0,"NDC");
	// paveCMS->AddText("CMS Preliminary L=9.2 fb^{-1} #sqrt{s} = 13 TeV");
	paveCMS->AddText("CMS Preliminary #sqrt{s} = 13 TeV");
	paveCMS->SetFillColor(0);
	paveCMS->SetBorderSize(0);
	paveCMS->SetTextSize(0.03);

	//float lumi = 2500.0;
	char name[100]; 
	float etamin=0, etamax=0;
	char filename[256]; 
	int era = 2016; 

	TH1D *h_ETAJet1=new TH1D("h_ETAJet1", "", 100,-5,5);
	TH1D *h_ETAJet1_with=new TH1D("h_ETAJet1_with", "", 100,-5,5);
	TH1D *h_ETA_noise, *h_ETA_noise_with;


	TH1D *h_METovSUMET[eta_bins], *h_CHFJet1[eta_bins], *h_NHFJet1[eta_bins], *h_CEMFJet1[eta_bins], *h_NEMFJet1[eta_bins], *h_MUFJet1[eta_bins], *h_TOTCONSTJet1[eta_bins], *h_CMJet1[eta_bins], *h_NMJet1[eta_bins], *h_ptJet1[eta_bins],*h_PMJet1[eta_bins], *h_PHIJet1[eta_bins];

	TH1D *h_METovSUMET_with[eta_bins], *h_CHFJet1_with[eta_bins], *h_NHFJet1_with[eta_bins], *h_CEMFJet1_with[eta_bins], *h_NEMFJet1_with[eta_bins], *h_MUFJet1_with[eta_bins], *h_TOTCONSTJet1_with[eta_bins], *h_CMJet1_with[eta_bins], *h_NMJet1_with[eta_bins], *h_ptJet1_with[eta_bins],*h_PMJet1_with[eta_bins] , *h_PHIJet1_with[eta_bins];

	TH1D *h_MetSig_noise[eta_bins], *h_CHF_noise[eta_bins], *h_NHF_noise[eta_bins], *h_CEMF_noise[eta_bins], *h_NEMF_noise[eta_bins], *h_MUF_noise[eta_bins], *h_ChM_noise[eta_bins], *h_NeutM_noise[eta_bins], *h_pt_noise[eta_bins],*h_PhM_noise[eta_bins], *h_PHI_noise[eta_bins];

	TH1D *h_MetSig_noise_with[eta_bins], *h_CHF_noise_with[eta_bins], *h_NHF_noise_with[eta_bins], *h_CEMF_noise_with[eta_bins], *h_NEMF_noise_with[eta_bins], *h_MUF_noise_with[eta_bins],*h_ChM_noise_with[eta_bins], *h_NeutM_noise_with[eta_bins], *h_pt_noise_with[eta_bins],*h_PhM_noise_with[eta_bins] ,*h_PHI_noise_with[eta_bins];


	for(Int_t h=0; h<eta_bins;h++)
	{ 
	//========== no JetID ===========
		sprintf(name,"h_METovSUMET%i",h);
		h_METovSUMET[h] = new TH1D(name, "", 50, 0, 1); // 40,0,1.0
		//h_METovSUMET[h]->Sumw2(); 
		sprintf(name,"h_CHFJet1%i",h);
		h_CHFJet1[h] = new TH1D(name, "", 60, 0, 1.2); //40, 0,1.2
		//h_CHFJet1[h]->Sumw2(); 
		sprintf(name,"h_NHFJet1%i",h);
		h_NHFJet1[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_NHFJet1[h]->Sumw2(); 
		sprintf(name,"h_CEMFJet1%i",h);
		h_CEMFJet1[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_CEMFJet1[h]->Sumw2(); 
		sprintf(name,"h_NEMFJet1%i",h);
		h_NEMFJet1[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_NEMFJet1[h]->Sumw2(); 
		sprintf(name,"h_MUFJet1%i",h);
		h_MUFJet1[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_MUFJet1[h]->Sumw2(); 

		sprintf(name,"h_CMJet1%i",h);
		h_CMJet1[h] = new TH1D(name, "", 100, 0, 100);
		
		sprintf(name,"h_PHIJet1%i",h);
		h_PHIJet1[h] = new TH1D(name, "", 40,-4,4);

		// h_CMJet1[h]->Sumw2(); 
		sprintf(name,"h_NMJet1%i",h);
		h_NMJet1[h] = new TH1D(name, "", 100, 0, 100);
		//h_NMJet1[h]->Sumw2(); 
		sprintf(name,"h_PMJet1%i",h);
		h_PMJet1[h] = new TH1D(name, "", 100, 0, 100);
		// h_PMJet1_with[h]->Sumw2();
		sprintf(name,"h_ptJet1%i",h);
		h_ptJet1[h] = new TH1D(name, "", 30,0,3000);
		//h_ptJet1[h]->Sumw2(); 
		 
		//=============== with JetID ===========
		sprintf(name,"h_METovSUMET_with%i",h);
		h_METovSUMET_with[h] = new TH1D(name, "", 50,0,1.0);
		//h_METovSUMET_with[h]->Sumw2();
		sprintf(name,"h_CHFJet1_with%i",h);
		h_CHFJet1_with[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_CHFJet1_with[h]->Sumw2();
		sprintf(name,"h_NHFJet1_with%i",h);
		h_NHFJet1_with[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_NHFJet1_with[h]->Sumw2();
		sprintf(name,"h_CEMFJet1_with%i",h);
		h_CEMFJet1_with[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_CEMFJet1_with[h]->Sumw2();
		sprintf(name,"h_NEMFJet1_with%i",h);
		h_NEMFJet1_with[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_NEMFJet1_with[h]->Sumw2();
		sprintf(name,"h_MUFJet1_with%i",h);
		h_MUFJet1_with[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_MUFJet1_with[h]->Sumw2();

		sprintf(name,"h_PHIJet1_with%i",h);
		h_PHIJet1_with[h] = new TH1D(name, "", 40,-4,4);
		
		sprintf(name,"h_CMJet1_with%i",h);
		h_CMJet1_with[h] = new TH1D(name, "", 100, 0, 100);
		//h_CMJet1_with[h]->Sumw2();
		sprintf(name,"h_NMJet1_with%i",h);
		h_NMJet1_with[h] = new TH1D(name, "", 100, 0, 100);
		sprintf(name,"h_PMJet1_with%i",h);
		h_PMJet1_with[h] = new TH1D(name, "", 100, 0, 100);
		// h_PMJet1_with[h]->Sumw2();
		//h_NMJet1_with[h]->Sumw2();
		sprintf(name,"h_ptJet1_with%i",h);
		h_ptJet1_with[h] = new TH1D(name, "", 30,0,3000);
		//h_ptJet1_with[h]->Sumw2();
	}

	 double passHLT4, passHLT3, passHLT2, passHLT1, passHLT, PassJSON, run, event, lumi, met_ov_sumet, nVtx;  
	double pT_j1, eta_j1, chf_j1, nhf_j1, cemf_j1, nemf_j1, muf_j1, cm_j1, nm_j1, pm_j1, elf_j1, phf_j1, phi_j1;
	double pT_j2, eta_j2, chf_j2, nhf_j2, cemf_j2, nemf_j2, muf_j2, cm_j2, nm_j2, pm_j2, elf_j2, phf_j2, phi_j2;
	double JetID_2016_j1, JetID_2017_j1, JetID_2018_j1, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2;
	bool JetID_j1, JetID_j2;
	double ymax; 
	double yBnd[eta_bins+1]={0.0,0.5,1.0,1.5,2.0,2.4,2.7, 3.0, 5.0}; 


	TChain *tree = new TChain("rootTupleTree/tree");

/*
	Char_t filechain[1024];
	const char *ext="reduced_skim.root" ;

	TSystemDirectory dir(input_directory, input_directory); 
	TList *files = dir.GetListOfFiles(); 
	if (files)
	{ 
		TSystemFile *file; 
		TString fname;
		TIter next(files); 
		while ((file=(TSystemFile*)next()))
		{
			fname = file->GetName(); 
			if (!file->IsDirectory() && fname.EndsWith(ext))
			{ 
				cout << fname.Data() << endl; 
				sprintf(filechain,"%s/%s",input_directory,fname.Data());
				tree->Add(filechain);
			} 
		}
	} 
 */

//==========================================================UL16 ak4CHS================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunBver2/JetHT__Run2016B-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunC/JetHT__Run2016C-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunD/JetHT__Run2016D-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunE/JetHT__Run2016E-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunF/JetHT__Run2016F-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");

	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunF/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunG/JetHT__Run2016G-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunH/JetHT__Run2016H-21Feb2020_UL2016_MINIAOD_reduced_skim.root");


//==========================================================UL16 ak4Puppi================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016Bver2-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016C-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016D-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016E-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016G-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016H-21Feb2020_UL2016_MINIAOD_reduced_skim.root");


//==========================================================UL17 ak4CHS================================================
/*
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunB/JetHT__Run2017B-09Aug2019_UL2017-v1_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunC/JetHT__Run2017C-09Aug2019_UL2017-v1_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunD/JetHT__Run2017D-09Aug2019_UL2017-v1_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunE/JetHT__Run2017E-09Aug2019_UL2017-v1_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunF/JetHT__Run2017F-09Aug2019_UL2017-v1_reduced_skim.root");
*/

//==========================================================UL17 ak4PUPPI================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunB/JetHT__Run2017B-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunC/JetHT__Run2017C-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunD/JetHT__Run2017D-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunE/JetHT__Run2017E-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunF/JetHT__Run2017F-09Aug2019_UL2017-v1_reduced_skim.root");




	tree->SetBranchAddress("passHLT",&passHLT);  //for ak8:    AK8PFHT800 TrimMass50_v12
	tree->SetBranchAddress("passHLT1",&passHLT1);  //for ak8:  AK8PFHT850 TrimMass50_v11
	tree->SetBranchAddress("passHLT2",&passHLT2);  //for ak8:  AK8PFHT900_TrimMass50_v11
	tree->SetBranchAddress("passHLT3",&passHLT3); //for ak8:   AK8PFJet200_v15
	tree->SetBranchAddress("passHLT4",&passHLT4); //for ak8:   AK8PFJet400_v16

	tree->SetBranchAddress("run",&run);
	tree->SetBranchAddress("event",&event);
	tree->SetBranchAddress("lumi",&lumi);
	tree->SetBranchAddress("metSig",&met_ov_sumet);
	tree->SetBranchAddress("nVtx",&nVtx);

//	tree->SetBranchAddress("JetIDlepVeto_2018_j1",&test_JetID);

/*

	tree->SetBranchAddress("JetIDlepVeto_2016_j1",&JetID_2016_j1);
	tree->SetBranchAddress("JetIDlepVeto_2017_j1",&JetID_2017_j1);
	tree->SetBranchAddress("JetIDlepVeto_2018_j1",&JetID_2018_j1);
	tree->SetBranchAddress("JetIDlepVeto_2016_j2",&JetID_2016_j2);
	tree->SetBranchAddress("JetIDlepVeto_2017_j2",&JetID_2017_j2);
	tree->SetBranchAddress("JetIDlepVeto_2018_j2",&JetID_2018_j2);
	
*/
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
	cout<<"Number of entries ="<<nentries<<endl;
 
	int LoopEntries =0;
	if(test_run) LoopEntries = 1000;
	else LoopEntries = nentries;
		
	for (int i=0; i<LoopEntries; i++) //event loop
	{	
		//if(i!=0 && i%1000==0) cout<<i<<endl;
		if(i!=0 && i%1000000==0) cout<<i<<endl;
		tree->GetEntry(i);
		if (pT_j1<0.1)  continue ;
		if ( pT_j1 < pTminCut || pT_j1 > pTmaxCut  ) continue;


		JetID_2016_j1 = getJetID(2016, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );
		JetID_2017_j1 = getJetID(2017, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );
		JetID_2018_j1 = getJetID(2018, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );

		JetID_2016_j2 = getJetID(2016, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );
		JetID_2017_j2 = getJetID(2017, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );
		JetID_2018_j2 = getJetID(2018, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );


		JetID_j1 = FindJetIDFromEra(era, JetID_2016_j1, JetID_2017_j1, JetID_2018_j1);
		JetID_j2 = FindJetIDFromEra(era, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2);


		if (passHLT3==1) h_ETAJet1->Fill(eta_j1);	
		if ( JetID_j1 && JetID_j2 && passHLT3==1 ) h_ETAJet1_with->Fill(eta_j1);
			

		if ( passHLT3 != 1 ) continue; //trigger cut

					//=== eta regions ====
		int ybin;
		if(useAbsoluteEta) ybin = getBin(fabs(eta_j1),yBnd,eta_bins);
		else ybin = getBin(eta_j1,yBnd,eta_bins);
		if (ybin > -1)//fill hist's in the corresponding eta bin
		{ 
			h_ETAJet1->Fill(eta_j1);
			h_CHFJet1[ybin]->Fill(chf_j1); 
			h_NHFJet1[ybin]->Fill(nhf_j1);
			h_CEMFJet1[ybin]->Fill(cemf_j1);
			h_NEMFJet1[ybin]->Fill(nemf_j1);
			h_MUFJet1[ybin]->Fill(muf_j1);
			h_PHIJet1[ybin]->Fill(phi_j1);
			h_CMJet1[ybin]->Fill(cm_j1);
			h_NMJet1[ybin]->Fill(nm_j1);
			h_PMJet1[ybin]->Fill(pm_j1);
			h_ptJet1[ybin]->Fill(pT_j1);
			h_METovSUMET[ybin]->Fill(met_ov_sumet);
		}// end of if ybin>-1

		if (JetID_j1 && JetID_j2 && ybin > -1   ) //fill hist's in the corresponding eta bin for events with passed JetID
		{ 

			h_ETAJet1_with->Fill(eta_j1);
			h_CHFJet1_with[ybin]->Fill(chf_j1);  //cout<<ybin<<"  "<<chf<<"   "<<eta_j1<<"  "<<etaj2<<endl;
			h_NHFJet1_with[ybin]->Fill(nhf_j1);
			h_CEMFJet1_with[ybin]->Fill(cemf_j1);
			h_NEMFJet1_with[ybin]->Fill(nemf_j1);
			h_MUFJet1_with[ybin]->Fill(muf_j1);
			h_CMJet1_with[ybin]->Fill(cm_j1);
			h_NMJet1_with[ybin]->Fill(nm_j1);
			h_PMJet1_with[ybin]->Fill(pm_j1);
			h_ptJet1_with[ybin]->Fill(pT_j1);
			h_PHIJet1_with[ybin]->Fill(phi_j1);
			h_METovSUMET_with[ybin]->Fill(met_ov_sumet);
		}//end of if ybin>-1
	}// end of event loop

	delete tree;



	//=======Minimum Bias Sample =====

	assert(f &&!f->IsZombie());


	TH1D *h_eta_total_noise  ;      
	TH1D *h_eta_total_noise_with;       

	 
	sprintf(name,"h_ETA");
	h_eta_total_noise = (TH1D*)f->Get(name); 

	sprintf(name,"h_ETA_with");
	h_eta_total_noise_with = (TH1D*)f->Get(name); 

	for(int iy=0; iy<eta_bins; iy++)
	{
		sprintf(name,"h_pT_%i",iy);
		h_pt_noise[iy] = (TH1D*)f->Get(name); 

		sprintf(name,"h_pT_with_%i",iy);
		h_pt_noise_with[iy] = (TH1D*)f->Get(name);
		 
		sprintf(name,"h_MetSig_%i",iy);
		h_MetSig_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_MetSig_with_%i",iy);
		h_MetSig_noise_with[iy] = (TH1D*)f->Get(name);
		 
		sprintf(name,"h_CHF_%i",iy);
		h_CHF_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_CHF_with_%i",iy);
		h_CHF_noise_with[iy] = (TH1D*)f->Get(name); 
		 
		sprintf(name,"h_NHF_%i",iy);
		h_NHF_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_NHF_with_%i",iy);
		h_NHF_noise_with[iy] = (TH1D*)f->Get(name); 
		 
		sprintf(name,"h_CEMF_%i",iy);
		h_CEMF_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_CEMF_with_%i",iy);
		h_CEMF_noise_with[iy] = (TH1D*)f->Get(name);
		 
		sprintf(name,"h_NEMF_%i",iy);
		h_NEMF_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_NEMF_with_%i",iy);
		h_NEMF_noise_with[iy] = (TH1D*)f->Get(name);

		sprintf(name,"h_MUF_%i",iy);
		h_MUF_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_MUF_with_%i",iy);
		h_MUF_noise_with[iy] = (TH1D*)f->Get(name);

		sprintf(name,"h_ChM_%i",iy);
		h_ChM_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_ChM_with_%i",iy);
		h_ChM_noise_with[iy] = (TH1D*)f->Get(name); 

		sprintf(name,"h_NeutM_%i",iy);
		h_NeutM_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_NeutM_with_%i",iy);
		h_NeutM_noise_with[iy] = (TH1D*)f->Get(name);

		sprintf(name,"h_PhM_%i",iy);
		h_PhM_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_PhM_with_%i",iy);
		h_PhM_noise_with[iy] = (TH1D*)f->Get(name);

//		sprintf(name,"h_ETA_%i",iy);
//		h_ETA_noise[iy] = (TH1D*)f->Get(name); 
//		sprintf(name,"h_ETA_with_%i",iy);
//		h_ETA_noise_with[iy] = (TH1D*)f->Get(name);

		sprintf(name,"h_PHI_%i",iy);
		h_PHI_noise[iy] = (TH1D*)f->Get(name); 
		sprintf(name,"h_PHI_with_%i",iy);
		h_PHI_noise_with[iy] = (TH1D*)f->Get(name); 
/*
		if (iy==0)  h_eta_total_noise = (TH1D*)(h_ETA_noise[iy]->Clone());
		else h_eta_total_noise->Add(h_ETA_noise[iy]);
		if (iy==0)  h_eta_total_noise_with = (TH1D*)(h_ETA_noise_with[iy]->Clone());
		else h_eta_total_noise_with->Add(h_ETA_noise_with[iy]);
*/

	} // end of ybnd loop


	TCanvas *pad1 = new TCanvas("pad1", "",1);
	pad1->Divide(3,3);
	TCanvas *pad2 = new TCanvas("pad2", "",1);
	pad2->Divide(3,3);
	TCanvas *pad3 = new TCanvas("pad3", "",1);
	pad3->Divide(3,3);
	TCanvas *pad4 = new TCanvas("pad4", "",1);
	pad4->Divide(3,3);
	TCanvas *pad5 = new TCanvas("pad5", "",1);
	pad5->Divide(3,3);
	TCanvas *pad9 = new TCanvas("pad9", "",1);
	pad9->Divide(3,3);
	TCanvas *pad10= new TCanvas("pad10", "",1);
	pad10->Divide(3,3);
	TCanvas *pad11= new TCanvas("pad11", "",1);
	pad11 ->Divide(3,3);
	TCanvas *pad12= new TCanvas("pad12", "",1);
	pad12 ->Divide(3,3);
	TCanvas *pad13= new TCanvas("pad13", "",1);
	pad13 ->Divide(3,3);

	TCanvas *pad14= new TCanvas("pad14", "",1);
	//TCanvas *pad15= new TCanvas("pad15", "",1);
	//pad15 ->Divide(3,3);
	TCanvas *pad16= new TCanvas("pad16", "",1);
	pad16 ->Divide(3,3);
	//TCanvas *pad17= new TCanvas("pad17", "",1);
	//pad17 ->Divide(3,3); 
	

	TLegend *leg1 =new TLegend(.2, .6, .9, .9);//7899//4899
	leg1->SetTextSize(0.06);
	leg1->SetFillColor(0); 
	leg1->SetBorderSize(0);
	leg1->SetHeader(jet_type); 
	leg1->AddEntry(h_CHFJet1[0], "Back-to-back", "L");
	leg1->AddEntry(h_CHFJet1_with[0], "Back-to-back JetID", "L");
	leg1->AddEntry(h_CHF_noise[0], "MinBias", "L");
	leg1->AddEntry(h_CHF_noise_with[0], "MinBias JetID", "L");

	for(int iy=0; iy<eta_bins; iy++)
	{
 
		etamin = yBnd[iy];
		etamax = yBnd[iy+1];
		const char *seta = (etamin==0 ? Form("|y| < %1.2g",etamax) :
		Form("%1.2g #leq |y| < %1.2g",etamin,etamax));
		TLatex *teta = new TLatex(0.68,0.96,seta); cout<<seta<<endl;
		teta->SetNDC();
		teta->SetTextSize(0.05);

		pad1->cd(iy+1);
		pad1->cd(iy+1)->SetLogy(1);
		h_CHFJet1[iy]->GetXaxis()->SetTitle("Charged Hadron Fraction");
		h_CHFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CHFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_CHFJet1_with[iy]->SetLineColor(4);

		h_CHF_noise[iy]->SetLineColor(2);
		h_CHF_noise_with[iy]->SetLineColor(6);
		h_CHF_noise[iy]->SetLineWidth(2);
		h_CHF_noise_with[iy]->SetLineWidth(2);
		h_CHFJet1[iy]->SetLineStyle(1);
		h_CHF_noise[iy]->SetLineStyle(1);
		h_CHFJet1[iy]->SetMinimum(0.1);
		h_CHFJet1[iy]->SetMaximum(1000000000);
		h_CHFJet1[iy]->Draw("");

		//h_CHF_noise[iy]->Scale( h_CHFJet1[iy]->Integral() /h_CHF_noise[iy]->Integral() );
		//h_CHF_noise_with[iy]->Scale( h_CHFJet1[iy]->Integral() /h_CHF_noise_with[iy]->Integral() );
		h_CHFJet1_with[iy]->Draw("same hist");
		h_CHF_noise[iy]->Draw("same hist");
		h_CHF_noise_with[iy]->Draw("same hist");

		paveCMS ->Draw("same");
		teta->Draw();

		//leg1->Draw();

		pad2->cd(iy+1);
		pad2->cd(iy+1)->SetLogy(1);
		h_NHFJet1[iy]->GetXaxis()->SetTitle("Neutral Hadron Fraction");
		h_NHFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NHFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_NHFJet1[iy]->SetLineColor(1);
		h_NHFJet1_with[iy]->SetLineColor(4);
		// h_NHF_noise[iy]->Scale( h_NHFJet1[iy]->Integral() /h_NHF_noise[iy]->Integral() );
		//h_NHF_noise_with[iy]->Scale( h_NHFJet1[iy]->Integral() /h_NHF_noise_with[iy]->Integral() );
		h_NHF_noise[iy]->SetLineColor(2);
		h_NHF_noise_with[iy]->SetLineColor(6);
		h_NHF_noise[iy]->SetLineWidth(2);
		h_NHF_noise_with[iy]->SetLineWidth(2);
		h_NHFJet1[iy]->SetLineStyle(1);
		h_NHF_noise[iy]->SetLineStyle(1);
		if(iy>4)h_NHFJet1[iy]->SetMinimum(0.1);
		h_NHFJet1[iy]->SetMaximum(1000000000);
		h_NHFJet1[iy]->Draw();
		h_NHFJet1_with[iy]->Draw("same hist");
		h_NHF_noise[iy]->Draw("same hist");
		h_NHF_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		 //leg1->Draw(); 

		pad3->cd(iy+1);
		pad3->cd(iy+1)->SetLogy(1);
		h_CEMFJet1[iy]->GetXaxis()->SetTitle("Charged Electromagnetic Fraction");
		h_CEMFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CEMFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_CEMFJet1[iy]->SetLineColor(1);
		h_CEMFJet1_with[iy]->SetLineColor(4);
		// h_CEMF_noise[iy]->Scale( h_CEMFJet1[iy]->Integral() /h_CEMF_noise[iy]->Integral() );
		// h_CEMF_noise_with[iy]->Scale( h_CEMFJet1[iy]->Integral() /h_CEMF_noise_with[iy]->Integral() );
		h_CEMF_noise[iy]->SetLineColor(2);
		h_CEMF_noise_with[iy]->SetLineColor(6);
		h_CEMF_noise[iy]->SetLineWidth(2);
		h_CEMF_noise_with[iy]->SetLineWidth(2);
		h_CEMFJet1[iy]->SetLineStyle(1);
		h_CEMF_noise[iy]->SetLineStyle(1);
		h_CEMFJet1[iy]->SetMinimum(0.1);
		h_CEMFJet1[iy]->SetMaximum(100000000);
		h_CEMFJet1[iy]->Draw();
		h_CEMFJet1_with[iy]->Draw("same hist");
		h_CEMF_noise[iy]->Draw("same hist");
		h_CEMF_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1->Draw();

		pad4->cd(iy+1);
		pad4->cd(iy+1)->SetLogy(1);
		h_NEMFJet1[iy]->GetXaxis()->SetTitle("Neutral Electromagnetic Fraction");
		h_NEMFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NEMFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_NEMFJet1[iy]->SetLineColor(1);
		h_NEMFJet1_with[iy]->SetLineColor(4);
		// h_NEMF_noise[iy]->Scale( h_NEMFJet1[iy]->Integral() /h_NEMF_noise[iy]->Integral() );
		// h_NEMF_noise_with[iy]->Scale( h_NEMFJet1[iy]->Integral() /h_NEMF_noise_with[iy]->Integral() );
		h_NEMF_noise[iy]->SetLineColor(2);
		h_NEMF_noise_with[iy]->SetLineColor(6);
		h_NEMF_noise[iy]->SetLineWidth(2);
		h_NEMF_noise_with[iy]->SetLineWidth(2);
		h_NEMFJet1[iy]->SetLineStyle(1);
		h_NEMF_noise[iy]->SetLineStyle(1);
		h_NEMFJet1[iy]->SetMinimum(0.1);
		h_NEMFJet1[iy]->SetMaximum(1000000000.);
		h_NEMFJet1[iy]->Draw();
		h_NEMFJet1_with[iy]->Draw("same hist");
		h_NEMF_noise[iy]->Draw("same hist");
		h_NEMF_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1->Draw();
		pad5->cd(iy+1);
		pad5->cd(iy+1)->SetLogy(1);
		h_MUFJet1[iy]->GetXaxis()->SetTitle("Muon Fraction");
		h_MUFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_MUFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_MUFJet1[iy]->SetLineColor(1);
		h_MUFJet1_with[iy]->SetLineColor(4);
		// h_MUF_noise[iy]->Scale( h_MUFJet1[iy]->Integral() /h_MUF_noise[iy]->Integral() );
		// h_MUF_noise_with[iy]->Scale( h_MUFJet1[iy]->Integral() /h_MUF_noise_with[iy]->Integral() );
		h_MUF_noise[iy]->SetLineColor(2);
		h_MUF_noise_with[iy]->SetLineColor(6);
		h_MUF_noise[iy]->SetLineWidth(2);
		h_MUF_noise_with[iy]->SetLineWidth(2); 
		h_MUFJet1[iy]->SetLineStyle(1);
		h_MUF_noise[iy]->SetLineStyle(1);
		h_MUFJet1[iy]->SetMaximum(100000000);
		if(iy>4)h_MUFJet1[iy]->SetMinimum(10);
		h_MUFJet1[iy]->Draw();
		h_MUFJet1_with[iy]->Draw("same hist");
		h_MUF_noise[iy]->Draw("same hist");
		h_MUF_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		TLegend *leg1a =new TLegend(.4, .6, .9, .9);//7899//4899
		leg1a->SetTextSize(0.06);
		leg1a->SetFillColor(0); 
		leg1a->SetBorderSize(0);
		//leg1a->SetHeader("ReReco");
		leg1a->AddEntry(h_CHFJet1[0], "Back-to-back", "L");
		//leg1a->AddEntry(h_CHFJet1_with[0], "Back-to-back JetID", "L");
		leg1a->AddEntry(h_CHF_noise[0], "MinBias", "L");
		//leg1a->AddEntry(h_CHF_noise_with[0], "MinBias JetID", "L");
		//leg1a->Draw();

		pad10->cd(iy+1);
		pad10->cd(iy+1)->SetLogy(1);
		h_METovSUMET[iy]->GetXaxis()->SetTitle("MET/SumET") ;
		h_METovSUMET[iy]->GetYaxis()->SetTitle("Entries");
		h_METovSUMET[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_METovSUMET[iy]->SetLineColor(1);
		h_METovSUMET_with[iy]->SetLineColor(4);
		//h_MetSig_noise[iy]->Scale( h_METovSUMET[iy]->Integral() /h_MetSig_noise[iy]->Integral() );
		// h_MetSig_noise_with[iy]->Scale( h_METovSUMET[iy]->Integral() /h_MetSig_noise_with[iy]->Integral() );
		h_MetSig_noise[iy]->SetLineColor(2);
		h_MetSig_noise_with[iy]->SetLineColor(6);
		h_MetSig_noise[iy]->SetLineWidth(2);
		h_MetSig_noise_with[iy]->SetLineWidth(2); 
		h_METovSUMET[iy]->SetLineStyle(1);
		h_MetSig_noise[iy]->SetLineStyle(1);
		h_METovSUMET[iy]->SetMaximum(100000000);
		h_METovSUMET[iy]->SetMinimum(0.1);
		h_METovSUMET[iy]->Draw();
		h_METovSUMET_with[iy]->Draw("same hist");
		h_MetSig_noise[iy]->Draw("same hist");
		h_MetSig_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1->Draw();

		pad11->cd(iy+1);
		pad11->cd(iy+1)->SetLogy(1);
		h_NMJet1[iy]->GetXaxis()->SetTitle("Neutral Multiplicity") ;
		h_NMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_NMJet1[iy]->SetLineColor(1);
		h_NMJet1_with[iy]->SetLineColor(4);
		//h_NeutM_noise[iy]->Scale( h_NMJet1[iy]->Integral() /h_NeutM_noise[iy]->Integral() );
		//h_NeutM_noise_with[iy]->Scale( h_NMJet1[iy]->Integral() /h_NeutM_noise_with[iy]->Integral() );
		h_NeutM_noise[iy]->SetLineColor(2);
		h_NeutM_noise_with[iy]->SetLineColor(6);
		h_NeutM_noise[iy]->SetLineWidth(2);
		h_NeutM_noise_with[iy]->SetLineWidth(2);
		h_NMJet1[iy]->SetLineStyle(1);
		h_NeutM_noise[iy]->SetLineStyle(1); 
		h_NMJet1[iy]->SetMinimum(0.1);
		h_NMJet1[iy]->SetMaximum(100000000.);
		if (iy==6) h_NMJet1[iy]->GetXaxis()->SetRangeUser(0., 40.);
		h_NMJet1[iy]->Draw("hist");
		h_NMJet1_with[iy]->Draw("same hist");
		h_NeutM_noise[iy]->Draw("same hist");
		h_NeutM_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1a->Draw();

		pad12->cd(iy+1);
		pad12->cd(iy+1)->SetLogy(1);
		h_CMJet1[iy]->GetXaxis()->SetTitle("Charged Multiplicity") ;
		h_CMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_CMJet1[iy]->SetLineColor(1);
		h_CMJet1_with[iy]->SetLineColor(4);
		//h_ChM_noise[iy]->Scale( h_CMJet1[iy]->Integral() /h_ChM_noise[iy]->Integral() );
		//h_ChM_noise_with[iy]->Scale( h_CMJet1[iy]->Integral() /h_ChM_noise_with[iy]->Integral() );
		h_ChM_noise[iy]->SetLineColor(2);
		h_ChM_noise_with[iy]->SetLineColor(6);
		h_ChM_noise[iy]->SetLineWidth(2);
		h_ChM_noise_with[iy]->SetLineWidth(2);
		h_CMJet1[iy]->SetLineStyle(1);
		h_ChM_noise[iy]->SetLineStyle(1); 
		h_CMJet1[iy]->SetMinimum(0.1);
		if (iy<5) h_CMJet1[iy]->SetMaximum(100000.);
		if (iy>4) h_CMJet1[iy]->SetMaximum(100000000.);
		h_CMJet1[iy]->Draw();
		h_CMJet1_with[iy]->Draw("same hist");
		h_ChM_noise[iy]->Draw("same hist");
		h_ChM_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1a->Draw();

		pad13->cd(iy+1);
		pad13->cd(iy+1)->SetLogy(1);
		h_PMJet1[iy]->GetXaxis()->SetTitle("Photon Multiplicity") ;
		h_PMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_PMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_PMJet1[iy]->SetLineColor(1);
		h_PMJet1_with[iy]->SetLineColor(4);
		//h_PhM_noise[iy]->Scale( h_PMJet1[iy]->Integral() /h_PhM_noise[iy]->Integral() );
		//h_PhM_noise_with[iy]->Scale( h_PMJet1[iy]->Integral() /h_PhM_noise_with[iy]->Integral() );
		h_PhM_noise[iy]->SetLineColor(2);
		h_PhM_noise_with[iy]->SetLineColor(6);
		h_PhM_noise[iy]->SetLineWidth(2);
		h_PhM_noise_with[iy]->SetLineWidth(2);
		h_PMJet1[iy]->SetLineStyle(1);
		h_PhM_noise[iy]->SetLineStyle(1); 
		h_PMJet1[iy]->SetMinimum(0.1);
		h_PMJet1[iy]->SetMaximum(100000000.);
		h_PMJet1[iy]->Draw();
		h_PMJet1_with[iy]->Draw("same hist");
		h_PhM_noise[iy]->Draw("same hist");
		h_PhM_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1a->Draw();

		/* 
		 pad15->cd(iy+1);
		 pad15->cd(iy+1)->SetLogy(1);
		 h_DijetMassAK4[iy]->GetXaxis()->SetTitle("Dijet Mass (GeV)") ;
		 h_DijetMassAK4[iy]->GetYaxis()->SetTitle("Entries");
		 h_DijetMassAK4[iy]->GetYaxis()->SetTitleOffset(1.3);
		 h_DijetMassAK4[iy]->SetLineColor(1);
		 h_DijetMassAK4_with[iy]->SetLineColor(4);
		 h_DijetMassAK4[iy]->SetLineStyle(1);
		 h_DijetMassAK4[iy]->GetXaxis()->SetLabelSize(0.035);
		 h_DijetMassAK4_with[iy]->GetXaxis()->SetLabelSize(0.035);
		 if(iy<5)h_DijetMassAK4[iy]->SetMaximum(10000000);
		 if(iy==5)h_DijetMassAK4[iy]->SetMaximum(2000);
		 if(iy==6)h_DijetMassAK4[iy]->SetMaximum(30); 
		 h_DijetMassAK4[iy]->Draw();
		 h_DijetMassAK4_with[iy]->Draw("same hist");
		 paveCMS ->Draw("same");
		 teta->Draw();
		 TLegend *leg2 =new TLegend(.2, .8, .9, .9);//7899//4899
		 leg2->SetTextSize(0.06);
		 leg2->SetFillColor(0); 
		 leg2->SetBorderSize(0); 
		 leg2->AddEntry(h_DijetMassAK4[0], "Back-to-back", "L");
		 leg2->AddEntry(h_DijetMassAK4_with[0], "Back-to-back JetID", "L");
		 leg2->Draw();
*/
		pad16->cd(iy+1);
		pad16->cd(iy+1)->SetLogy(1);
		h_PHIJet1[iy]->GetXaxis()->SetTitle("#phi") ;
		h_PHIJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_PHIJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_PHIJet1[iy]->SetLineColor(1);
		h_PHIJet1_with[iy]->SetLineColor(4);
		h_PHI_noise[iy]->SetLineColor(2);
		h_PHI_noise_with[iy]->SetLineColor(6);
		h_PHI_noise[iy]->SetLineWidth(2);
		h_PHI_noise_with[iy]->SetLineWidth(2);
		h_PHIJet1[iy]->SetLineStyle(1);
		h_PHI_noise[iy]->SetLineStyle(1); 
		h_PHIJet1[iy]->SetMinimum(0.5); 
		h_PHIJet1[iy]->SetMaximum(1000000.);
		h_PHIJet1[iy]->Draw();
		h_PHIJet1_with[iy]->Draw("same hist");
		h_PHI_noise[iy]->Draw("same hist");
		h_PHI_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1->Draw();
/*
		pad17->cd(iy+1);
		pad17->cd(iy+1)->SetLogy(1);
		h_ETAJet1[iy]->GetXaxis()->SetTitle("#eta") ;
		h_ETAJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_ETAJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_ETAJet1[iy]->SetLineColor(1);
		h_ETAJet1_with[iy]->SetLineColor(4);
		h_ETA_noise[iy]->SetLineColor(2);
		h_ETA_noise_with[iy]->SetLineColor(6);
		h_ETA_noise[iy]->SetLineWidth(2);
		h_ETA_noise_with[iy]->SetLineWidth(2);
		h_ETAJet1[iy]->SetLineStyle(1);
		h_ETA_noise[iy]->SetLineStyle(1); 
		h_ETAJet1[iy]->SetMinimum(0.5); 
		h_ETAJet1[iy]->SetMaximum(100000000.);
		h_ETAJet1[iy]->Draw();
		h_ETAJet1_with[iy]->Draw("same hist");
		h_ETA_noise[iy]->Draw("same hist");
		h_ETA_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1->Draw();
		*/
		pad9->cd(iy+1);
		pad9->cd(iy+1)->SetLogy(1);
		h_ptJet1[iy]->GetXaxis()->SetTitle("pT of Jet1 (GeV)");
		h_ptJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_ptJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_ptJet1[iy]->SetLineColor(1);
		h_ptJet1_with[iy]->SetLineColor(4);
		//h_pt_noise[iy]->Scale( h_ptJet1[iy]->Integral() /h_pt_noise[iy]->Integral() );
		//h_pt_noise_with[iy]->Scale( h_ptJet1[iy]->Integral() /h_pt_noise_with[iy]->Integral() );
		h_pt_noise[iy]->SetLineColor(2);
		h_pt_noise_with[iy]->SetLineColor(6);
		h_pt_noise[iy]->SetLineWidth(2);
		h_pt_noise_with[iy]->SetLineWidth(2);
		h_ptJet1[iy]->SetLineStyle(1);
		h_pt_noise[iy]->SetLineStyle(1); 
		h_ptJet1[iy]->SetMinimum(0.1); 
		h_ptJet1[iy]->SetMaximum(50000000);
		h_ptJet1[iy]->Draw();
		h_ptJet1_with[iy]->Draw("same hist");
		h_pt_noise[iy]->Draw("same hist");
		h_pt_noise_with[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1->Draw();
	} //end of eta regions

	pad1->cd(eta_bins+1);
	leg1->Draw();
	pad2->cd(eta_bins+1);
	leg1->Draw();
	pad3->cd(eta_bins+1);
	leg1->Draw();
	pad4->cd(eta_bins+1);
	leg1->Draw();
	pad5->cd(eta_bins+1);
	leg1->Draw();
	pad9->cd(eta_bins+1);
	leg1->Draw();
	pad10->cd(eta_bins+1);
	leg1->Draw();
	pad11->cd(eta_bins+1);
	leg1->Draw();
	pad12->cd(eta_bins+1);
	leg1->Draw();
	pad13->cd(eta_bins+1);
	leg1->Draw();
	pad16->cd(eta_bins+1);
	leg1->Draw();

	pad14->cd()->SetLogy(1);
	h_ETAJet1->GetXaxis()->SetTitle("#eta") ;
	h_ETAJet1->GetYaxis()->SetTitle("Entries");
	h_ETAJet1->GetYaxis()->SetRangeUser(0.5,1000000000);
	h_ETAJet1->GetYaxis()->SetTitleOffset(1.3);
	h_ETAJet1->SetLineWidth(2);
	h_ETAJet1->SetLineColor(1);
	h_ETAJet1->SetMarkerSize(0.04);
	h_ETAJet1_with->SetLineWidth(2);
	h_ETAJet1_with->SetLineColor(4);
	h_ETAJet1_with->SetMarkerSize(0.04);
//	h_ETAJet1->Scale(h_ETAJet1_with->Integral()/h_ETAJet1->Integral());
	h_ETAJet1->GetYaxis()->SetRangeUser(0.5,1000000000);
	h_eta_total_noise->SetLineColor(2);
	h_eta_total_noise_with->SetLineColor(6);
	h_eta_total_noise->SetLineWidth(2);
	h_eta_total_noise_with->SetLineWidth(2);
	h_eta_total_noise->SetLineStyle(1); 
	h_ETAJet1->Draw("hist");
	h_ETAJet1_with->Draw("same");
	h_eta_total_noise->Draw("same");
	h_eta_total_noise_with->Draw("same");
	paveCMS ->Draw("same");

	TLegend *leg2 =new TLegend(.2, .75, .4, .9);//7899//4899
	leg2->SetTextSize(0.025);
	leg2->SetFillColor(0); 
	leg2->SetBorderSize(0);
	leg2->SetHeader(jet_type); 

	leg2->AddEntry(h_ETAJet1, "Back-to-back", "L");
	leg2->AddEntry(h_ETAJet1_with, "Back-to-back JetID", "L");
	leg2->AddEntry(h_eta_total_noise, "MinBias", "L");
	leg2->AddEntry(h_eta_total_noise_with, "MinBias JetID", "L");
	leg2->Draw("same");





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
	sprintf(filename,"%s/%s/%s_eta.png",analyzer_path,output_directory,image_name);
	pad14->SaveAs(filename);
	//sprintf(filename,"%s/%s/%s_%s_DijetMass.png",analyzer_path,output_directory,image_name,c);
	//pad15->SaveAs(filename);
	sprintf(filename,"%s/%s/%s_phi.png",analyzer_path,output_directory,image_name);
	pad16->SaveAs(filename);
	//sprintf(filename,"%s/%s/%s_%s_eta.png",analyzer_path,output_directory,image_name,c);
	//pad17->SaveAs(filename);
	//sprintf(filename,"%s/%s/%s_%s_%s_eta_phi.png",analyzer_path,output_directory,image_name,legend_1,c);
	//eta_phi_canvas->SaveAs(filename);
	//sprintf(filename,"%s/%s/%s_%s_%s_eta_phi.png",analyzer_path,output_directory,image_name,legend_2,c);
	//eta_phi_canvas_with->SaveAs(filename);

	

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


bool FindJetIDFromEra ( int flag_era, bool JetID_16, bool JetID_17, bool JetID_18 ) 
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
				extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nm>=1 );  
				//extracut_27_3 = ( fabs(eta)> 2.7 && fabs(eta)<=3.0 && nhf<0.9999 );  
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nm>1 ); 
				lepton_cut =  fabs(eta)>2.4 || ( muf<0.8 && cemf<0.8 && fabs(eta)<=2.4 );

				if (LepVeto) JetID = ( tight || extracut_26_27 || extracut_27_3 || extracut_3_5) && lepton_cut;
				else JetID =  tight || extracut_26_27 || extracut_27_3 || extracut_3_5 ;
			}
			else 
			{
				if (era != 2018 && era!= 2017 ) cout << "\nWARNING! era "<< era <<" is not valid. Will use era 2018. Valid era's are the integers: 2016, 2017, 2018. " << endl;

				tight = ( fabs(eta)<=2.6 && cm>0 && nemf<0.9 && chf>0 && nhf < 0.9 && ( cm + nm)>1   );
				extracut_26_27 = ( fabs(eta)> 2.6 && fabs(eta)<=2.7 && nemf<0.99 && nhf<0.9 );
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


	} // end of if for UL datasets.

return JetID;
}
