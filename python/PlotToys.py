# https://root.cern.ch/download/doc/RooFit_Users_Manual_2.91-33.pdf

import ROOT


colors = [
ROOT.kBlack,

ROOT.kYellow+1,
ROOT.kRed,
ROOT.kMagenta,
ROOT.kBlue,
ROOT.kCyan+1,
ROOT.kGreen+1,

ROOT.kOrange,
ROOT.kPink,
ROOT.kViolet,
ROOT.kAzure,
ROOT.kTeal,
ROOT.kSpring,

ROOT.kGray,
] 

c1 = ROOT.TCanvas("c1")
c1.SetLogy()


#-rw-r--r-- 1 sdonato uniz-higgs  828 Aug  3 15:36 higgsCombineqq_475_lumi-27.637_r-1.000_CaloTrijet2016_silvio6_atlas6.GenerateOnly.mH120.123456.root
#-rw-r--r-- 1 sdonato uniz-higgs 6.1K Aug  3 15:37 higgsCombineqq_425_lumi-27.637_r-1.000_CaloTrijet2016_silvio6_atlas6.MaxLikelihoodFit.mH120.123456.root


#file_ = ROOT.TFile.Open("/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/signal_bias_test/higgsCombineqq_300_lumi-35.900_r-1.000_CaloTrijet2016_fiveparam_fiveparam.MaxLikelihoodFit.mH120.123456.root")

#fileFit = ROOT.TFile.Open("fits_trijet_silvio_2018/DijetFitResults_CaloTrijet2016.root")
#fileFit = ROOT.TFile.Open("signal_bias_silvio/qq/modexp_silvio6/dijet_combine_qq_600_lumi-27.637_CaloTrijet2016.root")


#fileFit = ROOT.TFile.Open("signal_bias_silvio/qq/atlas6_silvio5/higgsCombineqq_400_lumi-27.637_r-1.641_CaloTrijet2016_atlas6_silvio5.MaxLikelihoodFit.mH120.123456.root")
#fileToys = ROOT.TFile.Open("signal_bias_silvio/qq/atlas6_silvio5/higgsCombineqq_400_lumi-27.637_r-1.641_CaloTrijet2016_atlas6_silvio5.GenerateOnly.mH120.123456.root")


files_ = [
#    "signal_bias_silvio/qq/silvio4_silvio4/higgsCombineqq_300_lumi-27.637_r-5.020_CaloTrijet2016_silvio4_silvio4.GenerateOnly.mH120.123456.root",
####    "signal_bias_silvio/qq/silvio4_silvio4/higgsCombineqq_600_lumi-27.637_r-0.564_CaloTrijet2016_silvio4_silvio4.GenerateOnly.mH120.123456.root",
#    "signal_bias_silvio/qq/silvio5_silvio4/higgsCombineqq_300_lumi-27.637_r-5.020_CaloTrijet2016_silvio5_silvio4.GenerateOnly.mH120.123456.root",
#    "signal_bias_silvio/qq/silvio6_silvio4/higgsCombineqq_300_lumi-27.637_r-5.020_CaloTrijet2016_silvio6_silvio4.GenerateOnly.mH120.123456.root",
    "signal_bias_silvio/qq/atlas_silvio4/higgsCombineqq_500_lumi-0.971_r-0.498_CaloTrijet2016_atlas_silvio4.GenerateOnly.mH120.123456.root",
    "signal_bias_silvio/qq/atlas6_silvio4/higgsCombineqq_500_lumi-0.971_r-0.498_CaloTrijet2016_atlas6_silvio4.GenerateOnly.mH120.123456.root",
    "signal_bias_silvio/qq/silvio4_silvio4/higgsCombineqq_500_lumi-0.971_r-0.498_CaloTrijet2016_silvio4_silvio4.GenerateOnly.mH120.123456.root",
    "signal_bias_silvio/qq/silvio5_silvio4/higgsCombineqq_500_lumi-0.971_r-0.498_CaloTrijet2016_silvio5_silvio4.GenerateOnly.mH120.123456.root",
    "signal_bias_silvio/qq/silvio6_silvio4/higgsCombineqq_500_lumi-0.971_r-0.498_CaloTrijet2016_silvio6_silvio4.GenerateOnly.mH120.123456.root",
    "signal_bias_silvio/qq/modexp_silvio4/higgsCombineqq_500_lumi-0.971_r-0.498_CaloTrijet2016_modexp_silvio4.GenerateOnly.mH120.123456.root",
    "signal_bias_silvio/qq/fiveparam_silvio4/higgsCombineqq_500_lumi-0.971_r-0.498_CaloTrijet2016_fiveparam_silvio4.GenerateOnly.mH120.123456.root",
#    "signal_bias_silvio/qq/atlas6_silvio4/higgsCombineqq_300_lumi-27.637_r-5.020_CaloTrijet2016_atlas6_silvio4.GenerateOnly.mH120.123456.root",
#    "signal_bias_silvio/qq/modexp_silvio4/higgsCombineqq_300_lumi-27.637_r-5.020_CaloTrijet2016_modexp_silvio4.GenerateOnly.mH120.123456.root",
#    "signal_bias_silvio/qq/fiveparam_silvio4/higgsCombineqq_300_lumi-27.637_r-5.020_CaloTrijet2016_fiveparam_silvio4.GenerateOnly.mH120.123456.root",
]



fileFit = ROOT.TFile.Open("signal_bias_silvio/qq/atlas_silvio4/dijet_combine_qq_500_lumi-0.971_CaloTrijet2016.root")

try:
    w = fileFit.Get("w")
    if w == None:
        w = fileFit.Get("wCaloTrijet2016")
    print("\nWorkSpace:")
    w.Print()
    print()
except:
    print("CANNOT OPEN WORKSPACE!!!")

frame = w.var("th1x").frame()

frame
for i, file_ in enumerate(files_):
    print("OPENING:"+file_)
    fileToys = ROOT.TFile.Open(file_)
    toys = fileToys.Get("toys")
    toy1 = toys.Get("toy_1")
    toy1.plotOn(frame,ROOT.RooFit.LineColor(colors[i]),ROOT.RooFit.MarkerColor(colors[i]))
    print("\toy5:")
    toy1.Print()
    print()



#mjj = w.var("mjj")

#function = w.pdf("CaloTrijet2016_multi")


frame.Draw("")

c1.Modify()
c1.Update()

w.cat("pdf_index").Print()
