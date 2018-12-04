#! /usr/bin/env python

from ROOT import *
import os, multiprocessing
import copy
import math
from array import array
import optparse
import re

gStyle.SetOptStat(0)
default_function_tag = 'gaus[0]'
default_isrpt = "50"
default_dir = "./"
default_mass = "300"
default_path = ""
leg_pos_x1 = 0.75
leg_pos_x2 = 0.9
leg_pos_y1 = 0.5
leg_pos_y2 = 0.65
chi_square_file = open("chi_squares.txt", "a")
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
parser.add_option("-F", "--fit", action="store", type="string", dest="fit", default="nofit")
parser.add_option("-H", "--histo", action="store", type="string", dest="histo", default="False")
parser.add_option("-c", "--constituents", action="store", type="string", dest="constituents", default="False")
parser.add_option("",   "--range-of-fit", action="store", type="string", dest="range_of_fit", default="")
parser.add_option("",   "--bkg", action="store", type="string", dest="bkg", default="nofit")

(options, args) = parser.parse_args()

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

# print histo_range_right, range_of_fit_right
# exit()

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
            fx = max(0.001,function_fit.Eval(ratio.GetBinCenter(i)))
            val = (hist.GetBinContent(i) - fx)/(fx**0.5)
            ratio.SetBinContent(i,val)

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
    if data == False:
        for i,el in enumerate(elementaryFunc):
            if el == 'gaus['+str(i)+']' or 'myexp['+str(i)+']' or 'landau['+str(j)+']':
                funcTitle = re.sub("\[|\]", "", el)
                print "funcTitle = ", funcTitle
                func = function_builder(el)
                print "func = ", func
                func = func.replace("["+str(3*i)+"]", str(function_fit.GetParameter(3*i)))
                func = func.replace("["+str(3*i+1)+"]", str(function_fit.GetParameter(3*i+1)))
                func = func.replace("["+str(3*i+2)+"]", str(function_fit.GetParameter(3*i+2)))
                tf_array.append(TF1(funcTitle, func, range_of_fit_left, range_of_fit_right))
                # tf_array[i].Draw("same")
                # tf_array[i].SetLineColor(i)
                # legend.AddEntry(tf_array[i], funcTitle, "l")
    else:
        fexpr = function_expression(function_tag, 'function_expression')
        func = function_builder("bkg[0]")
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
    # print func
    # exit()
    j = int(delim_out[1])
    if data == True: jj = j+4
    return {
        'bias['+str(j)+']' : "["+str(jj)+"]",
        'myline['+str(j)+']' : "["+str(jj)+"]+["+str(jj+1)+"]*x",
        #'gaus['+str(j)+']' : "gaus("+str(jj)+")",
        'gaus['+str(j)+']' : "["+str(jj)+"]*TMath::Gaus(x, ["+str(jj+1)+"], ["+str(jj+2)+"], 1)",
        'myexp['+str(j)+']' : "["+str(jj)+"]*exp(-["+str(jj+1)+"]*(x-["+str(jj+2)+"]))",
        'landau['+str(j)+']' : "["+str(jj)+"]*TMath::Landau(x,["+str(jj+1)+"],["+str(jj+2)+"],1)",
        'crystalball['+str(j)+']' : "["+str(jj+4)+"]*ROOT::Math::crystalball_function(x, ["+str(jj)+"], ["+str(jj+1)+"], ["+str(jj+2)+"], ["+str(jj+3)+"])",
#        'bkg['+str(j)+']' : "["+str(j)+"]*(1-x/13000)**["+str(j+1)+"]/((x/13000)**(["+str(j+2)+"]+["+str(j+3)+"]*TMath::Log(x/13000)))",
        'bkg['+str(j)+']' : "["+str(j)+"]*(1-x)**["+str(j+1)+"]/((x)**(["+str(j+2)+"]+["+str(j+3)+"]*TMath::Log(x)))",
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
selection = "isr_pt > " + options.isrpt +" && jet2_pt>45  && abs(dijet_deta)<1.2 && jet1_pt>90 && L1_HTT240 == 1"
number_of_fit = options.number_of_fit
print function_builder('bkg[0]')
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
def dijet_mass_function_setparameters(hist, function_fit, function_tag):
    number_of_par = 0
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
    namesOfPars = { 'gaus':         ['Area', 'mean', 'sigma'],
                    'landau':       ['Area', 'x0', 's'],
                    'myexp':        ['A','a','s'],
                    'crystalball':  ['alpha','n', 'mean', 'sigma'],
                    'bkg':          ['p0','p1','p2','p3'],
                    't_student':    ['Area', 'mean', 'sigma'],
                    'bias':         ['offset'],
                    'myline':       ['offset', 'slope'],
                    'gamma':        ['Area', 'alpha', 'theta', 'x0'],
                }
    start_value = { 'gaus':         {'Area': [hist.Integral(), hist.Integral(), hist.Integral()], 'mean': [hist.GetMaximum(), hist.GetMaximum(), hist.GetMaximum()], 'sigma': [hist.GetRMS(), hist.GetRMS(), hist.GetRMS()]},
                    'landau':       {'Area': [hist.Integral(), hist.Integral()], 'x0':   [hist.GetMaximum(), hist.GetMaximum()], 's':     [500, 500]},
                    'myexp':        {'A': [0],'a': [0],'s': [0]},
                    'crystalball':  {'alpha': [1],'n': [1], 'mean': [hist.GetMaximum()], 'sigma': [hist.GetRMS()], 'Area': [hist.Integral()]},
                    'bkg':          {'p0': [0],'p1': [1],'p2': [1], 'p3': [1]},
                    't_student':    {'Area': [hist.Integral()], 'mean': [hist.GetMaximum()], 'sigma': [hist.GetRMS()]},
                    'bias':         {'offset': [0]},
                    'myline':       {'offset': [0], 'slope': [1]},
                    'gamma':        {'Area': [hist.Integral()], 'alpha': [1], 'theta': [1], 'x0': [hist.GetMaximum()]}
                    }
    print start_value
    limits_value = {
                    'low': {
                             'gaus':         {  'Area':     [0.001*hist.Integral(),0.001*hist.Integral(),0.001*hist.Integral()],
                                                'mean':     [0,0,0],
                                                'sigma':    [0,0,0]},
                             'landau':       {  'Area':     [0,0,0],
                                                'x0':       [0,0,0],
                                                's':        [0,0,0]},
                             'myexp':        {  'A':        [0,0,0],
                                                'a':        [0,0,0],
                                                's':        [0,0,0]},
                             'crystalball':  {  'alpha':    [0,0,0],
                                                'n':        [0,0,0],
                                                'mean':     [0,0,0],
                                                'sigma':    [0,0,0],
                                                'Area':     [0,0,0]},
                             'bkg':          {  'p0':       [-1,0,0],
                                                'p1':       [-1,0,0],
                                                'p2':       [-1,0,0],
                                                'p3':       [-1,0,0]},
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
                             'gaus':         {  'Area':     [10*hist.Integral(),10*hist.Integral(),10*hist.Integral()],
                                                'mean':     [1000,1000,1000],
                                                'sigma':    [5*hist.GetRMS(),5*hist.GetRMS(),5*hist.GetRMS()]},
                             'landau':       {  'Area':     [10*hist.Integral(),10*hist.Integral(),10*hist.Integral()],
                                                'x0':       [1000,1000,1000],
                                                's':        [1000,1000,1000]},
                             'myexp':        {  'A':        [10*hist.Integral(),10*hist.Integral(),10*hist.Integral()],
                                                'a':        [1000,1000,1000],
                                                's':        [1000,1000,1000]},
                             'crystalball':  {  'alpha':    [1000,1000,1000],
                                                'n':        [1000,1000,1000],
                                                'mean':     [1000,1000,1000],
                                                'sigma':    [700,700,700],
                                                'Area':     [10*hist.Integral(),10*hist.Integral(),10*hist.Integral()]},
                             'bkg':          {  'p0':       [50,10,10],
                                                'p1':       [50,10,10],
                                                'p2':       [50,10,10],
                                                'p3':       [50,10,10]},
                             't_student':    {  'Area':     [10*hist.Integral(),10*hist.Integral(),10*hist.Integral()],
                                                'mean':     [1000,1000,1000],
                                                'sigma':    [700,700,700]},
                             'bias':         {  'offset':   [1000,1000,1000]},
                             'myline':       {  'offset':   [1000,1000,1000],
                                                'slope':    [1000,1000,1000]},
                             'gamma':        {  'Area':     [10*hist.Integral(),10*hist.Integral(),10*hist.Integral()],
                                                'alpha':    [1000,1000,1000],
                                                'theta':    [1000,1000,1000],
                                                'x0':       [1000,1000,1000]},
                             },
                    }

    parameter_num = 0
    for i,f in enumerate(elementaryFunc):
        delim_out = re.split("\[|\]", f)
        # j = int(delim_out[1])
        for j,func in start_value.iteritems():
            if delim_out[0] == j:
                for nameOfParsIter,par in enumerate(namesOfPars[j]):
                    nameOfPar = namesOfPars[j][nameOfParsIter]+'_'+j+'_'+str(num_of_func[j])
                    function_fit.SetParName(parameter_num+nameOfParsIter, namesOfPars[j][nameOfParsIter]+'_'+j+'_'+str(num_of_func[j]))
                for k,par in start_value[j].iteritems():
                    nameOfPar = k+'_'+j+'_'+str(num_of_func[j])
                    function_fit.SetParameter(function_fit.GetParNumber(nameOfPar), start_value[j][k][num_of_func[j]])
                    function_fit.SetParLimits(function_fit.GetParNumber(nameOfPar), limits_value['low'][j][k][num_of_func[j]], limits_value['up'][j][k][num_of_func[j]])
                    # function_fit.SetParName(parameter_num, k+'_'+j+'_'+str(num_of_func[j]))
                    parameter_num += 1
                number_of_par += len(start_value[j])
                num_of_func[j] += 1


    ####################################################


    # for f in elementaryFunc:
    #     delim_out = re.split("\[|\]", f)
    #     j = int(delim_out[1])
    #     if delim_out[0] == 'gaus':
    #         if num_of_func[delim_out[0]] == 0:
    #             function_fit.SetParameter(j, hist.Integral())
    #             function_fit.SetParameter(j+1, hist.GetMaximum())
    #             function_fit.SetParameter(j+2, hist.GetRMS())
    #             function_fit.SetParLimits(j, 0, 10*hist.Integral())
    #             function_fit.SetParLimits(j+1, 0, 1000)
    #             function_fit.SetParLimits(j+2, 0, 5*hist.GetRMS())
    #             function_fit.SetParName(j, "A_gauss_"+str(num_of_func[delim_out[0]]))
    #             function_fit.SetParName(j+1, "m_gauss_"+str(num_of_func[delim_out[0]]))
    #             function_fit.SetParName(j+2, "s_gauss_"+str(num_of_func[delim_out[0]]))
    #         if num_of_func[delim_out[0]] == 1:
    #             function_fit.SetParameter(j, hist.Integral())
    #             function_fit.SetParLimits(j, 0, 10*hist.Integral())
    #             function_fit.SetParameter(j+1, hist.GetMaximum()-100)
    #             function_fit.SetParLimits(j+1, 0, 1000)
    #             function_fit.SetParameter(j+2, hist.GetRMS())
    #             function_fit.SetParLimits(j+2, 0, 5*hist.GetRMS())
    #             function_fit.SetParName(j, "A_gauss_"+str(num_of_func[delim_out[0]]))
    #             function_fit.SetParName(j+1, "m_gauss_"+str(num_of_func[delim_out[0]]))
    #             function_fit.SetParName(j+2, "s_gauss_"+str(num_of_func[delim_out[0]]))
    #         number_of_par += 3
    #         num_of_func[delim_out[0]] += 1
    #
    #     if delim_out[0] == 'myexp':
    #         function_fit.SetParameter(j, hist.Integral()/10)
    #         function_fit.SetParameter(j+1, 1.)
    #         function_fit.SetParameter(j+2, 0)
    #         function_fit.SetParName(j, "A_exp_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+1, "a_exp_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+2, "m_exp_"+str(num_of_func[delim_out[0]]))
    #         number_of_par += 3
    #         num_of_func[delim_out[0]] += 1
    #
    #     if delim_out[0] == 'landau':
    #         function_fit.SetParameter(j, hist.Integral())
    #         function_fit.SetParLimits(j, 0, 10*hist.Integral())
    #         function_fit.SetParameter(j+1, m_landau)
    #         function_fit.SetParLimits(j+1, 0, 1000)
    #         function_fit.SetParameter(j+2, 500)
    #         function_fit.SetParLimits(j+2, 0, 1000)
    #         function_fit.SetParName(j, "A_landau_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+1, "m_landau_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+2, "s_landau_"+str(num_of_func[delim_out[0]]))
    #         number_of_par += 3
    #         num_of_func[delim_out[0]] += 1
    #
    #     if delim_out[0] == 'crystalball':
    #         # function_fit.SetParameter(j, 300)
    #         # function_fit.SetParLimits(j, 100, 700)
    #         # function_fit.SetParameter(j+1, 1)
    #         # function_fit.SetParLimits(j+1, 100, 700)
    #         # function_fit.SetParameter(j+2, hist.GetRMS())
    #         # function_fit.SetParLimits(j+2, 0, 5*hist.GetRMS())
    #         function_fit.SetParameter(j+3, m_gaus)
    #         # function_fit.SetParLimits(j+3, 25, 1000)
    #         # function_fit.SetParameter(j+4, hist.Integral())
    #         # function_fit.SetParLimits(j+4, 0, 10*hist.Integral())
    #         function_fit.SetParName(j, "a_crlball_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+1, "n_crlball_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+2, "s_crlball_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+3, "m_crlball_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+4, "A_crlball_"+str(num_of_func[delim_out[0]]))
    #         num_of_func[delim_out[0]] += 1
    #         number_of_par += 4
    #
        # if delim_out[0] == 'bkg':
        #     function_fit.SetParameter(j, 1)
        #     function_fit.SetParLimits(j, 0, 5)
        #     function_fit.SetParameter(j+1, 1)
        #     function_fit.SetParLimits(j+1, 0, 15)
        #     function_fit.SetParameter(j+2, 1)
        #     function_fit.SetParLimits(j+2, 0, 10)
        #     function_fit.SetParameter(j+3, 0)
        #     function_fit.SetParLimits(j+3, 0, 10)
        #     function_fit.SetParName(j,   "p0_"+str(num_of_func[delim_out[0]]))
        #     function_fit.SetParName(j+1, "p1_"+str(num_of_func[delim_out[0]]))
        #     function_fit.SetParName(j+2, "p2_"+str(num_of_func[delim_out[0]]))
        #     function_fit.SetParName(j+3, "p3_"+str(num_of_func[delim_out[0]]))
        #     num_of_func[delim_out[0]] += 1
        #     number_of_par += 4
    #
    #     if delim_out[0] == 't_student':
    #         function_fit.SetParameter(j, hist.Integral())
    #         function_fit.SetParLimits(j, 0, 10*hist.Integral())
    #         function_fit.SetParameter(j+1, hist.GetMaximum())
    #         function_fit.SetParLimits(j+1, 0, 1000)
    #         function_fit.SetParameter(j+2, 500)
    #         function_fit.SetParLimits(j+2, 0, 1000)
    #         function_fit.SetParName(j, "A_student_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+1, "m_student_"+str(num_of_func[delim_out[0]]))
    #         function_fit.SetParName(j+2, "s_student_"+str(num_of_func[delim_out[0]]))
    #         number_of_par += 3
    #         num_of_func[delim_out[0]] += 1
    return number_of_par


def dijet_mass_function(hist, fexpr, function_tag):
    fitFunction = ""
    function_fit = TF1(function_name, fexpr, range_of_fit_left, range_of_fit_right)
    number_of_par =  dijet_mass_function_setparameters(hist, function_fit, function_tag)
    return function_fit

def dijet_mass_fit(hist, fexpr, function_tag):
    function_fit = dijet_mass_function(hist, fexpr, function_tag)
    print("I'm using",function_fit.GetExpFormula("P"))
    # function_fit.SetNpx(10*int((histo_range_right-histo_range_left)/float(options.bin_width)) )
    number_of_par =  dijet_mass_function_setparameters(hist, function_fit, function_tag)
    # print "formula: ", function_fit.GetExpFormula()
    TVirtualFitter.SetMaxIterations(100000)
    for i in range(0, int(number_of_fit)):
        hist.Fit(function_name, "RLM", "ep")
    chi_square_file.write(function_tag+": ")
    chi_square_file.write(str(function_fit.GetChisquare())+"/"+str(((range_of_fit_right-range_of_fit_left)/bin_width-number_of_par))+"\n")
    print "chi_square = ", str(function_fit.GetChisquare())+"/"+str(((range_of_fit_right-range_of_fit_left)/bin_width-number_of_par))
    print("Aftert fit",function_fit.GetExpFormula("P"))
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
    print "data = ", data
    if data == False:
        legend = TLegend(leg_pos_x1, leg_pos_y1, leg_pos_x2, leg_pos_y2)
        if options.fit == "fit":
            function_fit = dijet_mass_fit(hist, fexpr, function_tag)
            hist.Draw("E1P")
            function_fit.Draw("same")
            function_fit.SetNpx(1000)
            function_fit.SetLineWidth(4)
        else:
            hist.SetLineWidth(2)
            hist.Draw()
        if options.histo == "True":
            hist.Rebin(int(bin_width))
            hist.GetXaxis().SetRangeUser(histo_range_left, histo_range_right)
        set_hist_style(hist)
        legend.AddEntry(hist, "MC", "l")
        if options.fit == "fit":
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
        if options.bkg == "fit" and options.fit == "nofit":
            legend = TLegend(leg_pos_x1, leg_pos_y1, leg_pos_x2, leg_pos_y2)
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
            function_fit = dijet_mass_fit(hist, function_expression('bkg[0]', 'function_expression'), 'bkg[0]')
            set_hist_style(hist)
            function_fit.Draw("same")
            function_fit.SetNpx(1000)
            function_fit.SetLineWidth(1)
            legend.AddEntry(function_fit, "background", "l")
            legend.Draw("same")
            padRatio.cd()
            padSizeRatio = (padPlot.GetWh()*padPlot.GetAbsHNDC())/(padRatio.GetWh()*padRatio.GetAbsHNDC())
            ratio = getRatio(hist, function_fit, padSizeRatio)
            ratio.Draw("E1")
            # zerof = TF1("zero", "0*x", histo_range_left, histo_range_right)
            # zerof.SetLineColor(kBlack)
            # zerof.Draw("same")
        elif options.bkg == "fit" and options.fit == "fit":
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
    canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+"_"+function_expression(function_tag, 'output_filename_part')+".pdf")
    canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+"_"+function_expression(function_tag, 'output_filename_part')+".root")
    canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+"_"+function_expression(function_tag, 'output_filename_part')+".png")
    canvas.SaveAs("output_plots/"+fileName+"_isrpt"+options.isrpt+"_"+function_expression(function_tag, 'output_filename_part')+".eps")

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
    # else:
    #     if options.histo == "False":
    #         rootFile = TFile.Open(path)
    #         rootTree = rootFile.Get("rootTupleTree/tree")
    #         histDijetMass = TH1F("dijetMass","Dijet Mass", int((histo_range_right-histo_range_left)/float(options.bin_width)), histo_range_left, histo_range_right)
    #         if options.bkg == "fit":
    #             fexpr = bkg_and_sig_builder("bkg[0]")
    #             dijet_mass_draw(rootTree, histDijetMass, canvas, path, "dijet_mass", "dijetMass", selection, fexpr, "bkg[0]")
    #         if options.bkg == "fit" and options.fit == "fit":
    #             fexpr = bkg_and_sig_builder("bkg[0]+signal[4]")
    #             dijet_mass_draw(rootTree, histDijetMass, canvas, path, "dijet_mass", "dijetMass", selection, fexpr, "bkg[0]+signal[4]")
    #         raw_input('Press <ENTER> to continue')
    #     else:
    #         histDijetMass = TH1F("dijetMass","Dijet Mass", int((histo_range_right-histo_range_left)), histo_range_left, histo_range_right)
    #         f =TFile(path)
    #         histDijetMass = f.Get("DijetFilter/dijetMassHisto/dijet_mass")
    #         if options.bkg == "fit":
    #             fexpr = bkg_and_sig_builder("bkg[0]")
    #             dijet_mass_draw(rootTree, histDijetMass, canvas, path, "dijet_mass", "dijetMass", selection, fexpr, "bkg[0]")
    #         if options.bkg == "fit" and options.fit == "fit":
    #             fexpr = bkg_and_sig_builder("bkg[0]+signal[4]")
    #             dijet_mass_draw(rootTree, histDijetMass, canvas, path, "dijet_mass", "dijetMass", selection, fexpr, "bkg[0]+signal[4]")
    #         raw_input('Press <ENTER> to continue')

if data == False: dijet_mass_plot(options.path, options.dir, options.mass, options.function_tag, options.var)
else : dijet_mass_plot(options.path, options.dir, options.mass, "bkg[0]+"+options.function_tag, options.var)
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
