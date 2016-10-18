#define DRESSER_CXX
#include "dresser.h"
#include "TTree.h"
#include "miniTree.cxx"
#include <iostream>
using namespace std;
MJ::dresser::dresser(){
}
MJ::dresser::~dresser(){
}
void MJ::dresser::initialize(){
  //Open minitree file and load miniTree
  m_miniTreeFile = TFile::Open(m_miniTreeFileName.c_str());
  if (!m_miniTreeFile){
    throw "The file could not be opened";
  }
  TTree *t = (TTree*)m_miniTreeFile->Get("miniTree");
  if (!t){
    throw "Could not find miniTree in file";
  }
  m_miniTree.Init(t);
  m_outFile = TFile::Open(m_outFileName.c_str(),"RECREATE");
  //Set pT and eta binning -> at some point change this to use config file instead
  if(m_templateType == 0){
    //pt/eta/b-match binning
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};
  }
  if(m_templateType == 1){
    //pt/BDT/b-match binning
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {-1.0,0.0,0.3,1.0};
  }
  if(m_templateType == 2){
    //ICHEP binning (soft jets + b-tag)
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.244,0.293,0.364,0.445,0.52,0.6,0.733,0.896};
    m_ptBins5 = {0.2,0.244,0.293,0.364,0.445,0.52,0.6,0.733};
    m_yBins = {0,0.5,1.0,1.5,2.0};
  }
  //Setup output histograms
  vector<string> regionNames = {"4jVRb0","4jVRb1","4jVRb9","5jVRb0","5jVRb1","5jVRb9",
				"4jSRb0","4jSRb1","4jSRb9","5jSRb0","5jSRb1","5jSRb9"};
  
}
void MJ::dresser::loop(){
  TTree *t = m_miniTree.fChain;
  int nEntries = t->GetEntries();
  //  nEntries = 100;
  cout<<"Looping over miniTree with "<<nEntries<<" entries"<<endl;
  for(unsigned int entry = 0; entry < nEntries; entry++){
    if( entry % 100000 == 0 ){
      cout<<"Processing entry "<<entry<<endl;
    }
    m_miniTree.GetEntry(entry);
    if(m_miniTree.njet >=4){
      for(unsigned int i = 0; i < m_miniTree.jet_pt->size(); i++){
	string templateHistName = "";
	try{
	  templateHistName = getTemplateName(m_miniTree.jet_pt->at(i),
					     m_miniTree.jet_eta->at(i),
					     m_miniTree.jet_bmatched_Fix70->at(i),
					     m_miniTree.BDTG,
					     m_miniTree.njet_soft,
					     m_miniTree.nbjet_Fix70,
					     m_miniTree.dEta);
	  //cout<<"Sampling from histogram "<<templateHistName<<endl;
	}  
	catch( const char *msg ){
	  cerr<<msg<<endl;
	}
      }
    }
  }
}
string MJ::dresser::getTemplateName(float pt, float eta, int bMatch, float BDT, int njet_soft, int nbjet, float dEta){
  if(m_templateType == 0){
    int ptBin = -1;
    int etaBin = -1;
    if ( pt >= m_ptBins3.back() ){
      ptBin = m_ptBins3.size()-1;
    }
    for( unsigned int i = 0; i < m_ptBins3.size()-1; i++){
      if (pt >= m_ptBins3.at(i) && pt < m_ptBins3.at(i+1)){
	ptBin = i+1;
	break;
      }
    }
    for( unsigned int i = 0; i < m_yBins.size()-1; i++){
      if (fabs(eta) >= m_yBins.at(i) && fabs(eta) < m_yBins.at(i+1)){
	etaBin = i+1;
	break;
      }
    }
    if( ptBin == -1 || etaBin == -1 ){
      throw "Could not find pT or BDT bin";
    }
    return "templ_b"+to_string(bMatch)+"_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);
  }
  else if (m_templateType == 1){
    int ptBin = -1;
    int bdtBin = -1;
    if ( pt >= m_ptBins3.back() ){
      ptBin = m_ptBins3.size()-1;
    }
    for( unsigned int i = 0; i < m_ptBins3.size()-1; i++){
      if (pt >= m_ptBins3.at(i) && pt < m_ptBins3.at(i+1)){
	ptBin = i+1;
	break;
      }
    }
    for( unsigned int i = 0; i < m_yBins.size()-1; i++){
      if (BDT >= m_yBins.at(i) && BDT < m_yBins.at(i+1)){
	bdtBin = i+1;
	break;
      }
    }
    if( ptBin == -1 || bdtBin == -1 ){
      throw "Could not find pT or BDT bin";
    }
    return "templ_b"+to_string(bMatch)+"_ptBin"+to_string(ptBin)+"_bdtBin"+to_string(bdtBin);
  }
  else if (m_templateType == 2){
    int ptBin = -1;
    int etaBin = -1;
    int njet = -1;
    int btag = -1;
    vector<float> ptBins;
    if (njet_soft == 0 ) return "";
    if (njet_soft == 1 ){
      if (nbjet > 0){
	if (dEta < 1.4) return "";
	btag = 1;
      }
      else btag = 0;
      ptBins = m_ptBins4;
      njet = 4;
    }
    if (njet_soft >= 2){
      ptBins = m_ptBins5;
      njet = 5;
      btag = 9;
    }
    if ( pt >= ptBins.back() ){
      ptBin = ptBins.size()-1;
    }
    for( unsigned int i = 0; i < ptBins.size()-1; i++){
      if (pt >= ptBins.at(i) && pt < ptBins.at(i+1)){
	ptBin = i+1;
	break;
      }
    }
    for( unsigned int i = 0; i < m_yBins.size()-1; i++){
      if (fabs(eta) >= m_yBins.at(i) && fabs(eta) < m_yBins.at(i+1)){
	etaBin = i+1;
	break;
      }
    }
    if( ptBin == -1 || etaBin == -1 || btag == -1 || njet == -1){
      throw "Could not find pT bin, eta bin, b-tag status, or njet";
    }
    return  "templ_b"+to_string(btag)+"_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin)+"_njet"+to_string(njet);
  }
  else{
    throw "Template type not found";
  }
}
