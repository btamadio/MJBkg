#define TEMPLATEMAKER_CXX
#include "TemplateMaker.h"
#include "Tree.h"
#include <iostream>
#include <fstream>
using namespace std;
MJ::TemplateMaker::TemplateMaker(){
  for (int i = 0; i < m_GRLFileNames.size(); i++){
    readGRL(i);
  }
  /*
  for (auto const &ent1 : m_GRLMap){
    cout<<ent1.first<<endl;
    for( auto const &ent2 : ent1.second ){
      cout<<ent2.first<<"\t"<<ent2.second<<endl;
    }
    }*/
  m_inFile = TFile::Open(m_inFileName.c_str(),"READ");
  m_outFile = TFile::Open(m_outFileName.c_str(),"RECREATE");
}

MJ::TemplateMaker::~TemplateMaker(){
}

void MJ::TemplateMaker::Loop(){
  TTree *t = (TTree*)m_inFile->Get(m_treeName.c_str());
  cout<<t->GetEntries()<<endl;
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
  cout<<m_GRLMap.size()<<endl;
  return 0;
}
