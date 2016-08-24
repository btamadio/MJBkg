#define MJ_MINIEVENT_CXX
#include "MiniEvent.h"

MJ::MiniEvent::MiniEvent(){
}

MJ::MiniEvent::~MiniEvent(){
}

MJ::MiniEvent::clear(){
  runNumber=0;
  mcChannelNumber=0;
  eventNumber=0;
  lumiBlock=0;
  mu=0;
  isMC=0;
  weight=0;
  njet=0;
  nbjet_Fix60=0;
  nbjet_Fix70=0;
  nbjet_Fix77=0;
  nbjet_Fix85=0;
  nbjet_Flt60=0;
  nbjet_Flt70=0;
  nbjet_Flt77=0;
  nbjet_Flt85=0;
  jet_pt->clear();
  jet_eta->clear();
  jet_phi->clear();
  jet_m->clear();
  jet_matchFix60->clear();
  jet_matchFix70->clear();
  jet_matchFix77->clear();
  jet_matchFix85->clear();
  jet_matchFlt60->clear();
  jet_matchFlt70->clear();
  jet_matchFlt77->clear();
  jet_matchFlt85->clear();
  dEta=0;
  MJ=0;
}
