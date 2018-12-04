# https://root.cern.ch/download/doc/RooFit_Users_Manual_2.91-33.pdf

#[sdonato@t3ui03 DijetRootTreeAnalyzer]$ combine signal_bias_silvio/qq/fiveparam_silvio6/dijet_combine_qq_500_lumi-27.637_CaloTrijet2016.txt -M MaxLikelihoodFit  --setPhysicsModelParameters pdf_index=1  --rMin -10 --rMax 10 --freezeNuisances pdf_index -v 2

import ROOT


c1 = ROOT.TCanvas("c1")


#-rw-r--r-- 1 sdonato uniz-higgs  828 Aug  3 15:36 higgsCombineqq_475_lumi-27.637_r-1.000_CaloTrijet2016_silvio6_atlas6.GenerateOnly.mH120.123456.root
#-rw-r--r-- 1 sdonato uniz-higgs 6.1K Aug  3 15:37 higgsCombineqq_425_lumi-27.637_r-1.000_CaloTrijet2016_silvio6_atlas6.MaxLikelihoodFit.mH120.123456.root


#file_ = ROOT.TFile.Open("/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/signal_bias_test/higgsCombineqq_300_lumi-35.900_r-1.000_CaloTrijet2016_fiveparam_fiveparam.MaxLikelihoodFit.mH120.123456.root")

#fileFit = ROOT.TFile.Open("fits_trijet_silvio_2018/DijetFitResults_CaloTrijet2016.root")
#fileFit = ROOT.TFile.Open("signal_bias_silvio/qq/modexp_silvio6/dijet_combine_qq_600_lumi-27.637_CaloTrijet2016.root")

#fileFit = ROOT.TFile.Open("signal_bias_silvio/qq/fiveparam_silvio6/dijet_combine_qq_500_lumi-27.637_CaloTrijet2016.root")
#fileFit = ROOT.TFile.Open("fits_trijet_silvio_2018/DijetFitResults_CaloTrijet2016.root")

#fileFit = ROOT.TFile.Open("signal_bias_silvio_test/dijet_combine_qq_300_lumi-27.637_CaloTrijet2016.root")
fileFit = ROOT.TFile.Open("dijet_combine_qq_500_lumi-27637000.000_CaloTrijet2016.root")


#fileToys = ROOT.TFile.Open("signal_bias_silvio/qq/atlas6_silvio6/higgsCombineqq_600_lumi-27.637_r-1.000_CaloTrijet2016_silvio6_atlas6.MaxLikelihoodFit.mH120.123456.root")
#fileToys = ROOT.TFile.Open("signal_bias_silvio/qq/fiveparam_silvio6/dijet_combine_qq_500_lumi-27.637_CaloTrijet2016.root")
#toys = fileToys.Get("toys")
#toy1 = toys.Get("toy_1")

try:
    w = fileFit.Get("w")
    print("\nWorkSpace:")
    w.Print()
    print()
except:
    try:
        w = fileFit.Get("wCaloTrijet2016")
        print("\nWorkSpace:")
        w.Print()
        print()
    except:
        print("CANNOT OPEN WORKSPACE!!!")

#print("\toy5:")
#toy1.Print()
#print()


mjj = w.var("mjj")
th1x = w.var("th1x")

data = w.data("data_obs")
#asimov = w.data("_Asymptotic_asimovDataset_")

function = w.pdf("extDijetPdf")

try:
    sig_shape = w.pdf("shapeSig_CaloTrijet2016_CaloTrijet2016_qq_morph")
    bkg_shape = w.pdf("shapeBkg_CaloTrijet2016_bkg_CaloTrijet2016")
    bkgsig_shape = w.pdf("pdf_binCaloTrijet2016")
except:
    pass

try:
    old_nll = w.genobj("nll_extDijetPdf_data_obs")
    old_nll.Print()
except:
    pass
    
#m2 = ROOT.RooMinimizer(function)
#m2.setStrategy(2)
#m2.setMaxFunctionCalls(100000 * 10000)
#m2.setMaxIterations(100000 * 10000)
#migrad_status = m2.minimize('Minuit2','migrad')


#Ntot_bkg_CaloTrijet2016 = w.var("Ntot_bkg_CaloTrijet2016")
#print("Ntot_bkg_CaloTrijet2016 = ", Ntot_bkg_CaloTrijet2016.getVal())

frame = th1x.frame()
#frame = mjj.frame()


#toy1.plotOn(frame)

try:
    pdf_index = w.variable("pdf_index")
except:
    pass

#Ntot_bkg_CaloTrijet2016.setVal(1)

#varName = "p2_CaloTrijet2016"
#w.var(varName).setVal(w.var(varName).getVal() )
#function.fitTo(data)

#data.plotOn(frame)
#asimov.plotOn(frame)

#sig_shape.plotOn(frame)
#bkg_shape.plotOn(frame)
#bkgsig_shape.fitTo(asimov)


function.fitTo(data)

data.plotOn(frame)

function.plotOn(frame)

#function.plotOn(frame)
#mjj.plotOn(frame)
#th1x.plotOn(frame)

c1.SetLogy()
frame.Draw("")

1./0

#model_s = w.pdf("model_s")
model_s.Print()

frac = ROOT.RooRealVar("frac","frac",0.5,0.0,1.0)
 
nll = bkgsig_shape.createNLL(asimov,ROOT.RooFit.Range("All"),ROOT.RooFit.Extended(True),ROOT.RooFit.Offset(True))
n_exp_binCaloTrijet2016_proc_CaloTrijet2016_qq = w.var("n_exp_binCaloTrijet2016_proc_CaloTrijet2016_qq")
pll_frac = nll.createProfile(frac) ;
frame2 = n_exp_binCaloTrijet2016_proc_CaloTrijet2016_qq.frame()

c2 = ROOT.TCanvas("c1")
frame2.Draw("")

#print("Ntot_bkg_CaloTrijet2016 = ", Ntot_bkg_CaloTrijet2016.getVal())

'''
nll = pdf.createNLL(data,rt.RooFit.Range(fitRange),rt.RooFit.Extended(True),rt.RooFit.Offset(True))
m2 = rt.RooMinimizer(nll)
m2.setPrintLevel(0)
m2.setPrintEvalErrors(0)
m2.setStrategy(2)
m2.setMaxFunctionCalls(100000 * 10000)
m2.setMaxIterations(100000 * 10000)
migrad_status = m2.minimize('Minuit2','migrad')
improve_status = m2.minimize('Minuit2','improve')
hesse_status = m2.minimize('Minuit2','hesse')
minos_status = m2.minos()
'''
