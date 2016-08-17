#ifndef MJ_TREE_H
#define MJ_TREE_H

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

#include <vector>
using namespace std;
namespace MJ {
  class Tree {
  public :
    TTree          *fChain;   //!pointer to the analyzed TTree or TChain
    Int_t           fCurrent; //!current Tree number in a TChain
    bool            isMC = false;
    // Declaration of leaf types
    Int_t           runNumber;
    Long64_t        eventNumber;
    Int_t           lumiBlock;
    UInt_t          coreFlags;
    Int_t           mcEventNumber;
    Int_t           mcChannelNumber;
    Float_t         mcEventWeight;
    Float_t         weight_xs;
    Float_t         weight;
    UInt_t          timeStamp;
    UInt_t          timeStampNSOffset;
    Bool_t          TileError;
    Bool_t          SCTError;
    Bool_t          LArError;
    UInt_t          TileFlags;
    UInt_t          SCTFlags;
    UInt_t          LArFlags;
    Float_t         weight_pileup;
    Int_t           NPV;
    Float_t         actualInteractionsPerCrossing;
    Float_t         averageInteractionsPerCrossing;
    Int_t           passL1;
    Int_t           passHLT;
    vector<string>  *passedTriggers;
    vector<float>   *triggerPrescales;
    Int_t           njets;
    vector<float>   *jet_E;
    vector<float>   *jet_m;
    vector<float>   *jet_pt;
    vector<float>   *jet_phi;
    vector<float>   *jet_eta;
    vector<float>   *jet_Timing;
    vector<float>   *jet_LArQuality;
    vector<float>   *jet_HECQuality;
    vector<float>   *jet_NegativeE;
    vector<float>   *jet_AverageLArQF;
    vector<float>   *jet_BchCorrCell;
    vector<float>   *jet_N90Constituents;
    vector<float>   *jet_LArBadHVEFracnergyFrac;
    vector<int>     *jet_LArBadHVNCell;
    vector<float>   *jet_OotFracClusters5;
    vector<float>   *jet_OotFracClusters10;
    vector<float>   *jet_LeadingClusterPt;
    vector<float>   *jet_LeadingClusterSecondLambda;
    vector<float>   *jet_LeadingClusterCenterLambda;
    vector<float>   *jet_LeadingClusterSecondR;
    vector<int>     *jet_clean_passLooseBad;
    vector<int>     *jet_clean_passLooseBadUgly;
    vector<int>     *jet_clean_passTightBad;
    vector<int>     *jet_clean_passTightBadUgly;
    vector<float>   *jet_HECFrac;
    vector<float>   *jet_EMFrac;
    vector<float>   *jet_CentroidR;
    vector<float>   *jet_FracSamplingMax;
    vector<float>   *jet_FracSamplingMaxIndex;
    vector<float>   *jet_LowEtConstituentsFrac;
    vector<float>   *jet_GhostMuonSegmentCount;
    vector<float>   *jet_Width;
    vector<float>   *jet_emScalePt;
    vector<float>   *jet_constScalePt;
    vector<float>   *jet_pileupScalePt;
    vector<float>   *jet_originConstitScalePt;
    vector<float>   *jet_etaJESScalePt;
    vector<float>   *jet_gscScalePt;
    vector<float>   *jet_insituScalePt;
    vector<float>   *jet_SV0;
    vector<float>   *jet_SV1;
    vector<float>   *jet_IP3D;
    vector<float>   *jet_SV1IP3D;
    vector<float>   *jet_MV1;
    vector<float>   *jet_MV2c00;
    vector<float>   *jet_MV2c10;
    vector<float>   *jet_MV2c20;
    vector<int>     *jet_HadronConeExclTruthLabelID;
    Int_t           njets_Fix60;
    vector<int>     *jet_isFix60;
    vector<vector<float> > *jet_SFFix60;
    vector<float>   *weight_jet_SFFix60;
    Int_t           njets_Fix70;
    vector<int>     *jet_isFix70;
    vector<vector<float> > *jet_SFFix70;
    vector<float>   *weight_jet_SFFix70;
    Int_t           njets_Fix77;
    vector<int>     *jet_isFix77;
    vector<vector<float> > *jet_SFFix77;
    vector<float>   *weight_jet_SFFix77;
    Int_t           njets_Fix85;
    vector<int>     *jet_isFix85;
    vector<vector<float> > *jet_SFFix85;
    vector<float>   *weight_jet_SFFix85;
    Int_t           njets_Flt60;
    vector<int>     *jet_isFlt60;
    vector<vector<float> > *jet_SFFlt60;
    vector<float>   *weight_jet_SFFlt60;
    Int_t           njets_Flt70;
    vector<int>     *jet_isFlt70;
    vector<vector<float> > *jet_SFFlt70;
    vector<float>   *weight_jet_SFFlt70;
    Int_t           njets_Flt77;
    vector<int>     *jet_isFlt77;
    vector<vector<float> > *jet_SFFlt77;
    vector<float>   *weight_jet_SFFlt77;
    Int_t           njets_Flt85;
    vector<int>     *jet_isFlt85;
    vector<vector<float> > *jet_SFFlt85;
    vector<float>   *weight_jet_SFFlt85;
    vector<int>     *jet_ConeTruthLabelID;
    vector<int>     *jet_TruthCount;
    vector<float>   *jet_TruthLabelDeltaR_B;
    vector<float>   *jet_TruthLabelDeltaR_C;
    vector<float>   *jet_TruthLabelDeltaR_T;
    vector<int>     *jet_PartonTruthLabelID;
    vector<float>   *jet_GhostTruthAssociationFraction;
    vector<float>   *jet_truth_E;
    vector<float>   *jet_truth_pt;
    vector<float>   *jet_truth_phi;
    vector<float>   *jet_truth_eta;
    Int_t           nfatjets;
    vector<float>   *fatjet_E;
    vector<float>   *fatjet_m;
    vector<float>   *fatjet_pt;
    vector<float>   *fatjet_phi;
    vector<float>   *fatjet_eta;
    vector<float>   *fatjet_Split12;
    vector<float>   *fatjet_Split23;
    vector<float>   *fatjet_Split34;
    vector<float>   *fatjet_tau1_wta;
    vector<float>   *fatjet_tau2_wta;
    vector<float>   *fatjet_tau3_wta;
    vector<float>   *fatjet_tau21_wta;
    vector<float>   *fatjet_tau32_wta;
    vector<float>   *fatjet_ECF1;
    vector<float>   *fatjet_ECF2;
    vector<float>   *fatjet_ECF3;
    vector<float>   *fatjet_C2;
    vector<float>   *fatjet_D2;
    vector<float>   *fatjet_NTrimSubjets;

    // List of branches
    TBranch        *b_runNumber;   //!
    TBranch        *b_eventNumber;   //!
    TBranch        *b_lumiBlock;   //!
    TBranch        *b_coreFlags;   //!
    TBranch        *b_mcEventNumber;   //!
    TBranch        *b_mcChannelNumber;   //!
    TBranch        *b_mcEventWeight;   //!
    TBranch        *b_weight_xs;   //!
    TBranch        *b_weight;   //!
    TBranch        *b_timeStamp;   //!
    TBranch        *b_timeStampNSOffset;   //!
    TBranch        *b_TileError;   //!
    TBranch        *b_SCTError;   //!
    TBranch        *b_LArError;   //!
    TBranch        *b_TileFlags;   //!
    TBranch        *b_SCTFlags;   //!
    TBranch        *b_LArFlags;   //!
    TBranch        *b_weight_pileup;   //!
    TBranch        *b_NPV;   //!
    TBranch        *b_actualInteractionsPerCrossing;   //!
    TBranch        *b_averageInteractionsPerCrossing;   //!
    TBranch        *b_passL1;   //!
    TBranch        *b_passHLT;   //!
    TBranch        *b_passedTriggers;   //!
    TBranch        *b_triggerPrescales;   //!
    TBranch        *b_njets;   //!
    TBranch        *b_jet_E;   //!
    TBranch        *b_jet_m;   //!
    TBranch        *b_jet_pt;   //!
    TBranch        *b_jet_phi;   //!
    TBranch        *b_jet_eta;   //!
    TBranch        *b_jet_Timing;   //!
    TBranch        *b_jet_LArQuality;   //!
    TBranch        *b_jet_HECQuality;   //!
    TBranch        *b_jet_NegativeE;   //!
    TBranch        *b_jet_AverageLArQF;   //!
    TBranch        *b_jet_BchCorrCell;   //!
    TBranch        *b_jet_N90Constituents;   //!
    TBranch        *b_jet_LArBadHVEFracnergyFrac;   //!
    TBranch        *b_jet_LArBadHVNCell;   //!
    TBranch        *b_jet_OotFracClusters5;   //!
    TBranch        *b_jet_OotFracClusters10;   //!
    TBranch        *b_jet_LeadingClusterPt;   //!
    TBranch        *b_jet_LeadingClusterSecondLambda;   //!
    TBranch        *b_jet_LeadingClusterCenterLambda;   //!
    TBranch        *b_jet_LeadingClusterSecondR;   //!
    TBranch        *b_jet_clean_passLooseBad;   //!
    TBranch        *b_jet_clean_passLooseBadUgly;   //!
    TBranch        *b_jet_clean_passTightBad;   //!
    TBranch        *b_jet_clean_passTightBadUgly;   //!
    TBranch        *b_jet_HECFrac;   //!
    TBranch        *b_jet_EMFrac;   //!
    TBranch        *b_jet_CentroidR;   //!
    TBranch        *b_jet_FracSamplingMax;   //!
    TBranch        *b_jet_FracSamplingMaxIndex;   //!
    TBranch        *b_jet_LowEtConstituentsFrac;   //!
    TBranch        *b_jet_GhostMuonSegmentCount;   //!
    TBranch        *b_jet_Width;   //!
    TBranch        *b_jet_emScalePt;   //!
    TBranch        *b_jet_constScalePt;   //!
    TBranch        *b_jet_pileupScalePt;   //!
    TBranch        *b_jet_originConstitScalePt;   //!
    TBranch        *b_jet_etaJESScalePt;   //!
    TBranch        *b_jet_gscScalePt;   //!
    TBranch        *b_jet_insituScalePt;   //!
    TBranch        *b_jet_SV0;   //!
    TBranch        *b_jet_SV1;   //!
    TBranch        *b_jet_IP3D;   //!
    TBranch        *b_jet_SV1IP3D;   //!
    TBranch        *b_jet_MV1;   //!
    TBranch        *b_jet_MV2c00;   //!
    TBranch        *b_jet_MV2c10;   //!
    TBranch        *b_jet_MV2c20;   //!
    TBranch        *b_jet_HadronConeExclTruthLabelID;   //!
    TBranch        *b_njets_Fix60;   //!
    TBranch        *b_jet_isFix60;   //!
    TBranch        *b_jet_SFFix60;   //!
    TBranch        *b_weight_jet_SFFix60;   //!
    TBranch        *b_njets_Fix70;   //!
    TBranch        *b_jet_isFix70;   //!
    TBranch        *b_jet_SFFix70;   //!
    TBranch        *b_weight_jet_SFFix70;   //!
    TBranch        *b_njets_Fix77;   //!
    TBranch        *b_jet_isFix77;   //!
    TBranch        *b_jet_SFFix77;   //!
    TBranch        *b_weight_jet_SFFix77;   //!
    TBranch        *b_njets_Fix85;   //!
    TBranch        *b_jet_isFix85;   //!
    TBranch        *b_jet_SFFix85;   //!
    TBranch        *b_weight_jet_SFFix85;   //!
    TBranch        *b_njets_Flt60;   //!
    TBranch        *b_jet_isFlt60;   //!
    TBranch        *b_jet_SFFlt60;   //!
    TBranch        *b_weight_jet_SFFlt60;   //!
    TBranch        *b_njets_Flt70;   //!
    TBranch        *b_jet_isFlt70;   //!
    TBranch        *b_jet_SFFlt70;   //!
    TBranch        *b_weight_jet_SFFlt70;   //!
    TBranch        *b_njets_Flt77;   //!
    TBranch        *b_jet_isFlt77;   //!
    TBranch        *b_jet_SFFlt77;   //!
    TBranch        *b_weight_jet_SFFlt77;   //!
    TBranch        *b_njets_Flt85;   //!
    TBranch        *b_jet_isFlt85;   //!
    TBranch        *b_jet_SFFlt85;   //!
    TBranch        *b_weight_jet_SFFlt85;   //!
    TBranch        *b_jet_ConeTruthLabelID;   //!
    TBranch        *b_jet_TruthCount;   //!
    TBranch        *b_jet_TruthLabelDeltaR_B;   //!
    TBranch        *b_jet_TruthLabelDeltaR_C;   //!
    TBranch        *b_jet_TruthLabelDeltaR_T;   //!
    TBranch        *b_jet_PartonTruthLabelID;   //!
    TBranch        *b_jet_GhostTruthAssociationFraction;   //!
    TBranch        *b_jet_truth_E;   //!
    TBranch        *b_jet_truth_pt;   //!
    TBranch        *b_jet_truth_phi;   //!
    TBranch        *b_jet_truth_eta;   //!
    TBranch        *b_nfatjets;   //!
    TBranch        *b_fatjet_E;   //!
    TBranch        *b_fatjet_m;   //!
    TBranch        *b_fatjet_pt;   //!
    TBranch        *b_fatjet_phi;   //!
    TBranch        *b_fatjet_eta;   //!
    TBranch        *b_fatjet_Split12;   //!
    TBranch        *b_fatjet_Split23;   //!
    TBranch        *b_fatjet_Split34;   //!
    TBranch        *b_fatjet_tau1_wta;   //!
    TBranch        *b_fatjet_tau2_wta;   //!
    TBranch        *b_fatjet_tau3_wta;   //!
    TBranch        *b_fatjet_tau21_wta;   //!
    TBranch        *b_fatjet_tau32_wta;   //!
    TBranch        *b_fatjet_ECF1;   //!
    TBranch        *b_fatjet_ECF2;   //!
    TBranch        *b_fatjet_ECF3;   //!
    TBranch        *b_fatjet_C2;   //!
    TBranch        *b_fatjet_D2;   //!
    TBranch        *b_fatjet_NTrimSubjets;   //!

    Tree(TTree *tree=0);
    virtual ~Tree();
    virtual Int_t    GetEntry(Long64_t entry);
    virtual Long64_t LoadTree(Long64_t entry);
    virtual void     Show(Long64_t entry = -1);
    virtual void     Init(TTree *tree);
  };
}

#endif
