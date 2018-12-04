# https://root.cern.ch/download/doc/RooFit_Users_Manual_2.91-33.pdf

import ROOT

c1 = ROOT.TCanvas("c1")

# file generated with
#/mnt/t3nfs01/data01/shome/sdonato/scoutingNew/copy/CMSSW_7_4_14/src/HiggsAnalysis/CombinedLimit/scripts/text2workspace.py  signal_bias_silvio/qq/atlas6_silvio5/dijet_combine_qq_480_lumi-27.637_CaloTrijet2016.txt  -o model.root

fileFit = ROOT.TFile.Open("model.root")



try:
    w = fileFit.Get("w")
    if w == None:
        w = fileFit.Get("wCaloTrijet2016")
    print("\nWorkSpace:")
    w.Print()
    print()
except:
    print("CANNOT OPEN WORKSPACE!!!")



try:
    pdf_index = w.cat("pdf_index")
    pdf_index.setIndex(1)
    print("#"*20)
    print("#"*5 + "I'm selecting" +  pdf_index.getLabel() + "#"*5 )
    print("#"*20)
except:
    pass


try:
    w.var("r").setVal(0)
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


data = w.data("data_obs")
#mjj = w.var("mjj")
th1x = w.var("th1x")

frame = th1x.frame()


data.plotOn(frame)
#toy1.plotOn(frame)


#w.pdf("pdf_binCaloTrijet2016").printCompactTree()

#function = w.pdf("pdf_binCaloTrijet2016")
#function = w.pdf("pdf_binCaloTrijet2016__model_bonly_")

#function = w.pdf("shapeBkg_CaloTrijet2016_multi_CaloTrijet2016")

function = w.pdf("pdf_binCaloTrijet2016_nuis")

#function = w.pdf("pdf_binCaloTrijet2016_bonly_nuis")

#pdf_binCaloTrijet2016_bonly
#pdf_binCaloTrijet2016_bonly_nuis
#pdf_binCaloTrijet2016_nuis




#pdf_binCaloTrijet2016__model_bonly_


#function = w.pdf("_model_bonly_")
#function = w.pdf("model_s")
#function = w.function("pdf_binCaloTrijet2016_nuis")
#function = w.function("pdf_binCaloTrijet2016")
#function = w.function("model_s")
#function = w.function("pdf_binCaloTrijet2016")
#function = w.function("shapeBkg_CaloTrijet2016_multi_CaloTrijet2016")
#function = w.function("CaloTrijet2016_multi")
#function = w.function("pdf_binCaloTrijet2016_nuis")
#function = w.function("extDijetPdf")


#, ROOT.Constrain(shapeBkg_CaloTrijet2016_multi_CaloTrijet2016__norm=1


par_fiveparams=[
    'p51_CaloTrijet2016',
    'p52_CaloTrijet2016',
    'p53_CaloTrijet2016',
    'p54_CaloTrijet2016',
]

par_modexp=[
    'pm1_CaloTrijet2016',
    'pm2_CaloTrijet2016',
    'pm3_CaloTrijet2016',
    'pm4_CaloTrijet2016',
]

par_atlas=[
    'pa1_CaloTrijet2016', 
    'pa2_CaloTrijet2016',
    'pa3_CaloTrijet2016',
    'pa4_CaloTrijet2016',
]

par_atlas6=[
    'pa61_CaloTrijet2016', 
    'pa62_CaloTrijet2016',
    'pa63_CaloTrijet2016',
    'pa64_CaloTrijet2016',
    'pa65_CaloTrijet2016',
]

par_silvio6=[
    'p1s6_CaloTrijet2016', 
    'p2s6_CaloTrijet2016',
    'p3s6_CaloTrijet2016',
    'p4s6_CaloTrijet2016',
    'p5s6_CaloTrijet2016',
]

par_silvio5=[
    'p1s5_CaloTrijet2016', 
    'p2s5_CaloTrijet2016',
    'p3s5_CaloTrijet2016',
    'p4s5_CaloTrijet2016',
]

pdf_index_value = pdf_index.getIndex()

if pdf_index_value==0:
    funct_param = par_modexp
elif pdf_index_value==1:
    funct_param = par_fiveparams
elif pdf_index_value==2:
    funct_param = par_atlas
elif pdf_index_value==3:
    funct_param = par_atlas6
elif pdf_index_value==4:
    funct_param = par_silvio4
elif pdf_index_value==5:
    funct_param = par_silvio5
elif pdf_index_value==6:
    funct_param = par_silvio6



parList = par_fiveparams + par_modexp + par_atlas + par_atlas6 + par_silvio6 + par_silvio5

pdf_index_value = pdf_index.getIndex()
for par in parList:
    if "CaloTrijet2016" in par:
        if par in funct_param:
            print("par: "+par)
            var = w.var(par)
            print("was constant "+str(var.isConstant())+". Now I set it to FALSE")
            var.setConstant(ROOT.kFALSE)
        else:
            print("par: "+par)
            var = w.var(par)
            print("was constant "+str(var.isConstant())+". Now I set it to TRUE")
            var.setConstant(ROOT.kTRUE)

#function.fitTo(data,ROOT.RooFit.Range("Full"),ROOT.RooFit.Extended(True),ROOT.RooFit.Offset(True),ROOT.RooFit.Strategy(2),ROOT.RooFit.PrintLevel(0)) 
#1/0

#w.var("jer").setConstant(ROOT.kTRUE)
#w.var("jes").setConstant(ROOT.kTRUE)
#w.var("jer_In").setConstant(ROOT.kTRUE)
#w.var("jes_In").setConstant(ROOT.kTRUE)
#w.var("pm1_CaloTrijet2016").setVal(-620)
#w.var("pm1_CaloTrijet2016").setVal(-530)

#nll = function.createNLL(data,ROOT.RooFit.Range("Full"),ROOT.RooFit.Extended(True),ROOT.RooFit.Offset(True), ROOT.RooFit.NumCPU(3), ROOT.RooFit.Optimize(2))

llist = ROOT.RooLinkedList()
#nll = function.createNLL(data, llist)
nll = function.createNLL(data,ROOT.RooFit.Range("Full"),ROOT.RooFit.Extended(True),ROOT.RooFit.Offset(True), ROOT.RooFit.NumCPU(3), ROOT.RooFit.Optimize(2))

#ROOT.RooFit.Range("Full"),ROOT.RooFit.Extended(True),ROOT.RooFit.Offset(True), ROOT.RooFit.NumCPU(3), ROOT.RooFit.Optimize(2))
m2 = ROOT.RooMinimizer(nll)
m2.setPrintLevel(2)
m2.setPrintEvalErrors(2)
m2.setStrategy(2)
m2.setMaxFunctionCalls(100000 * 10000)
m2.setMaxIterations(100000 * 10000)
#migrad_status = m2.minimize('Minuit2','migrad')

#w.var("n_exp_binCaloTrijet2016_proc_CaloTrijet2016_multi").setVal(1)
#function.fitTo(data,ROOT.RooFit.Extended(True),ROOT.RooFit.Offset(True), ROOT.RooFit.NumCPU(3), ROOT.RooFit.Optimize(2))

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
