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

fileName = "../ntupleTrigger/CaloJet40Skim.root"
denTrigger = "HLT_CaloJet40_CaloScouting_PFScouting"

#preselect = denTrigger + "&& min(dijet_pt,isr_pt)>140 && dijet_dr>0 && min(dijet_pt,isr_pt)"
#preselect = denTrigger + "&& min(dijet_pt,isr_pt)>0"

preselect = denTrigger + " && run<280385  && abs(dijet_deta)<0.7 && jet2_pt>40  && HTgoodJets>210"

preselect = denTrigger + "   && abs(dijet_deta)<1.3 && abs(jet1_eta)<2.5 &&  abs(jet2_eta)<2.5 && jet1_pt>60 && jet2_pt>30 && run<280385"

preselect = denTrigger +  " && abs(dijet_deta)<1.3 && run<=280385 && PassJSON" #&& isr_pt>90

#preselect  = denTrigger +  "  && abs(dijet_deta)<1.3  && abs(jet1_eta)<2.5 && abs(jet2_eta)<2.5 && jet1_pt>65 && jet2_pt>40 && dijet_mass>100 && PassJSON && HLT_CaloJet40_CaloScouting_PFScouting && run<=280385 && run>=277991"

# && PassJSON

# cutString = 'abs(deltaETAjj)<1.3&&abs(etaWJ_j1)<2.5&&abs(etaWJ_j2)<2.5&&pTWJ_j1%s>60&&pTWJ_j2%s>30&&PassJSON&&passHLT_CaloJet40_CaloScouting_PFScouting&&mjj%s>=%i&&mjj%s<%i&&run>=%i&&run<=%i'%(corr,corr,corr,w.var("mjj").getMin("Eff"),corr,w.var("mjj").getMax("Eff"),options.runMin,options.runMax)

#  

# && min(dijet_pt,isr_pt)>=0
# && abs(dijet_deta)<1.3 

file_ = ROOT.TFile(fileName)

tree = file_.Get("rootTupleTree/tree")

triggers = [
"HLT_CaloScoutingHT250 && (L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)",
"HLT_CaloScoutingHT250 && (L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)",
"HLT_CaloScoutingHT250 && (L1_HTT280||L1_HTT270||L1_HTT240)",
"HLT_CaloScoutingHT250 && (L1_HTT270||L1_HTT240)",
"HLT_CaloScoutingHT250 && (L1_HTT240)",
]

title = "Trigger efficiency of HLT_CaloScoutingHT250"
#trigger = "(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)"
#trigger = "HLT_L1HTT_CaloScouting_PFScouting"
#preselect = "HLT_CaloJet40_CaloScouting_PFScouting"
#(L1_HTT320||L1_HTT300||L1_HTT280||L1_HTT270||L1_HTT240)

 
#varX = "min(dijet_pt,isr_pt)"
#varX_nbins,   varX_min,  varX_max = 20,120,320
#varX_title = "min(dijet_pt,isr_pt)"

varX = "dijet_mass"
varX_nbins,   varX_min,  varX_max = 40,200,700
varX_title = "m_{jj}"

#varX = "HTgoodJets"
##varX = "htAK4"
#varX_nbins,   varX_min,  varX_max = 100,0,500
#varX_title = "HT (GeV)"

#varX = "jet1_eta"
#varX_nbins,   varX_min,  varX_max = 100,-5,5
#varX_title = "#eta"

preselect += "&& (%s < %d)"%(varX,varX_max)


effs = []
for trigger in triggers:
    tree.Draw("%s >> den1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"")
    den = ROOT.gDirectory.Get("den1D")
    tree.Draw("%s >> num1D(%d,%d,%d)"%(varX,varX_nbins,varX_min,varX_max),"%s && %s"%(preselect,trigger) ,"")
    num = ROOT.gDirectory.Get("num1D")
    num.Sumw2()
    den.Sumw2()
    eff = ROOT.TGraphAsymmErrors();
    eff.SetName("eff1D_diff")
    eff.Divide(num,den)
    eff.SetMarkerColor(colors[triggers.index(trigger)])
    eff.SetLineColor(colors[triggers.index(trigger)])

    eff.SetTitle(title)
    eff.SetMaximum(1.0001)
    eff.SetMinimum(0.)
    num.SetTitle("numerator")
    den.SetTitle("denominator")
    eff.GetXaxis().SetTitle(varX_title)
    
    effs.append(eff.Clone(trigger))

for eff in effs:
    if effs.index(eff)==0: eff.Draw("AP")
    else: eff.Draw("P")

name = "eff1D_diff"
canv.SaveAs(name+".png")
canv.SaveAs(name+".root")
canv.SaveAs(name+".C")
