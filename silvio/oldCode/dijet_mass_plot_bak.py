#! /usr/bin/env python

from ROOT import *
import os, multiprocessing
import copy
import math
from array import array
import optparse
import re

gStyle.SetOptStat(0)
default_function_tag = ""
default_isrpt = "50"
default_dir = "./"
default_mass = "300"
default_path = ""
leg_pos_x1 = 0.75
leg_pos_x2 = 0.9
leg_pos_y1 = 0.5
leg_pos_y2 = 0.65
chi_square_file = open("chi_squares.txt", "a")
# fit_file = open("fit_outpu.txt", "a")
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-p", "--path", action="store", type="string", dest="path", default=default_path)
parser.add_option("-d", "--directory", action="store", type="string", dest="dir", default=default_dir)
parser.add_option("-m", "--mass", action="store", type="string", dest="mass", default=default_mass)
parser.add_option("-f", "--function", action="store", type="string", dest="function_tag", default=default_function_tag)
#parser.add_option("-s", "--selection", action="store", type="string", dest="selection", default="")
parser.add_option("-i", "--isrpt", action="store", type="string", dest="isrpt", default=default_isrpt)
parser.add_option("-n", "--number-of-fit", action="store", type="string", dest="number_of_fit", default="1")
parser.add_option("-D", "--data", action="store", type="string", dest="data", default="False")
parser.add_option("-B", "--bin-width", action="store", type="string", dest="bin_width", default="10")
parser.add_option("-r", "--range", action="store", type="string", dest="range", default="0,2000")
parser.add_option("-v", "--var", action="store", type="string", dest="var", default="dijet_mass")
parser.add_option("-b", "--batch", action="store", type="string", dest="batch", default="True")
# parser.add_option("-F", "--fit", action="store", type="string", dest="fit", default="nofit")
parser.add_option("-H", "--histo", action="store", type="string", dest="histo", default="False")
parser.add_option("-c", "--constituents", action="store", type="string", dest="constituents", default="False")
parser.add_option("",   "--range-of-fit", action="store", type="string", dest="range_of_fit", default="")

parser.add_option("",   "--bkg", action="store", type="string", dest="bkg", default="nofit")
parser.add_option("",   "--bkg-par-start", action="store", type="string", dest="par_start", default="1,1,1,1")
parser.add_option("",   "--p0-range", action="store", type="string", dest="p0_range", default="0,1000")
parser.add_option("",   "--p1-range", action="store", type="string", dest="p1_range", default="0,1000")
parser.add_option("",   "--p2-range", action="store", type="string", dest="p2_range", default="0,1000")
parser.add_option("",   "--p3-range", action="store", type="string", dest="p3_range", default="0,1000")


parser.add_option("-F",   "--fit-option", action="store", type="string", dest="fit_option", default="default")

(options, args) = parser.parse_args()
sqrtS=13000
p = re.split(",", options.par_start)
pranges = [re.split(",", options.p1_range), re.split(",", options.p1_range), re.split(",", options.p2_range), re.split(",", options.p3_range)]
# par_start
# p0,p1,p2,p3 = float(p[0]), float(p[1]), float(p[2]), float(p[3])
lumi=1
# p0,p1,p2,p3  = 6.845, 6.845, 6.7807, 0.30685
# p0_left, p0_right, p1_left, p1_right, p2_left, p2_right, p3_left, p3_right = 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, -10.0, 10.0
# p0_left, p0_right, p1_left, p1_right, p2_left, p2_right, p3_left, p3_right = float(pranges[0][0]), float(pranges[0][1]), float(pranges[1][0]), float(pranges[1][1]),float(pranges[2][0]), float(pranges[2][1]), float(pranges[3][0]), float(pranges[3][1]),

# print p0, p1, p2, p3, p0_left, p0_right, p1_left, p1_right, p2_left, p2_right, p3_left, p3_right

if options.data == "False": data = False
if options.data == "True":  data = True

histo_range = re.split(",|\, ", options.range)
if options.range_of_fit == "": range_of_fit = histo_range
else: range_of_fit = re.split(",|\, ", options.range_of_fit)
# print histo_range
function_name = "dijet_func"

histo_range_left, histo_range_right = float(histo_range[0]), float(histo_range[1])
range_of_fit_left, range_of_fit_right = float(range_of_fit[0]), float(range_of_fit[1])
bin_width = float(options.bin_width)

namesOfPars = { 'gaus':         ['Area', 'mean', 'sigma'],
                'landau':       ['Area', 'x0', 's'],
                'myexp':        ['A','a','s'],
                'crystalball':  ['alpha','n', 'mean', 'sigma'],
                'bkg0':         ['p0','p1','p2','p3'],
                'bkg_norm':     ['p1','p2','p3','m_eff','sigma_eff'],
                'bkg':          ['p0','p1','p2','p3','m_eff','sigma_eff'],
                't_student':    ['Area', 'mean', 'sigma'],
                'bias':         ['offset'],
                'myline':       ['offset', 'slope'],
                'gamma':        ['Area', 'alpha', 'theta', 'x0'],
            }

# print histo_range_right, range_of_fit_right
# exit()

def roofit_fexpr_converter(fexpr):
    roofit_fexpr = fexpr.replace("x","@0")
    roofit_fexpr = list(roofit_fexpr)
    for i,l in enumerate(roofit_fexpr):
        if l == "[":
            roofit_fexpr[i+1] = str(int(roofit_fexpr[i+1])+1)
    roofit_fexpr = ''.join(roofit_fexpr)
    roofit_fexpr = roofit_fexpr.replace("[","@")
    roofit_fexpr = roofit_fexpr.replace("]","")
    return roofit_fexpr

def fit_roofit(hist, fexpr, function_tag):
    mjj = RooRealVar('mjj', 'mjj', range_of_fit_left, range_of_fit_right)
    mjj.setRange("Range", range_of_fit_left, range_of_fit_right)
    h_data_roo = RooDataHist('h_data_roo', 'h_data_roo', RooArgList(mjj), hist)
    # p0 = RooRealVar('p0', 'p0', 50, 0.0, 100.0)
    parameters = []
    set_init         = dijet_mass_function_pars_init(hist, function_tag)
    number_of_pars   = set_init['number_of_pars']
    parameters_name  = set_init['name_of_pars']
    parameters_start = set_init['start_values']
    parameters_left  = set_init['lower_bound']
    parameters_right = set_init['upper_bound']
    roofitArgList = RooArgList(mjj)
    for i in range(0, number_of_pars):
        p = RooRealVar(parameters_name[i], parameters_name[i], parameters_start[i], parameters_left[i], parameters_right[i])
#        if p.GetTitle().find('m_eff_bkg_norm') != -1 or p.GetTitle().find('sigma_eff_bkg_norm') != -1: p.setConstant(kTRUE)
        parameters.append(p)
        roofitArgList.add(p)
    print roofitArgList

    # exit()
    if options.data == "True":
        if options.bkg == "fit":
            massMin = range_of_fit_left
            massMax = range_of_fit_right
            num_regions = 1
            dataInt = hist.Integral(hist.GetXaxis().FindBin(massMin), hist.GetXaxis().FindBin(massMax))
            print "hist.GetXaxis().FindBin(massMin) = ", hist.GetXaxis().FindBin(massMin), "hist.GetXaxis().FindBin(massMax) = ", hist.GetXaxis().FindBin(massMax)
            norm = RooRealVar('norm', 'norm', dataInt, 0.0, 1.0e9)
            # m_eff = RooRealVar('m_eff','m_eff',495.7,450.,550.)
            # sigma_eff = RooRealVar('sigma_eff','sigma_eff',96.0,80.,120.)
            # m_eff.setConstant(kTRUE)
            # sigma_eff.setConstant(kTRUE)
            # p1 = RooRealVar('p1', 'p1', 6.845, -100.0, 10000.0)
            # p2 = RooRealVar('p2', 'p2', 6.7807, -100.0, 10000.0)
            # p3 = RooRealVar('p3', 'p3', 0.30685, -100.0, 100.0)

            background = RooGenericPdf('background', 'background', roofit_fexpr_converter(fexpr),roofitArgList)
            # RooGenericPdf('background','(pow(1-@0/%.1f,@1)/pow(@0/%.1f,@2+@3*log(@0/%.1f)))*(0.5*(1.0 + TMath::Erf((@0 - @4)/@5)))'%(sqrtS,sqrtS,sqrtS), RooArgList(mjj, p1, p2, p3, m_eff, sigma_eff))
            print("background.Print()")
            background.Print()
            # background = RooGenericPdf('background','(pow(1-@0/%.1f,@1)/pow(@0/%.1f,@2+@3*log(@0/%.1f)))*(0.5*(1.0 + TMath::Erf((@0 - @4)/@5)))'%(sqrtS,sqrtS,sqrtS),RooArgList(mjj, p1, p2, p3, m_eff, sigma_eff))
            background_ext = RooExtendPdf("background_ext","",background,norm)
#            res_b = background_ext.fitTo(h_data_roo, RooFit.Extended(kTRUE), RooFit.Save(kTRUE), RooFit.Strategy(1))

            res_b = background_ext.fitTo(h_data_roo, 
            RooFit.Save(1)
            ,RooFit.Minimizer(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo())
            ,RooFit.Strategy(0) 
#            ,RooFit.Minos(1)
            )

            #CloseCoutSentry sentry(verbose < 2);
            #res_prefit = nuisancePdf->fitTo(*globalData,
            #RooFit::Save(1),
            #RooFit::Minimizer(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str()),
            #RooFit::Strategy(minimizerStrategy_),
            #RooFit::Minos(minos_ == "all")
#);


#            RooFit::Minimizer(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str()),
#            RooFit::Strategy(minimizerStrategy_), RooFit::Minos(minos_ == "all")

            norm_b = res_b.floatParsFinal().find("norm")
            background_noNorm = TF1("background_noNorm",function_expression("bkg_norm[0]",'function_expression'),range_of_fit_left, range_of_fit_right)
            # background_noNorm = TF1("background_noNorm","( TMath::Power(1-x/%.1f,[0]) ) / ( TMath::Power(x/%.1f,[1]+[2]*log(x/%.1f)) )*(0.5*(1.0 + TMath::Erf((x - [3])/[4])))"%(sqrtS,sqrtS,sqrtS),float(massMin),float(massMax))
            for i,n in enumerate(parameters_name):
                background_noNorm.SetParName(i,n)
            for i,p in enumerate(parameters):
#                print 'p.GetTitle() = ', p.GetTitle()
                background_noNorm.SetParameter(p.GetTitle(), p.getVal())
                print p.GetTitle(), "=", p.getVal()
            int_b = background_noNorm.Integral(massMin, massMax)
            p0_b = norm_b.getVal() / (int_b*lumi)*float(options.bin_width)

            # p1_b = p1
            # p2_b = p2
            # p3_b = p3
            # background_noNorm.SetParameter(0,p1_b.getVal())
            # background_noNorm.SetParameter(1,p2_b.getVal())
            # background_noNorm.SetParameter(2,p3_b.getVal())
            # background_noNorm.SetParameter(3,m_eff.getVal())
            # background_noNorm.SetParameter(4,sigma_eff.getVal())
            # print "p0_b = " , p0_b , " +" , norm_b.getErrorHi()/int_b*math.sqrt(num_regions) , " -" , norm_b.getErrorLo()/int_b*math.sqrt(num_regions)
            # print "p1_b = " , p1_b.getVal() , " +" , p1_b.getErrorHi() , " " , p1_b.getErrorLo()
            # print "p2_b = " , p2_b.getVal() , " +" , p2_b.getErrorHi() , " " , p2_b.getErrorLo()
            # print "p3_b = " , p3_b.getVal() , " +" , p3_b.getErrorHi() , " " , p3_b.getErrorLo()
            # print "m_eff =", m_eff.getVal()
            # print "sigma_eff =", sigma_eff.getVal()
            # function_fit.SetParameter(0, p0_b)
            # # function_fit = TF1("background","( [0]*TMath::Power(1-x/%.1f,[1]) ) / ( TMath::Power(x/%.1f,[2]+[3]*log(x/%.1f)) )*(0.5*(1.0 + TMath::Erf((x - [4])/[5])))"%(sqrtS,sqrtS,sqrtS),float(massMin),float(massMax))
            # function_fit.SetParameter(1,p1_b.getVal())
            # function_fit.SetParameter(2,p2_b.getVal())
            # function_fit.SetParameter(3,p3_b.getVal())
            # function_fit.SetParameter(4,m_eff.getVal())
            # function_fit.SetParameter(5,sigma_eff.getVal())

            function_fit = TF1("background", function_expression("bkg[0]",'function_expression'), range_of_fit_left, range_of_fit_right)
            function_fit.SetParameter(0,p0_b)
            function_fit.SetParName(0,'p0')
            for i,n in enumerate(parameters_name):
                function_fit.SetParName(i+1,n)
            for i,p in enumerate(parameters):
                function_fit.SetParameter(p.GetTitle(), p.getVal())
                print p.GetTitle(), "=", p.getVal()
            chi_square_file.write(function_tag+": ")
            chi_square_file.write(str(function_fit.GetChisquare())+"/"+str(((range_of_fit_right-range_of_fit_left)/bin_width-number_of_pars))+"\n")
            print "chi_square = ", str(function_fit.GetChisquare())+"/"+str(((range_of_fit_right-range_of_fit_left)/bin_width-number_of_pars))

    # else:
        # for i,p in enumerate(parameters):
        #     function_fit.SetParameter(i, p.getValue())

    return function_fit

def getRatio(hist, function_fit, padSizeRatio):
    ratio = hist.Clone("ratio")
    ratio.Reset()

    ratio.GetYaxis().SetLabelSize(padSizeRatio*hist.GetYaxis().GetLabelSize())
    ratio.GetXaxis().SetLabelSize(padSizeRatio*hist.GetXaxis().GetLabelSize())
    ratio.GetYaxis().SetTitleSize(padSizeRatio*hist.GetYaxis().GetTitleSize())
    ratio.GetXaxis().SetTitleSize(padSizeRatio*hist.GetXaxis().GetTitleSize())
    ratio.GetYaxis().SetTitleOffset(1./padSizeRatio*hist.GetYaxis().GetTitleOffset())
    ratio.GetXaxis().SetTitleOffset(1./hist.GetXaxis().GetTitleOffset())
    ratio.GetYaxis().SetTitle("Pull")
    ratio.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    ratio.GetYaxis().SetNdivisions(805)

    for i in range(hist.GetNbinsX()):
        if ratio.GetBinCenter(i) >= range_of_fit_left and ratio.GetBinCenter(i) <= range_of_fit_right:
            fx = function_fit.Eval(ratio.GetBinCenter(i))
            val = (hist.GetBinContent(i) - fx)/(fx**0.5)
            ratio.SetBinContent(i,val)
            ratio.SetBinError(i,hist.GetBinError(i)/fx**0.5)

    ratio.SetMaximum(5)
    ratio.SetMinimum(-5)
    return ratio


def set_hist_style(hist):
    hist.SetMarkerStyle(8)
    hist.SetMarkerColor(kBlack)
    hist.SetLineColor(kBlack)
    hist.SetLineWidth(1)
    hist.GetXaxis().SetTitle("m_{jj}(GeV)")
    hist.GetYaxis().SetTitle("Events / "+str(hist.GetBinWidth(0))+" GeV")


def draw_f(function_fit, function_tag, legend):
    elementaryFunc = function_expression(function_tag, 'elementaryFunc')
    tf_array = []
    count = 0
    if data == False:
        for i,el in enumerate(elementaryFunc):
            number_of_pars = number_of_pars_func(el)
            funcTitle = re.sub("\[|\]", "", el)
            func = function_builder(el)
            for i in range(0, number_of_pars):
                func = func.replace("["+str(count)+"]", str(function_fit.GetParameter(count)))
                count = count+1
            tf_array.append(TF1(funcTitle, func, range_of_fit_left, range_of_fit_right))
            print func
    else:
        fexpr = function_expression(function_tag, 'function_expression')
        elementaryFunc = function_expression(function_tag, 'elementaryFunc')
        func = function_builder(elementaryFunc[0])
        for j in range(0,4):
            func = func.replace("["+str(j)+"]", str(function_fit.GetParameter(j)))
        tf_array.append(TF1("bkg", func, histo_range_left, histo_range_right))
        func = fexpr
        for j in range(4,3*len(elementaryFunc)+1):
            func = func.replace("["+str(j)+"]", str(function_fit.GetParameter(j)))
        print func
        tf_array.append(TF1("signal", func, histo_range_left, histo_range_right))
    return tf_array

def function_builder(func):
    delim_out = re.split("\[|\]", func)
    j = int(delim_out[1])
    if data == True: jj = j+4
    else: jj = j
    return {
        'bias['+str(j)+']' : "["+str(jj)+"]",
        'myline['+str(j)+']' : "["+str(jj)+"]+["+str(jj+1)+"]*x",
        #'gaus['+str(j)+']' : "gaus("+str(jj)+")",
        'gaus['+str(j)+']' : "["+str(jj)+"]*TMath::Gaus(x, ["+str(jj+1)+"], ["+str(jj+2)+"], 1)",
        'myexp['+str(j)+']' : "["+str(jj)+"]*exp(-["+str(jj+1)+"]*(x-["+str(jj+2)+"]))",
        'landau['+str(j)+']' : "["+str(jj)+"]*TMath::Landau(x,["+str(jj+1)+"],["+str(jj+2)+"],1)",
        'crystalball['+str(j)+']' : "["+str(jj+4)+"]*ROOT::Math::crystalball_function(x, ["+str(jj)+"], ["+str(jj+1)+"], ["+str(jj+2)+"], ["+str(jj+3)+"])",
        # 'bkg['+str(j)+']' : "(1-x/13000)**["+str(j)+"]/((x/13000)**(["+str(j)+"]+["+str(j)+"]*TMath::Log(x/13000)))",
        'bkg0['+str(j)+']' : "["+str(j)+"]*(1-x/13000)**["+str(j+1)+"]/((x/13000)**(["+str(j+2)+"]+["+str(j+3)+"]*TMath::Log(x/13000)))",
        'bkg_norm['+str(j)+']' : "TMath::Power(1-x/13000,["+str(j)+"])/TMath::Power(x/13000,["+str(j+1)+"]+["+str(j+2)+"]*log(x/13000))*0.5*(1.0 + TMath::Erf((x - ["+str(j+3)+"])/["+str(j+4)+"]))",
        'bkg['+str(j)+']' : "["+str(j)+"]*( TMath::Power(1-x/13000,["+str(j+1)+"]) )/TMath::Power(x/13000,["+str(j+2)+"]+["+str(j+3)+"]*log(x/13000))*0.5*(1.0 + TMath::Erf((x - ["+str(j+4)+"])/["+str(j+5)+"]))",
        # 'bkg['+str(j)+']' : "["+str(j)+"]*(1-x/13000)**["+str(j+1)+"]/((x/13000)**(["+str(j+2)+"]))",
        # 'bkg['+str(j)+']' : "TMath::Exp(-TMath::Log(450/13000)*([2]+[3]*TMath::Log(450/13000)))*"+"["+str(j)+"]*((1-450/13000)**["+str(j+1)+"]+[1]*(1-450/13000)**([1]-1)*(x-450/13000))/(1+(["+str(j+2)+"]+2*["+str(j+3)+"]*TMath::Log(450/13000))/(450/13000)*(x-450/13000))",
        'gamma['+str(j)+']': "["+str(jj)+"]*ROOT::Math::gamma_pdf(x, ["+str(jj+1)+"], ["+str(jj+2)+"], ["+str(jj+3)+"])",
        't_student['+str(j)+']': "["+str(jj)+"]*TMath::Student((x-["+str(jj+1)+"])/["+str(jj+2)+"],3)",
    }[func]
# def bkg_and_sig_builder(func):
#     delim_out = re.split("\[|\]", func)
#     j = int(delim_out[1])
#     return {
#         'bkg['+str(j)+']' : function_builder('bkg['+str(j)+']'),
#         'signal['+str(j)+']': function_builder('gaus['+str(j)+']')+'+'+function_builder('gaus['+str(j+3)+']')+'+'+function_builder('gaus['+str(j+6)+']')+'+'+function_builder('landau['+str(j+9)+']')
#     }[func]
#selection = options.selection
selection = "isr_pt > " + options.isrpt +" && jet2_pt>45  && abs(dijet_deta)<1.2 && jet1_pt>90"
number_of_fit = options.number_of_fit
# print function_builder('bkg[0]')
def function_expression(function_tag, return_tag):
    #function_tag = options.function_tag
    elementaryFunc = re.split("\+|\/|\*|\-", function_tag)
    str_to_find_delim = ""
    for f in elementaryFunc:
        str_to_find_delim += f +"|"
    str_to_find_delim = str_to_find_delim.replace("[", "\[")
    str_to_find_delim = str_to_find_delim.replace("]", "\]")
    str_to_find_delim = str_to_find_delim.replace(")", "\)")
    str_to_find_delim = str_to_find_delim.replace("(", "\(")
    #str_to_find_delim = "gaus\[0\]|myexp\[3\]|landau\[6\]|"
    operatorsFunc = re.split(str_to_find_delim, function_tag)
    function_expression = ''
    find_result = 0

    for k, f in enumerate(elementaryFunc):
        f0 = f
        if f0.find("(")+1:
            f0 = f0.replace("(","")
            function_expression += "(" + function_builder(f0) + operatorsFunc[k+1]
            # if data == False: function_expression += "(" + function_builder(f0) + operatorsFunc[k+1]
            # else: function_expression += "(" + bkg_and_sig_builder(f0) + operatorsFunc[k+1]
            elementaryFunc[k] = f0
        elif f0.find(")")+1:
            f0 = f0.replace(")","")
            function_expression += function_builder(f0) + ")" + operatorsFunc[k+1]
            # if data == False: function_expression += function_builder(f0) + ")" + operatorsFunc[k+1]
            # else: function_expression += bkg_and_sig_builder(f0) + ")" + operatorsFunc[k+1]
            elementaryFunc[k] = f0
        elif f0.find("(")+1 and f0.find(")")+1:
            f0 = f0.replace("(","")
            f0 = f0.replace(")","")
            function_expression += "(" + function_builder(f0) + ")" + operatorsFunc[k+1]
            # if data == False: function_expression += "(" + function_builder(f0) + ")" + operatorsFunc[k+1]
            # else: function_expression += "(" + bkg_and_sig_builder(f0) + ")" + operatorsFunc[k+1]
            elementaryFunc[k] = f0
        else:
            function_expression += function_builder(f0) + operatorsFunc[k+1]
            # if data == False: function_expression += function_builder(f0) + operatorsFunc[k+1]
            # else: function_expression += bkg_and_sig_builder(f0) + operatorsFunc[k+1]

    output_filename_part = re.sub("\[[0-9]+\]", "", function_tag)
    output_filename_part = output_filename_part.replace('+','_plus_')
    output_filename_part = output_filename_part.replace('-','_minus_')
    output_filename_part = output_filename_part.replace('*','_muliply_')
    output_filename_part = output_filename_part.replace('/','_divide_')
    return {'function_expression': function_expression,
            'elementaryFunc': elementaryFunc,
            'output_filename_part': output_filename_part,
    }[return_tag]

# function_expression = ''
# set_parameters = {
#         'gaus': [[],[]]
#         'landau' [[],[]]
#         'myexp' [[],[]]
#
# }

def dijet_mass_function_pars_init(hist, function_tag):
    number_of_pars = 0
    num_of_func = {}
    elementaryFunc = function_expression(function_tag, 'elementaryFunc')
    for f in elementaryFunc:
        delim_out = re.split("\[|\]", f)
        num_of_func[delim_out[0]] = 0
    # num_of_func = {'gaus': 0,
    #                 'myexp': 0,
    #                 'landau': 0,
    #                 'crystalball': 0,
    #                 'bkg': 0}

    # print num_of_func
    # exit()
    area = hist.Integral()
    x0 = hist.GetBinCenter(hist.GetMaximumBin())
    sigma = hist.GetRMS()

    start_value = { 'gaus':         {'Area': [area, area, area], 'mean': [200, 450, x0], 'sigma': [sigma/2, sigma/2, sigma/2]},
                    'landau':       {'Area': [area, area], 'x0':   [750, x0], 's':     [500, 500]},
                    'myexp':        {'A': [0],'a': [0],'s': [0]},
                    'crystalball':  {'alpha': [1],'n': [1], 'mean': [x0], 'sigma': [sigma], 'Area': [area]},
                    'bkg0':         {'p0': [6.845],'p1': [6.7807], 'p2': [6.7807], 'p3': [0.30685]},
                    'bkg_norm':     {'p1': [2.24156e+01],'p2': [4.90035e+00], 'p3': [2.14805e-01], 'm_eff': [1.32162e+02], 'sigma_eff': [1.82948e+02]},
                    'bkg':          {'p0': [6.845], 'p1': [6.845],'p2': [6.7807], 'p3': [0.30685], 'm_eff': [495.7], 'sigma_eff': [96.0]},
                    't_student':    {'Area': [area], 'mean': [x0], 'sigma': [sigma]},
                    'bias':         {'offset': [0]},
                    'myline':       {'offset': [0], 'slope': [1]},
                    'gamma':        {'Area': [area, area], 'alpha': [1,1], 'theta': [1,1], 'x0': [x0,x0]}
                    }
    print start_value
    limits_value = {
                    'low': {
                             'gaus':         {  'Area':     [0.1,0.1,0],
                                                'mean':     [100,200,0],
                                                'sigma':    [0,0,0]},
                             'landau':       {  'Area':     [0,0,0],
                                                'x0':       [400,0,0],
                                                's':        [0,0,0]},
                             'myexp':        {  'A':        [0,0,0],
                                                'a':        [0,0,0],
                                                's':        [0,0,0]},
                             'crystalball':  {  'alpha':    [0,0,0],
                                                'n':        [0,0,0],
                                                'mean':     [0,0,0],
                                                'sigma':    [0,0,0],
                                                'Area':     [0,0,0]},
                             'bkg0':         { 'p0':        [0,0,0],
                                                'p1':       [0,0,0],
                                                'p2':       [0,0,0],
                                                'p3':       [-10,0,0],},
                             'bkg_norm':     {  'p1':       [-1000,0,0],
                                                'p2':       [-100,0,0],
                                                'p3':       [-100,0,0],
                                                'm_eff':    [0,0,0],
                                                'sigma_eff':[0,0,0]},
                             'bkg':          {  'p0':       [0,0,0],
                                                'p1':       [0,0,0],
                                                'p2':       [0,0,0],
                                                'p3':       [-10,0,0],
                                                'm_eff':    [450,0,0],
                                                'sigma_eff':[80,0,0]},
                             't_student':    {  'Area':     [0,0,0],
                                                'mean':     [0,0,0],
                                                'sigma':    [0,0,0]},
                             'bias':         {  'offset':   [0,0,0]},
                             'myline':       {  'offset':   [0,0,0],
                                                'slope':    [0,0,0]},
                             'gamma':        {  'Area':     [0,0,0],
                                                'alpha':    [0,0,0],
                                                'theta':    [0,0,0],
                                                'x0':       [0,0,0]},
                             },
                    'up': {
                             'gaus':         {  'Area':     [100*area,10*area,10*area],
                                                'mean':     [700, 700, 1000],
                                                'sigma':    [10*sigma,10*sigma,10*sigma]},
                             'landau':       {  'Area':     [100*area,20*area,10*area],
                                                'x0':       [1000,1000,1000],
                                                's':        [10000,10000,1000]},
                             'myexp':        {  'A':        [10*area,10*area,10*area],
                                                'a':        [1000,1000,1000],
                                                's':        [1000,1000,1000]},
                             'crystalball':  {  'alpha':    [1000,1000,1000],
                                                'n':        [1000,1000,1000],
                                                'mean':     [1000,1000,1000],
                                                'sigma':    [700,700,700],
                                                'Area':     [10*area,10*area,10*area]},
                             'bkg0':         {  'p0':       [100,0,0],
                                                'p1':       [100,0,0],
                                                'p2':       [100,0,0],
                                                'p3':       [10,0,0],},
                             'bkg_norm':     {  'p1':       [100,0,0],
                                                'p2':       [100,0,0],
                                                'p3':       [10,0,0],
                                                'm_eff':    [10000,0,0],
                                                'sigma_eff':[220,0,0]},
                             'bkg':          {  'p0':       [100,0,0],
                                                'p1':       [100,0,0],
                                                'p2':       [100,0,0],
                                                'p3':       [10,0,0],
                                                'm_eff':    [550,0,0],
                                                'sigma_eff':[120,0,0]},
                             't_student':    {  'Area':     [10*area,10*area,10*area],
                                                'mean':     [1000,1000,1000],
                                                'sigma':    [700,700,700]},
                             'bias':         {  'offset':   [1000,1000,1000]},
                             'myline':       {  'offset':   [1000,1000,1000],
                                                'slope':    [1000,1000,1000]},
                             'gamma':        {  'Area':     [10*area,10*area,10*area],
                                                'alpha':    [1000,1000,1000],
                                                'theta':    [1000,1000,1000],
                                                'x0':       [1000,1000,1000]},
                             },
                    }
    parameter_num = 0
    name_of_pars = []
    start_values = []
    lower_bound = []
    upper_bound = []
    for i,f in enumerate(elementaryFunc):
        delim_out = re.split("\[|\]", f)
        # j = int(delim_out[1])
        for j,pars in start_value.iteritems():
            if delim_out[0] == j:
                for nameOfParsIter,par in enumerate(namesOfPars[j]):
                    name_of_pars.append(namesOfPars[j][nameOfParsIter]+'_'+j+'_'+str(num_of_func[j]))
                    start_values.append(start_value[j][namesOfPars[j][nameOfParsIter]][num_of_func[j]])
                    lower_bound.append(limits_value['low'][j][namesOfPars[j][nameOfParsIter]][num_of_func[j]])
                    upper_bound.append(limits_value['up'][j][namesOfPars[j][nameOfParsIter]][num_of_func[j]])
                    # function_fit.SetParName(parameter_num, k+'_'+j+'_'+str(num_of_func[j]))
                number_of_pars += len(start_value[j])
                num_of_func[j] += 1
    return {
            'number_of_pars'    : number_of_pars,
            'name_of_pars'      : name_of_pars,
            'start_values'      : start_values,
            'lower_bound'       : lower_bound,
            'upper_bound'       : upper_bound,
            }


def number_of_pars_func(function_tag):
    number_of_pars = 0
    elementaryFunc = function_expression(function_tag, 'elementaryFunc')
    for i,f in enumerate(elementaryFunc):
        delim_out = re.split("\[|\]", f)
        for j,pars in namesOfPars.iteritems():
            if delim_out[0] == j:
                number_of_pars += len(pars)
    return number_of_pars


def simple_fit(hist, fexpr, function_tag):
    fitFunction = ""
    function_fit = TF1(function_name, fexpr, range_of_fit_left, range_of_fit_right)
    # number_of_pars =  dijet_mass_function_pars_init(hist, function_fit, function_tag, 'number_of_pars')
    set_init = dijet_mass_function_pars_init(hist, function_tag)
    number_of_pars = set_init['number_of_pars']
    print number_of_pars
    for i in range(0, number_of_pars):
        nameOfPar = set_init['name_of_pars'][i]
        start_value = set_init['start_values'][i]
        lower_bound = set_init['lower_bound'][i]
        upper_bound = set_init['upper_bound'][i]
        function_fit.SetParName(i, nameOfPar)
        function_fit.SetParameter(i, start_value)
        function_fit.SetParLimits(i, lower_bound, upper_bound)
    for i in range(0, int(number_of_fit)):
        hist.Fit(function_name, "RLM", "ep")
    chi_square_file.write(function_tag+": ")
    chi_square_file.write(str(function_fit.GetChisquare())+"/"+str(((range_of_fit_right-range_of_fit_left)/bin_width-number_of_pars))+"\n")
    print "chi_square = ", str(function_fit.GetChisquare())+"/"+str(((range_of_fit_right-range_of_fit_left)/bin_width-number_of_pars)), " = ",function_fit.GetChisquare()/(((range_of_fit_right-range_of_fit_left)/bin_width-number_of_pars))
    return function_fit

def dijet_mass_fit(hist, fexpr, function_tag):
    print("fexpr = ",fexpr)
    print("function_tag = ", function_tag)
    # function_fit.SetNpx(10*int((histo_range_right-histo_range_left)/float(options.bin_width)) )
    # print "formula: ", function_fit.GetExpFormula()
    TVirtualFitter.SetMaxIterations(100000)
    if options.fit_option == "roofit":
        function_fit = fit_roofit(hist, fexpr,function_tag)
        # number_of_pars =  dijet_mass_function_pars_init(hist, function_fit, function_tag, 'number_of_pars')
    elif options.fit_option == "default":
        function_fit = simple_fit(hist, fexpr, function_tag)
    # exit()
    return function_fit


def dijet_mass_draw(rootTree, hist, canvas, fileName, var, nameHist, selection, fexpr, function_tag):
    if not rootTree == "": rootTree.Project(nameHist, var, selection)
    if options.path == "":
        fileName = re.split("_|\-", fileName)
        if data == False:
            fileName = fileName[2]+"_"+fileName[3]+"GeV_"+fileName[4]+"_"+fileName[6]+"_"+fileName[7]
        else:
            fileName = fileName[3]
    else:
        fileName = re.split("\.|\/", fileName)
        fileName = fileName[-2]
    # print "data = ", data
    #hist.Sumw2()
    if data == False:
        legend = TLegend(leg_pos_x1, leg_pos_y1, leg_pos_x2, leg_pos_y2)
        if options.function_tag != "":
            if options.histo == "True":
                hist.Draw("E1P")
                hist = hist.Rebin(int(bin_width))
                hist.GetXaxis().SetRangeUser(histo_range_left, histo_range_right)
            function_fit = dijet_mass_fit(hist, fexpr, function_tag)
            # hist.Draw("E1P")
            function_fit.Draw("same")
            function_fit.SetNpx(1000)
            function_fit.SetLineWidth(4)
        else:
            hist.SetLineWidth(2)
            hist.Draw()
        set_hist_style(hist)
        legend.AddEntry(hist, "MC", "l")
        if options.function_tag != "":
            legend.AddEntry(function_fit, "Signal", "l")
            colors = [kGreen, kMagenta, kPink, kOrange, kCyan]
            tf_array = draw_f(function_fit, function_tag, legend)
            if options.constituents == "True":
                for i,f in enumerate(tf_array):
                    f.Draw("same")
                    f.SetNpx(10*int((histo_range_right-histo_range_left)/bin_width) )
                    f.SetLineColor(colors[i%(len(colors))])
                    f.SetLineStyle(2)
                    funcTitle = f.GetName()
                    legend.AddEntry(f, funcTitle, "l")
        legend.Draw("same")
    else:
        legend = TLegend(leg_pos_x1, leg_pos_y1, leg_pos_x2, leg_pos_y2)
        if options.bkg == "fit" and options.function_tag == "":
            yPadSeparation = 0.25
            padPlot = TPad("padPlot","",0.,yPadSeparation,1.,1.)
            padPlot.SetBottomMargin(.04)
            padRatio = TPad("padRatio","",0.,0.,1.,yPadSeparation)
            padRatio.SetTopMargin(0)
            padRatio.SetBottomMargin(.09/yPadSeparation)
            padRatio.Draw()
            padPlot.Draw()
            padRatio.SetGridx()
            padRatio.SetGridy()
            padPlot.SetGridx()
            padPlot.SetGridy()
            padPlot.SetLogy(1)
            padPlot.cd()
            if options.histo == "True":
                hist.Draw("E1P")
                hist.Rebin(int(bin_width))
                hist.GetXaxis().SetRangeUser(histo_range_left, histo_range_right)
            print
            function_fit = dijet_mass_fit(hist, fexpr, function_tag)
            set_hist_style(hist)
            function_fit.Draw("same")
            function_fit.SetNpx(1000)
            function_fit.SetLineWidth(2)
            legend.AddEntry(function_fit, "background", "l")
            legend.Draw("same")
            padRatio.cd()
            padSizeRatio = (padPlot.GetWh()*padPlot.GetAbsHNDC())/(padRatio.GetWh()*padRatio.GetAbsHNDC())
            ratio = getRatio(hist, function_fit, padSizeRatio)
            ratio.Draw("E1")
            # zerof = TF1("zero", "0*x", histo_range_left, histo_range_right)
            # zerof.SetLineColor(kBlack)
            # zerof.Draw("same")
        elif options.bkg == "fit" and options.function_tag != "":
            function_fit = dijet_mass_fit(hist, fexpr, function_tag)
            hist.Draw("E1P")
            set_hist_style(hist)
            function_fit.Draw("same")
            function_fit.SetNpx(1000)
            function_fit.SetLineWidth(4)
            legend.AddEntry(hist, "data", "l")
            legend.AddEntry(function_fit, "background+signal", "l")
            colors = [kGreen, kMagenta]
            titles = ["background","signal"]
            tf_array = draw_f(function_fit, function_tag, legend)
            # print tf_array
            for i,f in enumerate(tf_array):
                f.Draw("same")
                f.SetNpx(10*int((histo_range_right-histo_range_left)/bin_width) )
                f.SetLineColor(colors[i%(len(colors))])
                f.SetLineStyle(2)
                funcTitle = f.GetName()
                legend.AddEntry(f, titles[i], "l")
    #hist.Draw("E same")
    if not os.path.isdir("output_plots"):
        os.mkdir("output_plots")
    # fit_func = fexpr.replace("(*)","")
    # print fit_func
    # exit()
    if options.function_tag != "":
        canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+"_"+function_expression(function_tag, 'output_filename_part')+".pdf")
        canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+"_"+function_expression(function_tag, 'output_filename_part')+".root")
        canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+"_"+function_expression(function_tag, 'output_filename_part')+".png")
        canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+"_"+function_expression(function_tag, 'output_filename_part')+".eps")
    else:
        canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+".pdf")
        canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+".root")
        canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+".png")
        canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+".eps")

def dijet_mass_plot(path, directory, mass, function_tag, var):
    canvas = TCanvas("c1", "c1", 0, 0, 1600, 900)
    fexpr = function_expression(function_tag, 'function_expression')
    # print fexpr
    # exit()
    # if data == False:
    if path == "":
        rootTree = {}
        histDijetMass = {}
        pathlist = os.listdir(directory)
        # print data
        mass = re.split(",|, ", mass)
        for m in mass:
            rootTree[m] = TChain("rootTupleTree/tree")
            histDijetMass[m] = TH1F(var,"Dijet Mass", int((histo_range_right-histo_range_left)/bin_width), histo_range_left, histo_range_right)
            for file in pathlist:
                if ('rootfile_list_VectorDiJet1Jet_'+m) in file and 'reduced_skim.root' in file:
                    rootTree[m].Add(directory+"/"+file)
                    fileName = file
            dijet_mass_draw(rootTree[m], histDijetMass[m], canvas, fileName, var, var, selection, fexpr, function_tag)
            raw_input('Press <ENTER> to continue')
    else:
        if options.histo == "False":
            # fileName = re.split("/|\.", path)
            # fileName = fileName[-2]
            rootFile = TFile.Open(path)
            rootTree = rootFile.Get("rootTupleTree/tree")
            histDijetMass = TH1F("dijetMass","Dijet Mass", int((histo_range_right-histo_range_left)/bin_width), histo_range_left, histo_range_right)
            dijet_mass_draw(rootTree, histDijetMass, canvas, path, "dijet_mass", "dijetMass", selection, fexpr, function_tag)
            raw_input('Press <ENTER> to continue')
        else:
            histDijetMass = TH1F("dijetMass","Dijet Mass", int((histo_range_right-histo_range_left)), histo_range_left, histo_range_right)
            f =TFile(path)
            histDijetMass = f.Get("DijetFilter/dijetMassHisto/dijet_mass")
            dijet_mass_draw("", histDijetMass, canvas, path, "dijet_mass", "dijetMass", "", fexpr, function_tag)
            # print histDijetMass.GetBinWidth(3)
            raw_input('Press <ENTER> to continue')


if data == False: dijet_mass_plot(options.path, options.dir, options.mass, options.function_tag, options.var)
else :
    if options.function_tag == "":
        if options.fit_option == "roofit": dijet_mass_plot(options.path, options.dir, options.mass, "bkg_norm[0]", options.var)
        else: dijet_mass_plot(options.path, options.dir, options.mass, "bkg_norm[0]", options.var)
    else: dijet_mass_plot(options.path, options.dir, options.mass, "bkg_norm[0]+"+options.function_tag, options.var)


# dijet_mass_plot(options.path, options.dir, options.mass, 'bkg[0]+signal[4]', options.var)
# for f in fexpr_array:
#     dijet_mass_plot(options.path, options.dir, options.mass, f)
# function_tags = ['gaus[0]+myexp[3]',
#                  'gaus[0]+myexp[3]+myline[6]',
#                  'gaus[0]+gaus[3]',
#                  'gaus[0]+gaus[3]+myexp[6]',
#                  'gaus[0]+gaus[3]+myexp[6]+myline[9]',
#                  'gaus[0]+gaus[3]+gaus[6]+myexp[9]+myline[12]',
#                  'landau[0]',
#                   'gaus[0]+myexp[3]+myline[6]+landau[9]',
#                   'gaus[0]+gaus[3]+landau[6]',
#                   'gaus[0]+gaus[3]+myexp[6]+landau[9]',
#                   'gaus[0]+gaus[3]+myexp[6]+myline[9]+landau[12]',
#                   'gaus[0]+gaus[3]+gaus[6]+myexp[9]+myline[12]+landau[15]',
#                   'landau[0]+landau[3]',
#                   'gaus[0]+myexp[3]+myline[6]+landau[9]+landau[12]',
#                   'gaus[0]+gaus[3]+landau[6]+landau[9]',
#                   'gaus[0]+gaus[3]+myexp[6]+landau[9]+landau[12]',
#                   'gaus[0]+gaus[3]+myexp[6]+myline[9]+landau[12]+landau[15]',
#                   'gaus[0]+gaus[3]+gaus[6]+myexp[9]+myline[12]+landau[15]+landau[18]',
#                   'crystalball[0]',
#                   'crystalball[0]+gaus[5]',
#                   'crystalball[0]+landau[5]',
#                   'crystalball[0]+landau[5]+gaus[10]',
#                   'crystalball[0]+gaus[5]+gaus[10]',
#                   'crystalball[0]+landau[5]+landau[10]',
#                   'crystalball[0]+crystalball[5]',
#                   'crystalball[0]+crystalball[5]+landau[10]',
#                   'crystalball[0]+crystalball[5]+landau[10]+landau[13]',
#                   'crystalball[0]+crystalball[5]+gaus[10]',
#                   'crystalball[0]+crystalball[5]+gaus[10]+gaus[13]',
#                   'crystalball[0]+crystalball[5]+landau[10]+gaus[13]',
#                   'crystalball[0]+crystalball[5]+landau[10]+landau[13]+gaus[16]',
#                   'crystalball[0]+crystalball[5]+landau[10]+gaus[13]+gaus[16]',
#                   'crystalball[0]+crystalball[5]+landau[10]+landau[13]+gaus[16]+gaus[19]',
#                   'landau[0]+landau[3]+landau[6]',
#                   'crystalball[0]+crystalball[5]+crystalball[10]',
#
#                  ]
# for f in function_tags:
#     print "=======================   ", f, "   =======================",
#     dijet_mass_plot(options.path, options.dir, options.mass, f, options.var)
