# https://root.cern.ch/download/doc/RooFit_Users_Manual_2.91-33.pdf

import ROOT

c1 = ROOT.TCanvas("c1")



fileFit = ROOT.TFile.Open("signal_bias_silvio/qq/atlas_silvio4/higgsCombineqq_420_lumi-27.637_r-1.362_CaloTrijet2016_atlas_silvio4.MaxLikelihoodFit.mH120.123456.root")
fileToys = ROOT.TFile.Open("signal_bias_silvio/qq/atlas_silvio4/higgsCombineqq_420_lumi-27.637_r-1.362_CaloTrijet2016_atlas_silvio4.GenerateOnly.mH120.123456.root")




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
    pdf_index = w.cat("pdf_index")
    pdf_index.setIndex(5)
    print("#"*20)
    print("#"*5 + "I'm selecting" +  pdf_index.getLabel() + "#"*5 )
    print("#"*20)
except:
    pass

#try:
    #shapeBkg_CaloTrijet2016_multi_CaloTrijet2016__norm = w.var("shapeBkg_CaloTrijet2016_multi_CaloTrijet2016__norm")
    #shapeBkg_CaloTrijet2016_multi_CaloTrijet2016__norm.setVal(1)
    #shapeBkg_CaloTrijet2016_multi_CaloTrijet2016__norm.setConstant(ROOT.kTrue)
#except:
    #pass

#try:
    #r = w.var("r")
    #r.setVal(1)
    #r.setConstant(ROOT.kTrue)
#except:
    #pass


#mjj = w.var("mjj")
th1x = w.var("th1x")

frame = th1x.frame()


#data.plotOn(frame)
toy1.plotOn(frame)


#w.pdf("pdf_binCaloTrijet2016").printCompactTree()

#function = w.pdf("pdf_binCaloTrijet2016")
function = w.pdf("pdf_binCaloTrijet2016_nuis")

function.fitTo(toy1,ROOT.RooFit.Range("Full"),ROOT.RooFit.Extended(True),ROOT.RooFit.Offset(True),ROOT.RooFit.Strategy(2),ROOT.RooFit.PrintLevel(0)) 


#w.var("jer").setConstant(ROOT.kTRUE)
#w.var("jes").setConstant(ROOT.kTRUE)
#w.var("jer_In").setConstant(ROOT.kTRUE)
#w.var("jes_In").setConstant(ROOT.kTRUE)
#w.var("pm1_CaloTrijet2016").setVal(-620)
#w.var("pm1_CaloTrijet2016").setVal(-530)

nll = function.createNLL(toy1,ROOT.RooFit.Range("Full"),ROOT.RooFit.Extended(True),ROOT.RooFit.Offset(True))
m2 = ROOT.RooMinimizer(nll)
m2.setPrintLevel(2)
m2.setPrintEvalErrors(2)
m2.setStrategy(2)
m2.setMaxFunctionCalls(100000 * 10000)
m2.setMaxIterations(100000 * 10000)
migrad_status = m2.minimize('Minuit2','migrad')


c1.SetLogy()
function.plotOn(frame)
frame.Draw("")


#par.isConstant()
#par.setConstant(ROOT.kTRUE)


#r.Print()
#shapeBkg_CaloTrijet2016_multi_CaloTrijet2016__norm.Print()


print("pdf index: ", pdf_index.getIndex() )
pdf_index.Print()

c1.Update()
c1.Modify()
