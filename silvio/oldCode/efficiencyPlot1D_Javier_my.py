import ROOT

# ROOT.gROOT.SetBatch(0)
# canv2 = ROOT.TCanvas()

ROOT.gROOT.SetBatch(1)
canv = ROOT.TCanvas()
canv.SetGridx()
canv.SetGridy()

ROOT.gStyle.SetOptStat(0)

massBoundaries = [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]

#fileName = "../ntupleTrigger/CaloJet40Skim_similOriginal.root"
fileName = "/mnt/t3nfs01/data01/shome/sdonato/scratch/ntupleScouting/ntupleTrigger_pt20/CaloJet40Skim_similOriginal.root"

denTrigger = "HLT_CaloJet40_CaloScouting_PFScouting"

preselect  = denTrigger +  "  && abs(dijet_deta)<1.3  && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && jet1_pt>65 && jet2_pt>40 && dijet_mass>100 && PassJSON && HLT_CaloJet40_CaloScouting_PFScouting && run<=280385 && run>=277991"

file_ = ROOT.TFile.Open(fileName)

tree = file_.Get("rootTupleTree/tree")

#trigger = "passHLT_CaloScoutingHT250"
trigger = "HLT_CaloScoutingHT250"
title = "Trigger efficiency of HLT_CaloScoutingHT250"

varX = "dijet_mass"
varX_nbins,   varX_min,  varX_max = 100,200,700
varX_title = "m_{jj}"

preselect += "&& (%s < %d)"%(varX,varX_max)


tree.Draw("%s >> den1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"")
den = ROOT.gDirectory.Get("den1D")
tree.Draw("%s >> num1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s && %s"%(preselect,trigger) ,"")
num = ROOT.gDirectory.Get("num1D")
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

for histo in [num, den]:
    histo.GetXaxis().SetTitle(varX_title)
    histo.Draw("E")
    canv.SaveAs(histo.GetName()+".png")
    canv.SaveAs(histo.GetName()+".root")
    canv.SaveAs(histo.GetName()+".C")
    

func = ROOT.TF1("func","erf((x-[0])/[1])*[2]+[3]",varX_min,varX_max)
func.SetParameters(200,40,0.5,0.5)
func = ROOT.TF1("func","[0]",varX_min,varX_max)
func.SetParameter(0,0.99)
eff.Fit(func)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
#eff.Fit(func,"","",max(varX_min,func.GetParameter(0)),varX_max)
eff.GetXaxis().SetTitle(varX_title)
eff.Draw("AP")
canv.SaveAs(eff.GetName()+"_Javier_my.png")
canv.SaveAs(eff.GetName()+"_Javier_my.root")
canv.SaveAs(eff.GetName()+"_Javier_my.C")
