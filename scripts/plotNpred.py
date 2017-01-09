#!/usr/bin/env python
import argparse,os,ROOT,math
from array import array
from glob import glob

parser = argparse.ArgumentParser(add_help=False, description='make N_pred histogram from resampled files')
parser.add_argument('inDir')
parser.add_argument('inDirResamp')
parser.add_argument('jobName')
parser.add_argument('date')
args = parser.parse_args()
def mean(lst):
    if len(lst) < 1:
        return 0
    return sum(lst) / float(len(lst))
def err(lst):
    if len(lst) < 2:
        return 0
    xbar = mean(lst)
    std = 0.0
    for entry in lst:
        std += (entry-xbar)*(entry-xbar)
    std /= float(len(lst)-1)
    return math.sqrt(std)
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gStyle.SetOptFit()
inFileList = sorted(glob(args.inDir+'/*.root'))
inFileResampList = sorted(glob(args.inDirResamp+'/*.root'))

mjCut = 0.6
histName = 'h_MJ_dressNom_4jb9'
kinHistName = 'h_MJ_kin_4jb9'

nPredList = []
nPredResampList = []

for fileName in inFileList:
    f = ROOT.TFile.Open(fileName)
    h = f.Get('h_MJ_dressNom_4jb9')
    binLow = h.FindBin(mjCut)
    binUp = h.GetNbinsX()
    nPred = h.Integral(binLow,binUp)
    nPredList.append(nPred)
for fileName in inFileResampList:
    f = ROOT.TFile.Open(fileName)
    h = f.Get('h_MJ_dressNom_4jb9')
    binLow = h.FindBin(mjCut)
    binUp = h.GetNbinsX()
    nPred = h.Integral(binLow,binUp)
    nPredResampList.append(nPred)

xBar = mean(nPredList)
s = err(nPredList)
nBins = 8
xMin = xBar-3*s
xMax = xBar+3*s
c1 = ROOT.TCanvas('c1','c1',800,600)
c1.cd()

hist = ROOT.TH1F('h_nPred','h_nPred',nBins,xMin,xMax)
for nPred in nPredList:
    hist.Fill(nPred)
hist.Draw()
hist.Fit('gaus')
hist.GetXaxis().SetTitle('N_{pred}')
hist.GetYaxis().SetTitle('number of toys')

outDir = '/project/projectdirs/atlas/www/multijet/RPV/btamadio/Resampling/'+args.date+'_'+args.jobName
cmd = 'mkdir -p '+outDir
os.system(cmd)

c1.Print(outDir+'/plot_Npred.pdf')
c1.Print(outDir+'/plot_Npred.png')
c1.Print(outDir+'/plot_Npred.C')


xBar = mean(nPredResampList)
s = err(nPredResampList)
nBins = 8
xMin = xBar-3*s
xMax = xBar+3*s
c2 = ROOT.TCanvas('c2','c2',800,600)
c2.cd()

histResamp = ROOT.TH1F('h_nPred_resamp','h_nPred_resamp',nBins,xMin,xMax)
for nPred in nPredResampList:
    histResamp.Fill(nPred)
histResamp.Draw()
histResamp.GetXaxis().SetTitle('N_{pred}')
histResamp.GetYaxis().SetTitle('number of toys')
histResamp.Fit('gaus')

outDir = '/project/projectdirs/atlas/www/multijet/RPV/btamadio/Resampling/'+args.date+'_'+args.jobName
cmd = 'mkdir -p '+outDir
os.system(cmd)

c2.Print(outDir+'/plot_Npred_resamp.pdf')
c2.Print(outDir+'/plot_Npred_resamp.png')
c2.Print(outDir+'/plot_Npred_resamp.C')

os.system('chmod a+r '+outDir+'/*')
print 'hist.Mean() = %f, histResamp.Mean() = %f' % (hist.GetMean(),histResamp.GetMean())
print 'hist.RMS() = %f, histResamp.RMS() = %f' % (hist.GetRMS(),histResamp.GetRMS())



