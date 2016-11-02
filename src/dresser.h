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
    //void setDelta( float d ){ m_delta = d; }
    void setTemplateType( int t ){ m_templateType = t; }
    void doCorrections(){ m_doCorrections = true; }
    void initialize();
    void loop();
    void blind(float);
    dresser();
    ~dresser();
  private:
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
    miniTree m_miniTree;
    TTree *m_outTree;
    vector<double> *b_jet_m_dressed_nom;
    vector<double> *b_jet_m_dressed_up;
    vector<double> *b_jet_m_dressed_down;
    bool m_doCorrections;
    vector<float> m_mass_corr_SR;
    vector<float> m_mass_corr_VR;
    vector<double> m_ptBins3;
    vector<double> m_ptBins4;
    vector<double> m_ptBins5;
    vector<double> m_yBins;
    vector<float> m_deltas;
    string getTemplateName(float,float,int,int,int,int,float,int,int);
    string getRegionName(int,float);
    
    pair<int,int> getTemplateBin(float, float, int);
    vector<float> getDressedMass(TH1F *, float, float, bool);
    map<string,TProfile> m_prof1d_kin;
    map<string,TProfile> m_prof1d_dressUp;
    map<string,TProfile> m_prof1d_dressNom;
    map<string,TProfile> m_prof1d_dressDown;

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

    map<string,TH1F> m_hists_m_dressUp;
    map<string,TH1F> m_hists_m1_dressUp;
    map<string,TH1F> m_hists_m2_dressUp;
    map<string,TH1F> m_hists_m3_dressUp;
    map<string,TH1F> m_hists_m4_dressUp;
    map<string,TH1F> m_hists_MJ_dressUp;

    map<string,TH1F> m_hists_m_dressDown;
    map<string,TH1F> m_hists_m1_dressDown;
    map<string,TH1F> m_hists_m2_dressDown;
    map<string,TH1F> m_hists_m3_dressDown;
    map<string,TH1F> m_hists_m4_dressDown;
    map<string,TH1F> m_hists_MJ_dressDown;
  };
}
#endif
