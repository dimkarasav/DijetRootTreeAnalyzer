import ROOT
import array
fullRatioPlot = False
ROOT.gStyle.SetOptFit(1111)

#varX_min,  varX_max = 0,6000
#fitX_min,  fitX_max = 260,4000

#varX_min,  varX_max = 200,800
#fitX_min,  fitX_max = 296,693

varX_min,  varX_max = 100,1000
#fitX_min,  fitX_max = 280,700
fitX_min,  fitX_max = 250,900


#massBoundaries = [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838,  890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808,  7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]
massBoundaries = [i*10 for i in range(1000)]

histoNames = [
#    "dijetMassHisto_isrptcut_50",
#    "dijetMassHisto_isrptcut_40_50",
#    "dijetMassHisto_isrptcut_50_60",
#    "dijetMassHisto_isrptcut_60_70",

#    "dijetMassHisto_isrptcut_70_80",
#    "dijetMassHisto_isrptcut_80_90",
    "dijetMassHisto_isrptcut_90_100",
    "dijetMassHisto_isrptcut_100_150",
    "dijetMassHisto_isrptcut_150_200",
    "dijetMassHisto_isrptcut_200_300",
    "dijetMassHisto_isrptcut_300",
]


print(fitX_min,fitX_max)
for m in massBoundaries:
    if m>=fitX_min:
        fitX_min = m
#        print(fitX_min)
        break
    
for m in reversed(massBoundaries):
    if m<=fitX_max:
        fitX_max = m
        break

print(fitX_min,fitX_max)


#function = "exp([p0]+[p1]*x+[p2]*x*x+[p3]*x*x*x+[p4]*x*x*x*x+[p5]*x*x*x*x*x+[p6]*x*x*x*x*x*x)"
#function = "[0]*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000))*0.5*(1.0 + TMath::Erf((x - [4])/[5]))"
#function = "[0]*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000))"
#funct.SetParameters(20,10,10,0.1)
#function = "([0]+[4]*x)*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000))"
#function = "exp([0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x)"

#function = "exp([0]+[1]*x+[2]*x**2+[3]*x**3+[4]*x**4+[5]*x**5+[6]*x**6)*(1+TMath::Erf((x - [7])/[8]))"
#function = "exp([0]+[1]*x+[2]*x**2+[3]*x**3)*(1+TMath::Erf((x - [7])/[8]))"
#function = "exp([0]+[1]*x)*(1+[2]*x+[3]*x**2+[4]*x**3+[5]*x**6+[6]*x**6)"
#function = "exp([0]+[1]*x)"
#function = "exp([0]+[4]*x+[5]*x**2+[6]*x**3+[7]*x**4+[8]*x**5)*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000))"
#function = "exp([0]+[4]*x+[5]*x**2+[6]*x**3+[7]*x**4+[8]*x**5)*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000)) + gaus(9)"
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000)) + gaus(9)"
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000))"
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000))"
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000)) *  (TMath::ATan((x-[4])/[5])/(TMath::Pi())+0.5 )  " #
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000)) *  (1./(1.+exp((x-[4])/[5])))  " #(TMath::ATan([5]*(x-[4])*(x-[6]))/(TMath::Pi())+0.5 )
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000)) * (1.0 + TMath::Erf((x - [4])/[5]))"
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000)) * (1.0 + TMath::Erf((x - [4])/[5]))"
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000)) * (cos(asin(2*[4]/(x-[5]) * (x>[5]))))"
#function = "exp([0])*TMath::Power(1-x/13000,[1])/TMath::Power(x/13000,[2]+[3]*log(x/13000)) + gaus(9) "
#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2)-[4]*pow(x/13000,3))/pow(x/13000,[1]) + gaus(9)"
#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2)-[4]*pow(x/13000,3))/pow(x/13000,[1]) + gaus(9)"
#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2)-[4]*pow(x/13000,3))/pow(x/13000,[1]) * (cos(asin(2*[4]/(x-[5]) )))"
#function = "exp([0]+[5]*x+[6]*x*x++[7]*x*x*x)*exp(-[2]*(x/13000)-[3]*pow(x/13000,2)-[4]*pow(x/13000,3))/pow(x/13000,[1])"

#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2)-[4]*pow(x/13000,3)-[5]*pow(x/13000,4))/pow(x/13000,[1]) * (1+TMath::Erf((x - [6])/[7]))"
#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2)-[4]*pow(x/13000,3)-[5]*pow(x/13000,4))/pow(x/13000,[1]) * (1+0*TMath::Erf((x - [6])/[7]))"
#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2)-[4]*pow(x/13000,3))/pow(x/13000,[1]) * (1+TMath::Erf((x - [5])/[6]))"
#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2)-[4]*pow(x/13000,3))/pow(x/13000,[1]) * (1+0*TMath::Erf((x - [5])/[6]))"
#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2))/pow(x/13000,[1]) * (1+TMath::Erf((x - [4])/[5]))"
#function = "exp([0])*exp(-[2]*(x/13000)-[3]*pow(x/13000,2))/pow(x/13000,[1]) * (1+0*TMath::Erf((x - [4])/[5]))"
#function = "exp([0]) / pow(x + [2] , 5 + [3] * log(x/13000) ) / ( exp([1]/(x+[3])) - 1) * (1+0*TMath::Erf((x - [4])/[5]))"

#function = "exp([0]) / pow(x + [2] , 5 + [3] * log(x/13000) ) / ( exp([1]/(x+[3])) - 1) * (1+TMath::Erf((x - [4])/[5]))"

#function = "exp([0]) / pow(x + [2] , 5 + [3] * log(x/13000) ) / ( exp([1]/(x+[3])) - 1) * (1+TMath::Erf((x - [4])/[5]))"
#function = "exp([0]) / pow(x + [2] , 5 + [3] * log(x/13000) ) / ( exp([1]/(x+[3])) - 1) * (1 - exp(-(x - [4])/[5]))"
#function = "TMath::Exp([0]) / TMath::Power(x + [2] , 5 + [3] * TMath::Log(x/13000) ) / ( TMath::Exp([1]/(x+[3])) - 1) * (TMath::Cos(TMath::ASin(2*[5]/ TMath::Max((x-[4]),20.) )))"

#function = "exp([0])*exp(-[2]*(x/13000))/pow(x/13000,[1])  * (1. - [4]/TMath::Max((x-[3]),1.))"
function = "exp([0]*(x/1000)^5+[1]*(x/1000)^4*(1-x/1000)+[2]*(x/1000)^3*(1-x/1000)^2 + [3]*(x/1000)^2*(1-x/1000)^3) + [4]*(x/1000)*(1-x/1000)^4  + [5]*(1-x/1000)^5"
#function = "exp([0]*(x/1000)^6+[1]*(x/1000)^5*(1-x/1000)+[2]*(x/1000)^4*(1-x/1000)^2 + [3]*(x/1000)^3*(1-x/1000)^3 + [4]*(x/1000)^2*(1-x/1000)^4  + [5]*(x/1000)*(1-x/1000)^5 + [6]*(1-x/1000)^6)"
#function = "exp([0] + [1]*(x/1000) + [2]*(x/1000)^2 + [3]*(x/1000)^3 + [4]*(x/1000)^4 + [5]*(x/1000)^5 + [6]*(x/1000)^6)"



funct = ROOT.TF1("funct",function,fitX_min,fitX_max)

Npar = funct.GetNpar()


funct.SetParameters(7.,2,3,2,2,2,2,0) 

#funct.SetParameter(0,6.800771236849048e-11)
#funct.SetParameter(0,6.800771236849048e-11*1E7)



#funct.SetParameters(20,10,20,1,-2000,50)



#funct.Draw("")
#1/0


title = "Di-jet mass plot"

varX = "dijet_mass"
varX_nbins = 50
varX_title = "m_{jj}"

def rebin(histo):
    oldWidth = 1.* histo.GetBinWidth(1)
    newHisto = ROOT.TH1F("histo", "", len(massBoundaries)-1, array.array('f',massBoundaries))
    for i in range(histo.GetNbinsX()):
        newHisto.Fill(histo.GetBinCenter(i), histo.GetBinContent(i))
    for i in range(newHisto.GetNbinsX()):
        newHisto.SetBinError(i, newHisto.GetBinContent(i)**0.5)
        newHisto.SetBinContent(i, newHisto.GetBinContent(i) * oldWidth / newHisto.GetBinWidth(i)  )
        newHisto.SetBinError(i, newHisto.GetBinError(i) * oldWidth / newHisto.GetBinWidth(i)  )
    return newHisto

## evaluate the ratio
def getRatio(data, funct, padSizeRatio):
    ratio = data.Clone("ratio")
    ratio.Reset()
    
    ratio.GetYaxis().SetLabelSize(padSizeRatio*data.GetYaxis().GetLabelSize())
    ratio.GetXaxis().SetLabelSize(padSizeRatio*data.GetXaxis().GetLabelSize())
    ratio.GetYaxis().SetTitleSize(padSizeRatio*data.GetYaxis().GetTitleSize())
    ratio.GetXaxis().SetTitleSize(padSizeRatio*data.GetXaxis().GetTitleSize())
    ratio.GetYaxis().SetTitleOffset(1./padSizeRatio*data.GetYaxis().GetTitleOffset())
    ratio.GetXaxis().SetTitleOffset(1./data.GetXaxis().GetTitleOffset())
    ratio.GetYaxis().SetTitle("Pull")    
    ratio.GetXaxis().SetTitle(data.GetXaxis().GetTitle())    
    ratio.GetYaxis().SetNdivisions(805)
    
    maxPull = -1 
    for i in range(data.GetNbinsX()):
        bin_low = ratio.GetBinLowEdge(i)
        bin_high = ratio.GetBinLowEdge(i+1)
        bin_cen = ratio.GetBinCenter(i)
        if(funct.GetXmin()<=bin_low and funct.GetXmax()>=bin_high ) or (fullRatioPlot and True):
            fx_cen = max(0.001,funct.Eval(bin_cen))
            fx = max(0.001,funct.Integral(bin_low,bin_high) / (bin_high-bin_low) )
            
            val = (data.GetBinContent(i) - fx)/(data.GetBinError(i)+1E-9)
            ratio.SetBinContent(i,val)
            maxPull = max(maxPull,abs(val))
        else:
            ratio.SetBinContent(i,100)
    
    ratio.SetMaximum(3)
    ratio.SetMinimum(-3)
    print("maxPull=",maxPull)
    return ratio
    



'''
ROOT.gROOT.SetBatch(0)
canv2 = ROOT.TCanvas()
'''

#ROOT.gROOT.SetBatch(1)
#canv = ROOT.TCanvas("canv","",1280,720)
canv = ROOT.TCanvas("canv","",640,480)
canv.SetGridx()
canv.SetGridy()
#canv.SetLogy(1)

ROOT.gStyle.SetOptStat(0)
#fileName = "/eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ScoutingCaloCommissioning_2017-01-18/CommissioningG/rootfile_CaloScoutingCommissioning2016G_JEC_CaloHLT_plus_V10p2_20170119_001201_reduced_skim.root"
#fileName = "rootFile_reduced_skim.root"

#fileName = "/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_7_4_14/src/CMSDIJET/DijetRootTreeAnalyzer/inputs/full.root"
#fileName = "/mnt/t3nfs01/data01/shome/sdonato/scratch/scouting/histoCaloJet40.root"
#fileName = "new4.root"
fileName = "inputs/full.root"


redoPlot = False

if redoPlot:
    #preselect = "abs(dijet_deta)<1.2 && jet1_pt>20 && jet2_pt>20 && isr_pt>=50" #
    #title = "Di-jet mass plot"
##    file_ = ROOT.TFile("/mnt/t3nfs01/data01/shome/dbrzhech/DijetScouting/CMSSW_8_0_30/src/DijetRootTreeAnalyzer/rootfile_list_ScoutingCaloCommissioning_Run2016.root")
    #file_ = ROOT.TFile("/scratch/sdonato/scouting/ntupleTrigger/L1HTTSkim.root")
    #tree = file_.Get("rootTupleTree/tree")
    #tree.Draw("%s >> histo(%f,%f,%f)"%(varX,varX_nbins,varX_min,varX_max),"%s"%(preselect) ,"")
    #histo = ROOT.gDirectory.Get("histo")
    #histo.GetYaxis().SetTitle("Events / %d GeV"%((varX_max-varX_min)/varX_nbins)) 
    #histo.Sumw2()
    #histoOrig = histo.Clone("histoOrig")
    pass
else:
    file_ = ROOT.TFile.Open(fileName)
    try:
        histoOrig = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_80_90").Clone("histoOrig")
        histoOrig.Reset()
        for h in histoNames:
            histoOrig.Add(file_.Get("DijetFilter/dijetMassHisto/%s"%h))
    except:
        pass
        #histoOrig = file_.Get("DijetFilter/dijetMassHisto/dijetMassHisto_isrptcut_50_60").Clone("histoOrig")
        #histoOrig.Reset()
        #for h in histoNames:
            #histoOrig.Add(file_.Get("DijetFilter/dijetMassHisto/%s"%h))
        
#    histoOrig = file_.Get("DijetFilter/dijetMassHisto/dijet_mass")
#try:
    #file_ = ROOT.TFile.Open(fileName)
    #histoOrig = file_.Get("DijetFilter/dijetMassHisto/dijet_mass")
    #histoOrig.GetMaximum()
#except:
    #canv = file_.Get("canv")
    #histo = canv.GetPrimitive("histo")
    #histoOrig = histo.Clone("histoOrig")
    #histoOrig.GetMaximum()

if not redoPlot:
    histo = rebin(histoOrig)

tot = histo.Integral(histo.FindBin(fitX_min+0.01),histo.FindBin(fitX_max-0.01))
#histo.Scale(1./tot)


#######################################################

canv.SetTitle(title)

histo.GetXaxis().SetTitle(varX_title)
histo.GetXaxis().SetRangeUser(varX_min+1E-6, varX_max-1E-6)
histo.Draw("E")



'''
#funct = ROOT.TF1("funct","pol5",varX_min,varX_max)
#funct = ROOT.TF1("funct","expo",varX_min,varX_max)
#funct = ROOT.TF1("funct","expo(0) + gaus(2)",varX_min,varX_max)
#funct = ROOT.TF1("funct","expo(0)")
funct.SetParameter(0,14)
funct.SetParameter(1,-1E-3)
funct.FixParameter(2,0)
funct.FixParameter(3,0)
funct.FixParameter(4,0)
funct.FixParameter(5,0)
funct.FixParameter(6,0)
histo.Fit(funct,"L","",fitX_min,fitX_max)
funct.ReleaseParameter(2)
funct.SetParameter(2,-1E-6)
histo.Fit(funct,"L","",fitX_min,fitX_max)
funct.ReleaseParameter(3)
funct.SetParameter(3,-1E-8)
histo.Fit(funct,"L","",fitX_min,fitX_max)
funct.ReleaseParameter(4)
funct.SetParameter(4,-1E-11)
histo.Fit(funct,"L","",fitX_min,fitX_max)
funct.ReleaseParameter(5)
funct.SetParameter(5,-1E-15)
histo.Fit(funct,"L","",fitX_min,fitX_max)
funct.ReleaseParameter(6)
funct.SetParameter(6,-1E-20)
histo.Fit(funct,"L","",fitX_min,fitX_max)
'''


#histo.Fit(funct,"L","",fitX_min,fitX_max )
#histo.Fit(funct,"L","",fitX_min,fitX_max )
#histo.Fit(funct,"L","",fitX_min,fitX_max )
#histo.Fit(funct,"L","",fitX_min,fitX_max)


print(fitX_min,fitX_max)
print(funct.GetExpFormula("P"))



histo.Fit(funct,"W","",fitX_min,fitX_max)
histo.Fit(funct,"LS","",fitX_min,fitX_max)

for i in range (10): res = histo.Fit(funct,"IL","",fitX_min,fitX_max)
print("X"*50)
res = histo.Fit(funct,"IL","",fitX_min,fitX_max)
res = histo.Fit(funct,"ILS","",fitX_min,fitX_max)

res = histo.Fit(funct,"ILSW","",fitX_min,fitX_max)
res = histo.Fit(funct,"ILSW","",fitX_min,fitX_max)


'''
funct.ReleaseParameter(9)

res = histo.Fit(funct,"LS","",fitX_min,fitX_max)

funct.ReleaseParameter(11)

res = histo.Fit(funct,"LS","",fitX_min,fitX_max)

funct.ReleaseParameter(10)

res = histo.Fit(funct,"LS","",fitX_min,fitX_max)
'''

#histo.Fit(funct,"L","",fitX_min,fitX_max)



try:
    print(res.Prob())
    print(res.Chi2())
except:
    pass

histo.SetTitle(title)

canv.Draw()
yPadSeparation = 0.25
padPlot = ROOT.TPad("padPlot","",0.,yPadSeparation,1.,1.)
padPlot.SetBottomMargin(.02)
padRatio = ROOT.TPad("padRatio","",0.,0.,1.,yPadSeparation)
padRatio.SetTopMargin(0)
padRatio.SetBottomMargin(.09/yPadSeparation)
padRatio.Draw()
padPlot.Draw()
padRatio.SetGridx()
padRatio.SetGridy()
padPlot.SetGridx()
padPlot.SetGridy()
#padPlot.SetLogy(1)
padPlot.cd()
histo.Draw("HIST")
funct.Draw("same")



padPlot.SetTitle(title)
padRatio.SetTitle("")


padPlot.Draw()
padRatio.cd()

padSizeRatio = (padPlot.GetWh()*padPlot.GetAbsHNDC())/(padRatio.GetWh()*padRatio.GetAbsHNDC())
ratio = getRatio(histo,funct,padSizeRatio)
ratio.Draw("E")
padRatio.Draw()


canv.SaveAs(histo.GetName()+".png")
canv.SaveAs(histo.GetName()+".root")
canv.SaveAs(histo.GetName()+".C")

print(funct.GetExpFormula("P"))


"""
############################



#function = "exp([0]*x+[1]*(1000.-x))"
#funct = ROOT.TF1("funct",function,fitX_min,fitX_max)
#funct.SetParameters(7.34831e-03, 7.34831e-03) 

#function = "exp([0]*x^2+2*[1]*(1000.-(x*500))*(x/500)+[2]*(1000.-(x/500))^2) "
#funct = ROOT.TF1("funct",function,fitX_min,fitX_max)
#funct.SetParameters(4.00778e-06,1.31945e-05,1.93936e-06) 

#function = "exp([0]*(x/1000)^2+[1]*(x/1000)*(1-x/1000)+[2]*(1-x/1000)) "
#funct = ROOT.TF1("funct",function,fitX_min,fitX_max)
#funct.SetParameters(4.,20,2) 




#function = "exp([0]*(x/500)^3+2*[1]*(1000.-(x/500))*(x/500)^2+[2]*(1000.-(x/500))^2*(x/3))  + [3]*(1000.-(x/500))^3"
#funct = ROOT.TF1("funct",function,fitX_min,fitX_max)
#funct.SetParameters(3.62874e+00,-7.77232e-03,4.06293e-08,-1.22258e-06) 

#function = "exp([0]*(x/1000)^3+[1]*(x/1000)^2*(1-x/1000)+[2]*(x/1000)*(1-x/1000)^2 + [3]*(1-x/1000)^3) "
#funct = ROOT.TF1("funct",function,fitX_min,fitX_max)
#funct.SetParameters(4.,2,3,2) 

#function = "exp([0]*(x/1000)^4+[1]*(x/1000)^3*(1-x/1000)+[2]*(x/1000)^2*(1-x/1000)^2 + [3]*(x/1000)*(1-x/1000)^3) + [4]*(1-x/1000)^4 "
#funct = ROOT.TF1("funct",function,fitX_min,fitX_max)
#funct.SetParameters(4.,2,3,2,2) 

function = "exp([0]*(x/1000)^5+[1]*(x/1000)^4*(1-x/1000)+[2]*(x/1000)^3*(1-x/1000)^2 + [3]*(x/1000)^2*(1-x/1000)^3) + [4]*(x/1000)*(1-x/1000)^4  + [5]*(1-x/1000)^5"
funct = ROOT.TF1("funct",function,fitX_min,fitX_max)
funct.SetParameters(4.,2,3,2,2,2) 



#function = "exp([0] + [1]*(x/1000) + [2]*(x/1000)^2 + [3]*(x/1000)^3)"
#funct = ROOT.TF1("funct",function,fitX_min,fitX_max)
#funct.SetParameters(-7,0.01,0.0001,0.00001, 0.01) 


#res = histo.Fit(funct,"W","",fitX_min,fitX_max)
#for i in range(10): res = histo.Fit(funct,"L","",fitX_min,fitX_max)
#funct.Draw("")
#1/0
#res = histo.Fit(funct,"L","",fitX_min,fitX_max)
#res = histo.Fit(funct,"L","",fitX_min,fitX_max)

"""
