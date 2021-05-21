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


void error1(double n1,double n2);
void error2(double n1,double n2);
 

void Calculate_total_efficiencies()
{

	gROOT->LoadMacro("setTDRStyle_teliko.C");
//	setTDRStyle_teliko(); 
	gStyle->SetOptStat(0);

//	TFile *f1 = new TFile ("/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/2018_Puppi_studies/Preliminary_JetID_efficiency_plots/effLepton_btb_2triggers_allEtaBins_data2018_noMjjcut_data_Puppi_2018_RunD_new_criteria_v2.root","READ");

	TFile *f1 = new TFile ("/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/UL_datasets_JetID/UL_2016/PUPPI/v15/nonAPV/effLepton_btb_2triggers_allEtaBins_data2018_noMjjcut_UL16_MCnonAPV_allpThatBins.root","READ");

	const int eta_bins =8;

	float etamin=0, etamax=0;
	char name[300]; 

	bool isData = true;
	  
	TH1D *h_pT_probe_all[eta_bins], *h_pT_probe_JetID[eta_bins];  
	TH1D *h_pT_probe_all_HLT_PFJet400[eta_bins], *h_pT_probe_JetID_HLT_PFJet400[eta_bins]; 

//	float yBnd[eta_bins+1]={0.0, 0.5, 1.0, 1.5, 2.0, 2.6, 2.7, 3.0, 5.0};
	float yBnd[eta_bins+1]={0.0, 0.5, 1.0, 1.5, 2.0, 2.4, 2.7, 3.0, 5.0};

	for(Int_t h=0; h<eta_bins;h++)
	{

		sprintf(name,"h_pT_probe_all%i",h);
		h_pT_probe_all[h] = (TH1D*)(f1->Get(name));

		sprintf(name,"h_pT_probe_JetID%i",h);
		h_pT_probe_JetID[h] = (TH1D*)(f1->Get(name));


		sprintf(name,"h_pT_probe_JetID_HLT_PFJet400%i",h);
		h_pT_probe_JetID_HLT_PFJet400[h] = (TH1D*)(f1->Get(name));

		sprintf(name,"h_pT_probe_all_HLT_PFJet400%i",h);
		h_pT_probe_all_HLT_PFJet400[h] = (TH1D*)(f1->Get(name));

	}

	double total_JetID, total_all, total_JetID_PFJet400, total_all_PFJet400;

	total_JetID = 0;
	total_all = 0;
	total_JetID_PFJet400 = 0;
	total_all_PFJet400 = 0;

	for(Int_t h=0; h<eta_bins;h++)
//	for(Int_t h=0; h<1;h++)
	{

		cout << "\n\n For " <<  yBnd[h]  <<" <= |#eta| < " << yBnd[h+1] << ": "<< endl;
		
		if (isData)
		{
			cout << "\n PFJet200 Efficiency = " <<  100*h_pT_probe_JetID_HLT_PFJet400[h]->Integral() / h_pT_probe_all_HLT_PFJet400[h]->Integral()<<" % "  << endl;
			cout << " PFHT1050 Efficiency = " <<  100*h_pT_probe_JetID[h]->Integral() / h_pT_probe_all[h]->Integral() <<" % "<< endl;
		}
		else
		{

			cout << "\n MC Efficiency = " <<  100*h_pT_probe_JetID[h]->Integral() / h_pT_probe_all[h]->Integral()<<" % "  << endl;

		}
	
//		cout << " For " <<  yBnd[h]  <<" < |#eta| #leq " << yBnd[h+1] << ": "<< endl;
//		cout << " PFHT1050 JetID Integral = " <<  h_pT_probe_JetID[h]->Integral() << " PFHT1050 All Integral = " << h_pT_probe_all[h]->Integral() << endl;
//		cout << " PFHT1050 JetID Integral = " <<  h_pT_probe_JetID_HLT_PFJet400[h]->Integral() << " PFHT1050 All Integral = " << h_pT_probe_all_HLT_PFJet400[h]->Integral() << endl;


		
		total_JetID = total_JetID + h_pT_probe_JetID[h]->Integral();
		total_all = total_all + h_pT_probe_all[h]->Integral();

		if (isData) total_JetID_PFJet400 = total_JetID_PFJet400 + h_pT_probe_JetID_HLT_PFJet400[h]->Integral();
		if (isData) total_all_PFJet400   = total_all_PFJet400 + h_pT_probe_all_HLT_PFJet400[h]->Integral();

	}

	cout << "\n\n"<< endl;
	if (isData) 	cout << " PFHT1050 Total Efficiency = " <<  100*total_JetID / total_all <<" % "<< endl;
	if (isData) 	cout << " PFJet200 Total Efficiency = " <<  100*total_JetID_PFJet400 / total_all_PFJet400<<" % "  << endl;
	if (!isData)    cout << " MC Total Efficiency = " <<  100*total_JetID / total_all << " % "  << endl;
}
