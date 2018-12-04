#!/usr/bin/env python2.7
import sys, os

try:
    import importlib
except:
    Exception(ValueError,"Please use python >2.7")

njobs = 100
f = open('parameters.csv', 'w')

plots = []
configs = sys.argv[1:]
print "config;histo_total;histo_i"
f.write("config;histo_total;histo_i\n")
for config in configs:
    configName = config.replace("configs/","")
    configName = configName.replace(".py","")
    tempForCSV = importlib.import_module('configs.'+configName)
    counter = 0
    for histo in tempForCSV.histos:
        if counter<njobs:
            print "%s;%s;%s"%(config,njobs,counter)
            f.write("%s;%s;%s\n"%(config,njobs,counter))
        plots.append(histo.folder+"/"+histo.plotName+".png")
        counter+=1

print
print "-"*10
print "List of plots"
print "-"*10
print

check = set()
for plot in plots:
    if plot in check:
        print "### This plot will be overwritten! ###"
    print plot
    check.add(plot)

