
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
TGraphAsymmErrors* GetEfficiencyGraph(TH1D* numerator, TH1D* denominator );
TGraphAsymmErrors* GetEfficiencyScaleFactor(TGraphAsymmErrors* numerator, TGraphAsymmErrors* denominator );
void PrintEfficiencyScaleFactors( TH1D* h_data_num, TH1D* h_data_den, TH1D* h_MC_num, TH1D* h_MC_den );
double PropagateRatioError (double num, double numErr, double den, double denErr);

void Get_JetID_Efficiency_Scale_Factors()
{

	TFile *fdata = new TFile ("/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/UL_datasets_JetID/UL_2016/PUPPI/v15/nonAPV/First_try/effLepton_btb_2triggers_allEtaBins_data2018_noMjjcut_allRuns.root","READ"); //data 

	TFile *fMC = new TFile ("/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/UL_datasets_JetID/UL_2016/PUPPI/v15/nonAPV/effLepton_btb_2triggers_allEtaBins_data2018_noMjjcut_UL16_MCnonAPV_allpThatBins.root","READ"); // mc 

	bool Save_plots = true;
	char analyzer_path[300] = "/afs/cern.ch/work/d/dkarasav/public/CMSSW_10_1_5/src/CMSDIJET/DijetRootTreeAnalyzer/"; 
	char output_directory[300] = "UL_datasets_JetID/UL_2016/PUPPI/v15/nonAPV/";     
	char image_name[300] = "_MC_ScaleFactors_PUPPI"; 
	char legend_text[100] = "AK4 PUPPI";

	const int eta_bins = 8;
	gROOT->LoadMacro("setTDRStyle_teliko.C");
	setTDRStyle_teliko(); 
	gStyle->SetOptStat(0);


	float etamin=0, etamax=0;
	char name[300]; 

	TH1D *h_pT_probe_all[eta_bins], *h_pT_probe_JetID[eta_bins];  
	TH1D *h_pT_probe_all_HLT_PFJet400[eta_bins], *h_pT_probe_JetID_HLT_PFJet400[eta_bins]; 

	TH1D *h_pT_probe_all_MC[eta_bins], *h_pT_probe_JetID_MC[eta_bins];  
	TH1D *h_pT_probe_all_HLT_PFJet400_MC[eta_bins], *h_pT_probe_JetID_HLT_PFJet400_MC[eta_bins];

	TGraphAsymmErrors *eff_data[eta_bins], *eff_PFJet400_data[eta_bins]; 
	TGraphAsymmErrors *eff_MC[eta_bins], *eff_PFJet400_MC[eta_bins];  
 	TGraphAsymmErrors *ScaleFactor[eta_bins], *ScaleFactor_PFJet400[eta_bins]; 

	float yBnd[eta_bins+1]={0.0, 0.5, 1.0, 1.5, 2.0, 2.4, 2.7, 3.0, 5.0};
//	float yBnd[eta_bins+1]={0.0, 0.5, 1.0, 1.5, 2.0, 2.6, 2.7, 3.0, 5.0};

//	char eta_bins_legend[eta_bins][25] = { "|#eta|<0.5", "0.5 #leq |#eta| < 1.0", "1.0 #leq |#eta| < 1.5", "1.5 #leq |#eta| < 2.0", "2.0 #leq |#eta| < 2.6","2.6 #leq |#eta| < 2.7" , "2.7 #leq |#eta| < 3.0" , "3.0 #leq |#eta| < 5.0" }; 

	char eta_bins_legend[eta_bins][25] = { "|#eta|<0.5", "0.5 #leq |#eta| < 1.0", "1.0 #leq |#eta| < 1.5", "1.5 #leq |#eta| < 2.0", "2.0 #leq |#eta| < 2.4","2.4 #leq |#eta| < 2.7" , "2.7 #leq |#eta| < 3.0" , "3.0 #leq |#eta| < 5.0" }; 

	for(Int_t h=0; h<eta_bins;h++)
	{

		sprintf(name,"h_pT_probe_all%i",h);
		h_pT_probe_all[h] = (TH1D*)(fdata->Get(name));

		sprintf(name,"h_pT_probe_JetID%i",h);
		h_pT_probe_JetID[h] = (TH1D*)(fdata->Get(name));


		sprintf(name,"h_pT_probe_JetID_HLT_PFJet400%i",h);
		h_pT_probe_JetID_HLT_PFJet400[h] = (TH1D*)(fdata->Get(name));

		sprintf(name,"h_pT_probe_all_HLT_PFJet400%i",h);
		h_pT_probe_all_HLT_PFJet400[h] = (TH1D*)(fdata->Get(name));


		sprintf(name,"h_pT_probe_all%i",h);
		h_pT_probe_all_MC[h] = (TH1D*)(fMC->Get(name));

		sprintf(name,"h_pT_probe_JetID%i",h);
		h_pT_probe_JetID_MC[h] = (TH1D*)(fMC->Get(name));


		sprintf(name,"h_pT_probe_JetID_HLT_PFJet400%i",h);
		h_pT_probe_JetID_HLT_PFJet400_MC[h] = (TH1D*)(fMC->Get(name));

		sprintf(name,"h_pT_probe_all_HLT_PFJet400%i",h);
		h_pT_probe_all_HLT_PFJet400_MC[h] = (TH1D*)(fMC->Get(name));

	}

	for (int h=0; h<eta_bins; h++)
	{
		eff_data[h] = GetEfficiencyGraph(h_pT_probe_JetID[h] , h_pT_probe_all[h] );
		eff_PFJet400_data[h] = GetEfficiencyGraph(h_pT_probe_JetID_HLT_PFJet400[h] , h_pT_probe_all_HLT_PFJet400[h] );
		eff_MC[h] = GetEfficiencyGraph(h_pT_probe_JetID_MC[h] , h_pT_probe_all_MC[h] );
		eff_PFJet400_MC[h] = GetEfficiencyGraph(h_pT_probe_JetID_HLT_PFJet400_MC[h] , h_pT_probe_all_HLT_PFJet400_MC[h] );

		ScaleFactor[h] = GetEfficiencyScaleFactor( eff_data[h] , eff_MC[h]);
		ScaleFactor_PFJet400[h] = GetEfficiencyScaleFactor( eff_PFJet400_data[h] , eff_PFJet400_MC[h]);
	
		cout << "\n\n For " <<  yBnd[h]  <<" <= |#eta| < " << yBnd[h+1] << ": "<< endl;
		cout << "\n Trigger PFJet200 : " ;
		PrintEfficiencyScaleFactors( h_pT_probe_JetID_HLT_PFJet400[h] , h_pT_probe_all_HLT_PFJet400[h], h_pT_probe_JetID_HLT_PFJet400_MC[h] , h_pT_probe_all_HLT_PFJet400_MC[h] );
		cout << " Trigger PFHT1050 : " ;
		PrintEfficiencyScaleFactors( h_pT_probe_JetID[h] , h_pT_probe_all[h], h_pT_probe_JetID_MC[h] , h_pT_probe_all_MC[h] );
	}


	TCanvas *pad1 = new TCanvas("pad1", "",1);
	pad1->Divide(3,3);

	for (int h=0; h<eta_bins; h++)
	{
		pad1->cd(h+1);
		// draw a frame to define the range, in order to plot many graphs in the same pad
		TH1F *hr;
		if(h < 4) hr = pad1->cd(h+1)->DrawFrame(0,0.85,3000,1.15);
		else if(h == 4) hr = pad1->cd(h+1)->DrawFrame(0,0.85,2000,1.15);
		else  hr = pad1->cd(h+1)->DrawFrame(0,0.85,800,1.15);
		//if(h==5) TH1F *hr = pad1->cd(h+1)->DrawFrame(0,0.8,3000,1.2);
		//if(h==6) TH1F *hr = pad1->cd(h+1)->DrawFrame(0,0.0,3000,1.5);
		hr->SetXTitle("jet p_{T} (GeV)");
		hr->SetYTitle("PFJetID Scale Factor");
		hr->GetYaxis()->SetTitleOffset(1.3);

		hr->SetTitle(eta_bins_legend[h]);

		ScaleFactor[h]->SetMarkerStyle(24);
		ScaleFactor[h]->SetMarkerColor(1);
		ScaleFactor[h]->SetMarkerSize(0.3);
		ScaleFactor[h]->SetLineColor(1);
		ScaleFactor[h]->Draw("p"); 

		ScaleFactor_PFJet400[h]->SetMarkerStyle(24);
		ScaleFactor_PFJet400[h]->SetMarkerColor(2);
		ScaleFactor_PFJet400[h]->SetMarkerSize(0.3);
		ScaleFactor_PFJet400[h]->SetLineColor(2);
		ScaleFactor_PFJet400[h]->Draw("p same"); 

		etamin=yBnd[h];
		etamax=yBnd[h+1];

		const char *seta = (etamin==0 ? Form("|y| < %1.2g",etamax) :
//		Form("%1.2g #leq |y| < %1.2g",etamin,etamax));
		Form("%1.2g #leq |y| < %1.2g",yBnd[h],yBnd[h+1]));
		TLatex *teta = new TLatex(0.68,0.96,seta); //cout<<seta<<endl; //0.69
		teta->SetNDC();
		teta->SetTextSize(0.05);
		teta->Draw();

	}

	TLegend *leg1 =new TLegend(.1, .1, .9, .9);//7899//4899
	leg1->SetTextSize(0.07);
	leg1->SetFillColor(0); 
	leg1->SetBorderSize(0);
	leg1->SetHeader("");
	leg1->AddEntry((TObject*)0, legend_text, "");
//	leg1->AddEntry((TObject*)0, "MC AK4 CHS", "");
	leg1->AddEntry(ScaleFactor[0], "PFHT900", "L");
//	leg1->AddEntry(ScaleFactor[0], "PFHT1050", "L");
	leg1->AddEntry(ScaleFactor_PFJet400[0], "PFJet200", "L");
	pad1->cd(eta_bins+1);
	leg1->Draw();	

	if (Save_plots)
	{
		char filename[256];
		sprintf(filename,"%s/%s/ScaleFactors_JetID_%s.png",analyzer_path,output_directory,image_name);
		pad1->SaveAs(filename);
		sprintf(filename,"%s/%s/ScaleFactors_JetID_%s.pdf",analyzer_path,output_directory,image_name);
		pad1->SaveAs(filename);
	}

}




TGraphAsymmErrors* GetEfficiencyGraph(TH1D* numerator, TH1D* denominator )
{
	const int nbins = denominator->GetNbinsX(); 
	double eff_x[nbins], eff_y[nbins], eff_eyu[nbins], eff_eyl[nbins], eff_ex[nbins];

	for (int i=0; i<nbins; i++)
	{
		eff_x[i] = 0.0; eff_y[i] = 0.0; eff_eyu[i] = 0.0; eff_eyl[i] = 0.0; eff_ex[i] = 0.0;

		if( numerator->GetBinContent(i)>0 )
		{
			eff_x[i]   = denominator->GetBinCenter(i);
			eff_y[i]   = numerator->GetBinContent(i) / denominator->GetBinContent(i);
			eff_eyu[i] = error1(denominator->GetBinContent(i), numerator->GetBinContent(i) );
			eff_eyl[i] = error2(denominator->GetBinContent(i), numerator->GetBinContent(i) );
			eff_ex[i]  = denominator->GetBinWidth(i)/2;
		}
	}
	TGraphAsymmErrors *Eff = new TGraphAsymmErrors( nbins, eff_x, eff_y,eff_ex, eff_ex, eff_eyl, eff_eyu );	

	return Eff;
}



TGraphAsymmErrors* GetEfficiencyScaleFactor(TGraphAsymmErrors* numerator, TGraphAsymmErrors* denominator )
{
	const int nbins = denominator->GetN(); 
	double SF_x[nbins], SF_y[nbins], SF_eyu[nbins], SF_eyl[nbins], SF_ex[nbins];
	double num_x[nbins], num_y[nbins], num_eyu[nbins], num_eyl[nbins], num_ex[nbins];
	double den_x[nbins], den_y[nbins], den_eyu[nbins], den_eyl[nbins];

	for (int i=0; i<nbins; i++)
	{
		SF_y[i] = 0.0; SF_eyu[i] = 0.0; SF_eyl[i] = 0.0; 
		
		numerator->GetPoint(i,num_x[i],num_y[i]); 
		num_eyu[i] = numerator->GetErrorYhigh(i);
		num_eyl[i] = numerator->GetErrorYlow(i);
		num_ex[i] = numerator->GetErrorXhigh(i);

		denominator->GetPoint(i,den_x[i],den_y[i]); 
		den_eyu[i] = denominator->GetErrorYhigh(i);
		den_eyl[i] = denominator->GetErrorYlow(i);

		SF_ex[i] = num_ex[i];
		SF_x[i] = num_x[i];

		if( den_y[i] > 0 )
		{
			SF_y[i]   = num_y[i] / den_y[i];
	//		SF_eyu[i] = PropagateRatioError( num_y[i],num_eyu[i],den_y[i],den_eyu[i]);
			SF_eyu[i] = PropagateRatioError( num_y[i],num_eyl[i],den_y[i],den_eyl[i]); // conservative approach: take into account only the larger error
			SF_eyl[i] = PropagateRatioError( num_y[i],num_eyl[i],den_y[i],den_eyl[i]);
		}
	}

	TGraphAsymmErrors *SF = new TGraphAsymmErrors( nbins, SF_x, SF_y,SF_ex, SF_ex, SF_eyl, SF_eyu );	

	return SF;
}

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

double PropagateRatioError (double num, double numErr, double den, double denErr)
{


	if (den>0 || den<0)
	{
		double Error = sqrt( pow( numErr/den ,2) + pow( num*denErr/(den*den) , 2) );
		return Error;
	}
	else 
	{
		cout << "Warning!  Numerator is zero! Will return 0 as error.";
		return 0;
	}
}

void PrintEfficiencyScaleFactors( TH1D* h_data_num, TH1D* h_data_den, TH1D* h_MC_num, TH1D* h_MC_den )
{

	double data_num, data_den, dataErr_num, dataErr_den;
	double MC_num, MC_den, MCErr_num, MCErr_den;
	double ScaleF, ScaleF_Err;


	data_num = h_data_num->Integral();
	data_den = h_data_den->Integral();

	MC_num = h_MC_num->Integral();
	MC_den = h_MC_den->Integral();

	dataErr_num = sqrt(data_num);
	dataErr_den = sqrt(data_den);


	double data_eff = data_num / data_den ;
	double data_effErr =  PropagateRatioError(data_num, dataErr_num,data_den, dataErr_den);

	double MC_eff = MC_num / MC_den ;
	double MC_effErr =  PropagateRatioError(MC_num, MCErr_num,MC_den, MCErr_den);

	ScaleF = data_eff / MC_eff;
	ScaleF_Err = PropagateRatioError(data_eff, data_effErr, MC_eff, MC_effErr );

	cout << " Scale Factor = " << ScaleF << " +- " << ScaleF_Err << endl;



}



