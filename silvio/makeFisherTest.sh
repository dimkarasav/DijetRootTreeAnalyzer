mkdir -p fits_trijet_silvio_2018/Nom3
mkdir -p fits_trijet_silvio_2018/Nom4
mkdir -p fits_trijet_silvio_2018/Nom5
mkdir -p fits_trijet_silvio_2018/Nom6
mkdir -p fits_trijet_silvio_2018/Nom7
mkdir -p fits_trijet_silvio_2018/Alt3
mkdir -p fits_trijet_silvio_2018/Alt4
mkdir -p fits_trijet_silvio_2018/Alt5
mkdir -p fits_trijet_silvio_2018/Alt6
mkdir -p fits_trijet_silvio_2018/Alt7

python python/BinnedFit.py -c config/dijet_isr_DijetFisherNom3.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Nom3 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logNom3 &
python python/BinnedFit.py -c config/dijet_isr_DijetFisherNom4.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Nom4 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logNom4 &
python python/BinnedFit.py -c config/dijet_isr_DijetFisherNom5.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Nom5 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logNom5 &
python python/BinnedFit.py -c config/dijet_isr_DijetFisherNom6.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Nom6 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logNom6 &
python python/BinnedFit.py -c config/dijet_isr_DijetFisherNom7.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Nom7 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logNom7 &

python python/BinnedFit.py -c config/dijet_isr_DijetFisherAlt3.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Alt3 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logAlt3 &
python python/BinnedFit.py -c config/dijet_isr_DijetFisherAlt4.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Alt4 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logAlt4 &
python python/BinnedFit.py -c config/dijet_isr_DijetFisherAlt5.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Alt5 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logAlt5 &
python python/BinnedFit.py -c config/dijet_isr_DijetFisherAlt6.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Alt6 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logAlt6 &
python python/BinnedFit.py -c config/dijet_isr_DijetFisherAlt7.config -l 971  -b CaloTrijet2016 -d fits_trijet_silvio_2018/Alt7 --fit-spectrum inputs/data_blind_eta2.5_jets01.root --signal inputs/ResonanceShapes_qq_13TeV_CaloScouting_2016.root  --model qq --mass 410 --xsec 20 >& logAlt7 &

cat logNom3 | grep Chi2
cat logNom4 | grep Chi2
cat logNom5 | grep Chi2
cat logNom6 | grep Chi2
cat logNom7 | grep Chi2

cat logAlt3 | grep Chi2
cat logAlt4 | grep Chi2
cat logAlt5 | grep Chi2
cat logAlt6 | grep Chi2
cat logAlt7 | grep Chi2



