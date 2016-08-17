#define MJ_TREE_CXX
#include "Tree.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

MJ::Tree::Tree(TTree *tree) : fChain(0) {
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
     TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("tree.root");
      if (!f || !f->IsOpen()) {
	f = new TFile("tree.root");
	f->cd("tree.root:/outTree");
      }
      TDirectory * dir = (TDirectory*)f->Get("tree.root:/outTree");
      dir->GetObject("nominal",tree);
   }
   Init(tree);
}


MJ::Tree::~Tree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}


void MJ::Tree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}

Int_t MJ::Tree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t MJ::Tree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
   }
   return centry;
}

void MJ::Tree::Init(TTree *tree)
{
   // Set object pointer
   passedTriggers = 0;
   triggerPrescales = 0;
   jet_E = 0;
   jet_m = 0;
   jet_pt = 0;
   jet_phi = 0;
   jet_eta = 0;
   jet_Timing = 0;
   jet_LArQuality = 0;
   jet_HECQuality = 0;
   jet_NegativeE = 0;
   jet_AverageLArQF = 0;
   jet_BchCorrCell = 0;
   jet_N90Constituents = 0;
   jet_LArBadHVEFracnergyFrac = 0;
   jet_LArBadHVNCell = 0;
   jet_OotFracClusters5 = 0;
   jet_OotFracClusters10 = 0;
   jet_LeadingClusterPt = 0;
   jet_LeadingClusterSecondLambda = 0;
   jet_LeadingClusterCenterLambda = 0;
   jet_LeadingClusterSecondR = 0;
   jet_clean_passLooseBad = 0;
   jet_clean_passLooseBadUgly = 0;
   jet_clean_passTightBad = 0;
   jet_clean_passTightBadUgly = 0;
   jet_HECFrac = 0;
   jet_EMFrac = 0;
   jet_CentroidR = 0;
   jet_FracSamplingMax = 0;
   jet_FracSamplingMaxIndex = 0;
   jet_LowEtConstituentsFrac = 0;
   jet_GhostMuonSegmentCount = 0;
   jet_Width = 0;
   jet_emScalePt = 0;
   jet_constScalePt = 0;
   jet_pileupScalePt = 0;
   jet_originConstitScalePt = 0;
   jet_etaJESScalePt = 0;
   jet_gscScalePt = 0;
   jet_insituScalePt = 0;
   jet_SV0 = 0;
   jet_SV1 = 0;
   jet_IP3D = 0;
   jet_SV1IP3D = 0;
   jet_MV1 = 0;
   jet_MV2c00 = 0;
   jet_MV2c10 = 0;
   jet_MV2c20 = 0;
   jet_HadronConeExclTruthLabelID = 0;
   jet_isFix60 = 0;
   jet_SFFix60 = 0;
   weight_jet_SFFix60 = 0;
   jet_isFix70 = 0;
   jet_SFFix70 = 0;
   weight_jet_SFFix70 = 0;
   jet_isFix77 = 0;
   jet_SFFix77 = 0;
   weight_jet_SFFix77 = 0;
   jet_isFix85 = 0;
   jet_SFFix85 = 0;
   weight_jet_SFFix85 = 0;
   jet_isFlt60 = 0;
   jet_SFFlt60 = 0;
   weight_jet_SFFlt60 = 0;
   jet_isFlt70 = 0;
   jet_SFFlt70 = 0;
   weight_jet_SFFlt70 = 0;
   jet_isFlt77 = 0;
   jet_SFFlt77 = 0;
   weight_jet_SFFlt77 = 0;
   jet_isFlt85 = 0;
   jet_SFFlt85 = 0;
   weight_jet_SFFlt85 = 0;
   jet_ConeTruthLabelID = 0;
   jet_TruthCount = 0;
   jet_TruthLabelDeltaR_B = 0;
   jet_TruthLabelDeltaR_C = 0;
   jet_TruthLabelDeltaR_T = 0;
   jet_PartonTruthLabelID = 0;
   jet_GhostTruthAssociationFraction = 0;
   jet_truth_E = 0;
   jet_truth_pt = 0;
   jet_truth_phi = 0;
   jet_truth_eta = 0;
   fatjet_E = 0;
   fatjet_m = 0;
   fatjet_pt = 0;
   fatjet_phi = 0;
   fatjet_eta = 0;
   fatjet_Split12 = 0;
   fatjet_Split23 = 0;
   fatjet_Split34 = 0;
   fatjet_tau1_wta = 0;
   fatjet_tau2_wta = 0;
   fatjet_tau3_wta = 0;
   fatjet_tau21_wta = 0;
   fatjet_tau32_wta = 0;
   fatjet_ECF1 = 0;
   fatjet_ECF2 = 0;
   fatjet_ECF3 = 0;
   fatjet_C2 = 0;
   fatjet_D2 = 0;
   fatjet_NTrimSubjets = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
   fChain->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
   fChain->SetBranchAddress("lumiBlock", &lumiBlock, &b_lumiBlock);
   fChain->SetBranchAddress("coreFlags", &coreFlags, &b_coreFlags);
   fChain->SetBranchAddress("timeStamp", &timeStamp, &b_timeStamp);
   fChain->SetBranchAddress("timeStampNSOffset", &timeStampNSOffset, &b_timeStampNSOffset);
   fChain->SetBranchAddress("TileError", &TileError, &b_TileError);
   fChain->SetBranchAddress("SCTError", &SCTError, &b_SCTError);
   fChain->SetBranchAddress("LArError", &LArError, &b_LArError);
   fChain->SetBranchAddress("TileFlags", &TileFlags, &b_TileFlags);
   fChain->SetBranchAddress("SCTFlags", &SCTFlags, &b_SCTFlags);
   fChain->SetBranchAddress("LArFlags", &LArFlags, &b_LArFlags);
   fChain->SetBranchAddress("weight_pileup", &weight_pileup, &b_weight_pileup);
   fChain->SetBranchAddress("NPV", &NPV, &b_NPV);
   fChain->SetBranchAddress("actualInteractionsPerCrossing", &actualInteractionsPerCrossing, &b_actualInteractionsPerCrossing);
   fChain->SetBranchAddress("averageInteractionsPerCrossing", &averageInteractionsPerCrossing, &b_averageInteractionsPerCrossing);
   fChain->SetBranchAddress("passL1", &passL1, &b_passL1);
   fChain->SetBranchAddress("passHLT", &passHLT, &b_passHLT);
   fChain->SetBranchAddress("passedTriggers", &passedTriggers, &b_passedTriggers);
   fChain->SetBranchAddress("triggerPrescales", &triggerPrescales, &b_triggerPrescales);
   fChain->SetBranchAddress("njets", &njets, &b_njets);
   fChain->SetBranchAddress("jet_E", &jet_E, &b_jet_E);
   fChain->SetBranchAddress("jet_m", &jet_m, &b_jet_m);
   fChain->SetBranchAddress("jet_pt", &jet_pt, &b_jet_pt);
   fChain->SetBranchAddress("jet_phi", &jet_phi, &b_jet_phi);
   fChain->SetBranchAddress("jet_eta", &jet_eta, &b_jet_eta);
   fChain->SetBranchAddress("jet_Timing", &jet_Timing, &b_jet_Timing);
   fChain->SetBranchAddress("jet_LArQuality", &jet_LArQuality, &b_jet_LArQuality);
   fChain->SetBranchAddress("jet_HECQuality", &jet_HECQuality, &b_jet_HECQuality);
   fChain->SetBranchAddress("jet_NegativeE", &jet_NegativeE, &b_jet_NegativeE);
   fChain->SetBranchAddress("jet_AverageLArQF", &jet_AverageLArQF, &b_jet_AverageLArQF);
   fChain->SetBranchAddress("jet_BchCorrCell", &jet_BchCorrCell, &b_jet_BchCorrCell);
   fChain->SetBranchAddress("jet_N90Constituents", &jet_N90Constituents, &b_jet_N90Constituents);
   fChain->SetBranchAddress("jet_LArBadHVEFracnergyFrac", &jet_LArBadHVEFracnergyFrac, &b_jet_LArBadHVEFracnergyFrac);
   fChain->SetBranchAddress("jet_LArBadHVNCell", &jet_LArBadHVNCell, &b_jet_LArBadHVNCell);
   fChain->SetBranchAddress("jet_OotFracClusters5", &jet_OotFracClusters5, &b_jet_OotFracClusters5);
   fChain->SetBranchAddress("jet_OotFracClusters10", &jet_OotFracClusters10, &b_jet_OotFracClusters10);
   fChain->SetBranchAddress("jet_LeadingClusterPt", &jet_LeadingClusterPt, &b_jet_LeadingClusterPt);
   fChain->SetBranchAddress("jet_LeadingClusterSecondLambda", &jet_LeadingClusterSecondLambda, &b_jet_LeadingClusterSecondLambda);
   fChain->SetBranchAddress("jet_LeadingClusterCenterLambda", &jet_LeadingClusterCenterLambda, &b_jet_LeadingClusterCenterLambda);
   fChain->SetBranchAddress("jet_LeadingClusterSecondR", &jet_LeadingClusterSecondR, &b_jet_LeadingClusterSecondR);
   fChain->SetBranchAddress("jet_clean_passLooseBad", &jet_clean_passLooseBad, &b_jet_clean_passLooseBad);
   fChain->SetBranchAddress("jet_clean_passLooseBadUgly", &jet_clean_passLooseBadUgly, &b_jet_clean_passLooseBadUgly);
   fChain->SetBranchAddress("jet_clean_passTightBad", &jet_clean_passTightBad, &b_jet_clean_passTightBad);
   fChain->SetBranchAddress("jet_clean_passTightBadUgly", &jet_clean_passTightBadUgly, &b_jet_clean_passTightBadUgly);
   fChain->SetBranchAddress("jet_HECFrac", &jet_HECFrac, &b_jet_HECFrac);
   fChain->SetBranchAddress("jet_EMFrac", &jet_EMFrac, &b_jet_EMFrac);
   fChain->SetBranchAddress("jet_CentroidR", &jet_CentroidR, &b_jet_CentroidR);
   fChain->SetBranchAddress("jet_FracSamplingMax", &jet_FracSamplingMax, &b_jet_FracSamplingMax);
   fChain->SetBranchAddress("jet_FracSamplingMaxIndex", &jet_FracSamplingMaxIndex, &b_jet_FracSamplingMaxIndex);
   fChain->SetBranchAddress("jet_LowEtConstituentsFrac", &jet_LowEtConstituentsFrac, &b_jet_LowEtConstituentsFrac);
   fChain->SetBranchAddress("jet_GhostMuonSegmentCount", &jet_GhostMuonSegmentCount, &b_jet_GhostMuonSegmentCount);
   fChain->SetBranchAddress("jet_Width", &jet_Width, &b_jet_Width);
   fChain->SetBranchAddress("jet_emScalePt", &jet_emScalePt, &b_jet_emScalePt);
   fChain->SetBranchAddress("jet_constScalePt", &jet_constScalePt, &b_jet_constScalePt);
   fChain->SetBranchAddress("jet_pileupScalePt", &jet_pileupScalePt, &b_jet_pileupScalePt);
   fChain->SetBranchAddress("jet_originConstitScalePt", &jet_originConstitScalePt, &b_jet_originConstitScalePt);
   fChain->SetBranchAddress("jet_etaJESScalePt", &jet_etaJESScalePt, &b_jet_etaJESScalePt);
   fChain->SetBranchAddress("jet_gscScalePt", &jet_gscScalePt, &b_jet_gscScalePt);
   fChain->SetBranchAddress("jet_insituScalePt", &jet_insituScalePt, &b_jet_insituScalePt);
   fChain->SetBranchAddress("jet_SV0", &jet_SV0, &b_jet_SV0);
   fChain->SetBranchAddress("jet_SV1", &jet_SV1, &b_jet_SV1);
   fChain->SetBranchAddress("jet_IP3D", &jet_IP3D, &b_jet_IP3D);
   fChain->SetBranchAddress("jet_SV1IP3D", &jet_SV1IP3D, &b_jet_SV1IP3D);
   fChain->SetBranchAddress("jet_MV1", &jet_MV1, &b_jet_MV1);
   fChain->SetBranchAddress("jet_MV2c00", &jet_MV2c00, &b_jet_MV2c00);
   fChain->SetBranchAddress("jet_MV2c10", &jet_MV2c10, &b_jet_MV2c10);
   fChain->SetBranchAddress("jet_MV2c20", &jet_MV2c20, &b_jet_MV2c20);
   fChain->SetBranchAddress("jet_HadronConeExclTruthLabelID", &jet_HadronConeExclTruthLabelID, &b_jet_HadronConeExclTruthLabelID);
   fChain->SetBranchAddress("njets_Fix60", &njets_Fix60, &b_njets_Fix60);
   fChain->SetBranchAddress("jet_isFix60", &jet_isFix60, &b_jet_isFix60);
   fChain->SetBranchAddress("njets_Fix70", &njets_Fix70, &b_njets_Fix70);
   fChain->SetBranchAddress("jet_isFix70", &jet_isFix70, &b_jet_isFix70);
   fChain->SetBranchAddress("njets_Fix77", &njets_Fix77, &b_njets_Fix77);
   fChain->SetBranchAddress("jet_isFix77", &jet_isFix77, &b_jet_isFix77);
   fChain->SetBranchAddress("njets_Fix85", &njets_Fix85, &b_njets_Fix85);
   fChain->SetBranchAddress("jet_isFix85", &jet_isFix85, &b_jet_isFix85);
   fChain->SetBranchAddress("njets_Flt60", &njets_Flt60, &b_njets_Flt60);
   fChain->SetBranchAddress("jet_isFlt60", &jet_isFlt60, &b_jet_isFlt60);
   fChain->SetBranchAddress("njets_Flt70", &njets_Flt70, &b_njets_Flt70);
   fChain->SetBranchAddress("jet_isFlt70", &jet_isFlt70, &b_jet_isFlt70);
   fChain->SetBranchAddress("njets_Flt77", &njets_Flt77, &b_njets_Flt77);
   fChain->SetBranchAddress("jet_isFlt77", &jet_isFlt77, &b_jet_isFlt77);
   fChain->SetBranchAddress("njets_Flt85", &njets_Flt85, &b_njets_Flt85);
   fChain->SetBranchAddress("jet_isFlt85", &jet_isFlt85, &b_jet_isFlt85);
   fChain->SetBranchAddress("nfatjets", &nfatjets, &b_nfatjets);
   fChain->SetBranchAddress("fatjet_E", &fatjet_E, &b_fatjet_E);
   fChain->SetBranchAddress("fatjet_m", &fatjet_m, &b_fatjet_m);
   fChain->SetBranchAddress("fatjet_pt", &fatjet_pt, &b_fatjet_pt);
   fChain->SetBranchAddress("fatjet_phi", &fatjet_phi, &b_fatjet_phi);
   fChain->SetBranchAddress("fatjet_eta", &fatjet_eta, &b_fatjet_eta);
   fChain->SetBranchAddress("fatjet_Split12", &fatjet_Split12, &b_fatjet_Split12);
   fChain->SetBranchAddress("fatjet_Split23", &fatjet_Split23, &b_fatjet_Split23);
   fChain->SetBranchAddress("fatjet_Split34", &fatjet_Split34, &b_fatjet_Split34);
   fChain->SetBranchAddress("fatjet_tau1_wta", &fatjet_tau1_wta, &b_fatjet_tau1_wta);
   fChain->SetBranchAddress("fatjet_tau2_wta", &fatjet_tau2_wta, &b_fatjet_tau2_wta);
   fChain->SetBranchAddress("fatjet_tau3_wta", &fatjet_tau3_wta, &b_fatjet_tau3_wta);
   fChain->SetBranchAddress("fatjet_tau21_wta", &fatjet_tau21_wta, &b_fatjet_tau21_wta);
   fChain->SetBranchAddress("fatjet_tau32_wta", &fatjet_tau32_wta, &b_fatjet_tau32_wta);
   fChain->SetBranchAddress("fatjet_ECF1", &fatjet_ECF1, &b_fatjet_ECF1);
   fChain->SetBranchAddress("fatjet_ECF2", &fatjet_ECF2, &b_fatjet_ECF2);
   fChain->SetBranchAddress("fatjet_ECF3", &fatjet_ECF3, &b_fatjet_ECF3);
   fChain->SetBranchAddress("fatjet_C2", &fatjet_C2, &b_fatjet_C2);
   fChain->SetBranchAddress("fatjet_D2", &fatjet_D2, &b_fatjet_D2);
   fChain->SetBranchAddress("fatjet_NTrimSubjets", &fatjet_NTrimSubjets, &b_fatjet_NTrimSubjets);
   if(fChain->GetListOfBranches()->Contains("mcChannelNumber")){
     //Branches that only appear in the MC trees
     isMC = true;
     fChain->SetBranchAddress("jet_SFFix60", &jet_SFFix60, &b_jet_SFFix60);
     fChain->SetBranchAddress("jet_SFFix70", &jet_SFFix70, &b_jet_SFFix70);
     fChain->SetBranchAddress("jet_SFFix77", &jet_SFFix77, &b_jet_SFFix77);
     fChain->SetBranchAddress("jet_SFFix85", &jet_SFFix85, &b_jet_SFFix85);
     fChain->SetBranchAddress("jet_SFFlt60", &jet_SFFlt60, &b_jet_SFFlt60);
     fChain->SetBranchAddress("jet_SFFlt70", &jet_SFFlt70, &b_jet_SFFlt70);
     fChain->SetBranchAddress("jet_SFFlt77", &jet_SFFlt77, &b_jet_SFFlt77);
     fChain->SetBranchAddress("jet_SFFlt85", &jet_SFFlt85, &b_jet_SFFlt85);
     fChain->SetBranchAddress("weight_jet_SFFix60", &weight_jet_SFFix60, &b_weight_jet_SFFix60);
     fChain->SetBranchAddress("weight_jet_SFFix70", &weight_jet_SFFix70, &b_weight_jet_SFFix70);
     fChain->SetBranchAddress("weight_jet_SFFix77", &weight_jet_SFFix77, &b_weight_jet_SFFix77);
     fChain->SetBranchAddress("weight_jet_SFFix85", &weight_jet_SFFix85, &b_weight_jet_SFFix85);
     fChain->SetBranchAddress("weight_jet_SFFlt60", &weight_jet_SFFlt60, &b_weight_jet_SFFlt60);
     fChain->SetBranchAddress("weight_jet_SFFlt70", &weight_jet_SFFlt70, &b_weight_jet_SFFlt70);
     fChain->SetBranchAddress("weight_jet_SFFlt77", &weight_jet_SFFlt77, &b_weight_jet_SFFlt77);
     fChain->SetBranchAddress("weight_jet_SFFlt85", &weight_jet_SFFlt85, &b_weight_jet_SFFlt85);
     fChain->SetBranchAddress("mcEventNumber", &mcEventNumber, &b_mcEventNumber);
     fChain->SetBranchAddress("mcChannelNumber", &mcChannelNumber, &b_mcChannelNumber);
     fChain->SetBranchAddress("mcEventWeight", &mcEventWeight, &b_mcEventWeight);
     fChain->SetBranchAddress("weight_xs", &weight_xs, &b_weight_xs);
     fChain->SetBranchAddress("weight", &weight, &b_weight);
     fChain->SetBranchAddress("jet_ConeTruthLabelID", &jet_ConeTruthLabelID, &b_jet_ConeTruthLabelID);
     fChain->SetBranchAddress("jet_TruthCount", &jet_TruthCount, &b_jet_TruthCount);
     fChain->SetBranchAddress("jet_TruthLabelDeltaR_B", &jet_TruthLabelDeltaR_B, &b_jet_TruthLabelDeltaR_B);
     fChain->SetBranchAddress("jet_TruthLabelDeltaR_C", &jet_TruthLabelDeltaR_C, &b_jet_TruthLabelDeltaR_C);
     fChain->SetBranchAddress("jet_TruthLabelDeltaR_T", &jet_TruthLabelDeltaR_T, &b_jet_TruthLabelDeltaR_T);
     fChain->SetBranchAddress("jet_PartonTruthLabelID", &jet_PartonTruthLabelID, &b_jet_PartonTruthLabelID);
     fChain->SetBranchAddress("jet_GhostTruthAssociationFraction", &jet_GhostTruthAssociationFraction, &b_jet_GhostTruthAssociationFraction);
     fChain->SetBranchAddress("jet_truth_E", &jet_truth_E, &b_jet_truth_E);
     fChain->SetBranchAddress("jet_truth_pt", &jet_truth_pt, &b_jet_truth_pt);
     fChain->SetBranchAddress("jet_truth_phi", &jet_truth_phi, &b_jet_truth_phi);
     fChain->SetBranchAddress("jet_truth_eta", &jet_truth_eta, &b_jet_truth_eta);
   }
}

