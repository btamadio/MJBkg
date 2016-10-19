#ifndef MJ_DRESSER_H
#define MJ_DRESSER_H
#include <vector>
#include <string>
#include <map>
#include <utility>
#include "TH1F.h"
#include "TFile.h"

#include "miniTree.h"
using namespace std;
namespace MJ{
  class dresser{
  public:
    void setMiniTreeFileName(string s){ m_miniTreeFileName = s; }
    void setTemplateFileName(string s){ m_templateFileName = s; }
    void setOutFileName(string s){ m_outFileName = s; }
    void setDelta( float d ){ m_delta = d; }
    void setTemplateType( int t ){ m_templateType = t; }
    void initialize();
    void loop();
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
    miniTree m_miniTree;
    vector<float> m_ptBins3;
    vector<float> m_ptBins4;
    vector<float> m_ptBins5;
    vector<float> m_yBins;
    string getTemplateName(float,float,int,float,int,int);
    string getRegionName(int,float);
    pair<float,float> getDressedMass(TH1F *, float);
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
