import ROOT

nbins = 14

chi2 = {}
chi2[3] = 5033.
chi2[4] = 23.8
chi2[5] = 8.76
chi2[6] = 8.62
chi2[7] = 8.85

chi2Alt = {}
chi2Alt[3] = 5033.
chi2Alt[4] = 14.6
chi2Alt[5] = 9.21
chi2Alt[6] = 9.09
chi2Alt[7] = 8.98

## NB n2>n1 !
def fisher(n1,n2,chi2):
  fisher = ((chi2[n1]-chi2[n2])/(n2-n1))/(chi2[n2]/(nbins-n2))
  return fisher

def CL(fisher, n1):
  cl = 1.0 - ROOT.TMath.FDistI(fisher, 1.0, nbins - n2)
  return cl

print("")
print("NOMINAL")
print("Fisher\tCL")
for n1 in chi2.keys():
  n2 = n1+1
  if not (n2 in chi2.keys()): continue
  fish = fisher(n1,n2,chi2) 
  cl = CL(fish,n1)
  print("%d vs %d\t%f\t%f"%(n1,n2,fish,cl))


print("")
print("ALTERNATIVE")
print("Fisher\tCL")
for n1 in chi2Alt.keys():
  n2 = n1+1
  if not (n2 in chi2Alt.keys()): continue
  fish = fisher(n1,n2,chi2Alt) 
  cl = CL(fish,n1)
  print("%d vs %d\t%f\t%f"%(n1,n2,fish,cl))
