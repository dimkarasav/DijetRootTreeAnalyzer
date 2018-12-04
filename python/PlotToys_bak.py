# https://root.cern.ch/download/doc/RooFit_Users_Manual_2.91-33.pdf

import ROOT

c1 = ROOT.TCanvas("c1")


#-rw-r--r-- 1 sdonato uniz-higgs  828 Aug  3 15:36 higgsCombineqq_475_lumi-27.637_r-1.000_CaloTrijet2016_silvio6_atlas6.GenerateOnly.mH120.123456.root
#-rw-r--r-- 1 sdonato uniz-higgs 6.1K Aug  3 15:37 higgsCombineqq_425_lumi-27.637_r-1.000_CaloTrijet2016_silvio6_atlas6.MaxLikelihoodFit.mH120.123456.root


#file_ = ROOT.TFile.Open("/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/signal_bias_test/higgsCombineqq_300_lumi-35.900_r-1.000_CaloTrijet2016_fiveparam_fiveparam.MaxLikelihoodFit.mH120.123456.root")

#fileFit = ROOT.TFile.Open("fits_trijet_silvio_2018/DijetFitResults_CaloTrijet2016.root")
#fileFit = ROOT.TFile.Open("signal_bias_silvio/qq/modexp_silvio6/dijet_combine_qq_600_lumi-27.637_CaloTrijet2016.root")


#fileFit = ROOT.TFile.Open("signal_bias_silvio/qq/atlas6_silvio5/higgsCombineqq_400_lumi-27.637_r-1.641_CaloTrijet2016_atlas6_silvio5.MaxLikelihoodFit.mH120.123456.root")
#fileToys = ROOT.TFile.Open("signal_bias_silvio/qq/atlas6_silvio5/higgsCombineqq_400_lumi-27.637_r-1.641_CaloTrijet2016_atlas6_silvio5.GenerateOnly.mH120.123456.root")


fileFit = ROOT.TFile.Open("signal_bias_silvio_test/dijet_combine_qq_300_lumi-27.637_CaloTrijet2016.root")

#fileFit = ROOT.TFile.Open("signal_bias_silvio_test/higgsCombineqq_300_lumi-27.637_r-5.020_CaloTrijet2016_silvio4_silvio4.MaxLikelihoodFit.mH120.123456.root")
fileToys = ROOT.TFile.Open("signal_bias_silvio_test/higgsCombineqq_300_lumi-27.637_r-5.020_CaloTrijet2016_silvio4_silvio4.GenerateOnly.mH120.123456.root")



toys = fileToys.Get("toys")
toy1 = toys.Get("toy_1")

try:
    w = fileFit.Get("w")
    if w == None:
        w = fileFit.Get("wCaloTrijet2016")
    print("\nWorkSpace:")
    w.Print()
    print()
except:
    print("CANNOT OPEN WORKSPACE!!!")

print("\toy5:")
toy1.Print()
print()

try:
    data = w.data("data_obs")
except:
    pass


try:
    data = w.data("data_obs")
except:
    pass


#mjj = w.var("mjj")
th1x = w.var("th1x")

frame = th1x.frame()


data.plotOn(frame)
#toy1.plotOn(frame)


#w.pdf("pdf_binCaloTrijet2016").printCompactTree()

#function = w.pdf("pdf_binCaloTrijet2016")
#function = w.pdf("pdf_binCaloTrijet2016__model_bonly_")
function = w.pdf("CaloTrijet2016_multi")


#pdf_binCaloTrijet2016__model_bonly_


#function = w.pdf("_model_bonly_")
#function = w.pdf("model_s")
#function = w.function("pdf_binCaloTrijet2016_nuis")
#function = w.function("pdf_binCaloTrijet2016")
#function = w.function("model_s")
#function = w.function("pdf_binCaloTrijet2016")
#function = w.function("shapeBkg_CaloTrijet2016_multi_CaloTrijet2016")
#function = w.function("CaloTrijet2016_multi")
#function = w.function("pdf_binCaloTrijet2016_nuis")
#function = w.function("extDijetPdf")


c1.SetLogy()
#function.fitTo(toy1)
#function.plotOn(frame)
frame.Draw("")

c1.Modify()
c1.Update()

w.cat("pdf_index").Print()


#par.isConstant()
#par.setConstant(ROOT.kTRUE)


#r.Print()
#shapeBkg_CaloTrijet2016_multi_CaloTrijet2016__norm.Print()


