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

int getBin(double x, double boundaries[], int eta_bins) ;

bool FindJetIDFromEra ( int flag_era, double JetID_16, double JetID_17, double JetID_18 ) ;

void btbdijets_data_vs_MC()
{

	char analyzer_path[300] = "/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/"; 
	char output_directory[300] = "UL_datasets_JetID/UL_2016/PUPPI/v15/nonAPV/data_vs_MC/";     
	char image_name[300] = "data_vs_MC"; 

	char input_directory[500];	

	const int eta_bins = 8;
	// full name to MC reduced.root would be: /eos/cms/store/group/phys_jetmet/dimitris/QCD_UL16APV_btb_PUPPI_reduced/Pt_30to50_QCD_TuneCP5_13TeV_pythia8_UL16_btb_reduced_skim.root
	char MC_path_start[300] = "/eos/cms/store/group/phys_jetmet/dimitris/QCD_UL16nonAPV_btb_PUPPIv15_reduced/Pt_";
	char MC_path_end[300]   = "_QCD_TuneCP5_13TeV_pythia8_UL16_btb_reduced_skim.root";


	bool Save_plots_and_histos = true;
	bool test_run=false;
//	double yBnd[eta_bins+1]={2.8,3.4}; 

	char legend_1[300] = "Back-to-Back";

	char *jet_kind = "AK4 PUPPI"; //"PUPPI"
	double lumin = 35900;
	double pTmin=30;
	double pTmax=30000;
	gROOT->LoadMacro("setTDRStyle_teliko.C");
	setTDRStyle_teliko();
	TPaveText *paveCMS = new TPaveText(0.45,0.95,0.5,1.0,"NDC");
	// paveCMS->AddText("CMS Preliminary L=9.2 fb^{-1} #sqrt{s} = 13 TeV");
	paveCMS->AddText("CMS Preliminary  #sqrt{s} = 13 TeV");
	paveCMS->SetFillColor(0);
	paveCMS->SetBorderSize(0);
	paveCMS->SetTextSize(0.04);

	double yBnd[eta_bins+1]={0.0,0.5,1.0,1.5,2.0,2.4,2.7, 3.0, 5.0}; 
//	double yBnd[eta_bins+1]={0.0,0.5,1.0,1.5,2.0,2.6,2.7, 3.0, 5.0}; 



	//float lumi = 2500.0;
	char name[100]; 
	float etamin=0, etamax=0;
	char filename[256]; 

	TH1D *h_METovSUMET[eta_bins], *h_CHFJet1[eta_bins], *h_NHFJet1[eta_bins], *h_CEMFJet1[eta_bins], *h_NEMFJet1[eta_bins], *h_MUFJet1[eta_bins], *h_TOTCONSTJet1[eta_bins], *h_CMJet1[eta_bins], *h_NMJet1[eta_bins], *h_ptJet1[eta_bins],*h_PMJet1[eta_bins],*h_DijetMassAK4[eta_bins], *h_PHIJet1[eta_bins], *h_nVtx[eta_bins];



	TH1D *h_METovSUMET_MC[eta_bins], *h_CHFJet1_MC[eta_bins], *h_NHFJet1_MC[eta_bins], *h_CEMFJet1_MC[eta_bins], *h_NEMFJet1_MC[eta_bins], *h_MUFJet1_MC[eta_bins], *h_TOTCONSTJet1_MC[eta_bins], *h_CMJet1_MC[eta_bins], *h_NMJet1_MC[eta_bins], *h_ptJet1_MC[eta_bins],*h_PMJet1_MC[eta_bins] , *h_DijetMassAK4_MC[eta_bins], *h_PHIJet1_MC[eta_bins],*h_nVtx_MC[eta_bins];

	TH1D *h_ETAJet1=new TH1D("h_ETAJet1", "", 100,-5,5);
	TH1D *h_ETAJet1_MC=new TH1D("h_ETAJet1_MC", "", 100,-5,5);




	for(Int_t h=0; h<eta_bins;h++)
	{ 
	//========== Data histos ===========
		sprintf(name,"h_METovSUMET%i",h);
		h_METovSUMET[h] = new TH1D(name, "", 50, 0, 1); // 40,0,1.0
		//h_METovSUMET[h]->Sumw2(); 
		sprintf(name,"h_DijetMassAK4%i",h);
		h_DijetMassAK4[h] = new TH1D(name,"",100,0,7500);

		sprintf(name,"h_nVtx%i",h);
		h_nVtx[h] = new TH1D(name, "", 25, 0,100);

		//===============Jet 1 histos======================
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
		h_CMJet1[h] = new TH1D(name, "", 80,0,80);
		
		sprintf(name,"h_PHIJet1%i",h);
		h_PHIJet1[h] = new TH1D(name, "", 40,-4,4);
		
		// h_CMJet1[h]->Sumw2(); 
		sprintf(name,"h_NMJet1%i",h);
		h_NMJet1[h] = new TH1D(name, "", 80,-0.5,79.5);
		//h_NMJet1[h]->Sumw2(); 
		sprintf(name,"h_PMJet1%i",h);
		h_PMJet1[h] = new TH1D(name, "", 80,0,80);
		// h_PMJet1_MC[h]->Sumw2();
		sprintf(name,"h_ptJet1%i",h);
		//h_ptJet1[h] = new TH1D(name, "", 30,0,3000);
		h_ptJet1[h] = new TH1D(name, "", 60,0,2000);
		//h_ptJet1[h]->Sumw2(); 
		
		//h_CHFJet1[h]->Sumw2(); 
		


		 
		//=============== MC histos ===========
		sprintf(name,"h_METovSUMET_MC%i",h);
		h_METovSUMET_MC[h] = new TH1D(name, "", 50,0,1.0);
		sprintf(name,"h_DijetMassAK4_MC%i",h);
		h_DijetMassAK4_MC[h] = new TH1D(name,"",100,0,7500);
		sprintf(name,"h_nVtx_MC%i",h);
		h_nVtx_MC[h] = new TH1D(name, "", 25, 0,100);
		
	

				//===============MC Jet 1 histos======================
		//h_METovSUMET_MC[h]->Sumw2();
		sprintf(name,"h_CHFJet1_MC%i",h);
		h_CHFJet1_MC[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_CHFJet1_MC[h]->Sumw2();
		sprintf(name,"h_NHFJet1_MC%i",h);
		h_NHFJet1_MC[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_NHFJet1_MC[h]->Sumw2();
		sprintf(name,"h_CEMFJet1_MC%i",h);
		h_CEMFJet1_MC[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_CEMFJet1_MC[h]->Sumw2();
		sprintf(name,"h_NEMFJet1_MC%i",h);
		h_NEMFJet1_MC[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_NEMFJet1_MC[h]->Sumw2();
		sprintf(name,"h_MUFJet1_MC%i",h);
		h_MUFJet1_MC[h] = new TH1D(name, "", 60, 0, 1.2);
		//h_MUFJet1_MC[h]->Sumw2();

		sprintf(name,"h_PHIJet1_MC%i",h);
		h_PHIJet1_MC[h] = new TH1D(name, "", 40,-4,4);

		
		sprintf(name,"h_CMJet1_MC%i",h);
		h_CMJet1_MC[h] = new TH1D(name, "", 80,0,80);
		//h_CMJet1_MC[h]->Sumw2();
		sprintf(name,"h_NMJet1_MC%i",h);
		h_NMJet1_MC[h] = new TH1D(name, "", 80,-0.5,79.5);
		sprintf(name,"h_PMJet1_MC%i",h);
		h_PMJet1_MC[h] = new TH1D(name, "", 100, 0, 100);
		// h_PMJet1_MC[h]->Sumw2();
		//h_NMJet1_MC[h]->Sumw2();
		sprintf(name,"h_ptJet1_MC%i",h);
		h_ptJet1_MC[h] = new TH1D(name, "", 60,0,2000);
		//h_ptJet1_MC[h] = new TH1D(name, "", 30,0,3000);
		//h_ptJet1_MC[h]->Sumw2();

		
	}

	double passHLT, passHLT1, passHLT2, passHLT3, passHLT4, PassJSON, run, lumi, event;
	double chf, nhf, cemf, nemf, muf, cm, nm, pm,eta_j1, eta_j2, pT_j1,met_ov_sumet,elf,phf,DijetMassAK4, nVtx ,phi_j1,phi_j2,pT_j2;
	double chf_j2, nhf_j2, cemf_j2, nemf_j2, muf_j2, cm_j2, nm_j2, pm_j2,elf_j2,phf_j2 ;
	double JetID_2016_j1, JetID_2017_j1, JetID_2018_j1, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2;
	double ymax; 


	
	TChain *tree = new TChain("rootTupleTree/tree");
/*
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/JetHT__Run2018A-12Nov2019_UL2018-v2__MINIAOD_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/JetHT__Run2018B-12Nov2019_UL2018-v2__MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/JetHT__Run2018C-12Nov2019_UL2018-v4__MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/JetHT__Run2018D-12Nov2019_UL2018-v4__MINIAOD_reduced_skim.root");
*/
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunBver2/JetHT__Run2016B-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunC/JetHT__Run2016C-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunD/JetHT__Run2016D-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunE/JetHT__Run2016E-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunF/JetHT__Run2016F-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunF/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunG/JetHT__Run2016G-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunH/JetHT__Run2016H-21Feb2020_UL2016_MINIAOD_reduced_skim.root");

//	/==========================================================UL16 ak4Puppi================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016Bver2-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016C-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016D-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016E-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");

	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016G-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016H-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
 
	tree->SetBranchAddress("run",&run);
	tree->SetBranchAddress("event",&event);
	tree->SetBranchAddress("lumi",&lumi);
	tree->SetBranchAddress("metSig",&met_ov_sumet);

	tree->SetBranchAddress("chargedHadEnFrac_j1",&chf);
	tree->SetBranchAddress("neutrHadEnFrac_j1",&nhf);
	tree->SetBranchAddress("chargedElectromFrac_j1",&cemf);
	tree->SetBranchAddress("neutrElectromFrac_j1",&nemf);
	tree->SetBranchAddress("muEnFract_j1",&muf);
	tree->SetBranchAddress("chargedMult_j1",&cm);
	tree->SetBranchAddress("neutrMult_j1",&nm);
	tree->SetBranchAddress("photonMult_j1",&pm);
	tree->SetBranchAddress("eta_j1",&eta_j1);
	tree->SetBranchAddress("eta_j2",&eta_j2);
	tree->SetBranchAddress("pT_j1",&pT_j1);
	tree->SetBranchAddress("eleEnFract_j1",&elf);
	tree->SetBranchAddress("photonEnFrac_j1",&phf);
	tree->SetBranchAddress("phi_j1",&phi_j1);

	tree->SetBranchAddress("pT_j2",&pT_j2);
	tree->SetBranchAddress("chargedHadEnFrac_j2",&chf_j2);
	tree->SetBranchAddress("neutrHadEnFrac_j2",&nhf_j2);
	tree->SetBranchAddress("chargedElectromFrac_j2",&cemf_j2);
	tree->SetBranchAddress("neutrElectromFrac_j2",&nemf_j2);
	tree->SetBranchAddress("muEnFract_j2",&muf_j2);
	tree->SetBranchAddress("chargedMult_j2",&cm_j2);
	tree->SetBranchAddress("neutrMult_j2",&nm_j2);
	tree->SetBranchAddress("photonMult_j2",&pm_j2);
	tree->SetBranchAddress("eleEnFract_j2",&elf_j2);
	tree->SetBranchAddress("photonEnFrac_j2",&phf_j2);
	tree->SetBranchAddress("phi_j2",&phi_j2);

	tree->SetBranchAddress("nVtx",&nVtx);
	tree->SetBranchAddress("passHLT",&passHLT);  //for ak8:    AK8PFHT800 TrimMass50_v12
	tree->SetBranchAddress("passHLT1",&passHLT1);  //for ak8:  AK8PFHT850 TrimMass50_v11
	tree->SetBranchAddress("passHLT2",&passHLT2);  //for ak8:  AK8PFHT900_TrimMass50_v11
	tree->SetBranchAddress("passHLT3",&passHLT3); //for ak8:   AK8PFJet200_v15
	tree->SetBranchAddress("passHLT4",&passHLT4); //for ak8:   AK8PFJet400_v16	
	tree->SetBranchAddress("JetIDlepVeto_2016_j1",&JetID_2016_j1);
	tree->SetBranchAddress("JetIDlepVeto_2017_j1",&JetID_2017_j1);
	tree->SetBranchAddress("JetIDlepVeto_2018_j1",&JetID_2018_j1);
	tree->SetBranchAddress("JetIDlepVeto_2016_j2",&JetID_2016_j2);
	tree->SetBranchAddress("JetIDlepVeto_2017_j2",&JetID_2017_j2);
	tree->SetBranchAddress("JetIDlepVeto_2018_j2",&JetID_2018_j2);

	Int_t nentries=(Int_t)tree->GetEntries(); 
	cout<<"Number of entries ="<<nentries<<endl;
	int LoopEntries =0;		
	if(test_run) LoopEntries = 1000;
	else LoopEntries = nentries;
	for (int i=0; i<LoopEntries; i++) //event loop
	{	
		//if(i!=0 && i%1000==0) cout<<i<<endl;
		if(i!=0 && i%5000000==0) cout<<i<<endl;
		tree->GetEntry(i);

			
		if(passHLT4==1)
		{
			//cout<<i<<", "<<ybin<<""<<chf<<" "<<DijetMassAK4<<""<<eta_j1<<""<<passHLT<<" "<<ybin<<endl; 
			if (pT_j1>pTmin && pT_j1<pTmax) h_ETAJet1->Fill(eta_j1);
			if (pT_j2>pTmin && pT_j2<pTmax) h_ETAJet1->Fill(eta_j2);
			//=== eta regions ====
			int ybin = getBin(fabs(eta_j1),yBnd,eta_bins);
			if (ybin > -1)//fill hist's in the corresponding eta bin
			{ 
				if (pT_j1>pTmin && pT_j1<pTmax)
				{
					h_CHFJet1[ybin]->Fill(chf); 
					h_NHFJet1[ybin]->Fill(nhf);
					h_CEMFJet1[ybin]->Fill(cemf);
					h_NEMFJet1[ybin]->Fill(nemf);
					h_MUFJet1[ybin]->Fill(muf);
					h_PHIJet1[ybin]->Fill(phi_j1);
					h_CMJet1[ybin]->Fill(cm);
					h_NMJet1[ybin]->Fill(nm);
					h_PMJet1[ybin]->Fill(pm);
					h_ptJet1[ybin]->Fill(pT_j1);		
				}
			}// end of if ybin>-1  for jet 1
			ybin = getBin(fabs(eta_j2),yBnd,eta_bins);
			if (ybin > -1)//fill hist's in the corresponding eta bin
			{ 
				if (pT_j2>pTmin && pT_j2<pTmax)
				{
					h_CHFJet1[ybin]->Fill(chf_j2); 
					h_NHFJet1[ybin]->Fill(nhf_j2);
					h_CEMFJet1[ybin]->Fill(cemf_j2);
					h_NEMFJet1[ybin]->Fill(nemf_j2);
					h_MUFJet1[ybin]->Fill(muf_j2);
					h_PHIJet1[ybin]->Fill(phi_j2);
					h_CMJet1[ybin]->Fill(cm_j2);
					h_NMJet1[ybin]->Fill(nm_j2);
					h_PMJet1[ybin]->Fill(pm_j2);
					h_ptJet1[ybin]->Fill(pT_j2);
					h_METovSUMET[ybin]->Fill(met_ov_sumet);
					h_nVtx[ybin]->Fill(nVtx);
				}
			}// end of if ybin>-1  for jet 2
		}//end of mjj, trigger cut
	}// end of event loop
	delete tree;

		//=========================2017 MC btb dijet Pythia =======================================

	
	char PtHatBin[15][50] = {"15to30" , "30to50", "50to80", "80to120", "120to170" , "170to300" , "300to470" , "470to600" , "600to800" , "800to1000" , "1000to1400", "1400to1800", "1800to2400", "2400to3200", "3200toInf"  }; //ptHatBins of MC

	//int PtHatBin_file_number[15] = {3, 3, 3, 5, 5, 5, 11, 6, 12, 8, 4, 1, 1, 1, 1};  //number of reduced_skim files in each ptHatBin


	double cross_section[15] = { 1820000000,138900000, 19100000 ,2735000 ,467500.,117400., 7753.,642.1, 185.9, 32.05, 9.365	, 0.8398, 0.1124, 0.006752, 0.0001626}; //xsec of 2017

													   
//  	double cross_section[15] = { 1246000000,106900000, 19222500 ,2758420 ,471100.,117276., 7823.,648.,186.9, 32.293, 9.4183, 0.84265, 0.114943, 0.0068298, 0.000165445};
		//cross section starts from 50to80

	long double weight[15];

	int Ntotal=0;

	char input_directory_MC[300];
	std::cout<<"Calculating the weights of each pt-hat bin file... "  << std::endl;
	TFile *f1;
	for(int fl=1; fl<15; fl++)
	{ 


		strcpy(input_directory_MC,MC_path_start);
		strcat(input_directory_MC,PtHatBin[fl]);
		strcat(input_directory_MC,MC_path_end);

		f1 = TFile::Open(input_directory_MC,"READ");
	    TH1D *h_Nev = (TH1D*)f1->Get("DijetFilter/EventCount/EventCounter");
	    int Nev = h_Nev->GetBinContent(2);
		Ntotal = Ntotal + Nev;
	    std::cout<<Nev<<std::endl;
		weight[fl] = cross_section[fl]*lumin/Nev;
	    std::cout<< "pT bin : " << PtHatBin[fl] <<", Weight is " << weight[fl] << std::endl;
		//weight[fl]=1.;
	}  

	cout << " Total number of events: " << Ntotal << endl;
 //============================until here ================================================

	for(Int_t fl=1;fl<15;fl++)
	{  

		strcpy(input_directory_MC,MC_path_start);
		strcat(input_directory_MC,PtHatBin[fl]);
		strcat(input_directory_MC,MC_path_end);

		f1 = TFile::Open(input_directory_MC,"READ");
		TTree *tree1 = (TTree*)f1->Get("rootTupleTree/tree");
	 
		tree1->SetBranchAddress("passHLT",&passHLT);  
		tree1->SetBranchAddress("passHLT1",&passHLT1);  
		tree1->SetBranchAddress("passHLT2",&passHLT2);  
		tree1->SetBranchAddress("passHLT3",&passHLT3); 
		tree1->SetBranchAddress("passHLT4",&passHLT4); 

		tree1->SetBranchAddress("run",&run);
		tree1->SetBranchAddress("event",&event);
		tree1->SetBranchAddress("lumi",&lumi);
		tree1->SetBranchAddress("metSig",&met_ov_sumet);
		tree1->SetBranchAddress("nVtx",&nVtx);



		tree1->SetBranchAddress("JetIDlepVeto_2016_j1",&JetID_2016_j1);
		tree1->SetBranchAddress("JetIDlepVeto_2017_j1",&JetID_2017_j1);
		tree1->SetBranchAddress("JetIDlepVeto_2018_j1",&JetID_2018_j1);
		tree1->SetBranchAddress("JetIDlepVeto_2016_j2",&JetID_2016_j2);
		tree1->SetBranchAddress("JetIDlepVeto_2017_j2",&JetID_2017_j2);
		tree1->SetBranchAddress("JetIDlepVeto_2018_j2",&JetID_2018_j2);
	

		tree1->SetBranchAddress("chargedHadEnFrac_j1",&chf);
		tree1->SetBranchAddress("neutrHadEnFrac_j1",&nhf);
		tree1->SetBranchAddress("chargedElectromFrac_j1",&cemf);
		tree1->SetBranchAddress("neutrElectromFrac_j1",&nemf);
		tree1->SetBranchAddress("muEnFract_j1",&muf);
		tree1->SetBranchAddress("chargedMult_j1",&cm);
		tree1->SetBranchAddress("neutrMult_j1",&nm);
		tree1->SetBranchAddress("photonMult_j1",&pm);
		tree1->SetBranchAddress("eta_j1",&eta_j1);
		tree1->SetBranchAddress("pT_j1",&pT_j1);


		tree1->SetBranchAddress("phi_j1",&phi_j1);

		tree1->SetBranchAddress("chargedHadEnFrac_j2",&chf_j2);
		tree1->SetBranchAddress("neutrHadEnFrac_j2",&nhf_j2);
		tree1->SetBranchAddress("chargedElectromFrac_j2",&cemf_j2);
		tree1->SetBranchAddress("neutrElectromFrac_j2",&nemf_j2);
		tree1->SetBranchAddress("muEnFract_j2",&muf_j2);
		tree1->SetBranchAddress("chargedMult_j2",&cm_j2);
		tree1->SetBranchAddress("neutrMult_j2",&nm_j2);
		tree1->SetBranchAddress("photonMult_j2",&pm_j2);
		tree1->SetBranchAddress("eta_j2",&eta_j2);
		tree1->SetBranchAddress("pT_j2",&pT_j2);


		tree1->SetBranchAddress("phi_j2",&phi_j2);



		Int_t nentries=(Int_t)tree1->GetEntries(); 
		cout << "Now proccessing pT bin : " << PtHatBin[fl] <<  ",  Number of entries =  "<< nentries << endl ;

	   	int LoopEntries =0;		
		if(test_run) LoopEntries = 1000;
		else LoopEntries = nentries;
		
		for (int i=0; i<LoopEntries; i++) //event loop
		{
			if(i!=0 && i%5000000==0) cout<<i<<endl;
			 tree1->GetEntry(i);
			//	 if (ybin!=-1) cout << ybin<<"  "  <<eta_j1<< endl ;
					if(passHLT4==1)
					{
						if(pT_j1>pTmin && pT_j1>60 && pT_j1<pTmax) h_ETAJet1_MC->Fill(eta_j1,weight[fl]);
						if(pT_j2>pTmin && pT_j2>30 && pT_j2<pTmax) h_ETAJet1_MC->Fill(eta_j2,weight[fl]);
						//=== eta regions ====
						int ybin = getBin(fabs(eta_j1),yBnd,eta_bins);
						if (ybin > -1)//fill hist's in the corresponding eta bin
						{
						//cout << " pt1 = " << pT_j1 << " pt2 = " << pT_j2 << endl;
							if(pT_j1>pTmin && pT_j1>60 && pT_j1<pTmax)
//							if(pT_j1>pTmin && pT_j1>0 && pT_j1<pTmax)
							{
								h_CHFJet1_MC[ybin]->Fill(chf,weight[fl]);
								h_NHFJet1_MC[ybin]->Fill(nhf,weight[fl]);
								h_CEMFJet1_MC[ybin]->Fill(cemf,weight[fl]);
								h_NEMFJet1_MC[ybin]->Fill(nemf,weight[fl]);
								h_MUFJet1_MC[ybin]->Fill(muf,weight[fl]);
								h_CMJet1_MC[ybin]->Fill(cm,weight[fl]);
								h_NMJet1_MC[ybin]->Fill(nm,weight[fl]);
								h_PMJet1_MC[ybin]->Fill(pm,weight[fl]);
								h_ptJet1_MC[ybin]->Fill(pT_j1,weight[fl]);
								h_PHIJet1_MC[ybin]->Fill(phi_j1,weight[fl]);
							
							}
						
						}//end of if ybin>-1 //for jet 1
						ybin = getBin(fabs(eta_j2),yBnd,eta_bins);
						if (ybin > -1)//fill hist's in the corresponding eta bin
						{ 
							if(pT_j2>pTmin && pT_j2>30 && pT_j2<pTmax)
//							if(pT_j2>pTmin && pT_j2>0 && pT_j2<pTmax)
							{
								h_CHFJet1_MC[ybin]->Fill(chf_j2,weight[fl]); 
								h_NHFJet1_MC[ybin]->Fill(nhf_j2,weight[fl]);
								h_CEMFJet1_MC[ybin]->Fill(cemf_j2,weight[fl]);
								h_NEMFJet1_MC[ybin]->Fill(nemf_j2,weight[fl]);
								h_MUFJet1_MC[ybin]->Fill(muf_j2,weight[fl]);
								h_PHIJet1_MC[ybin]->Fill(phi_j2,weight[fl]);
								h_CMJet1_MC[ybin]->Fill(cm_j2,weight[fl]);
								h_NMJet1_MC[ybin]->Fill(nm_j2,weight[fl]);
								h_PMJet1_MC[ybin]->Fill(pm_j2,weight[fl]);
								h_ptJet1_MC[ybin]->Fill(pT_j2,weight[fl]);
								h_METovSUMET_MC[ybin]->Fill(met_ov_sumet,weight[fl]);
								h_nVtx_MC[ybin]->Fill(nVtx,weight[fl]);
							}
	
						}// end of if ybin>-1  for jet 2
					} //trigger emulator
			}// end of event loop
	delete tree1;
	f1->Close();
	} // end of pT-hat bin loop

	cout<< "Event loops finished" << endl;
 
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

/*	
	TCanvas *pad16= new TCanvas("pad16", "",1);
	pad16 ->Divide(3,3);
	TCanvas *pad17= new TCanvas("pad17", "",1);
	pad17 ->Divide(3,3); 
	*/ 

	TLegend *leg1;
	for(int iy=0; iy<eta_bins; iy++)
	{
 
		etamin = yBnd[iy];
		etamax = yBnd[iy+1];
		const char *seta = (etamin==0 ? Form("|y| < %1.2g",etamax) :
		Form("%1.2g #leq |y| < %1.2g",etamin,etamax));
		 TLatex *teta;
		 if(eta_bins > 1)
		 {
		 	teta = new TLatex(0.38,0.86,seta); cout<<seta<<endl;
			teta->SetTextSize(0.06);
		 }
		 else 
		 {
		 	teta = new TLatex(0.23,0.86,seta); cout<<seta<<endl;
			teta->SetTextSize(0.04);
		 }
		 teta->SetNDC();


		 if(eta_bins > 1) pad1->cd(iy+1);
		 else pad1->cd();
		 if(eta_bins > 1) pad1->cd(iy+1)->SetLogy(1);
		 else pad1->cd()->SetLogy(1);
		 h_CHFJet1[iy]->GetXaxis()->SetTitle("Charged Hadron Fraction");
		 h_CHFJet1[iy]->GetYaxis()->SetTitle("Entries");
		 h_CHFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		 h_CHFJet1_MC[iy]->SetLineColor(4); 
		 h_CHFJet1[iy]->SetLineStyle(1);
		 h_CHFJet1[iy]->SetMinimum(0.1);
		 h_CHFJet1[iy]->SetMaximum(1000000000);
		 h_CHFJet1[iy]->Draw("");
		 h_CHFJet1_MC[iy]->Scale( h_CHFJet1[iy]->Integral() /h_CHFJet1_MC[iy]->Integral() );
		 h_CHFJet1_MC[iy]->Draw("same hist");
		 paveCMS ->Draw("same");
		 teta->Draw();


		 if(eta_bins > 1)
		 {
 			 leg1 = new TLegend(.2, .6, .9, .9);//7899//4899
			 leg1->SetTextSize(0.06);
		 }
		 else 
		 {
		 	leg1 = new TLegend(.7, .7, .9, .9);
		 	leg1->SetTextSize(0.04);
		 }
		 leg1->SetFillColor(0); 
		 leg1->SetBorderSize(0);
		 leg1->SetHeader(jet_kind); 
		 leg1->AddEntry(h_CHFJet1[0], "Data", "L");
		 leg1->AddEntry(h_CHFJet1_MC[0], "MC", "L");
		 if(eta_bins <= 1) leg1->Draw("same");


		if(eta_bins > 1) pad2->cd(iy+1);
		else pad2->cd();h_CMJet1[iy]->GetXaxis()->SetTitle("Charged Multiplicity") ;
		h_CMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_CMJet1[iy]->SetLineColor(1);
		h_CMJet1_MC[iy]->SetLineColor(4);
		h_CMJet1[iy]->SetLineStyle(1);
		h_CMJet1[iy]->SetMinimum(0.1);
		h_CMJet1[iy]->SetMaximum(100000000.);
		h_CMJet1[iy]->Draw();
		if(eta_bins > 1) pad2->cd(iy+1)->SetLogy(1);
		else pad2->cd()->SetLogy(1);
		h_NHFJet1[iy]->GetXaxis()->SetTitle("Neutral Hadron Fraction");
		h_NHFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NHFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_NHFJet1[iy]->SetLineColor(1);
		h_NHFJet1_MC[iy]->SetLineColor(4);
		h_NHFJet1[iy]->SetLineStyle(1);
		h_NHFJet1[iy]->SetMinimum(0.1);
		h_NHFJet1[iy]->SetMaximum(1000000000);
		h_NHFJet1[iy]->Draw();
		h_NHFJet1_MC[iy]->Scale( h_NHFJet1[iy]->Integral() /h_NHFJet1_MC[iy]->Integral() );
		h_NHFJet1_MC[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");

		if(eta_bins > 1) pad3->cd(iy+1);
		else pad3->cd();
		if(eta_bins > 1) pad3->cd(iy+1)->SetLogy(1);
		else pad3->cd()->SetLogy(1);
		h_CEMFJet1[iy]->GetXaxis()->SetTitle("Charged Electromagnetic Fraction");
		h_CEMFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CEMFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_CEMFJet1[iy]->SetLineColor(1);
		h_CEMFJet1_MC[iy]->SetLineColor(4);
		h_CEMFJet1[iy]->SetLineStyle(1);
		h_CEMFJet1[iy]->SetMinimum(0.1);
		h_CEMFJet1[iy]->SetMaximum(100000000);
		h_CEMFJet1[iy]->Draw();
		h_CEMFJet1_MC[iy]->Scale( h_CEMFJet1[iy]->Integral() /h_CEMFJet1_MC[iy]->Integral() );
		h_CEMFJet1_MC[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");

		if(eta_bins > 1) pad4->cd(iy+1);
		else pad4->cd();
		if(eta_bins > 1) pad4->cd(iy+1)->SetLogy(1);
		else pad4->cd()->SetLogy(1);
		h_NEMFJet1[iy]->GetXaxis()->SetTitle("Neutral Electromagnetic Fraction");
		h_NEMFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NEMFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_NEMFJet1[iy]->SetLineColor(1);
		h_NEMFJet1_MC[iy]->SetLineColor(4);
		h_NEMFJet1[iy]->SetLineStyle(1);
		h_NEMFJet1[iy]->SetMinimum(0.1);
		h_NEMFJet1[iy]->SetMaximum(1000000000.);
		h_NEMFJet1[iy]->Draw();
		h_NEMFJet1_MC[iy]->Scale( h_NEMFJet1[iy]->Integral() /h_NEMFJet1_MC[iy]->Integral() );
		h_NEMFJet1_MC[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");

		if(eta_bins > 1) pad5->cd(iy+1);
		else pad5->cd();
		if(eta_bins > 1) pad5->cd(iy+1)->SetLogy(1);
		else pad5->cd()->SetLogy(1);
		h_MUFJet1[iy]->GetXaxis()->SetTitle("Muon Fraction");
		h_MUFJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_MUFJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_MUFJet1[iy]->SetLineColor(1);
		h_MUFJet1_MC[iy]->SetLineColor(4);
		h_MUFJet1[iy]->SetLineStyle(1);
		h_MUFJet1[iy]->SetMaximum(100000000);
		h_MUFJet1[iy]->SetMinimum(0.1);
		h_MUFJet1[iy]->Draw();
		h_MUFJet1_MC[iy]->Draw("same hist");
		h_MUFJet1_MC[iy]->Scale( h_MUFJet1[iy]->Integral() /h_MUFJet1_MC[iy]->Integral() );
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");
		

		if(eta_bins > 1) pad10->cd(iy+1);
		else pad10->cd();
		if(eta_bins > 1) pad10->cd(iy+1)->SetLogy(1);
		else pad10->cd()->SetLogy(1);
		h_METovSUMET[iy]->GetXaxis()->SetTitle("MET/SumET") ;
		h_METovSUMET[iy]->GetYaxis()->SetTitle("Entries");
		h_METovSUMET[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_METovSUMET[iy]->SetLineColor(1);
		h_METovSUMET_MC[iy]->SetLineColor(4);
		h_METovSUMET[iy]->SetLineStyle(1);
		h_METovSUMET[iy]->SetMaximum(100000000);
		h_METovSUMET[iy]->SetMinimum(0.1);
		h_METovSUMET[iy]->Draw();
		h_METovSUMET_MC[iy]->Draw("same hist");
		h_METovSUMET_MC[iy]->Scale( h_METovSUMET[iy]->Integral() /h_METovSUMET_MC[iy]->Integral() );
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");

		if(eta_bins > 1) pad11->cd(iy+1);
		else pad11->cd();
		if(eta_bins > 1) pad11->cd(iy+1)->SetLogy(1);
		else pad11->cd()->SetLogy(1);
		//if(eta_bins > 1) pad11->cd(iy+1)->SetLogx(1);
		//else pad11->cd()->SetLogx(1);
		h_NMJet1[iy]->GetXaxis()->SetTitle("Neutral Multiplicity") ;
		h_NMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_NMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		if(iy>3)h_NMJet1[iy]->GetXaxis()->SetRangeUser(0.,30);
		h_NMJet1[iy]->SetLineColor(1);
		h_NMJet1_MC[iy]->SetLineColor(4);
		h_NMJet1[iy]->SetLineStyle(1);
		h_NMJet1[iy]->SetMinimum(0.1);
		h_NMJet1[iy]->SetMaximum(1000000.);
		h_NMJet1[iy]->Draw();
		h_NMJet1_MC[iy]->Scale( h_NMJet1[iy]->Integral() /h_NMJet1_MC[iy]->Integral() );
		h_NMJet1_MC[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");

		if(eta_bins > 1) pad12->cd(iy+1);
		else pad12->cd();
		if(eta_bins > 1) pad12->cd(iy+1)->SetLogy(1);
		else pad12->cd()->SetLogy(1);
		//if(eta_bins > 1) pad12->cd(iy+1)->SetLogx(1);
		//else pad12->cd()->SetLogx(1);
		
		h_CMJet1[iy]->GetXaxis()->SetTitle("Charged Multiplicity") ;
		h_CMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_CMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		if(iy>3)h_CMJet1[iy]->GetXaxis()->SetRangeUser(0.,30);
		h_CMJet1[iy]->SetLineColor(1);
		h_CMJet1_MC[iy]->SetLineColor(4);
		h_CMJet1[iy]->SetLineStyle(1);
		h_CMJet1[iy]->SetMinimum(0.1);
		h_CMJet1[iy]->SetMaximum(1000000.);
		h_CMJet1[iy]->Draw();
		h_CMJet1_MC[iy]->Scale( h_CMJet1[iy]->Integral() /h_CMJet1_MC[iy]->Integral() );
		h_CMJet1_MC[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");

		if(eta_bins > 1) pad13->cd(iy+1);
		else pad13->cd();
		if(eta_bins > 1) pad13->cd(iy+1)->SetLogy(1);
		else pad13->cd()->SetLogy(1);
		h_PMJet1[iy]->GetXaxis()->SetTitle("Photon Multiplicity") ;
		h_PMJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_PMJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_PMJet1[iy]->SetLineColor(1);
		h_PMJet1_MC[iy]->SetLineColor(4);
		h_PMJet1[iy]->SetLineStyle(1);
		h_PMJet1[iy]->SetMinimum(0.1);
		h_PMJet1[iy]->SetMaximum(100000000.);
		h_PMJet1[iy]->Draw();
		h_PMJet1_MC[iy]->Scale( h_PMJet1[iy]->Integral() /h_PMJet1_MC[iy]->Integral() );
		h_PMJet1_MC[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		 if(eta_bins <= 1) leg1->Draw("same");



		if(eta_bins > 1) pad14->cd(iy+1);
		else pad14->cd();
		if(eta_bins > 1) pad14->cd(iy+1)->SetLogy(1);
		else pad14->cd()->SetLogy(1);
		h_nVtx[iy]->GetXaxis()->SetTitle("nVtx") ;
		h_nVtx[iy]->GetYaxis()->SetTitle("Entries");
		h_nVtx[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_nVtx[iy]->SetLineColor(1);
		h_nVtx_MC[iy]->SetLineColor(4);
		h_nVtx[iy]->SetLineStyle(1);
		h_nVtx[iy]->SetMaximum(100000000);
		h_nVtx[iy]->SetMinimum(0.1);
		h_nVtx[iy]->Draw();
		h_nVtx_MC[iy]->Draw("same hist");
		h_nVtx_MC[iy]->Scale( h_nVtx[iy]->Integral() /h_nVtx_MC[iy]->Integral() );
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");


		/* 
		

		 pad16->cd(iy+1);
		h_PHIJet1[iy]->GetXaxis()->SetTitle("#phi") ;
		h_PHIJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_PHIJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_PHIJet1[iy]->SetLineColor(1);
		h_PHIJet1_MC[iy]->SetLineColor(4);
		h_PHI_noise[iy]->SetLineColor(2);
		h_PHI_noise_MC[iy]->SetLineColor(6);
		h_PHI_noise[iy]->SetLineWidth(2);
		h_PHI_noise_MC[iy]->SetLineWidth(2);
		h_PHIJet1[iy]->SetLineStyle(1);
		h_PHI_noise[iy]->SetLineStyle(1); 
		h_PHIJet1[iy]->SetMinimum(0.5); 
		h_PHIJet1[iy]->SetMaximum(1000000.);
		h_PHIJet1[iy]->Draw();
		h_PHIJet1_MC[iy]->Draw("same hist");
		h_PHI_noise[iy]->Draw("same hist");
		h_PHI_noise_MC[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		//leg1->Draw();

		*/
		if(eta_bins > 1) pad9->cd(iy+1);
		else pad9->cd();
		if(eta_bins > 1) pad9->cd(iy+1)->SetLogy(1);
		else pad9->cd()->SetLogy(1);
		h_ptJet1[iy]->GetXaxis()->SetTitle("Jet pT (GeV)");
		h_ptJet1[iy]->GetYaxis()->SetTitle("Entries");
		h_ptJet1[iy]->GetYaxis()->SetTitleOffset(1.3);
		h_ptJet1[iy]->SetLineColor(1);
		h_ptJet1_MC[iy]->SetLineColor(4);
		h_ptJet1[iy]->SetLineStyle(1);
		h_ptJet1[iy]->SetMinimum(0.1); 
		h_ptJet1[iy]->SetMaximum(50000000);
		h_ptJet1[iy]->Draw();
		h_ptJet1_MC[iy]->Scale( h_ptJet1[iy]->Integral() /h_ptJet1_MC[iy]->Integral() );
		h_ptJet1_MC[iy]->Draw("same hist");
		paveCMS ->Draw("same");
		teta->Draw();
		if(eta_bins <= 1) leg1->Draw("same");

	 
	} //end of eta regions


	if(eta_bins > 1)
	{
		pad1->cd(9);
		leg1->Draw();
		pad2->cd(9);
		leg1->Draw();
		pad3->cd(9);
		leg1->Draw();
		pad4->cd(9);
		leg1->Draw();
		pad5->cd(9);
		leg1->Draw();
		pad9->cd(9);
		leg1->Draw();
		pad10->cd(9);
		leg1->Draw();
		pad11->cd(9);
		leg1->Draw();
		pad12->cd(9);
		leg1->Draw();
		pad13->cd(9);
		leg1->Draw();
		pad14->cd(9);
		leg1->Draw();
	}


	pad15->cd()->SetLogy(1);
	h_ETAJet1->GetXaxis()->SetTitle("#eta") ;
	h_ETAJet1->GetYaxis()->SetTitle("Entries");
	h_ETAJet1->GetYaxis()->SetRangeUser(0.5,1000000);
	h_ETAJet1->GetYaxis()->SetTitleOffset(1.3);
	h_ETAJet1->SetLineWidth(2);
	h_ETAJet1->SetLineColor(1);
	h_ETAJet1->SetMarkerSize(0.04);
	h_ETAJet1_MC->SetLineWidth(2);
	h_ETAJet1_MC->SetLineColor(4);
	h_ETAJet1_MC->SetMarkerSize(0.04);
	h_ETAJet1_MC->Scale(h_ETAJet1->Integral()/h_ETAJet1_MC->Integral());
	h_ETAJet1->GetYaxis()->SetRangeUser(0.5,1000000);
	h_ETAJet1->Draw("hist");
	h_ETAJet1_MC->Draw("hist same");
	paveCMS ->Draw("same");

	TLegend *leg2 =new TLegend(.2, .75, .4, .9);//7899//4899
	leg2->SetTextSize(0.025);
	leg2->SetFillColor(0); 
	leg2->SetBorderSize(0);
	leg2->SetHeader("PUPPI"); 
	leg2->AddEntry(h_ETAJet1, "Data", "L");
	leg2->AddEntry(h_ETAJet1_MC, "MC", "L");
	leg2->Draw("same");

	TFile *fout;

	if(Save_plots_and_histos)
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
		sprintf(filename,"%s/%s/%s_nVtx.png",analyzer_path,output_directory,image_name);
		pad14->SaveAs(filename);
		sprintf(filename,"%s/%s/%s_eta.png",analyzer_path,output_directory,image_name);
		pad15->SaveAs(filename);
		//sprintf(filename,"%s/%s/%s_%s_phi.png",analyzer_path,output_directory,image_name,c);
		//pad16->SaveAs(filename);
		//sprintf(filename,"%s/%s/%s_%s_eta.png",analyzer_path,output_directory,image_name,c);
		//pad17->SaveAs(filename);

		sprintf(filename,"%s/%s/%s_jet_quantity_histos.root",analyzer_path,output_directory,image_name);
		fout = new TFile(filename,"recreate");
		fout->cd();
		for (int ybin=0; ybin<eta_bins; ybin++)
		{

			h_ETAJet1_MC->Write();
			h_ETAJet1->Write();

			h_CHFJet1[ybin]->Write();
			h_NHFJet1[ybin]->Write();
			h_CEMFJet1[ybin]->Write();
			h_NEMFJet1[ybin]->Write();
			h_MUFJet1[ybin]->Write();
			h_CMJet1[ybin]->Write();
			h_NMJet1[ybin]->Write();
			h_PMJet1[ybin]->Write();
			h_ptJet1[ybin]->Write();

			h_PHIJet1[ybin]->Write();


			h_METovSUMET[ybin]->Write();
			h_DijetMassAK4[ybin]->Write();
			h_nVtx[ybin]->Write();


			h_CHFJet1_MC[ybin]->Write();
			h_NHFJet1_MC[ybin]->Write();
			h_CEMFJet1_MC[ybin]->Write();
			h_NEMFJet1_MC[ybin]->Write();
			h_MUFJet1_MC[ybin]->Write();
			h_CMJet1_MC[ybin]->Write();
			h_NMJet1_MC[ybin]->Write();
			h_PMJet1_MC[ybin]->Write();
			h_ptJet1_MC[ybin]->Write();

			h_PHIJet1_MC[ybin]->Write();
			h_nVtx_MC[ybin]->Write();
			h_METovSUMET_MC[ybin]->Write();
			h_DijetMassAK4_MC[ybin]->Write();
		}
	}
}

int getBin(double x, double boundaries[],int eta_bins) 
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
