
txtTempl_cfg = '''[CaloTrijet2016]
variables = ['mjj[296.,296.,1000.]','th1x[0,0,1000]']

histoName = 'DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_70'

variables_range = ['mjj_Low[296.,1000.]', 'mjj_Blind[296.,1000.]', 'mjj_High[296.,1000.]']

combine_pdfs = ['RooXXXPdf::CaloTrijet2016_bkg(th1x,p1_CaloTrijet2016,p2_CaloTrijet2016,p3_CaloTrijet2016,p4_CaloTrijet2016,p5_CaloTrijet2016,p6_CaloTrijet2016,sqrts)',
 "EXPR::CaloTrijet2016_bkg_unbin('FUNCTION3',mjj,p0_CaloTrijet2016,p1_CaloTrijet2016,p2_CaloTrijet2016,p3_CaloTrijet2016,p4_CaloTrijet2016,p5_CaloTrijet2016,p6_CaloTrijet2016,sqrts)",
 'SUM::extDijetPdf(Ntot_bkg_CaloTrijet2016*CaloTrijet2016_bkg)']

#270, 296, 325, 354, 386, 
signal_mjj = [296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000]
#signal_mjj = [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]
'''

parametersNom = '''
combine_parameters = [
    'Ntot_bkg_CaloTrijet2016[3e+07]',
    'p0_CaloTrijet2016[1]',
    'p1_CaloTrijet2016[5]', 
    'p2_CaloTrijet2016[65]',
    'p3_CaloTrijet2016[-20]',
    'p4_CaloTrijet2016[0]',
    'p5_CaloTrijet2016[0]',
    'p6_CaloTrijet2016[0]',
    'sqrts[13000]',
    'CaloTrijet2016_bkg_norm[1]',
    'meff_CaloTrijet2016[-1]',
    'seff_CaloTrijet2016[-1]']
'''

parametersAlt = '''
combine_parameters = [
    'Ntot_bkg_CaloTrijet2016[3e+07]',
    'p0_CaloTrijet2016[1]',
    'p1_CaloTrijet2016[10]', 
    'p2_CaloTrijet2016[70]',
    'p3_CaloTrijet2016[0.5]',
    'p4_CaloTrijet2016[0]',
    'p5_CaloTrijet2016[0]',
    'p6_CaloTrijet2016[0]',
    'sqrts[13000]',
    'CaloTrijet2016_bkg_norm[1]',
    'meff_CaloTrijet2016[-1]',
    'seff_CaloTrijet2016[-1]']
'''

txtTempl_cc = '''
#include "RooFit.h"

#include "Riostream.h"
#include <TMath.h>
#include <cassert>
#include <cmath>
#include <math.h>

#include "../interface/RooXXXPdf.h"
#include "RooRealVar.h"
#include "RooConstVar.h"
#include "Math/Functor.h"
#include "Math/WrappedFunction.h"
#include "Math/IFunction.h"
#include "Math/Integrator.h"
#include "Math/GSLIntegrator.h"

using namespace std;
using namespace RooFit;

ClassImp(RooXXXPdf)
//---------------------------------------------------------------------------
RooXXXPdf::RooXXXPdf(const char *name, const char *title,
				   RooAbsReal& _th1x,  
				   RooAbsReal& _p1, 
                   RooAbsReal& _p2, 
				   RooAbsReal& _p3, 
                   RooAbsReal& _p4, 
                   RooAbsReal& _p5, 
                   RooAbsReal& _p6, 
                   RooAbsReal& _sqrts) : RooAbsPdf(name, title), 
//TH3* _Hnominal) : RooAbsPdf(name, title), 
  th1x("th1x", "th1x Observable", this, _th1x),
  p1("p1", "p1", this, _p1),
  p2("p2", "p2", this, _p2),
  p3("p3", "p3", this, _p3),
  p4("p4", "p4", this, _p4),
  p5("p5", "p5", this, _p5),
  p6("p6", "p6", this, _p6),
  sqrts("sqrts", "sqrts", this, _sqrts),
  xBins(0),
  xMax(0),
  xMin(0),
  relTol(2E-32),
  absTol(2E-32)
{
  memset(&xArray, 0, sizeof(xArray));
}
//---------------------------------------------------------------------------
RooXXXPdf::RooXXXPdf(const RooXXXPdf& other, const char* name) :
   RooAbsPdf(other, name), 
   th1x("th1x", this, other.th1x),  
   p1("p1", this, other.p1),
   p2("p2", this, other.p2),
   p3("p3", this, other.p3),
   p4("p4", this, other.p4),
   p5("p5", this, other.p5),
   p6("p6", this, other.p6),
   sqrts("sqrts", this, other.sqrts),
   xBins(other.xBins),
   xMax(other.xMax),
   xMin(other.xMin),
   relTol(other.relTol),
   absTol(other.absTol)
{
  //memset(&xArray, 0, sizeof(xArray));
  for (Int_t i=0; i<xBins+1; i++){
    xArray[i] = other.xArray[i];
  }
}
//---------------------------------------------------------------------------
void RooXXXPdf::setTH1Binning(TH1* _Hnominal){
  xBins = _Hnominal->GetXaxis()->GetNbins();
  xMin = _Hnominal->GetXaxis()->GetBinLowEdge(1);
  xMax = _Hnominal->GetXaxis()->GetBinUpEdge(xBins);
  memset(&xArray, 0, sizeof(xArray));
  for (Int_t i=0; i<xBins+1; i++){
    xArray[i] =  _Hnominal->GetXaxis()->GetBinLowEdge(i+1);
  }
}
//---------------------------------------------------------------------------
void RooXXXPdf::setRelTol(double _relTol){
  relTol = _relTol;
}
//---------------------------------------------------------------------------
void RooXXXPdf::setAbsTol(double _absTol){
  absTol = _absTol;
}
//---------------------------------------------------------------------------
Double_t RooXXXPdf::evaluate() const
{
  Double_t integral = 0.0;
  

  Int_t iBin = (Int_t) th1x;
  if(iBin < 0 || iBin >= xBins) {
    //cout << "in bin " << iBin << " which is outside of range" << endl;
    return 0.0;
  }

  
  Double_t xLow = xArray[iBin];
  Double_t xHigh = xArray[iBin+1];
    
  // define the function to be integrated numerically
  XXXFunction func;
  double params[NNN];
  params[0] = sqrts;    
  params[1] = p1;
  params[2] = p2;       
  params[3] = p3;
  params[4] = p4;       
  params[5] = p5;
  params[6] = p6;
  func.SetParameters(params);

  ROOT::Math::Integrator ig(ROOT::Math::IntegrationOneDim::kADAPTIVE,absTol,relTol);
  ig.SetFunction(func,false);

  
  integral = ig.Integral(xLow,xHigh);
  //Double_t total_integral = ig.Integral(xMin,xMax);

  if (integral>0.0) {
    return integral;
  } else return 0;

}

// //---------------------------------------------------------------------------
Int_t RooXXXPdf::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName) const{
  if (matchArgs(allVars, analVars, th1x)) return 1;
  return 0;
}

// //---------------------------------------------------------------------------
Double_t RooXXXPdf::analyticalIntegral(Int_t code, const char* rangeName) const{

   Double_t th1xMin = th1x.min(rangeName); Double_t th1xMax = th1x.max(rangeName);
   Int_t iBinMin = (Int_t) th1xMin; Int_t iBinMax = (Int_t) th1xMax;


   Double_t integral = 0.0;
      
   //cout <<  "iBinMin = " << iBinMin << ",iBinMax = " << iBinMax << endl;

   
   // define the function to be integrated numerically  
   XXXFunction func;
   double params[NNN+1];
   params[0] = sqrts;    
   params[1] = p1;
   params[2] = p2;       
   params[3] = p3;
   params[4] = p4;       
   params[5] = p5;
   params[6] = p6;
   func.SetParameters(params);

   
  ROOT::Math::Integrator ig(ROOT::Math::IntegrationOneDim::kADAPTIVE,absTol,relTol);
  ig.SetFunction(func,false);
    

   if (code==1 && iBinMin<=0 && iBinMax>=xBins){
     integral = ig.Integral(xMin,xMax);
     
   }
   else if(code==1) { 
     for (Int_t iBin=iBinMin; iBin<iBinMax; iBin++){
       
       if(iBin < 0 || iBin >= xBins) {
	 integral += 0.0;
       }
       else{	 
	 Double_t xLow = xArray[iBin];
	 Double_t xHigh = xArray[iBin+1];    
	 integral += ig.Integral(xLow,xHigh);
       }
     }
   } else {
     cout << "WARNING IN RooXXXPdf: integration code is not correct" << endl;
     cout << "                           what are you integrating on?" << endl;
     return 1.0;
   }

   if (integral>0.0) {
     
     return integral;
   } else return 1.0;
}
'''


txtTempl_h = '''
#ifndef HiggsAnalysis_CombinedLimit_RooXXXPdf_h
#define HiggsAnalysis_CombinedLimit_RooXXXPdf_h
//---------------------------------------------------------------------------
#include "RooAbsPdf.h"
#include "RooConstVar.h"
#include "RooRealProxy.h"
//---------------------------------------------------------------------------
class RooRealVar;
class RooAbsReal;

#include "Riostream.h"
#include "TMath.h"
#include <TH1.h>
#include "Math/SpecFuncMathCore.h"
#include "Math/SpecFuncMathMore.h"
#include "Math/Functor.h"
#include "Math/WrappedFunction.h"
#include "Math/IFunction.h"
#include "Math/Integrator.h"

//---------------------------------------------------------------------------
class RooXXXPdf : public RooAbsPdf
{
public:
   RooXXXPdf() {} ;
   RooXXXPdf(const char *name, const char *title,
        RooAbsReal& _th1x, 
        RooAbsReal& _p1,
        RooAbsReal& _p2, 
        RooAbsReal& _p3, 
        RooAbsReal& _p4, 
        RooAbsReal& _p5,
        RooAbsReal& _p6,
        RooAbsReal& _sqrts);
   RooXXXPdf(const RooXXXPdf& other,
      const char* name = 0);
   void setTH1Binning(TH1* _Hnominal);
   void setAbsTol(double _absTol);
   void setRelTol(double _relTol);
   virtual TObject* clone(const char* newname) const { return new RooXXXPdf(*this,newname); }
   inline virtual ~RooXXXPdf() { }

   Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const;
   Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const;

protected:   

   RooRealProxy th1x;        // dependent variable
   RooRealProxy p1;       // p1
   RooRealProxy p2;        // p2
   RooRealProxy p3;        // p3
   RooRealProxy p4;        // p4
   RooRealProxy p5;        // p5
   RooRealProxy p6;        // p6
   RooRealProxy sqrts;        // sqrts
   Int_t xBins;        // X bins
   Double_t xArray[2000]; // xArray[xBins+1]
   Double_t xMax;        // X max
   Double_t xMin;        // X min
   Double_t relTol;      //relative tolerance for numerical integration
   Double_t absTol;      //absolute tolerance for numerical integration

   Double_t evaluate() const;
private:
   ClassDef(RooXXXPdf,1) // RazorXXXPdf function
    
};
//---------------------------------------------------------------------------
#endif

#include "Math/IFunction.h"
#include "Math/IParamFunction.h"
 
class XXXFunction: public ROOT::Math::IParametricFunctionOneDim
{
private:
   const double *pars;
 
public:
   double DoEvalPar(double x,const double* p) const
   {
     double pdf = FUNCTION1;
     return pdf;
   }
   double DoEval(double x) const
   {
     double pdf = FUNCTION2;
     return pdf;
   }
 
   ROOT::Math::IBaseFunctionOneDim* Clone() const
   {
      return new XXXFunction();
   }
 
   const double* Parameters() const
   {
      return pars;
   }
 
   void SetParameters(const double* p)
   {
      pars = p;
   }
 
   unsigned int NPar() const
   {
      return NNN;
   }
};
'''


def getNparam(txt):
    txt = txt.replace("]","[")
    words = txt.split("[")
    max_ = -1
    for word in words:
        try:
            max_ = max(int(word),max_)
        except:
            pass
    return max_+1

def function3(function):
    function = function.replace("pars[0]","sqrts")
    function = function.replace("pars","p")
    function = function.replace("x","mjj")
    function = function.replace("emjjp","exp")
    function = function.replace("Mamjj","Max")
    function = function.replace("[","")
    function = function.replace("]","_CaloTrijet2016")
    function = "p0_CaloTrijet2016 * " + function
    return function

def fixCfg(cfg):
    for n in range(nparams,10): cfg = cfg.replace(",p%s_CaloTrijet2016"%(str(n)),"")
    cfg = cfg.replace('// "EXPR::',' "EXPR::')
    cfg = cfg.replace("//combine_pdfs","combine_pdfs")
    cfg = cfg.replace("//","#")
    return cfg

def updateTxt(txt):
    lines = txt.split("\n")
    for i,line in enumerate(lines):
        lines[i] = lines[i].replace("NNN+1",str(nparams+1))
        lines[i] = lines[i].replace("NNN",str(nparams))
        lines[i] = lines[i].replace("XXX",Tag)
        lines[i] = lines[i].replace("FUNCTION1",function.replace("pars","p"))
        lines[i] = lines[i].replace("FUNCTION2",function)
        lines[i] = lines[i].replace("FUNCTION3",function3(function))
        if ("p7" in lines[i] and nparams <= 6) or \
        ("p6" in lines[i] and nparams <= 6) or \
        ("p5" in lines[i] and nparams <= 5) or \
        ("p4" in lines[i] and nparams <= 4) or \
        ("p3" in lines[i] and nparams <= 3) or \
        ("p2" in lines[i] and nparams <= 2):
            lines[i] = "//" + lines[i]
    txt = "\n".join(lines)
    return txt
    

'''
("exp(pars[2]*x/pars[0]) * 1/pow(x/pars[0],pars[1])","DijetFisherNom3"),
("exp(pars[2]*x/pars[0]) * TMath::Max((- 1 + x/pars[0]*pars[3]),0.)/pow(x/pars[0],pars[1])","DijetFisherNom4"),
("exp(pars[2]*x/pars[0]) * TMath::Max((- 1 + x/pars[0]*pars[3] + pow(x/pars[0],3)*pars[4]),0.)/pow(x/pars[0],pars[1])","DijetFisherNom5"),
("exp(pars[2]*x/pars[0]) * TMath::Max((- 1 + x/pars[0]*pars[3] + pow(x/pars[0],3)*pars[4] + pow(x/pars[0],5)*pars[5]),0.)/pow(x/pars[0],pars[1])","DijetFisherNom6"),
("exp(pars[2]*x/pars[0]) * TMath::Max((- 1 + x/pars[0]*pars[3] + pow(x/pars[0],3)*pars[4] + pow(x/pars[0],5)*pars[5] + pow(x/pars[0],7)*pars[6]),0.)/pow(x/pars[0],pars[1])","DijetFisherNom7"),
'''


functions = [
("exp(log(pars[2] * x/pars[0] - 1))/pow(x/pars[0],pars[1])","DijetFisherNom3"),
("exp(log(pars[2] * x/pars[0] - 1) + pars[3]*x/pars[0])/pow(x/pars[0],pars[1])","DijetFisherNom4"),
("exp(log(pars[2] * x/pars[0] - 1) + pars[3]*x/pars[0] + pars[4]*pow(x/pars[0],2))/pow(x/pars[0],pars[1])","DijetFisherNom5"),
("exp(log(pars[2] * x/pars[0] - 1) + pars[3]*x/pars[0] + pars[4]*pow(x/pars[0],2) + pars[5]*pow(x/pars[0],3))/pow(x/pars[0],pars[1])","DijetFisherNom6"),
("exp(log(pars[2] * x/pars[0] - 1) + pars[3]*x/pars[0] + pars[4]*pow(x/pars[0],2) + pars[5]*pow(x/pars[0],3) + pars[6]*pow(x/pars[0],4))/pow(x/pars[0],pars[1])","DijetFisherNom7"),
("exp(log(pars[2] * x/pars[0] - 1))/pow(x/pars[0],pars[1]) ","DijetFisherAlt3"),
("exp(log(pars[2] * x/pars[0] - 1))/pow(x/pars[0],(pars[1] + pars[3]*log(x/pars[0]))) ","DijetFisherAlt4"),
("exp(log(pars[2] * x/pars[0] - 1))/pow(x/pars[0],(pars[1] + pars[3]*log(x/pars[0]) + pars[4]*pow(log(x/pars[0]),2))) ","DijetFisherAlt5"),
("exp(log(pars[2] * x/pars[0] - 1))/pow(x/pars[0],(pars[1] + pars[3]*log(x/pars[0]) + pars[4]*pow(log(x/pars[0]),2) + pars[5]*pow(log(x/pars[0]),3))) ","DijetFisherAlt6"),
("exp(log(pars[2] * x/pars[0] - 1))/pow(x/pars[0],(pars[1] + pars[3]*log(x/pars[0]) + pars[4]*pow(log(x/pars[0]),2) + pars[5]*pow(log(x/pars[0]),3) + pars[6]*pow(log(x/pars[0]),4))) ","DijetFisherAlt7"),
    ]

for function,Tag in functions:
    nparams = getNparam(function)
    fileName_h = "Roo"+Tag+"Pdf.h"
    fileName_cc = "Roo"+Tag+"Pdf.cc"
    fileName_cfg = "dijet_isr_"+Tag+".config"
    file_h = open(fileName_h,'w')
    file_cc = open(fileName_cc,'w')
    file_cfg = open(fileName_cfg,'w')

    txt_h = updateTxt(txtTempl_h)
    txt_cc = updateTxt(txtTempl_cc)
    txt_cfg = updateTxt(txtTempl_cfg)
    txt_cfg = fixCfg(txt_cfg)
    if "Nom" in Tag:
        txt_cfg += parametersNom
    elif "Alt" in Tag:
        txt_cfg += parametersAlt
    
    file_h.write(txt_h)
    file_cc.write(txt_cc)
    file_cfg.write(txt_cfg)
    print("cp %s $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/src/%s"%(fileName_cc,fileName_cc))
    print("cp %s $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/interface/%s"%(fileName_h,fileName_h))
    print("cp %s $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/config/%s"%(fileName_cfg,fileName_cfg))
    
    file_cc.close()
    file_h.close()
    file_cfg.close()

print("""
### Remember to update classes_def.xml and classes.h ###

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/
scram b -j8
cd -
#cd ..

python python/BinnedFit.py -c config/dijet_isr_%s.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/ --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20

"""%(functions[0][1]))
