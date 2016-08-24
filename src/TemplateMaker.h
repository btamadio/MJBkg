#ifndef MJ_TEMPLATEMAKER_H
#define MJ_TEMPLATEMAKER_H
#include <vector>
#include <string>
#include <map>
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "MiniEvent.h"
#include "TTree.h"
using namespace std;
namespace MJ{
  class TemplateMaker{
  public:
    string m_inFileName="/projecta/projectdirs/atlas/atlaslocalgroupdisk/rucio/user/btamadio/7e/53/user.btamadio.8724658._000002.tree.root";
    TFile *m_inFile;
    string m_treeName = "outTree/nominal";
    vector<string> m_GRLFileNames={"config/data15_13TeV.periodAllYear_DetStatus-v75-repro20-01_DQDefects-00-02-02_PHYS_StandardGRL_All_Good_25ns.xml",
				   "config/data16_13TeV.periodAllYear_DetStatus-v81-pro20-09_DQDefects-00-02-02_PHYS_StandardGRL_All_Good_25ns.xml"};
    map<int,vector<pair<int,int> > >  m_GRLMap;
    float m_fatJetPtCut = 200;
    float m_fatJetMPtCut = 1;
    float m_fatJetEtaCut = 2;
    float m_leadFatJetPtCut = 440;
    float m_jetPtCut = 2.5;
    float m_jetEtaCut = 2.5;
    float m_leadJetPtCut = 0;
    float m_htCut = 0;
    float m_lumi = 13.784;
    bool m_isMC = false;
    int m_templateType = 3; //b-matched template
    int m_bTagWP = 70;
    bool m_useFlatBTag = false;
    TFile *m_outFile;
    string m_outFileName = "output/test.root";
    TH1F *m_cutflow;
    MJ::MiniEvent m_miniEvent;
    TTree *m_miniTree;
    vector<TH2F*> m_templates;
    TemplateMaker();
    ~TemplateMaker();
    void setupOutput();
    void displayGRL();
    void Loop();
  private:
    int readGRL(int);
  };
}
#endif
