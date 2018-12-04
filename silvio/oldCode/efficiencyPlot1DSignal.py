import ROOT

# ROOT.gROOT.SetBatch(0)
# canv2 = ROOT.TCanvas()

ROOT.gROOT.SetBatch(1)
canv = ROOT.TCanvas()
canv.SetGridx()
canv.SetGridy()

ROOT.gStyle.SetOptStat(0)

#ROOT.gROOT.ProcessLine(".L /mnt/t3nfs01/data01/shome/sdonato/functions.C+")

#fileName = "/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ScoutingCaloCommissioning_2017-01-18/CommissioningG/rootfile_CaloScoutingCommissioning2016G_JEC_CaloHLT_plus_V10p2_20170119_001201_reduced_skim.root"
#fileName = "rootFile_reduced_skim.root"

#fileName = "../ntupleTrigger/L1HTTSkim.root"
#denTrigger = "HLT_L1HTT_CaloScouting_PFScouting"

fileName = "../output_20180130_174545/rootfile_list_VectorDiJet1Jet_300_13TeV_dR_0p7_20180130_174545_0_reduced_skim.root"
#fileName = "../output_20180130_174612/rootfile_list_VectorDiJet1Jet_300_13TeV_dR_0p9_20180130_174612_0_reduced_skim.root"
#fileName = "../output_20180130_174621/rootfile_list_VectorDiJet1Jet_300_13TeV_dR_1p1_20180130_174621_0_reduced_skim.root"
#fileName = "../output_20180130_174626/rootfile_list_VectorDiJet1Jet_300_13TeV_dR_1p3_20180130_174626_0_reduced_skim.root"

denTrigger = "1"

#preselect = denTrigger + "&& min(dijet_pt,isr_pt)>140 && dijet_dr>0 && min(dijet_pt,isr_pt)"
#preselect = denTrigger + "&& min(dijet_pt,isr_pt)>0"

preselect = denTrigger + " && run<280385  && abs(dijet_deta)<0.7 && jet2_pt>40  && HTgoodJets>210"

preselect = denTrigger + "   && abs(dijet_deta)<1.3 && abs(jet1_eta)<2.5 &&  abs(jet2_eta)<2.5 && jet1_pt>60 && jet2_pt>30 && run<280385"

preselect = denTrigger +  "  && abs(dijet_deta)<0.7 && abs(jet1_eta)<1.6 &&  abs(jet2_eta)<1.6 && isr_pt>80" #&& isr_pt>90

#preselect  = denTrigger +  "  && abs(dijet_deta)<1.3  && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && jet1_pt>65 && jet2_pt>40 && dijet_mass>100 && PassJSON && HLT_CaloJet40_CaloScouting_PFScouting && run<=280385 && run>=277991"

# && PassJSON

# cutString = 'abs(deltaETAjj)<1.3&&abs(etaWJ_j1)<2.5&&abs(etaWJ_j2)<2.5&&pTWJ_j1%s>60&&pTWJ_j2%s>30&&PassJSON&&passHLT_CaloJet40_CaloScouting_PFScouting&&mjj%s>=%i&&mjj%s<%i&&run>=%i&&run<=%i'%(corr,corr,corr,w.var("mjj").getMin("Eff"),corr,w.var("mjj").getMax("Eff"),options.runMin,options.runMax)

#  

# && min(dijet_pt,isr_pt)>=0
# && abs(dijet_deta)<1.3 

file_ = ROOT.TFile(fileName)

tree = file_.Get("rootTupleTree/tree")

trigger = "HTgoodJets>300"

title = "Trigger efficiency of HLT_CaloScoutingHT250"
#trigger = "(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)"
#trigger = "HLT_L1HTT_CaloScouting_PFScouting"
#preselect = "HLT_CaloJet40_CaloScouting_PFScouting"
#(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)

 
#varX = "min(dijet_pt,isr_pt)"
#varX_nbins,   varX_min,  varX_max = 20,120,320
#varX_title = "min(dijet_pt,isr_pt)"

varX = "dijet_mass"
varX_nbins,   varX_min,  varX_max = 100,200,700
varX_title = "m_{jj}"

#varX = "HTgoodJets"
##varX = "htAK4"
#varX_nbins,   varX_min,  varX_max = 100,0,500
#varX_title = "HT (GeV)"

#varX = "jet1_eta"
#varX_nbins,   varX_min,  varX_max = 100,-5,5
#varX_title = "#eta"

preselect += "&& (%s < %d)"%(varX,varX_max)

tree.Draw("%s >> den1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"")
den = ROOT.gDirectory.Get("den1D")
tree.Draw("%s >> num1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s && %s"%(preselect,trigger) ,"")
num = ROOT.gDirectory.Get("num1D")
num.Sumw2()
den.Sumw2()
eff = ROOT.TGraphAsymmErrors();
eff.SetName("eff1DSig")
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
canv.SaveAs(eff.GetName()+".png")
canv.SaveAs(eff.GetName()+".root")
canv.SaveAs(eff.GetName()+".C")
