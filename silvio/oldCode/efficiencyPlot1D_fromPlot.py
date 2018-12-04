import ROOT

# ROOT.gROOT.SetBatch(0)
# canv2 = ROOT.TCanvas()

ROOT.gROOT.SetBatch(1)
canv = ROOT.TCanvas("canv","",1280,1024)
canv.SetGridx()
canv.SetGridy()

ROOT.gStyle.SetOptStat(0)


title = ""
varX_title = "m_{jj} (GeV)"
fileName = "ScoutingCaloHT.root"

file_ = ROOT.TFile(fileName)

#num = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_50_L1_HTT240_L1_HTT270")
num = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_50_HT_270")
den = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_50")

#den = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_50_L1_HTT240_L1_HTT270")
#num = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_50_HT_270")

den.GetXaxis().SetRangeUser(200,400)
num.GetXaxis().SetRangeUser(200,400)



print(num.GetNbinsX(), num.GetXaxis().GetXmin(), num.GetXaxis().GetXmax())
print(den.GetNbinsX(), den.GetXaxis().GetXmin(), den.GetXaxis().GetXmax())

trigger = "HLT_CaloScoutingHT250"

num.Sumw2()
den.Sumw2()
eff = ROOT.TGraphAsymmErrors();
eff.SetName("eff1D")
eff.Divide(num,den)


eff.SetTitle(title)
eff.SetMaximum(1.0001)
eff.SetMinimum(0.)
num.SetTitle("numerator")
den.SetTitle("denominator")

num.Draw()
den.Draw()

varX_min = num.GetXaxis().GetXmin()
varX_max = num.GetXaxis().GetXmax()

for histo in [num, den]:
    histo.GetXaxis().SetTitle(varX_title)
    histo.Draw("E")
    canv.SaveAs(histo.GetName()+".png")
    canv.SaveAs(histo.GetName()+".root")
    canv.SaveAs(histo.GetName()+".C")
    

func = ROOT.TF1("func","erf((x-[0])/[1])*[2]+[3]",varX_min,varX_max)
func.SetParLimits(2,0.25,0.5)
func.SetParLimits(3,0.5,1)
func.SetParameters(200,40,0.5,0.5)
#func = ROOT.TF1("func","[0]",varX_min,varX_max)
func.SetParameter(0,0.99)
eff.Fit(func,"L","",varX_min,varX_max)
eff.Fit(func,"L","",func.GetParameter(0),varX_max)
eff.Fit(func,"L","",func.GetParameter(0)+func.GetParameter(1)*0.,varX_max)
eff.Fit(func,"L","",func.GetParameter(0)+func.GetParameter(1)*0.,varX_max)

eff.GetXaxis().SetRangeUser(200,400)

#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
eff.GetXaxis().SetTitle(varX_title)
eff.Draw("AP")
canv.SaveAs(eff.GetName()+".png")
canv.SaveAs(eff.GetName()+".root")
canv.SaveAs(eff.GetName()+".C")
