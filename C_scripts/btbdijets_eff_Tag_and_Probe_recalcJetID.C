#define N_histo_bins 300
#define eta_bins 8
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

double error1(double n1,double n2);
double error2(double n1,double n2);
bool getJetID(int era, bool isUL, bool isCHS, bool LepVeto, double eta, double cm, double nm, double nemf, double cemf, double nhf, double chf, double muf );
bool FindJetIDFromEra ( int flag_era, bool JetID_16, bool JetID_17, bool JetID_18 ) ;
bool FindProbeJetID (int irand, int flag_era, double JetID_16_j1, double JetID_17_j1, double JetID_18_j1, double JetID_16_j2, double JetID_17_j2, double JetID_18_j2 );
bool FindTagJetID (int irand, int flag_era, double JetID_16_j1, double JetID_17_j1, double JetID_18_j1, double JetID_16_j2, double JetID_17_j2, double JetID_18_j2 );
double FindProbeVariable(int irand, double var_j1,  double var_j2);
double FindTagVariable(int irand, double var_j1,  double var_j2);


void btbdijets_eff_Tag_and_Probe_recalcJetID()
{

	gROOT->LoadMacro("setTDRStyle_teliko.C");
	setTDRStyle_teliko(); 
	gStyle->SetOptStat(0);

	float etamin=0, etamax=0;
	char name[300]; 
	  
	TH1D *h_pT_probe_all[eta_bins], *h_pT_probe_JetID[eta_bins];  
	TH1D *h_pT_probe_all_HLT_PFJet400[eta_bins], *h_pT_probe_JetID_HLT_PFJet400[eta_bins]; 

	char analyzer_path[300] = "/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/"; 
	char output_directory[300] = "UL_datasets_JetID/UL_2016/PUPPI/v15/nonAPV/First_try/test_for_35/";     
	char image_name[300] = "RunFG_nemf0p2";

	bool Save_plots_and_histos = true ;
	bool isUL  = true;
	bool isCHS = false ;
	bool test_run = false;
	char *jet_type;
	if (isCHS) jet_type = " AK4 CHS";
	else jet_type = " AK4 PUPPI";
	int era = 2016;  // variable to choose the JetID year: 2016, 2017, 2018

	for(Int_t h=0; h<eta_bins;h++)
	{
		sprintf(name,"h_pT_probe_all%i",h);
		h_pT_probe_all[h] = new TH1D(name, "", N_histo_bins,0,9000);
		sprintf(name,"h_pT_probe_JetID%i",h);
		h_pT_probe_JetID[h] = new TH1D(name, "", N_histo_bins,0,9000); 
		sprintf(name,"h_pT_probe_all_HLT_PFJet400%i",h);
		h_pT_probe_all_HLT_PFJet400[h] = new TH1D(name, "", N_histo_bins,0,9000);
		sprintf(name,"h_pT_probe_JetID_HLT_PFJet400%i",h);
		h_pT_probe_JetID_HLT_PFJet400[h] = new TH1D(name, "", N_histo_bins,0,9000);      
	}

	double pT_j1, eta_j1, chf_j1, nhf_j1, cemf_j1, nemf_j1, muf_j1, cm_j1, nm_j1, pm_j1, elf_j1, phf_j1, phi_j1;
	double pT_j2, eta_j2, chf_j2, nhf_j2, cemf_j2, nemf_j2, muf_j2, cm_j2, nm_j2, pm_j2, elf_j2, phf_j2, phi_j2;

	double pT_tag, pT_probe, eta_probe, eta_tag, muf_tag, muf_probe, cemf_tag, cemf_probe;
	double passHLT, passHLT1, passHLT2, passHLT3, passHLT4, run, event, lumi, nVtx, met_ov_sumet;
	bool JetID_tag, JetID_probe;
	bool JetID_2016_j1, JetID_2017_j1, JetID_2018_j1, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2;


	float yBnd[eta_bins+1]={0.0, 0.5, 1.0, 1.5, 2.0, 2.4, 2.7, 3.0, 5.0 };

	char eta_bins_legend[eta_bins][25] = { "|#eta|<0.5", "0.5 #leq |#eta| < 1.0", "1.0 #leq |#eta| < 1.5", "1.5 #leq |#eta| < 2.0", "2.0 #leq |#eta| < 2.4","2.4 #leq |#eta| < 2.7" , "2.7 #leq |#eta| < 3.0" , "3.0 #leq |#eta| < 5.0" }; 


	TChain *tree = new TChain("rootTupleTree/tree");

//==========================================================UL16 ak4CHS================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunBver2/JetHT__Run2016B-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunC/JetHT__Run2016C-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunD/JetHT__Run2016D-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunE/JetHT__Run2016E-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/HIPM/RunF/JetHT__Run2016F-21Feb2020_UL2016_HIPM_MINIAOD_reduced_skim.root");
	
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunF/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunG/JetHT__Run2016G-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_rerun/nonAPV_goldenJSON/RunH/JetHT__Run2016H-21Feb2020_UL2016_MINIAOD_reduced_skim.root");

//==========================================================UL16 ak4Puppi================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016Bver2-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016C-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016D-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016E-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/APV/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");

	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016F-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016G-21Feb2020_UL2016_MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2016_data_reduced_PUPPIv15/nonAPV/JetHT__Run2016H-21Feb2020_UL2016_MINIAOD_reduced_skim.root");

//==========================================================UL17 ak4CHS================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunB/JetHT__Run2017B-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunC/JetHT__Run2017C-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunD/JetHT__Run2017D-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunE/JetHT__Run2017E-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_CHS_JetID_reduced/RunF/JetHT__Run2017F-09Aug2019_UL2017-v1_reduced_skim.root");


//==========================================================UL17 ak4PUPPI================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunB/JetHT__Run2017B-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunC/JetHT__Run2017C-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunD/JetHT__Run2017D-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunE/JetHT__Run2017E-09Aug2019_UL2017-v1_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/UL2017_btb_PUPPI_JetID_reduced/RunF/JetHT__Run2017F-09Aug2019_UL2017-v1_reduced_skim.root");


//==========================================================UL18 ak4CHS================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/JetHT__Run2018A-12Nov2019_UL2018-v2__MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/JetHT__Run2018B-12Nov2019_UL2018-v2__MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/JetHT__Run2018C-12Nov2019_UL2018-v4__MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced/JetHT__Run2018D-12Nov2019_UL2018-v4__MINIAOD_reduced_skim.root");

//==========================================================UL18 ak4PUPPI================================================

//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced_Ak4Puppi/JetHT__Run2018A-12Nov2019_UL2018-v4__MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced_Ak4Puppi/JetHT__Run2018B-12Nov2019_UL2018-v4__MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced_Ak4Puppi/JetHT__Run2018C-12Nov2019_UL2018-v4__MINIAOD_reduced_skim.root");
//	tree->Add("/eos/cms/store/group/phys_jetmet/dimitris/Data_UL18_reduced_Ak4Puppi/JetHT__Run2018D-12Nov2019_UL2018-v4__MINIAOD_reduced_skim.root");


	tree->SetBranchAddress("passHLT" ,&passHLT );  //for ak8:    AK8PFHT800 TrimMass50_v12
	tree->SetBranchAddress("passHLT1",&passHLT1);  //for ak8:  AK8PFHT850 TrimMass50_v11
	tree->SetBranchAddress("passHLT2",&passHLT2);  //for ak8:  AK8PFHT900_TrimMass50_v11
	tree->SetBranchAddress("passHLT3",&passHLT3); //for ak8:   AK8PFJet200_v15
	tree->SetBranchAddress("passHLT4",&passHLT4); //for ak8:   AK8PFJet400_v16

	tree->SetBranchAddress("run",&run);
	tree->SetBranchAddress("event",&event);
	tree->SetBranchAddress("lumi",&lumi);
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
   	int irand;
	cout.precision(13);
	int LoopEntries =0;		
	if(test_run) LoopEntries = 1000;
	else LoopEntries = nentries;
	for (int i=0; i<LoopEntries; i++) //event loop
	{    
	//	if(i>0 && i%1000==0) cout<<i<<endl;
		if(i>0 && i%500000==0) cout<<i<<endl;
		tree->GetEntry(i);
		if (pT_j1<0.1) continue; 
//		gRandom->SetSeed(i);

		irand = (gRandom->Uniform()>0.5) ? 0 : 1;  

		JetID_2016_j1 = getJetID(2016, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );
		JetID_2017_j1 = getJetID(2017, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );
		JetID_2018_j1 = getJetID(2018, isUL, isCHS, true, eta_j1, cm_j1, nm_j1, nemf_j1, cemf_j1, nhf_j1, chf_j1, muf_j1 );

		JetID_2016_j2 = getJetID(2016, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );
		JetID_2017_j2 = getJetID(2017, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );
		JetID_2018_j2 = getJetID(2018, isUL, isCHS, true, eta_j2, cm_j2, nm_j2, nemf_j2, cemf_j2, nhf_j2, chf_j2, muf_j2 );

		pT_tag   = FindTagVariable(irand, pT_j1  , pT_j2);
		eta_tag  = FindTagVariable(irand, eta_j1 , eta_j2);
		cemf_tag = FindTagVariable(irand, cemf_j1, cemf_j2);
		muf_tag  = FindTagVariable(irand, muf_j1 , muf_j2);
		JetID_tag = FindTagJetID(irand, era, JetID_2016_j1, JetID_2017_j1, JetID_2018_j1, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2 );

		pT_probe   = FindProbeVariable(irand,pT_j1,pT_j2);
		eta_probe  = FindProbeVariable(irand,eta_j1,eta_j2);
		cemf_probe = FindProbeVariable(irand,cemf_j1,cemf_j2);
		muf_probe  = FindProbeVariable(irand,muf_j1,muf_j2);
		JetID_probe = FindProbeJetID(irand, era, JetID_2016_j1, JetID_2017_j1, JetID_2018_j1, JetID_2016_j2, JetID_2017_j2, JetID_2018_j2 );

		bool lepton_cut;
		if(era == 2016) lepton_cut = fabs(eta_probe)>2.4 || ( muf_probe<0.8 && cemf_probe < 0.8 && fabs(eta_probe)<2.4 );
		else		lepton_cut = fabs(eta_probe)>2.7 || ( muf_probe<0.8 && cemf_probe < 0.8 && fabs(eta_probe)<2.7 );

		if(passHLT2==1 )
		{
			for (int eta_bin_counter=0; eta_bin_counter<eta_bins; eta_bin_counter++ )
			{
				//cout << " irand = " << irand << endl;
				if(fabs(eta_probe)>=yBnd[eta_bin_counter] && fabs(eta_probe)<yBnd[eta_bin_counter+1])
				{
					//cout <<"1"<< endl;
					//cout << JetID_tag<<;
					if(JetID_tag && lepton_cut) h_pT_probe_all[eta_bin_counter]->Fill(pT_probe);        //denominator for efficiency
					if(JetID_tag && JetID_probe && lepton_cut) h_pT_probe_JetID[eta_bin_counter]->Fill(pT_probe);  //numerator for efficiency
				}
			}
		}

		if(passHLT4==1 )
		{
			for (int eta_bin_counter=0; eta_bin_counter<eta_bins; eta_bin_counter++ )
			{
				if(fabs(eta_probe)>=yBnd[eta_bin_counter] && fabs(eta_probe)<yBnd[eta_bin_counter+1])
				{
					if(JetID_tag && lepton_cut) h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->Fill(pT_probe);        //denominator for efficiency
					if(JetID_tag && JetID_probe && lepton_cut) h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->Fill(pT_probe);  //numerator for efficiency
				}
			}
		}

	}//end of event loop

	double tot_entries=0, JetID_entries=0, sel_eff=0.0;
	double tot_entries_HLT_PFJet400=0, JetID_entries_HLT_PFJet400=0, sel_eff_HLT_PFJet400=0.0;
	TGraphAsymmErrors *gr[eta_bins], *gr1[eta_bins]; 

	TCanvas *pad1 = new TCanvas("pad1", "",1);
	pad1->Divide(3,3);

	double x[N_histo_bins], y[N_histo_bins], eyu[N_histo_bins], eyl[N_histo_bins], ex[N_histo_bins];
	double x_HLT_PFJet400[N_histo_bins], y_HLT_PFJet400[N_histo_bins], eyu_HLT_PFJet400[N_histo_bins], eyl_HLT_PFJet400[N_histo_bins], ex_HLT_PFJet400[N_histo_bins];

	double high_trigger_numerator = 0;
	double high_trigger_denominator = 0;
	double low_trigger_numerator = 0;
	double low_trigger_denominator = 0;

	for(int eta_bin_counter=0; eta_bin_counter<eta_bins; eta_bin_counter++)
	{  
		cout << "Eta bin: " << "" << yBnd[eta_bin_counter] << "-"<< yBnd[eta_bin_counter+1] << endl;

		cout << "PFHT 1050 Eff= " << h_pT_probe_JetID[eta_bin_counter]->Integral() << "/" << h_pT_probe_all[eta_bin_counter]->Integral() << "= "<<h_pT_probe_JetID[eta_bin_counter]->Integral()/h_pT_probe_all[eta_bin_counter]->Integral() << endl;

		cout << "HLT_PFjet200 Eff= " << h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->Integral() << "/" << h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->Integral() << "= "<<h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->Integral()/h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->Integral() << endl;

		high_trigger_numerator = high_trigger_numerator + h_pT_probe_JetID[eta_bin_counter]->Integral();
		high_trigger_denominator = high_trigger_denominator + h_pT_probe_all[eta_bin_counter]->Integral();
		
		low_trigger_numerator = low_trigger_numerator + h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->Integral();
		low_trigger_denominator = low_trigger_denominator + h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->Integral();

		pad1->cd(eta_bin_counter+1);
		// draw a frame to define the range, in order to plot many graphs in the same pad
		TH1F *hr;
//		hr = pad1->cd(eta_bin_counter+1)->DrawFrame(0,0.6,500,1.2);
		if(eta_bin_counter < 4) hr = pad1->cd(eta_bin_counter+1)->DrawFrame(0,0.6,3000,1.2);
		else if(eta_bin_counter == 4) hr = pad1->cd(eta_bin_counter+1)->DrawFrame(0,0.6,2000,1.2);
		else if(eta_bin_counter == 5) hr = pad1->cd(eta_bin_counter+1)->DrawFrame(0,0.6,1200,1.2);
		else if(eta_bin_counter == 6) hr = pad1->cd(eta_bin_counter+1)->DrawFrame(0,0.6,800,1.2);
		else  hr = pad1->cd(eta_bin_counter+1)->DrawFrame(0,0.6,800,1.2);
		//if(eta_bin_counter==5) TH1F *hr = pad1->cd(eta_bin_counter+1)->DrawFrame(0,0.8,3000,1.2);
		//if(eta_bin_counter==6) TH1F *hr = pad1->cd(eta_bin_counter+1)->DrawFrame(0,0.0,3000,1.5);
		hr->SetXTitle("p_{T} probe jet (GeV)");
		hr->SetYTitle("PFJetID Efficiency");
		hr->GetYaxis()->SetTitleOffset(1.3);

		hr->SetTitle(eta_bins_legend[eta_bin_counter]);
		tot_entries = h_pT_probe_all[eta_bin_counter]->GetEntries();
		JetID_entries = h_pT_probe_JetID[eta_bin_counter]->GetEntries();	

		 
		int nbins = h_pT_probe_all[eta_bin_counter]->GetNbinsX(); 
		if(eta_bin_counter==5) cout<<"HT1050"<<endl;

		for(int ibin=0; ibin<nbins; ibin++)
		{ 
			x[ibin]=0.0; y[ibin]=0.0; eyu[ibin]=0.0; eyl[ibin]=0.0; ex[ibin]=0.0;
			if(h_pT_probe_JetID[eta_bin_counter]->GetBinContent(ibin)>0) //(for entries<1, the error bars are huge. For entries=1, error_bar=0.5)
			{  
				x[ibin] = h_pT_probe_all[eta_bin_counter]->GetBinCenter(ibin);
				y[ibin] = h_pT_probe_JetID[eta_bin_counter]->GetBinContent(ibin)/h_pT_probe_all[eta_bin_counter]->GetBinContent(ibin);
				eyu[ibin] = error1(h_pT_probe_all[eta_bin_counter]->GetBinContent(ibin),h_pT_probe_JetID[eta_bin_counter]->GetBinContent(ibin));
				eyl[ibin] = error2(h_pT_probe_all[eta_bin_counter]->GetBinContent(ibin),h_pT_probe_JetID[eta_bin_counter]->GetBinContent(ibin));
				ex[ibin] = h_pT_probe_all[eta_bin_counter]->GetBinWidth(ibin)/2;
			//	if(eta_bin_counter==5)cout<<ibin<<"	"<<x[ibin]<<"  "<< y[ibin] <<endl;
			}
		}//end of ibins

		tot_entries_HLT_PFJet400 = h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetEntries();
		JetID_entries_HLT_PFJet400 = h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->GetEntries();
		int nbins_HLT_PFJet400 = h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetNbinsX(); 


		for(int ibin=0; ibin<nbins; ibin++)
		{ 
			x_HLT_PFJet400[ibin]=0.0; y_HLT_PFJet400[ibin]=0.0; eyu_HLT_PFJet400[ibin]=0.0; eyl_HLT_PFJet400[ibin]=0.0; ex_HLT_PFJet400[ibin]=0.0;
			if(h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->GetBinContent(ibin)>0)   //(for entries<1, the error bars are huge. For entries=1, error_bar=0.5)
			{  
				x_HLT_PFJet400[ibin] = h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetBinCenter(ibin);
				y_HLT_PFJet400[ibin] = h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->GetBinContent(ibin)/h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetBinContent(ibin);
				eyu_HLT_PFJet400[ibin] = error1(h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetBinContent(ibin),h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->GetBinContent(ibin));
				eyl_HLT_PFJet400[ibin] = error2(h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetBinContent(ibin),h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->GetBinContent(ibin));
				ex_HLT_PFJet400[ibin] = h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetBinWidth(ibin)/2;
			//	if(eta_bin_counter==5)cout<<ibin<<"	"<<x_HLT_PFJet400[ibin]<<"  "<< y_HLT_PFJet400[ibin] <<endl;
		  	}
		}//end of ibins

		gr[eta_bin_counter] = new TGraphAsymmErrors(nbins, x, y,ex, ex,eyl,eyu);
		//gr[eta_bin_counter] = new TGraphAsymmErrors(h_pT_probe_JetID[eta_bin_counter],h_pT_probe_all[eta_bin_counter], "cl=0.683 b(1,1) mode"); // Bayesian
		gr[eta_bin_counter]->SetMarkerStyle(24);
		gr[eta_bin_counter]->SetMarkerColor(1);
		gr[eta_bin_counter]->SetMarkerSize(0.3);
		gr[eta_bin_counter]->SetLineColor(1);
		gr[eta_bin_counter]->Draw("p"); 
		gr1[eta_bin_counter] = new TGraphAsymmErrors(nbins, x_HLT_PFJet400, y_HLT_PFJet400,ex_HLT_PFJet400, ex_HLT_PFJet400,eyl_HLT_PFJet400,eyu_HLT_PFJet400);
		gr1[eta_bin_counter]->SetMarkerStyle(24);
		gr1[eta_bin_counter]->SetMarkerColor(2);
		gr1[eta_bin_counter]->SetMarkerSize(0.3);
		gr1[eta_bin_counter]->SetLineColor(2);
		gr1[eta_bin_counter]->Draw("p same"); 
	

		etamin=yBnd[eta_bin_counter];
		etamax=yBnd[eta_bin_counter+1];

		const char *seta = (etamin==0 ? Form("|y| < %1.2g",etamax) :
//		Form("%1.2g #leq |y| < %1.2g",etamin,etamax));
		Form("%1.2g #leq |y| < %1.2g",yBnd[eta_bin_counter],yBnd[eta_bin_counter+1]));
		TLatex *teta = new TLatex(0.68,0.96,seta); //cout<<seta<<endl; //0.69
		teta->SetNDC();
		teta->SetTextSize(0.05);
		teta->Draw();
		sel_eff = JetID_entries/tot_entries;
	//	cout<<"ybin = "<<eta_bin_counter<<endl;
		cout<<"PFHT1050: All events = "<<tot_entries<<" , selected events = "<<JetID_entries<<" , selection eff. = "<<sel_eff*100<<" error_yu  "<<error1(h_pT_probe_all[eta_bin_counter]->GetEntries(),h_pT_probe_JetID[eta_bin_counter]->GetEntries())<<" error_yl =  "<<error2(h_pT_probe_all[eta_bin_counter]->GetEntries(),h_pT_probe_JetID[eta_bin_counter]->GetEntries())<<endl;; 
		sel_eff_HLT_PFJet400 = JetID_entries_HLT_PFJet400/tot_entries_HLT_PFJet400;
		cout<<"HLT_PFJet400: All events = "<<tot_entries_HLT_PFJet400<<" , selected events = "<<JetID_entries_HLT_PFJet400<<" , selection eff. = "<<sel_eff_HLT_PFJet400*100<<" error_yu  "<<error1(h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetEntries(),h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->GetEntries())<<" error_yl =  "<<error2(h_pT_probe_all_HLT_PFJet400[eta_bin_counter]->GetEntries(),h_pT_probe_JetID_HLT_PFJet400[eta_bin_counter]->GetEntries())<<endl;;   
		cout <<"\n" <<endl;
	} //end of ybin

	cout << "PFHT1050 tot eff = " << high_trigger_numerator << "/" <<high_trigger_denominator <<" = "    << high_trigger_numerator / high_trigger_denominator << endl;
	cout << "HLT_ PFJet200 tot eff = " << low_trigger_numerator << "/" <<low_trigger_denominator <<" = " <<  low_trigger_numerator /  low_trigger_denominator << endl;
	cout <<"\n" <<endl;
	cout <<"\n" <<endl;


   // pad1->SaveAs("../rereco_plots/effLepton_btb_2triggers_withMjjCut_allEtaBins_newJetID_runE.png");
//	delete pad1->cd(8);
	//pad1->cd(8);
	pad1->cd(9);	
	//pad1->Close("8");
	TLegend *leg1 =new TLegend(.1, .1, .9, .9);//7899//4899
	leg1->SetTextSize(0.07);
	leg1->SetFillColor(0); 
	leg1->SetBorderSize(0);
	leg1->SetHeader("");
	leg1->AddEntry((TObject*)0,jet_type, "");
//	leg1->AddEntry((TObject*)0, "AK4 CHS", "");
//	leg1->AddEntry(gr[0], "PFHT1050", "L");
//	leg1->AddEntry(gr1[0], "PFJet200", "L");
	leg1->AddEntry(gr[0], "PFHT900", "L");
	leg1->AddEntry(gr1[0], "PFJet200", "L");

	//leg1->Draw();
	//pad1->cd(9);	
	leg1->Draw();

	char filename[256]; 
	sprintf(filename,"%s/%s/effLepton_btb_2triggers_allEtaBins_data2018_noMjjcut_%s.root",analyzer_path,output_directory,image_name);
	TFile *fout;
	if (Save_plots_and_histos)
	{	
		fout = new TFile(filename,"recreate");
		fout->cd();
		pad1->Write();
		for(unsigned iy=0;iy<eta_bins;iy++)
		{
			h_pT_probe_JetID[iy]->Write();
			h_pT_probe_all[iy]->Write();
			h_pT_probe_all_HLT_PFJet400[iy]->Write();
			h_pT_probe_JetID_HLT_PFJet400[iy]->Write();
		}

		fout->Close();
		sprintf(filename,"%s/%s/effLepton_btb_2triggers_allEtaBins_JetID_%s.png",analyzer_path,output_directory,image_name);
		pad1->SaveAs(filename);
		sprintf(filename,"%s/%s/effLepton_btb_2triggers_allEtaBins_JetID_%s.pdf",analyzer_path,output_directory,image_name);
		pad1->SaveAs(filename);

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
				//tight = ( fabs(eta)<=2.4 && nemf<0.9 && nhf < 0.9 && ( cm + nm)>1   );
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
//				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.9 && nm>1 ); 
				extracut_3_5 = ( fabs(eta)> 3.0 && fabs(eta)<=5.0 && nemf< 0.2 && nm>1 ); 
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






