#define TEMPLATEMAKER_CXX
#include "TemplateMaker.h"
#include "TLorentzVector.h"
#include "Tree.cxx"
#include <iostream>
#include <fstream>
#include <algorithm>
using namespace std;
MJ::TemplateMaker::TemplateMaker(){
  for (int i = 0; i < m_GRLFileNames.size(); i++){
    readGRL(i);
  }
  cout<<"Done reading GRLs"<<endl;
  //displayGRL();
  
  m_inFile = TFile::Open(m_inFileName.c_str(),"READ");
  m_outFile = TFile::Open(m_outFileName.c_str(),"RECREATE");
  setupOutput();
  cout<<"Done setting up output"<<endl;
}

MJ::TemplateMaker::~TemplateMaker(){
}

void MJ::TemplateMaker::MakeMiniTree(){
  TTree *t = (TTree*)m_inFile->Get(m_treeName.c_str());
  MJ::Tree tree(t);
  int nEntries = t->GetEntries();
  for (int entry = 0; entry < nEntries; entry++){
    tree.GetEntry(entry);
    m_miniEvent.clear();

    int iCut = 1;
    float w = 1;

    //Now we run the selection, fill the cutflow and the minitree
    m_cutflow->Fill(++iCut,w);
    if( !passGRL( tree.runNumber, tree.lumiBlock ) ){ continue; }
    m_cutflow->Fill(++iCut,w);
    if ( tree.SCTError || tree.LArError || tree.TileError ){ continue; }
    m_cutflow->Fill(++iCut,w);

    bool passTrig = false;
    for( auto s : *tree.passedTriggers ){
      if ( s.find("HLT_j360_a10")!=string::npos || s.find("HLT_j380_a10")!=string::npos || s.find("HLT_j400_a10")!=string::npos || s.find("HLT_j420_a10")!=string::npos ){
	passTrig = true;
      }
    }
    if ( !passTrig ){ continue; }
    m_cutflow->Fill(++iCut,w);
    
    bool passLeadJet = false;
    for( int i = 0; i < tree.fatjet_pt->size(); i++){
      if( tree.fatjet_pt->at(i) > m_fatJetPtCut &&
	  fabs(tree.fatjet_eta->at(i)) < m_fatJetEtaCut &&
	  tree.fatjet_m->at(i)/tree.fatjet_pt->at(i) < m_fatJetMPtCut){
	m_miniEvent.njet++;
	if( tree.fatjet_pt->at(i) > m_leadFatJetPtCut ){
	  passLeadJet = true;
	}
      }
    }
    if (!passLeadJet ){ continue; }
    m_cutflow->Fill(++iCut,w);
    if ( m_miniEvent.njet < 3 ){ continue; }
    m_cutflow->Fill(++iCut,w);

    vector<TLorentzVector> fatJet4momVec;
    //Loop over fat jets again to fill jet kinematics only when event passes preselection
    for( int i = 0; i < tree.fatjet_pt->size(); i++){
      if( tree.fatjet_pt->at(i) > m_fatJetPtCut &&
	  fabs(tree.fatjet_eta->at(i)) < m_fatJetEtaCut &&
	  tree.fatjet_m->at(i)/tree.fatjet_pt->at(i) < m_fatJetMPtCut){
    	m_miniEvent.jet_pt->push_back(tree.fatjet_pt->at(i));
	m_miniEvent.jet_eta->push_back(tree.fatjet_eta->at(i));
	m_miniEvent.jet_phi->push_back(tree.fatjet_phi->at(i));
	m_miniEvent.jet_m->push_back(tree.fatjet_m->at(i));
	//b-jet matching
	bool match_fix60 = false;
	bool match_fix70 = false;
	bool match_fix77 = false;
	bool match_fix85 = false;
	bool match_flt60 = false;
	bool match_flt70 = false;
	bool match_flt77 = false;
	bool match_flt85 = false;
	TLorentzVector fatJet4mom, jet4mom;
	fatJet4mom.SetPtEtaPhiM(tree.fatjet_pt->at(i),tree.fatjet_eta->at(i),tree.fatjet_phi->at(i),tree.fatjet_m->at(i));
	fatJet4momVec.push_back(fatJet4mom);
	for( int j = 0; j < tree.jet_pt->size(); j++){
	  if( tree.jet_pt->at(j) > m_jetPtCut && fabs(tree.jet_eta->at(j)) < m_jetEtaCut){
	    jet4mom.SetPtEtaPhiM(tree.jet_pt->at(j),tree.jet_eta->at(j),tree.jet_phi->at(j),tree.jet_m->at(j));
	    if( fatJet4mom.DeltaR(jet4mom) < m_deltaRbMatch ){
	      if( tree.jet_isFix60->at(j) ){ match_fix60 = true; }
	      if( tree.jet_isFix70->at(j) ){ match_fix70 = true; }
	      if( tree.jet_isFix77->at(j) ){ match_fix77 = true; }
	      if( tree.jet_isFix85->at(j) ){ match_fix85 = true; }
	      if( tree.jet_isFlt60->at(j) ){ match_flt60 = true; }
	      if( tree.jet_isFlt70->at(j) ){ match_flt70 = true; }
	      if( tree.jet_isFlt77->at(j) ){ match_flt77 = true; }
	      if( tree.jet_isFlt85->at(j) ){ match_flt85 = true; }
	    }
	  }
	}
	m_miniEvent.jet_matchFix60->push_back(match_fix60);
	m_miniEvent.jet_matchFix70->push_back(match_fix70);
	m_miniEvent.jet_matchFix77->push_back(match_fix77);
	m_miniEvent.jet_matchFix85->push_back(match_fix85);
	m_miniEvent.jet_matchFlt60->push_back(match_flt60);
	m_miniEvent.jet_matchFlt70->push_back(match_flt70);
	m_miniEvent.jet_matchFlt77->push_back(match_flt77);
	m_miniEvent.jet_matchFlt85->push_back(match_flt85);
      }
    }
    sort(fatJet4momVec.begin(), fatJet4momVec.end(), sortFourVec);
    m_miniEvent.dEta = fabs(fatJet4momVec.at(0).Eta() - fatJet4momVec.at(1).Eta());
    int nJetLoop = 4;
    if (fatJet4momVec.size() < 4){ nJetLoop = fatJet4momVec.size(); }
    for( int i = 0; i < nJetLoop; i++){ m_miniEvent.MJ += fatJet4momVec.at(i).M(); }
    for( int i = 0; i < tree.jet_pt->size(); i++){
      if( tree.jet_pt->at(i) > m_jetPtCut && fabs(tree.jet_eta->at(i)) < m_jetEtaCut){
	if( tree.jet_isFix60->at(i) ){ m_miniEvent.nbjet_Fix60++; }
	if( tree.jet_isFix70->at(i) ){ m_miniEvent.nbjet_Fix70++; }
	if( tree.jet_isFix77->at(i) ){ m_miniEvent.nbjet_Fix77++; }
	if( tree.jet_isFix85->at(i) ){ m_miniEvent.nbjet_Fix85++; }
	if( tree.jet_isFlt60->at(i) ){ m_miniEvent.nbjet_Flt60++; }
	if( tree.jet_isFlt70->at(i) ){ m_miniEvent.nbjet_Flt70++; }
	if( tree.jet_isFlt77->at(i) ){ m_miniEvent.nbjet_Flt77++; }
	if( tree.jet_isFlt85->at(i) ){ m_miniEvent.nbjet_Flt85++; }
      }
    }
    m_miniEvent.runNumber = tree.runNumber;
    m_miniEvent.mcChannelNumber = m_isMC ? tree.mcChannelNumber : -1;
    m_miniEvent.eventNumber = tree.eventNumber;
    m_miniEvent.lumiBlock = tree.lumiBlock;
    m_miniEvent.mu = tree.averageInteractionsPerCrossing;
    m_miniEvent.isMC = m_isMC;
    m_miniEvent.weight = m_isMC ? tree.weight : 1;

    //fill the mini tree at the end
    m_miniTree->Fill();
  }
  m_outFile->cd();
  m_outFile->Write();
}

void MJ::TemplateMaker::setupOutput(){
  m_cutflow = new TH1F("h_cutflow","cutflow histogram",7,0.5,7.5);
  m_cutflow->GetXaxis()->SetBinLabel(1,"CBC Selected");
  m_cutflow->GetXaxis()->SetBinLabel(2,"nEvents Looped over");
  m_cutflow->GetXaxis()->SetBinLabel(3,"GRL");
  m_cutflow->GetXaxis()->SetBinLabel(4,"event cleaning");
  m_cutflow->GetXaxis()->SetBinLabel(5,"trigger");
  m_cutflow->GetXaxis()->SetBinLabel(6,"p_{T}^{lead} > 440 GeV");
  m_cutflow->GetXaxis()->SetBinLabel(7,"n_{fatjet} >= 3");
  m_cutflow->SetBinContent(1, ((TH1*)m_inFile->Get("MetaData_EventCount"))->GetBinContent(2));

  m_miniTree = new TTree("miniTree","miniTree");
  m_miniEvent.clear();
  m_miniTree->Branch("runNumber",&m_miniEvent.runNumber);
  m_miniTree->Branch("mcChannelNumber",&m_miniEvent.mcChannelNumber);
  m_miniTree->Branch("eventNumber",&m_miniEvent.eventNumber);
  m_miniTree->Branch("lumiBlock",&m_miniEvent.lumiBlock);
  m_miniTree->Branch("mu",&m_miniEvent.mu);
  m_miniTree->Branch("isMC",&m_miniEvent.isMC);
  m_miniTree->Branch("weight",&m_miniEvent.weight);
  m_miniTree->Branch("njet",&m_miniEvent.njet);
  m_miniTree->Branch("nbjet_Fix60",&m_miniEvent.nbjet_Fix60);
  m_miniTree->Branch("nbjet_Fix70",&m_miniEvent.nbjet_Fix70);
  m_miniTree->Branch("nbjet_Fix77",&m_miniEvent.nbjet_Fix77);
  m_miniTree->Branch("nbjet_Fix85",&m_miniEvent.nbjet_Fix85);
  m_miniTree->Branch("nbjet_Flt60",&m_miniEvent.nbjet_Flt60);
  m_miniTree->Branch("nbjet_Flt70",&m_miniEvent.nbjet_Flt70);
  m_miniTree->Branch("nbjet_Flt77",&m_miniEvent.nbjet_Flt77);
  m_miniTree->Branch("nbjet_Flt85",&m_miniEvent.nbjet_Flt85);
  m_miniTree->Branch("jet_pt",m_miniEvent.jet_pt);
  m_miniTree->Branch("jet_eta",m_miniEvent.jet_eta);
  m_miniTree->Branch("jet_phi",m_miniEvent.jet_phi);
  m_miniTree->Branch("jet_m",m_miniEvent.jet_m);
  m_miniTree->Branch("jet_matchFix60",m_miniEvent.jet_matchFix60);
  m_miniTree->Branch("jet_matchFix70",m_miniEvent.jet_matchFix70);
  m_miniTree->Branch("jet_matchFix77",m_miniEvent.jet_matchFix77);
  m_miniTree->Branch("jet_matchFix85",m_miniEvent.jet_matchFix85);
  m_miniTree->Branch("jet_matchFlt60",m_miniEvent.jet_matchFlt60);
  m_miniTree->Branch("jet_matchFlt70",m_miniEvent.jet_matchFlt70);
  m_miniTree->Branch("jet_matchFlt77",m_miniEvent.jet_matchFlt77);
  m_miniTree->Branch("jet_matchFlt85",m_miniEvent.jet_matchFlt85);
  m_miniTree->Branch("dEta",&m_miniEvent.dEta);
  m_miniTree->Branch("MJ",&m_miniEvent.MJ);
}

void MJ::TemplateMaker::displayGRL(){
  for (auto const &ent1 : m_GRLMap){
    cout<<ent1.first<<endl;
    for( auto const &ent2 : ent1.second ){
      cout<<ent2.first<<"\t"<<ent2.second<<endl;
    }
  }
}

int MJ::TemplateMaker::readGRL(int ind){
  Int_t RunNumber1 = 0, MinLum1 = 0, MaxLum1 = 0;
  TString line1;
  ifstream fGRL;
    fGRL.open(m_GRLFileNames.at(ind));
    if(!fGRL.is_open()){
      cout<<"ERROR opening GRL"<<endl;
      abort();
    }
    while(fGRL >> line1){
      if(line1.Contains("</Run>")){
	line1.ReplaceAll("PrescaleRD1=\"8\">", "");
	line1.ReplaceAll("<Run>", "");
	line1.ReplaceAll("</Run>", "");
	RunNumber1 = line1.Atoi();
	while(1){
	  fGRL>>line1;
	  if( line1.Contains("</LumiBlockCollection>") ) break;
	  fGRL>>line1;
	  line1.ReplaceAll("Start=\"", "");
	  line1.ReplaceAll("\"", "");
	  MinLum1 = line1.Atoi();
	  fGRL>>line1;
	  line1.ReplaceAll("End=\"", "");
	  line1.ReplaceAll("\"/>", "");
	  MaxLum1 = line1.Atoi();
	  pair<int,int> goodLBs;
	  goodLBs.first = MinLum1;
	  goodLBs.second = MaxLum1;
	  vector<pair<int,int> > emptyVec;
	  if( m_GRLMap.find(RunNumber1) == m_GRLMap.end()){
	    m_GRLMap[RunNumber1]=emptyVec;
	  }
	  m_GRLMap[RunNumber1].push_back(goodLBs);
	}
      }
    }
  return 0;
}

bool MJ::TemplateMaker::passGRL(int run, int lb){
  for ( auto& x : m_GRLMap){
    if ( run == x.first ){
      for ( auto&  p : x.second ){
	if ( lb >= p.first && lb <= p.second ){
	  return true;
	}
      }
    }
  }
  return false;
}

bool MJ::TemplateMaker::sortFourVec(const TLorentzVector &a, const TLorentzVector &b)
{
   return a.Pt() > b.Pt();
}
