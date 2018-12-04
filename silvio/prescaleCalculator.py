import ROOT

#ROOT.gROOT.SetBatch(1)

fileName = "/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_8_0_30/src/DijetRootTreeAnalyzer/data_L1test.root"

file_ = ROOT.TFile(fileName)

file_.Get("DijetFilter/dijetMassHisto").ls()
histoAND = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_50_L1_HTT240_L1_HTT320")
histoOR = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_L1_HTT_240_270_280_300_320_or")
histo240 = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_50")

histoAND.Rebin(200)
histoOR.Rebin(200)
histo240.Rebin(200)

histoAND.Sumw2()
histoOR.Sumw2()
histo240.Sumw2()

ratio = histoOR.Clone("ratio")
ratio2 = histoOR.Clone("ratio2")
ratio3 = histoOR.Clone("ratio3")
ratio4 = histoOR.Clone("ratio4")

ratio.Reset()
ratio2.Reset()
ratio3.Reset()
ratio4.Reset()

c1 = ROOT.TCanvas("c1","")
ratio.Divide(histo240,histoOR)
ratio.GetYaxis().SetRangeUser(0,1.1)
ratio.Draw("E")
ratio.Fit("pol0","","",1000,1000000)


c2 = ROOT.TCanvas("c2","")
ratio2.Divide(histoAND,histoOR)
ratio2.GetYaxis().SetRangeUser(0,1.1)
ratio2.Draw("E")
ratio2.Fit("pol0","","",1000,1000000)

c3 = ROOT.TCanvas("c3","")
ratio3.Divide(histoAND,histo240)
ratio3.GetYaxis().SetRangeUser(0,1.1)
ratio3.Draw("E")
ratio3.Fit("pol0","","",1000,1000000)

c4 = ROOT.TCanvas("c4","")
ratio4.Divide(ratio,histo240)
ratio4.GetYaxis().SetRangeUser(0,1.1)
ratio4.Draw("E")
ratio4.Fit("pol0","","",1000,1000000)
