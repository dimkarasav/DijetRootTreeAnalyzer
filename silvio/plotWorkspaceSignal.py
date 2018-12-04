import ROOT

_file = ROOT.TFile("/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/cards_qq_freq_jets01/dijet_combine_qq_900_lumi-1.001_CaloTrijet2016.root")
wCaloTrijet2016 = _file.Get("wCaloTrijet2016")

mjj = wCaloTrijet2016.var("mjj")
th1x = wCaloTrijet2016.var("th1x")

CaloTrijet2016_bkg = wCaloTrijet2016.pdf("CaloTrijet2016_bkg")
extDijetPdf = wCaloTrijet2016.pdf("extDijetPdf")


frame = th1x.frame()
CaloTrijet2016_bkg.plotOn(frame)

frame.Draw()
