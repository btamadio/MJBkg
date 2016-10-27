#define MINITREE_CXX
#include "miniTree.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

MJ::miniTree::miniTree():fChain(0)
{
}

// MJ::miniTree::miniTree(TTree *tree) : fChain(0) 
// {
// // if parameter tree is not specified (or zero), connect the file
// // used to generate this class and read the Tree.
//    if (tree == 0) {
//       TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("data2015/main_data2015.root");
//       if (!f || !f->IsOpen()) {
//          f = new TFile("data2015/main_data2015.root");
//       }
//       f->GetObject("miniTree",tree);
//    }
//    Init(tree);
// }

MJ::miniTree::~miniTree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t MJ::miniTree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t MJ::miniTree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void MJ::miniTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   jet_pt = 0;
   jet_eta = 0;
   jet_phi = 0;
   jet_m = 0;
   jet_bmatched_Fix60 = 0;
   jet_bmatched_Fix70 = 0;
   jet_bmatched_Fix77 = 0;
   jet_bmatched_Fix85 = 0;
   jet_bmatched_Flt60 = 0;
   jet_bmatched_Flt70 = 0;
   jet_bmatched_Flt77 = 0;
   jet_bmatched_Flt85 = 0;
   jet_NTrimSubjets = 0;
   jet_qmatched = 0;
   jet_gmatched = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
   fChain->SetBranchAddress("mcChannelNumber", &mcChannelNumber, &b_mcChannelNumber);
   fChain->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
   fChain->SetBranchAddress("lumiBlock", &lumiBlock, &b_lumiBlock);
   fChain->SetBranchAddress("mu", &mu, &b_mu);
   fChain->SetBranchAddress("isMC", &isMC, &b_isMC);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("njet", &njet, &b_njet);
   fChain->SetBranchAddress("njet_soft", &njet_soft, &b_njet_soft);
   fChain->SetBranchAddress("njet_ak4", &njet_ak4, &b_njet_ak4);
   fChain->SetBranchAddress("nbjet_Fix60", &nbjet_Fix60, &b_nbjet_Fix60);
   fChain->SetBranchAddress("nbjet_Fix70", &nbjet_Fix70, &b_nbjet_Fix70);
   fChain->SetBranchAddress("nbjet_Fix77", &nbjet_Fix77, &b_nbjet_Fix77);
   fChain->SetBranchAddress("nbjet_Fix85", &nbjet_Fix85, &b_nbjet_Fix85);
   fChain->SetBranchAddress("nbjet_Flt60", &nbjet_Flt60, &b_nbjet_Flt60);
   fChain->SetBranchAddress("nbjet_Flt70", &nbjet_Flt70, &b_nbjet_Flt70);
   fChain->SetBranchAddress("nbjet_Flt77", &nbjet_Flt77, &b_nbjet_Flt77);
   fChain->SetBranchAddress("nbjet_Flt85", &nbjet_Flt85, &b_nbjet_Flt85);

   fChain->SetBranchAddress("jet_pt", &jet_pt, &b_jet_pt);
   fChain->SetBranchAddress("jet_eta", &jet_eta, &b_jet_eta);
   fChain->SetBranchAddress("jet_phi", &jet_phi, &b_jet_phi);
   fChain->SetBranchAddress("jet_m", &jet_m, &b_jet_m);
   fChain->SetBranchAddress("jet_bmatched_Fix60", &jet_bmatched_Fix60, &b_jet_bmatched_Fix60);
   fChain->SetBranchAddress("jet_bmatched_Fix70", &jet_bmatched_Fix70, &b_jet_bmatched_Fix70);
   fChain->SetBranchAddress("jet_bmatched_Fix77", &jet_bmatched_Fix77, &b_jet_bmatched_Fix77);
   fChain->SetBranchAddress("jet_bmatched_Fix85", &jet_bmatched_Fix85, &b_jet_bmatched_Fix85);
   fChain->SetBranchAddress("jet_bmatched_Flt60", &jet_bmatched_Flt60, &b_jet_bmatched_Flt60);
   fChain->SetBranchAddress("jet_bmatched_Flt70", &jet_bmatched_Flt70, &b_jet_bmatched_Flt70);
   fChain->SetBranchAddress("jet_bmatched_Flt77", &jet_bmatched_Flt77, &b_jet_bmatched_Flt77);
   fChain->SetBranchAddress("jet_bmatched_Flt85", &jet_bmatched_Flt85, &b_jet_bmatched_Flt85);
   fChain->SetBranchAddress("jet_NTrimSubjets", &jet_NTrimSubjets, &b_jet_NTrimSubjets);
   fChain->SetBranchAddress("jet_qmatched",&jet_qmatched,&b_jet_qmatched);
   fChain->SetBranchAddress("jet_gmatched",&jet_gmatched,&b_jet_gmatched);
   fChain->SetBranchAddress("dEta", &dEta, &b_dEta);
   fChain->SetBranchAddress("HT", &HT, &b_HT);
   fChain->SetBranchAddress("MJ", &MJ, &b_MJ);
   fChain->SetBranchAddress("BDTG", &BDTG, &b_BDTG);
   fChain->SetBranchAddress("bSF_60", &bSF_60, &b_bSF_60);
   fChain->SetBranchAddress("bSF_70", &bSF_70, &b_bSF_70);
   fChain->SetBranchAddress("bSF_77", &bSF_77, &b_bSF_77);
   fChain->SetBranchAddress("bSF_85", &bSF_85, &b_bSF_85);
   Notify();
}

Bool_t MJ::miniTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void MJ::miniTree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t MJ::miniTree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}

void MJ::miniTree::Loop()
{
//   In a ROOT session, you can do:
//      root> .L miniTree.C
//      root> miniTree t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
   }
}
