#ifndef MJ_MINITREE_H
#define MJ_MINITREE_H
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "vector"
using namespace std;
namespace MJ{
  class miniTree {
  public :
    TTree          *fChain;   //!pointer to the analyzed TTree or TChain
    Int_t           fCurrent; //!current Tree number in a TChain

    // Fixed size dimensions of array or collections stored in the TTree if any.

    // Declaration of leaf types
    Int_t           runNumber;
    Int_t           mcChannelNumber;
    Long64_t        eventNumber;
    Int_t           lumiBlock;
    Double_t        mu;
    Bool_t          isMC;
    Double_t        weight;
    Int_t           njet;
    Int_t           njet_soft;
    Int_t           njet_ak4;
    Int_t           nbjet_Fix60;
    Int_t           nbjet_Fix70;
    Int_t           nbjet_Fix77;
    Int_t           nbjet_Fix85;
    Int_t           nbjet_Flt60;
    Int_t           nbjet_Flt70;
    Int_t           nbjet_Flt77;
    Int_t           nbjet_Flt85;
    vector<double>  *jet_pt;
    vector<double>  *jet_eta;
    vector<double>  *jet_phi;
    vector<double>  *jet_m;
    vector<int>     *jet_bmatched_Fix60;
    vector<int>     *jet_bmatched_Fix70;
    vector<int>     *jet_bmatched_Fix77;
    vector<int>     *jet_bmatched_Fix85;
    vector<int>     *jet_bmatched_Flt60;
    vector<int>     *jet_bmatched_Flt70;
    vector<int>     *jet_bmatched_Flt77;
    vector<int>     *jet_bmatched_Flt85;
    vector<int>     *jet_NTrimSubjets; 
    vector<int>     *jet_qmatched;
    vector<int>     *jet_gmatched;
    Double_t        dEta;
    Double_t        HT;
    Double_t        MJ;
    Double_t        MJ4;
    Float_t        BDTG;
    Double_t         bSF_60;
    Double_t         bSF_70;
    Double_t         bSF_77;
    Double_t         bSF_85;
  
    // List of branches
    TBranch        *b_runNumber;   //!
    TBranch        *b_mcChannelNumber;   //!
    TBranch        *b_eventNumber;   //!
    TBranch        *b_lumiBlock;   //!
    TBranch        *b_mu;   //!
    TBranch        *b_isMC;   //!
    TBranch        *b_weight;   //!
    TBranch        *b_njet;   //!
    TBranch        *b_njet_soft;   //!
    TBranch        *b_njet_ak4;   //!
    TBranch        *b_nbjet_Fix60;   //!
    TBranch        *b_nbjet_Fix70;   //!
    TBranch        *b_nbjet_Fix77;   //!
    TBranch        *b_nbjet_Fix85;   //!
    TBranch        *b_nbjet_Flt60;   //!
    TBranch        *b_nbjet_Flt70;   //!
    TBranch        *b_nbjet_Flt77;   //!
    TBranch        *b_nbjet_Flt85;   //!
    TBranch        *b_jet_pt;   //!
    TBranch        *b_jet_eta;   //!
    TBranch        *b_jet_phi;   //!
    TBranch        *b_jet_m;   //!
    TBranch        *b_jet_NTrimSubjets; //!
    TBranch        *b_jet_qmatched; //!
    TBranch        *b_jet_gmatched; //!
    TBranch        *b_jet_bmatched_Fix60;   //!
    TBranch        *b_jet_bmatched_Fix70;   //!
    TBranch        *b_jet_bmatched_Fix77;   //!
    TBranch        *b_jet_bmatched_Fix85;   //!
    TBranch        *b_jet_bmatched_Flt60;   //!
    TBranch        *b_jet_bmatched_Flt70;   //!
    TBranch        *b_jet_bmatched_Flt77;   //!
    TBranch        *b_jet_bmatched_Flt85;   //!
    TBranch        *b_dEta;   //!
    TBranch        *b_HT;   //!
    TBranch        *b_MJ;   //!
    TBranch        *b_BDTG; //!
    TBranch *b_bSF_60; //!
    TBranch *b_bSF_70; //!
    TBranch *b_bSF_77; //!
    TBranch *b_bSF_85; //!
    miniTree();
    //    miniTree(TTree *tree=0);
    ~miniTree();
    virtual Int_t    Cut(Long64_t entry);
    virtual Int_t    GetEntry(Long64_t entry);
    virtual Long64_t LoadTree(Long64_t entry);
    virtual void     Init(TTree *tree);
    virtual void     Loop();
    virtual Bool_t   Notify();
    virtual void     Show(Long64_t entry = -1);
  };
}
#endif

