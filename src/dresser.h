#ifndef MJ_DRESSER_H
#define MJ_DRESSER_H
#include <vector>
#include <string>
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
    string m_outFileName;
    float m_delta;
    miniTree m_miniTree;
    vector<float> m_ptBins3;
    vector<float> m_ptBins4;
    vector<float> m_ptBins5;
    vector<float> m_yBins;
    vector<float> dressJet(TH1F &);
    string getTemplateName(float pt, float eta, int bMatch, float BDT, int njet_soft, int nbjet, float dEta);
  };
}
#endif
