#include"TLorentzVector.h"
TLorentzVector a,b, genP;

float dRmatch(float j1_pt,float j1_eta,float j1_phi,float j2_pt,float j2_eta,float j2_phi,float gen_pt,float gen_eta,float gen_phi){
        a.SetPtEtaPhiM(j1_pt,j1_eta,j1_phi,0);
        b.SetPtEtaPhiM(j2_pt,j2_eta,j2_phi,0);
        genP.SetPtEtaPhiM(gen_pt,gen_eta,gen_phi,0);
        return genP.DeltaR(a+b);
}

bool match(float deltaR, float j1_pt,float j1_eta,float j1_phi,float j2_pt,float j2_eta,float j2_phi,float gen_pt,float gen_eta,float gen_phi){
        if(dRmatch(j1_pt,j1_eta,j1_phi,j2_pt,j2_eta,j2_phi,gen_pt,gen_eta,gen_phi) < deltaR) return true;
        else return false;
}
