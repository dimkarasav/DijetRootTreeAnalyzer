import ROOT
import array
import copy
#import RooFit

ROOT.gROOT.SetBatch(0)

matchings = [
"jets12",
"jets02",
"jets01",
]

masses = [
    200, 300, 400, 500, 600, 800, 1000
#    500
]


file_ = ROOT.TFile.Open("matchingStudyOk.root")

data = {}
signal = {}

mu = {}
mu_error = {}
acceptance = {}

rebin = 1
for matching in matchings:
    data[matching] = file_.Get("data_%s"%(matching))
    data[matching].Rebin(rebin)
    signal[matching] = {}
    mu[matching] = {}
    acceptance[matching] = {}
    mu_error[matching] = {}
    for mass in masses:
        signal[matching][mass] = file_.Get("sig_%s_%s"%(mass,matching))
        signal[matching][mass].Rebin(rebin)

print(signal)

'''
#// Declare observable x
x = ROOT.RooRealVar("x","x",0,10000) 
l = ROOT.RooArgList(x)

data = ROOT.RooDataHist("data", "data set with x1", l, data[matching])
signal = ROOT.RooDataHist("signal", "signal set with x1", l, signal[mass][matching])
#data2 = ROOT.RooDataHist("data2", "data set with x2", l, data[matching])

##  // Create a binned dataset that imports contents of TH1 and associates its contents to observable 'x'
#dh = ROOT.RooDataHist("dh","dh",x,ROOT.RooFit.Import(data[matching])) 




mean = ROOT.RooRealVar("mean","Mean of Gaussian",0,-100,100)
expo = ROOT.RooExponential("expo","expo(x,mean)",x,mean)

result = expo.fitTo((data),ROOT.RooFit.Range(270,1000))

xframe = x.frame()
data.plotOn(xframe)
signal.plotOn(xframe,ROOT.RooFit.MarkerColor(2))
expo.plotOn(xframe)
#data2.plotOn(xframe,ROOT.RooFit.MarkerColor(2))
xframe.Draw()


'''


for matching in matchings:
    for mass in masses:
#        data = data[matching]
#        signal = signal[matching][mass]
        
        
        w = ROOT.RooWorkspace("w",ROOT.kTRUE)
        #w.factory("Exponential::expo(x[0,1000],mean[-0.02,-10,10])")
        #w.factory("norm*Exponential::expo(x[0,1000],mean[-0.02,-10,10],norm[1000,0,1000000])")
        #w.factory("EXPR::expo('exp(x*mean  )',x[0,1000],mean[-0.002,-10,10])")
        #w.factory("norm*EXPR::expo('exp(x*mean  )',x[0,1000],mean[-0.002,-10,10],norm[1000,0,1000000])")
        w.factory("EXPR::expo('exp(x*mean + x*x*p2  )',x[270,1000],mean[-0.002,-1,0],p2[0,-10,10])")
#        w.factory("EXPR::expo_('exp(x*mean + x*x*p2  )',x[270,1000],mean[-0.002,-10,10],p2[0,-10,10])")
        w.factory("ExtendPdf::expoExt(expo,normBkg[1e3,0,1e9])")


        normSig = ROOT.RooRealVar("normSig","normSig",0,1e6)
#        normTot = ROOT.RooRealVar("normTot","normTot",1,1E13)

        x = w.var('x')
        #x.setBins(2)
        expoExt = w.pdf('expoExt')
        expo = w.pdf('expo')
        mean = w.var('mean')
        normBkg = w.var('normBkg')
        p2 = w.var('p2')
        p2.setVal(0)
        p2.setConstant()
        mean.setVal(-0.01)
#        mean.setConstant()
#        normTot.setVal(1e4)
#        normTot.setConstant()
        #expo = w.function('mypdf')


        #y = ROOT.RooRealVar("y","y",0,1000)
        #y.setBins(20)

        l = ROOT.RooArgList(x)
        signal_ = ROOT.RooDataHist("signal_", "data set with x1", l, signal[matching][mass])
        signalPdf = ROOT.RooHistPdf("signalPdf","signalPdf",ROOT.RooArgSet(x),signal_,0)
        signalPdfExt = ROOT.RooExtendPdf("signalPdfExt","extended signalPdf",signalPdf,normSig,"0")
        data_ = ROOT.RooDataHist("data_", "data set with x1", l, data[matching])


        sigfrac = ROOT.RooRealVar("sigfrac","fraction of component 1 in signal",0.5,-10.,10.)
        sigbkg = ROOT.RooAddPdf("sigbkg","expo + signalPdf", signalPdf, expo, sigfrac)
#        sigbkgExt = ROOT.RooExtendPdf("sigbkgExt","sigbkg",sigbkg,normTot,"0")
        sigbkgExt = ROOT.RooAddPdf("sigbkgExt","expoExt + signalPdfExt", ROOT.RooArgList(expoExt,signalPdfExt))
        sigfrac.setVal(0)
        sigfrac.setConstant()

        print("signal[matching][mass].Integral()=",signal[matching][mass].Integral())
        print("signal[matching][mass].Integral(A)=",signal[matching][mass].Integral(-100,1000000))
        print("signal[matching][mass].Integral(B)=",signal[matching][mass].Integral(signal[matching][mass].FindBin(270),1000000))
        print("signal_=",signal_.sum(0))
        print("signal_=",signal_.sum(1))

        normSig.setVal(1e-6)
        normSig.setConstant(1)
        result = sigbkgExt.fitTo((data_),ROOT.RooFit.Range(270,1000),ROOT.RooFit.PrintLevel(0),ROOT.RooFit.Save()) #
#        result = sigbkgExt.fitTo((data_),ROOT.RooFit.Range(270,1000),ROOT.RooFit.PrintLevel(0),ROOT.RooFit.Save()) #
#        norm.setConstant()

        xframe = x.frame()
        data_.plotOn(xframe)
        sigbkgExt.plotOn(xframe) #
        #signalPdf.plotOn(xframe,ROOT.RooFit.LineColor(2))
        #sigbkg.plotOn(xframe,ROOT.RooFit.LineColor(3))


        #asimov.plotOn(xframe,ROOT.RooFit.LineColor(4))

        #asimovData = ROOT.RooDataSet("asimovData","Asimov Dataset", ROOT.RooArgSet(x),1000)
        #asimovData.add(*w.set("obs"),w.function("mean")->getVal())
        #w.var("lumi0")->setVal(np_cmle->getRealValue("nuisance_lumi"))
        #w.var("b0")->setVal(np_cmle->getRealValue("nuisance_b"));
        #w.var("acc0")->setVal(np_cmle->getRealValue("nuisance_acc"));

        #asimov = ROOT.RooStats.AsymptoticCalculator.MakeAsimovData(data, signal, ROOT.RooArgSet(x), ROOT.RooArgSet()); 

        frac2 = expo.createIntegral(ROOT.RooArgSet(x))
        print(frac2.getVal())

        asimovScale = 10.
        asimov = sigbkgExt.generateBinned(ROOT.RooArgSet(x),1,ROOT.RooFit.Extended(),ROOT.RooFit.ExpectedData(),ROOT.RooFit.SumW2Error(ROOT.kTRUE)) #, ,ROOT.RooFit.ExpectedData() ,norm.getVal()
        asimov = sigbkgExt.generateBinned(ROOT.RooArgSet(x),asimovScale*data_.sum(ROOT.kTRUE)/asimov.sum(ROOT.kTRUE),ROOT.RooFit.Extended(),ROOT.RooFit.ExpectedData(),ROOT.RooFit.SumW2Error(ROOT.kTRUE)) #, ,ROOT.RooFit.ExpectedData() ,norm.getVal()
        normBkg.setVal(normSig.getVal()*asimovScale)
        asimov.plotOn(xframe,ROOT.RooFit.LineColor(4))
        xframe.Draw()


        print("data.sumEntries()=",data_.sumEntries())
        print("asimov.sumEntries()=",data_.sumEntries())
        print("data.sum(ROOT.kFALSE)=",data_.sum(ROOT.kFALSE))
        print("data.sum(ROOT.kTRUE)=",data_.sum(ROOT.kTRUE))
        print("asimov.sum(ROOT.kFALSE)=",asimov.sum(ROOT.kFALSE))
        print("asimov.sum(ROOT.kTRUE)=",asimov.sum(ROOT.kTRUE))
        print("frac2.getVal()=",frac2.getVal())

        cnew = ROOT.TCanvas("cnew","")
#        cnew.SetLogy()
        normSig.setConstant(0)
        result = sigbkgExt.fitTo((asimov),ROOT.RooFit.Range(270,1000),ROOT.RooFit.PrintLevel(0),ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE)) #
        par = result.floatParsFinal().at(2)
        x2frame = x.frame()
#        data_.plotOn(x2frame)
        
        # Overlay the background component of model with a dashed line
#        sigbkgExt.plotOn(xframe,ROOT.RooFit.Components("signalPdfExt"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected)) ;
        
        # Overlay the background+sig2 components of model with a dotted line
#        sigbkgExt.plotOn(xframe,ROOT.RooFit.Components("expoExt"),ROOT.RooFit.LineStyle(ROOT.kDotted),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected)) ;
        
        sig_tot = signal[matching][mass].Integral(-1,100000)
        sig_range = signal[matching][mass].Integral(signal[matching][mass].FindBin(270),signal[matching][mass].FindBin(1000))
        acc = sig_range/sig_tot
        acceptance[matching][mass] = acc
        mu_error[matching][mass] = par.getError()/acceptance[matching][mass]
        mu[matching][mass] = par.getVal()/acceptance[matching][mass]

        normSig.setVal(5*normSig.getError())
        asimov.plotOn(x2frame)
#        sigbkgExt.plotOn(x2frame, ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected))
        sigbkgExt.plotOn(x2frame)
        x2frame.Draw()
        cnew.SaveAs("matchingStudyPlot_"+matching+"_"+str(mass)+".png")

        '''
           RooDataSet* asimov2 = w.pdf("model")->generate(*w.set("obs"),1,false,true,"",true/*This is expected data option*/);

        asimov = expo.generate(x,1,false,true,"",true)
        w.var("n").setVal(w.function("mean")->getVal());
        w.var("b_obs").setVal(w.function("b")->getVal());
        asimov.add(*w.set("obs"));
        '''

grs = {}
accs = {}
for matching in matchings:
    grs[matching]  = ROOT.TGraph(len(masses),array.array('d',mu_error[matching].keys()),array.array('d',mu_error[matching].values()))
    accs[matching] = ROOT.TGraph(len(masses),array.array('d',acceptance[matching].keys()),array.array('d',acceptance[matching].values()))


canvas = {}
for matching in matchings:
    canvas[matching] = ROOT.TCanvas(matching,matching)
    canvas[matching].SetTitle(matching)
    grs[matching].SetTitle(matching)
    grs[matching].Draw("APL*")
    canvas[matching].SaveAs("matchingStudy"+matching+".png")
    
    canvas[matching+"acc"] = ROOT.TCanvas(matching+"acc",matching+"acc")
    canvas[matching+"acc"].SetTitle("Acceptance " + matching)
    accs[matching].SetTitle("Acceptance " + matching)
    accs[matching].Draw("APL*")
    canvas[matching+"acc"].SaveAs("matchingStudyAcceptance"+matching+".png")



for mass in masses:
    print("Mass = %d"%mass)
    for matching in matchings:
        mu_e = mu_error[matching][mass]
        acc = acceptance[matching][mass]
        print("matching = %s\t%f\t%f\t%f"%(matching,mu_e,acc,mu_e*acc))
