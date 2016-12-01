#ifndef MJ_DRESSER_H
#define MJ_DRESSER_H
#include <vector>
#include <string>
#include <map>
#include <utility>
#include "TH1F.h"
#include "TFile.h"
#include "TProfile.h"
#include "TProfile2D.h"

#include "miniTree.h"
using namespace std;
namespace MJ{
  class dresser{
  public:
    void setMiniTreeFileName(string s){ m_miniTreeFileName = s; }
    void setTemplateFileName(string s){ m_templateFileName = s; }
    void setOutFileName(string s){ m_outFileName = s; }
    void setTemplateType( int t ){ m_templateType = t; }
    void doCorrections(){ m_doCorrections = true; }
    void injectSignal(int signalNum, float signalLumi);
    void initialize();
    void loop();
    void blind(float);
    dresser();
    ~dresser();
  private:
    vector<string> m_regionNames;
    int m_templateType;
    string m_miniTreeFileName;
    TFile *m_miniTreeFile;
    TFile *m_outFile;
    string m_templateFileName;
    TFile *m_templateFile;
    string m_outFileName;
    float m_delta;
    float m_MJcut;
    bool m_blinded;
    int m_signalNum;
    float m_signalLumi;
    bool m_signalInjected;
    miniTree m_miniTree;
    TTree *m_outTree;
    vector<double> *b_jet_m_dressed_nom;
    vector<double> *b_jet_m_dressed_shift_eta1_b0;
    vector<double> *b_jet_m_dressed_shift_eta2_b0;
    vector<double> *b_jet_m_dressed_shift_eta3_b0;
    vector<double> *b_jet_m_dressed_shift_eta4_b0;

    vector<double> *b_jet_m_dressed_shift_eta1_b1;
    vector<double> *b_jet_m_dressed_shift_eta2_b1;
    vector<double> *b_jet_m_dressed_shift_eta3_b1;
    vector<double> *b_jet_m_dressed_shift_eta4_b1;

    bool m_doCorrections;
    vector<double> m_ptBins3;
    vector<double> m_ptBins4;
    vector<double> m_ptBins5;
    vector<double> m_yBins;

    vector<float> m_corr_eta1_b0;
    vector<float> m_corr_eta2_b0;
    vector<float> m_corr_eta3_b0;
    vector<float> m_corr_eta4_b0;
    vector<float> m_corr_eta1_b1;
    vector<float> m_corr_eta2_b1;
    vector<float> m_corr_eta3_b1;
    vector<float> m_corr_eta4_b1;

    float m_uncert_eta1_b0;
    float m_uncert_eta2_b0;
    float m_uncert_eta3_b0;
    float m_uncert_eta4_b0;

    float m_uncert_eta1_b1;
    float m_uncert_eta2_b1;
    float m_uncert_eta3_b1;
    float m_uncert_eta4_b1;

    float m_uncert;
    
    string getTemplateName(float,float,int,int,int,int,float,int,int);
    string getRegionName(int,float);
    
    pair<int,int> getTemplateBin(float, float, int);
    //    vector<float> getDressedMass(TH1F *, float, float, float, int, bool);
    vector<float> getDressedMass(TH1F *, float, float, int, bool,int);


    map<string,TProfile> m_prof1d_kin;
    map<string,TProfile> m_prof1d_eta1_kin;
    map<string,TProfile> m_prof1d_eta2_kin;
    map<string,TProfile> m_prof1d_eta3_kin;
    map<string,TProfile> m_prof1d_eta4_kin;

    map<string,TProfile> m_prof1d_dress;
    map<string,TProfile> m_prof1d_eta1_dress;
    map<string,TProfile> m_prof1d_eta2_dress;
    map<string,TProfile> m_prof1d_eta3_dress;
    map<string,TProfile> m_prof1d_eta4_dress;

    map<string,TH1F> m_hists_m_kin;
    map<string,TH1F> m_hists_m1_kin;
    map<string,TH1F> m_hists_m2_kin;
    map<string,TH1F> m_hists_m3_kin;
    map<string,TH1F> m_hists_m4_kin;
    map<string,TH1F> m_hists_MJ_kin;

    map<string,TH1F> m_hists_m_dressNom;
    map<string,TH1F> m_hists_m1_dressNom;
    map<string,TH1F> m_hists_m2_dressNom;
    map<string,TH1F> m_hists_m3_dressNom;
    map<string,TH1F> m_hists_m4_dressNom;
    map<string,TH1F> m_hists_MJ_dressNom;

    map<string,TH1F> m_hists_m_dressShift_eta1_b0;
    map<string,TH1F> m_hists_m1_dressShift_eta1_b0;
    map<string,TH1F> m_hists_m2_dressShift_eta1_b0;
    map<string,TH1F> m_hists_m3_dressShift_eta1_b0;
    map<string,TH1F> m_hists_m4_dressShift_eta1_b0;
    map<string,TH1F> m_hists_MJ_dressShift_eta1_b0;

    map<string,TH1F> m_hists_m_dressShift_eta1_b1;
    map<string,TH1F> m_hists_m1_dressShift_eta1_b1;
    map<string,TH1F> m_hists_m2_dressShift_eta1_b1;
    map<string,TH1F> m_hists_m3_dressShift_eta1_b1;
    map<string,TH1F> m_hists_m4_dressShift_eta1_b1;
    map<string,TH1F> m_hists_MJ_dressShift_eta1_b1;

    map<string,TH1F> m_hists_m_dressShift_eta2_b0;
    map<string,TH1F> m_hists_m1_dressShift_eta2_b0;
    map<string,TH1F> m_hists_m2_dressShift_eta2_b0;
    map<string,TH1F> m_hists_m3_dressShift_eta2_b0;
    map<string,TH1F> m_hists_m4_dressShift_eta2_b0;
    map<string,TH1F> m_hists_MJ_dressShift_eta2_b0;

    map<string,TH1F> m_hists_m_dressShift_eta2_b1;
    map<string,TH1F> m_hists_m1_dressShift_eta2_b1;
    map<string,TH1F> m_hists_m2_dressShift_eta2_b1;
    map<string,TH1F> m_hists_m3_dressShift_eta2_b1;
    map<string,TH1F> m_hists_m4_dressShift_eta2_b1;
    map<string,TH1F> m_hists_MJ_dressShift_eta2_b1;

    map<string,TH1F> m_hists_m_dressShift_eta3_b0;
    map<string,TH1F> m_hists_m1_dressShift_eta3_b0;
    map<string,TH1F> m_hists_m2_dressShift_eta3_b0;
    map<string,TH1F> m_hists_m3_dressShift_eta3_b0;
    map<string,TH1F> m_hists_m4_dressShift_eta3_b0;
    map<string,TH1F> m_hists_MJ_dressShift_eta3_b0;

    map<string,TH1F> m_hists_m_dressShift_eta3_b1;
    map<string,TH1F> m_hists_m1_dressShift_eta3_b1;
    map<string,TH1F> m_hists_m2_dressShift_eta3_b1;
    map<string,TH1F> m_hists_m3_dressShift_eta3_b1;
    map<string,TH1F> m_hists_m4_dressShift_eta3_b1;
    map<string,TH1F> m_hists_MJ_dressShift_eta3_b1;

    map<string,TH1F> m_hists_m_dressShift_eta4_b0;
    map<string,TH1F> m_hists_m1_dressShift_eta4_b0;
    map<string,TH1F> m_hists_m2_dressShift_eta4_b0;
    map<string,TH1F> m_hists_m3_dressShift_eta4_b0;
    map<string,TH1F> m_hists_m4_dressShift_eta4_b0;
    map<string,TH1F> m_hists_MJ_dressShift_eta4_b0;

    map<string,TH1F> m_hists_m_dressShift_eta4_b1;
    map<string,TH1F> m_hists_m1_dressShift_eta4_b1;
    map<string,TH1F> m_hists_m2_dressShift_eta4_b1;
    map<string,TH1F> m_hists_m3_dressShift_eta4_b1;
    map<string,TH1F> m_hists_m4_dressShift_eta4_b1;
    map<string,TH1F> m_hists_MJ_dressShift_eta4_b1;
  };
}
#endif
