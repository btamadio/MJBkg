#ifndef MJ_MINIEVENT_H
#define MJ_MINIEVENT_H
#include <vector>
using namespace std;
namespace MJ{
  class MiniEvent{
  public:
    int runNumber;
    int mcChannelNumber;
    int eventNumber;
    int lumiBlock;
    float mu;
    bool isMC;
    float weight;
    int njet;
    int nbjet_Fix60;
    int nbjet_Fix70;
    int nbjet_Fix77;
    int nbjet_Fix85;
    int nbjet_Flt60;
    int nbjet_Flt70;
    int nbjet_Flt77;
    int nbjet_Flt85;
    vector<float> *jet_pt;
    vector<float> *jet_eta;
    vector<float> *jet_phi;
    vector<float> *jet_m;
    vector<bool> *jet_matchFix60;
    vector<bool> *jet_matchFix70;
    vector<bool> *jet_matchFix77;
    vector<bool> *jet_matchFix85;
    vector<bool> *jet_matchFlt60;
    vector<bool> *jet_matchFlt70;
    vector<bool> *jet_matchFlt77;
    vector<bool> *jet_matchFlt85;
    float dEta;
    float MJ;
    MiniEvent();
    ~MiniEvent();
    void clear();
  };
}
#endif
