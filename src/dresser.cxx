#define DRESSER_CXX
#include "dresser.h"
#include "TTree.h"
#include "miniTree.cxx"
#include "TRandom3.h"
#include <iostream>
using namespace std;
MJ::dresser::dresser(){
  m_MJcut = 800;
  m_blinded = false;
  m_doCorrections = false;
}
MJ::dresser::~dresser(){
}
void MJ::dresser::blind(float mjCut){
  m_MJcut = mjCut;
  m_blinded = true;
}
void MJ::dresser::initialize(){
  //Open minitree file and load miniTree
  m_miniTreeFile = TFile::Open(m_miniTreeFileName.c_str());
  if (!m_miniTreeFile){
    throw "The miniTree file could not be opened";
  }
  TTree *t = (TTree*)m_miniTreeFile->Get("miniTree");
  if (!t){
    throw "Could not find miniTree in file";
  }
  m_templateFile = TFile::Open(m_templateFileName.c_str());
  if(!m_templateFile){
    throw "The template file could not be opened";
  }
  m_miniTree.Init(t);
  cout<<"Creating output file "<<m_outFileName<<endl;
  m_outFile = TFile::Open(m_outFileName.c_str(),"RECREATE");
  m_outTree=m_miniTree.fChain->CloneTree(0);

  b_jet_m_dressed_nom = new vector<double>;
  b_jet_m_dressed_shift_cenb0 = new vector<double>;
  b_jet_m_dressed_shift_cenb1 = new vector<double>;
  b_jet_m_dressed_shift_forb0 = new vector<double>;
  b_jet_m_dressed_shift_forb1 = new vector<double>;

  m_outTree->Branch("jet_m_dressed_nom",&b_jet_m_dressed_nom);
  m_outTree->Branch("jet_m_dressed_shift_cenb0",&b_jet_m_dressed_shift_cenb0);
  m_outTree->Branch("jet_m_dressed_shift_cenb1",&b_jet_m_dressed_shift_cenb1);
  m_outTree->Branch("jet_m_dressed_shift_forb0",&b_jet_m_dressed_shift_forb0);
  m_outTree->Branch("jet_m_dressed_shift_forb1",&b_jet_m_dressed_shift_forb1);

  //Set pT and eta binning -> at some point change this to use config file instead
  if(m_templateType == 0){
    //pt/eta/b-match binning
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};
    //Turn corrections off
    // m_corr_cen_b0 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    // m_corr_cen_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    // m_corr_for_b0 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    // m_corr_for_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    // m_uncert_cen_b0 = 0;
    // m_uncert_cen_b1 = 0;
    // m_uncert_for_b0 = 0;
    // m_uncert_for_b1 = 0;

    //Pythia
    // m_corr_cen_b0 = {-.063,.029,-.059,-.034,-.034,-.039,0,0,0,0,0,0,0,0,0};
    // m_corr_cen_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    // m_corr_for_b0 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    // m_corr_for_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    // m_uncert_cen_b0 = 0.063;
    // m_uncert_cen_b1 = 0.19;
    // m_uncert_for_b0 = 0.042;
    // m_uncert_for_b1 = 0.14;

    //post-ICHEP dataset
    m_corr_cen_b0 = {-.007,-.023,-.021,-.032,-.021,-.018,-.017,0,.016,.038,.021,.024,.020,.031,.052};
    m_corr_cen_b1 = {-.039,-.046,-.030,0,0,0,0,0,0,0,0,0,0,0,0};
    m_corr_for_b0 = {-.02,-.014,-.02,-.022,-.03,-.023,-.04,-.027,0,0,0,0,0,0,0};
    m_corr_for_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    m_uncert_cen_b0 = .051;
    m_uncert_cen_b1 = .075;
    m_uncert_for_b0 = .12;
    m_uncert_for_b1 = .092;

    //ICHEP dataset
    // m_corr_cen_b0 = {-.024,-.02,-.03,-.015,-.018,-.02,0,0,0,0,0,0,0,0,0};
    // m_corr_cen_b1 = {0,0,0,0,0,0,-.05,-.046,-.07,0,0,0,0,0,0};
    // m_corr_for_b0 = {-.032,-.033,-.028,-.028,-.025,-.054,-.048,0,0,0,0,0,0,0,0};
    // m_corr_for_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    // m_uncert_cen_b0 = 0.046;
    // m_uncert_cen_b1 = 0.11;
    // m_uncert_for_b0 = 0.068;
    // m_uncert_for_b1 = 0.082;

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

  }
  if(m_templateType == 3){
    //pt/eta/qg-match binning
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};
  }
  if(m_templateType == 4){
    //pt/eta/n_subjet binning
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};
  }
  //Setup output histograms
  m_regionNames = {"3jVRb0","3jVRb1","3jVRb9","3jVRbM","3jVRbU","3js0","3js1","3js2",
				"3jSRb0","3jSRb1","3jSRb9","3jSRbM","3jSRbU","4js0","4js1",
				"4jVRb0","4jVRb1","4jVRb9","4jVRbM","4jVRbU",
				"4jSRb0","4jSRb1","4jSRb9","4jSRbM","4jSRbU",
				"5jVRb0","5jVRb1","5jVRb9","5jVRbM","5jVRbU",
				"5jSRb0","5jSRb1","5jSRb9","5jSRbM","5jSRbU","5j"};
  for (unsigned int i = 0; i < m_regionNames.size(); i++){
    vector<double> ptBins;
    if (m_regionNames.at(i).find("3j") != string::npos){ ptBins = m_ptBins3; }
    else if (m_regionNames.at(i).find("4j") != string::npos) { ptBins = m_ptBins4; }
    else if (m_regionNames.at(i).find("5j") != string::npos) { ptBins = m_ptBins5; }
    //Declare 1D profile hists with pt bins same as templates
    m_prof1d_kin[m_regionNames.at(i)] = TProfile(("h_prof1d_kin_"+m_regionNames.at(i)).c_str(),("h_prof1d_kin_"+m_regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_cen_kin[m_regionNames.at(i)] = TProfile(("h_prof1d_cen_kin_"+m_regionNames.at(i)).c_str(),("h_prof1d_cen_kin_"+m_regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_for_kin[m_regionNames.at(i)] = TProfile(("h_prof1d_for_kin_"+m_regionNames.at(i)).c_str(),("h_prof1d_for_kin_"+m_regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());

    m_prof1d_dress[m_regionNames.at(i)] = TProfile(("h_prof1d_dress_"+m_regionNames.at(i)).c_str(),("h_prof1d_dress_"+m_regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_cen_dress[m_regionNames.at(i)] = TProfile(("h_prof1d_cen_dress_"+m_regionNames.at(i)).c_str(),("h_prof1d_cen_dress_"+m_regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_for_dress[m_regionNames.at(i)] = TProfile(("h_prof1d_for_dress_"+m_regionNames.at(i)).c_str(),("h_prof1d_for_dress_"+m_regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());

    int nBins = 200;
    float xMin = 0;
    float xMax = 1.2;
    m_hists_m_kin[m_regionNames.at(i)] = TH1F(("h_jetmass_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_cenb0[m_regionNames.at(i)] = TH1F(("h_jetmass_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),("h_jetmass_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_cenb1[m_regionNames.at(i)] = TH1F(("h_jetmass_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),("h_jetmass_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_forb0[m_regionNames.at(i)] = TH1F(("h_jetmass_dressShift_forb0_"+m_regionNames.at(i)).c_str(),("h_jetmass_dressShift_forb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_forb1[m_regionNames.at(i)] = TH1F(("h_jetmass_dressShift_forb1_"+m_regionNames.at(i)).c_str(),("h_jetmass_dressShift_forb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);

    m_hists_m1_kin[m_regionNames.at(i)] = TH1F(("h_jetmass1_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass1_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass1_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass1_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_cenb0[m_regionNames.at(i)] = TH1F(("h_jetmass1_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),("h_jetmass1_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_cenb1[m_regionNames.at(i)] = TH1F(("h_jetmass1_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),("h_jetmass1_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_forb0[m_regionNames.at(i)] = TH1F(("h_jetmass1_dressShift_forb0_"+m_regionNames.at(i)).c_str(),("h_jetmass1_dressShift_forb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_forb1[m_regionNames.at(i)] = TH1F(("h_jetmass1_dressShift_forb1_"+m_regionNames.at(i)).c_str(),("h_jetmass1_dressShift_forb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);

    m_hists_m2_kin[m_regionNames.at(i)] = TH1F(("h_jetmass2_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass2_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass2_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass2_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_cenb0[m_regionNames.at(i)] = TH1F(("h_jetmass2_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),("h_jetmass2_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_cenb1[m_regionNames.at(i)] = TH1F(("h_jetmass2_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),("h_jetmass2_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_forb0[m_regionNames.at(i)] = TH1F(("h_jetmass2_dressShift_forb0_"+m_regionNames.at(i)).c_str(),("h_jetmass2_dressShift_forb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_forb1[m_regionNames.at(i)] = TH1F(("h_jetmass2_dressShift_forb1_"+m_regionNames.at(i)).c_str(),("h_jetmass2_dressShift_forb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);

    xMax = 0.6;
    m_hists_m3_kin[m_regionNames.at(i)] = TH1F(("h_jetmass3_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass3_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass3_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass3_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_cenb0[m_regionNames.at(i)] = TH1F(("h_jetmass3_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),("h_jetmass3_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_cenb1[m_regionNames.at(i)] = TH1F(("h_jetmass3_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),("h_jetmass3_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_forb0[m_regionNames.at(i)] = TH1F(("h_jetmass3_dressShift_forb0_"+m_regionNames.at(i)).c_str(),("h_jetmass3_dressShift_forb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_forb1[m_regionNames.at(i)] = TH1F(("h_jetmass3_dressShift_forb1_"+m_regionNames.at(i)).c_str(),("h_jetmass3_dressShift_forb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);

    xMax = 0.4;
    m_hists_m4_kin[m_regionNames.at(i)] = TH1F(("h_jetmass4_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass4_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass4_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass4_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_cenb0[m_regionNames.at(i)] = TH1F(("h_jetmass4_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),("h_jetmass4_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_cenb1[m_regionNames.at(i)] = TH1F(("h_jetmass4_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),("h_jetmass4_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_forb0[m_regionNames.at(i)] = TH1F(("h_jetmass4_dressShift_forb0_"+m_regionNames.at(i)).c_str(),("h_jetmass4_dressShift_forb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_forb1[m_regionNames.at(i)] = TH1F(("h_jetmass4_dressShift_forb1_"+m_regionNames.at(i)).c_str(),("h_jetmass4_dressShift_forb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    
    xMax = 2.0;
    m_hists_MJ_kin[m_regionNames.at(i)] = TH1F(("h_MJ_kin_"+m_regionNames.at(i)).c_str(),("h_MJ_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressNom[m_regionNames.at(i)] = TH1F(("h_MJ_dressNom_"+m_regionNames.at(i)).c_str(),("h_MJ_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_cenb0[m_regionNames.at(i)] = TH1F(("h_MJ_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),("h_MJ_dressShift_cenb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_cenb1[m_regionNames.at(i)] = TH1F(("h_MJ_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),("h_MJ_dressShift_cenb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_forb0[m_regionNames.at(i)] = TH1F(("h_MJ_dressShift_forb0_"+m_regionNames.at(i)).c_str(),("h_MJ_dressShift_forb0_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_forb1[m_regionNames.at(i)] = TH1F(("h_MJ_dressShift_forb1_"+m_regionNames.at(i)).c_str(),("h_MJ_dressShift_forb1_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_kin[m_regionNames.at(i)].Sumw2();
    m_hists_MJ_dressNom[m_regionNames.at(i)].Sumw2();
    m_hists_MJ_dressShift_cenb0[m_regionNames.at(i)].Sumw2();
    m_hists_MJ_dressShift_cenb1[m_regionNames.at(i)].Sumw2();
    m_hists_MJ_dressShift_forb0[m_regionNames.at(i)].Sumw2();
    m_hists_MJ_dressShift_forb1[m_regionNames.at(i)].Sumw2();
  }
}
void MJ::dresser::loop(){
  TTree *t = m_miniTree.fChain;
  int nEntries = t->GetEntries();
  cout<<"Looping over miniTree with "<<nEntries<<" entries"<<endl;
  for(unsigned int entry = 0; entry < nEntries; entry++){
    b_jet_m_dressed_nom->clear();
    b_jet_m_dressed_shift_cenb0->clear();
    b_jet_m_dressed_shift_cenb1->clear();
    b_jet_m_dressed_shift_forb0->clear();
    b_jet_m_dressed_shift_forb1->clear();

    if( entry % 100000 == 0 ){
      cout<<"Processing entry "<<entry<<endl;
    }
    m_miniTree.GetEntry(entry);
    if(m_miniTree.njet >=3){
      float MJ_kin = 0;
      int unBlindEvent = 1;
      if( m_blinded ){
	for(unsigned int i = 0; i < min(4,m_miniTree.njet); i++){
	  MJ_kin += m_miniTree.jet_m->at(i);
	}
	if(MJ_kin > m_MJcut){
	  unBlindEvent = 0;
	}
      }
      MJ_kin = 0;
      float MJ_dressNom = 0;
      float MJ_dressShift_cenb0 = 0;
      float MJ_dressShift_cenb1 = 0;
      float MJ_dressShift_forb0 = 0;
      float MJ_dressShift_forb1 = 0;

      //regionName 0 based only on njet and dEta
      string regionNameS = "";
      if (m_miniTree.njet==3){
	if( m_miniTree.njet_soft == 0 ) regionNameS = "3js0";
	else if ( m_miniTree.njet_soft == 1 ) regionNameS = "3js1";
	else if ( m_miniTree.njet_soft >= 2 ) regionNameS = "3js2";
      }
      else if (m_miniTree.njet==4){
	if( m_miniTree.njet_soft == 0) regionNameS = "4js0";
	else if ( m_miniTree.njet_soft >= 1) regionNameS = "4js1";
      }
      else if (m_miniTree.njet >= 5){
	regionNameS = "5j";
      }
      string regionName0 = getRegionName(m_miniTree.njet,m_miniTree.dEta);
      //b-inclusive region name
      string regionName=regionName0+"b9";
      //b-tag/b-veto region name
      string regionNameB = regionName0;
      if( m_miniTree.nbjet_Fix70 > 0 ) regionNameB += "b1"; 
      else regionNameB += "b0";

      //4 different region names:
      //regionName = b-inclusive, separate VR, SR
      //regionNameB = b-tag/b-veto, separate VR, SR
      //regionNameM = b-match/b-unmatched, separate VR, SR
      //regionNameS = soft jet regions, inclusive in b-tagging and dEta

      //b-match/b-unmatch region name (different for each jet)
      for(unsigned int i = 0; i < min(4,m_miniTree.njet); i++){
	MJ_kin += m_miniTree.jet_m->at(i);
	string regionNameM = regionName0;
	if( m_miniTree.jet_bmatched_Fix70->at(i) == 1)regionNameM += "bM";
	else regionNameM += "bU";
	string templateHistName = "";
	//each event will have a b-inclusive region name and a b-tag/b-veto region name
	try{
	  int nsoft = 0;
	  //For ICHEP method, we have to consider number of soft jets when dressing 3-jet events
	  if(m_templateType == 2 and m_miniTree.njet==3){ nsoft = m_miniTree.njet_soft; }
	  templateHistName = getTemplateName(m_miniTree.jet_pt->at(i),
					     m_miniTree.jet_eta->at(i),
					     m_miniTree.jet_bmatched_Fix70->at(i),
					     m_miniTree.jet_qmatched->at(i),
					     m_miniTree.jet_gmatched->at(i),
					     m_miniTree.jet_NTrimSubjets->at(i),
					     //					     m_miniTree.BDTG,
					     0.0,
					     m_miniTree.nbjet_Fix70,
					     m_miniTree.njet+nsoft);
	}  
	catch( const char *msg ){
	  cerr<<msg<<endl;
	}
	TH1F *templateHist = (TH1F*)m_templateFile->Get(templateHistName.c_str());
	if(!templateHist){
	  cout<<"templateHistName = "<<templateHistName<<endl;
	  cout<<"Did you give the correct template type?"<<endl;
	  throw "Template hist could not be found in template file";
	}
	//	vector<float> dressedMass = getDressedMass(templateHist,m_miniTree.jet_pt->at(i),m_miniTree.jet_eta->at(i),m_miniTree.dEta,m_miniTree.njet,m_miniTree.isMC);
	vector<float> dressedMass = getDressedMass(templateHist,m_miniTree.jet_pt->at(i),m_miniTree.jet_eta->at(i),m_miniTree.jet_bmatched_Fix70->at(i),m_miniTree.isMC,m_miniTree.njet);

	MJ_dressNom += dressedMass.at(0);
	MJ_dressShift_cenb0 += dressedMass.at(1);
	MJ_dressShift_cenb1 += dressedMass.at(2);
	MJ_dressShift_forb0 += dressedMass.at(3);
	MJ_dressShift_forb1 += dressedMass.at(4);

	b_jet_m_dressed_nom->push_back(dressedMass.at(0));
	b_jet_m_dressed_shift_cenb0->push_back(dressedMass.at(1));
	b_jet_m_dressed_shift_cenb1->push_back(dressedMass.at(2));
	b_jet_m_dressed_shift_forb0->push_back(dressedMass.at(3));
	b_jet_m_dressed_shift_forb1->push_back(dressedMass.at(4));

	//Fill inclusive hists for every jet
	m_hists_m_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	m_hists_m_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	m_hists_m_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	m_hists_m_kin.at(regionNameS).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);

	m_hists_m_dressNom.at(regionName).Fill(dressedMass.at(0),m_miniTree.weight);
	m_hists_m_dressNom.at(regionNameB).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressNom.at(regionNameM).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressNom.at(regionNameS).Fill(dressedMass.at(0),m_miniTree.weight);

	//x and y values for profile histograms
	float xi = m_miniTree.jet_pt->at(i);
	//If overflow in pT, put this jet into the last bin
	if (xi >= m_prof1d_kin.at(regionName).GetXaxis()->GetBinUpEdge( m_prof1d_kin.at(regionName).GetNbinsX())){
	  xi = m_prof1d_kin.at(regionName).GetXaxis()->GetBinCenter(m_prof1d_kin.at(regionName).GetNbinsX());
	}
	float yi = fabs(m_miniTree.jet_eta->at(i));
	if( m_templateType == 1 ){ yi = m_miniTree.BDTG; }
	//Fill profile hists

	m_prof1d_kin.at(regionName).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight);
	m_prof1d_kin.at(regionNameS).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight);
	m_prof1d_kin.at(regionNameB).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);
	m_prof1d_kin.at(regionNameM).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);

	m_prof1d_dress.at(regionName).Fill(xi,dressedMass.at(0),m_miniTree.weight);
	m_prof1d_dress.at(regionNameS).Fill(xi,dressedMass.at(0),m_miniTree.weight);
	m_prof1d_dress.at(regionNameB).Fill(xi,dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	m_prof1d_dress.at(regionNameM).Fill(xi,dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);

	if( fabs(m_miniTree.jet_eta->at(i)) < 1){
	  //Fill profile hists for central jets
	  
	  m_prof1d_cen_kin.at(regionName).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight);
	  m_prof1d_cen_kin.at(regionNameS).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight);
	  m_prof1d_cen_kin.at(regionNameB).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof1d_cen_kin.at(regionNameM).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);
	  
	  m_prof1d_cen_dress.at(regionName).Fill(xi,dressedMass.at(0),m_miniTree.weight);
	  m_prof1d_cen_dress.at(regionNameS).Fill(xi,dressedMass.at(0),m_miniTree.weight);
	  m_prof1d_cen_dress.at(regionNameB).Fill(xi,dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof1d_cen_dress.at(regionNameM).Fill(xi,dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	}
	else{
	  //Fill profile hists for forward jets

	  m_prof1d_for_kin.at(regionName).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight);
	  m_prof1d_for_kin.at(regionNameS).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight);
	  m_prof1d_for_kin.at(regionNameB).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof1d_for_kin.at(regionNameM).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);
	  
	  m_prof1d_for_dress.at(regionName).Fill(xi,dressedMass.at(0),m_miniTree.weight);
	  m_prof1d_for_dress.at(regionNameS).Fill(xi,dressedMass.at(0),m_miniTree.weight);
	  m_prof1d_for_dress.at(regionNameB).Fill(xi,dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof1d_for_dress.at(regionNameM).Fill(xi,dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	}
	m_hists_m_dressShift_cenb0.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	m_hists_m_dressShift_cenb0.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	m_hists_m_dressShift_cenb0.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressShift_cenb0.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);

	m_hists_m_dressShift_cenb1.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	m_hists_m_dressShift_cenb1.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	m_hists_m_dressShift_cenb1.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressShift_cenb1.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);

	m_hists_m_dressShift_forb0.at(regionName).Fill(dressedMass.at(3),m_miniTree.weight);
	m_hists_m_dressShift_forb0.at(regionNameS).Fill(dressedMass.at(3),m_miniTree.weight);
	m_hists_m_dressShift_forb0.at(regionNameB).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressShift_forb0.at(regionNameM).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);

	m_hists_m_dressShift_forb1.at(regionName).Fill(dressedMass.at(4),m_miniTree.weight);
	m_hists_m_dressShift_forb1.at(regionNameS).Fill(dressedMass.at(4),m_miniTree.weight);
	m_hists_m_dressShift_forb1.at(regionNameB).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressShift_forb1.at(regionNameM).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);

	//Fill exclusive hists based on jet pT order
	if (i==0){ 
	  m_hists_m1_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m1_kin.at(regionNameS).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m1_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m1_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);

	  m_hists_m1_dressNom.at(regionName).Fill(dressedMass.at(0),m_miniTree.weight);
	  m_hists_m1_dressNom.at(regionNameS).Fill(dressedMass.at(0),m_miniTree.weight);
	  m_hists_m1_dressNom.at(regionNameB).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m1_dressNom.at(regionNameM).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);

	  m_hists_m1_dressShift_cenb0.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m1_dressShift_cenb0.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m1_dressShift_cenb0.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m1_dressShift_cenb0.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);

	  m_hists_m1_dressShift_cenb1.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m1_dressShift_cenb1.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m1_dressShift_cenb1.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m1_dressShift_cenb1.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);

	  m_hists_m1_dressShift_forb0.at(regionName).Fill(dressedMass.at(3),m_miniTree.weight);
	  m_hists_m1_dressShift_forb0.at(regionNameS).Fill(dressedMass.at(3),m_miniTree.weight);
	  m_hists_m1_dressShift_forb0.at(regionNameB).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m1_dressShift_forb0.at(regionNameM).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);

	  m_hists_m1_dressShift_forb1.at(regionName).Fill(dressedMass.at(4),m_miniTree.weight);
	  m_hists_m1_dressShift_forb1.at(regionNameS).Fill(dressedMass.at(4),m_miniTree.weight);
	  m_hists_m1_dressShift_forb1.at(regionNameB).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m1_dressShift_forb1.at(regionNameM).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);

	}
	if (i==1){ 
	  m_hists_m2_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m2_kin.at(regionNameS).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m2_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m2_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m2_dressNom.at(regionName).Fill(dressedMass.at(0),m_miniTree.weight);
	  m_hists_m2_dressNom.at(regionNameS).Fill(dressedMass.at(0),m_miniTree.weight);
	  m_hists_m2_dressNom.at(regionNameB).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressNom.at(regionNameM).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressShift_cenb0.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m2_dressShift_cenb0.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m2_dressShift_cenb0.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressShift_cenb0.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressShift_cenb1.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m2_dressShift_cenb1.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m2_dressShift_cenb1.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressShift_cenb1.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressShift_forb0.at(regionName).Fill(dressedMass.at(3),m_miniTree.weight);
	  m_hists_m2_dressShift_forb0.at(regionNameS).Fill(dressedMass.at(3),m_miniTree.weight);
	  m_hists_m2_dressShift_forb0.at(regionNameB).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressShift_forb0.at(regionNameM).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressShift_forb1.at(regionName).Fill(dressedMass.at(4),m_miniTree.weight);
	  m_hists_m2_dressShift_forb1.at(regionNameS).Fill(dressedMass.at(4),m_miniTree.weight);
	  m_hists_m2_dressShift_forb1.at(regionNameB).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressShift_forb1.at(regionNameM).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);
	}
	if (i==2){ 
	  m_hists_m3_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m3_kin.at(regionNameS).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m3_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m3_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m3_dressNom.at(regionName).Fill(dressedMass.at(0),m_miniTree.weight);
	  m_hists_m3_dressNom.at(regionNameS).Fill(dressedMass.at(0),m_miniTree.weight);
	  m_hists_m3_dressNom.at(regionNameB).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressNom.at(regionNameM).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);

	  m_hists_m3_dressShift_cenb0.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m3_dressShift_cenb0.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m3_dressShift_cenb0.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressShift_cenb0.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressShift_cenb1.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m3_dressShift_cenb1.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m3_dressShift_cenb1.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressShift_cenb1.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressShift_forb0.at(regionName).Fill(dressedMass.at(3),m_miniTree.weight);
	  m_hists_m3_dressShift_forb0.at(regionNameS).Fill(dressedMass.at(3),m_miniTree.weight);
	  m_hists_m3_dressShift_forb0.at(regionNameB).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressShift_forb0.at(regionNameM).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressShift_forb1.at(regionName).Fill(dressedMass.at(4),m_miniTree.weight);
	  m_hists_m3_dressShift_forb1.at(regionNameS).Fill(dressedMass.at(4),m_miniTree.weight);
	  m_hists_m3_dressShift_forb1.at(regionNameB).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressShift_forb1.at(regionNameM).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);
	}
	if (i==3){ 
	  m_hists_m4_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m4_kin.at(regionNameS).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m4_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m4_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m4_dressNom.at(regionName).Fill(dressedMass.at(0),m_miniTree.weight);
	  m_hists_m4_dressNom.at(regionNameS).Fill(dressedMass.at(0),m_miniTree.weight);
	  m_hists_m4_dressNom.at(regionNameB).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressNom.at(regionNameM).Fill(dressedMass.at(0),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressShift_cenb0.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m4_dressShift_cenb0.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m4_dressShift_cenb0.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressShift_cenb0.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressShift_cenb1.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m4_dressShift_cenb1.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m4_dressShift_cenb1.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressShift_cenb1.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressShift_forb0.at(regionName).Fill(dressedMass.at(3),m_miniTree.weight);
	  m_hists_m4_dressShift_forb0.at(regionNameS).Fill(dressedMass.at(3),m_miniTree.weight);
	  m_hists_m4_dressShift_forb0.at(regionNameB).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressShift_forb0.at(regionNameM).Fill(dressedMass.at(3),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressShift_forb1.at(regionName).Fill(dressedMass.at(4),m_miniTree.weight);
	  m_hists_m4_dressShift_forb1.at(regionNameS).Fill(dressedMass.at(4),m_miniTree.weight);
	  m_hists_m4_dressShift_forb1.at(regionNameB).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressShift_forb1.at(regionNameM).Fill(dressedMass.at(4),m_miniTree.weight*m_miniTree.bSF_70);
	}
      }
      m_hists_MJ_kin.at(regionName).Fill(MJ_kin,m_miniTree.weight*unBlindEvent);
      m_hists_MJ_kin.at(regionNameS).Fill(MJ_kin,m_miniTree.weight*unBlindEvent);
      m_hists_MJ_kin.at(regionNameB).Fill(MJ_kin,m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
      m_hists_MJ_dressNom.at(regionName).Fill(MJ_dressNom,m_miniTree.weight);
      m_hists_MJ_dressNom.at(regionNameS).Fill(MJ_dressNom,m_miniTree.weight);
      m_hists_MJ_dressNom.at(regionNameB).Fill(MJ_dressNom,m_miniTree.weight*m_miniTree.bSF_70);
      m_hists_MJ_dressShift_cenb0.at(regionName).Fill(MJ_dressShift_cenb0,m_miniTree.weight);
      m_hists_MJ_dressShift_cenb0.at(regionNameS).Fill(MJ_dressShift_cenb0,m_miniTree.weight);
      m_hists_MJ_dressShift_cenb0.at(regionNameB).Fill(MJ_dressShift_cenb0,m_miniTree.weight*m_miniTree.bSF_70);
      m_hists_MJ_dressShift_cenb1.at(regionName).Fill(MJ_dressShift_cenb1,m_miniTree.weight);
      m_hists_MJ_dressShift_cenb1.at(regionNameS).Fill(MJ_dressShift_cenb1,m_miniTree.weight);
      m_hists_MJ_dressShift_cenb1.at(regionNameB).Fill(MJ_dressShift_cenb1,m_miniTree.weight*m_miniTree.bSF_70);
      m_hists_MJ_dressShift_forb0.at(regionName).Fill(MJ_dressShift_forb0,m_miniTree.weight);
      m_hists_MJ_dressShift_forb0.at(regionNameS).Fill(MJ_dressShift_forb0,m_miniTree.weight);
      m_hists_MJ_dressShift_forb0.at(regionNameB).Fill(MJ_dressShift_forb0,m_miniTree.weight*m_miniTree.bSF_70);
      m_hists_MJ_dressShift_forb1.at(regionName).Fill(MJ_dressShift_forb1,m_miniTree.weight);
      m_hists_MJ_dressShift_forb1.at(regionNameS).Fill(MJ_dressShift_forb1,m_miniTree.weight);
      m_hists_MJ_dressShift_forb1.at(regionNameB).Fill(MJ_dressShift_forb1,m_miniTree.weight*m_miniTree.bSF_70);
    }
    m_outTree->Fill();
  }
  m_outFile->Write();
}
vector<float> MJ::dresser::getDressedMass(TH1F *h, float pt, float eta, int bMatch, bool isMC, int njet){
  int ptBin = -1;
  //need to know from which pT bin to get delta
  if(m_templateType==2){ ptBin= getTemplateBin(pt,0.0,4).first-1; }
  else{ ptBin = getTemplateBin(pt,0.0,3).first-1; }
  //bin corrections in pt/eta
  //  cout<<"m_corr_cen_b0.size = "<<m_corr_cen_b0.size()<<endl;
  //  cout<<"m_corr_cen_b1.size = "<<m_corr_cen_b1.size()<<endl;
  //  cout<<"m_corr_for_b0.size = "<<m_corr_cen_b0.size()<<endl;
  //  cout<<"m_corr_for_b1.size = "<<m_corr_cen_b0.size()<<endl;
    
  if( fabs(eta) < 1.0 and bMatch == 0) {
    m_delta = m_corr_cen_b0.at(ptBin);
    m_uncert = m_uncert_cen_b0;
  }
  else if( fabs(eta) < 1.0 and bMatch == 1){
    m_delta = m_corr_cen_b1.at(ptBin);
    m_uncert = m_uncert_cen_b1;
  }
  else if( fabs(eta) > 1.0 and bMatch == 0){
    m_delta = m_corr_for_b0.at(ptBin);
    m_uncert = m_uncert_for_b0;
  }
  else if( fabs(eta) > 1.0 and bMatch == 1){
    m_delta = m_corr_for_b1.at(ptBin);
    m_uncert = m_uncert_for_b1;
  }
  gRandom->SetSeed(0);
  TRandom3 tRandom(0);
  TH1F* hNew = (TH1F*)h->Clone("hnew");
  //Randomize template to get template statistical uncertainty
  for( int i = 1; i <= hNew->GetNbinsX(); i++){
    float binErr = hNew->GetBinError(i);
    float binCont = hNew->GetBinContent(i);
    float newBinCont = 0;
    if(isMC){
      float rand = tRandom.Gaus(0,binErr);
      newBinCont = binCont+rand;
    }
    else{
      newBinCont = tRandom.Poisson(binCont);
    }
    if (newBinCont < 0) { newBinCont = 0; }
    hNew->SetBinContent(i,newBinCont);
  }
  vector<float> answer;
  float r0 = hNew->GetRandom();
  delete hNew; hNew = 0;
  float m0 = pt*exp(r0);
  if (njet >= 4){
    m0 *= (1+m_delta);
  }
  answer = {m0,m0,m0,m0,m0};
  if( fabs(eta) < 1.0 and bMatch == 0) {
    answer.at(1) = answer.at(1)*(1+m_uncert);
  }
  else if( fabs(eta) < 1.0 and bMatch == 1){
    answer.at(2) = answer.at(2)*(1+m_uncert);
  }
  else if( fabs(eta) > 1.0 and bMatch == 0){
    answer.at(3) = answer.at(3)*(1+m_uncert);
  }
  else if( fabs(eta) > 1.0 and bMatch == 1){
    answer.at(4) = answer.at(4)*(1+m_uncert);
  }
  return answer;
}
string MJ::dresser::getRegionName(int njet, float dEta){
  string name = to_string(min(5,njet))+"j";
  if (dEta > 1.4) return name+"VR";
  return name+"SR";
}
pair<int,int> MJ::dresser::getTemplateBin(float pt, float y, int njet=3){
  int ptBin = -1;
  int yBin = -1;
  pair<int,int> bins;
  bins.first = -1;
  bins.second = -1;
  vector<double> ptBins;
  if (njet==3){ ptBins = m_ptBins3; }
  else if (njet==4){ ptBins = m_ptBins4; }
  else if (njet>=5){ ptBins = m_ptBins5; }
  if ( pt >= ptBins.back() ){
    bins.first = ptBins.size()-1;
  }
  for( unsigned int i = 0; i < ptBins.size()-1; i++){
    if (pt >= ptBins.at(i) && pt < ptBins.at(i+1)){
      bins.first = i+1;
      break;
    }
  }
  for( unsigned int i = 0; i < m_yBins.size()-1; i++){
    if (y >= m_yBins.at(i) && y < m_yBins.at(i+1)){
      bins.second = i+1;
      break;
    }
  }  
  return bins;
}
string MJ::dresser::getTemplateName(float pt, float eta, int bMatch, int qMatch, int gMatch, int nSubjets, float BDT, int nbjet, int njet){
  if(m_templateType == 0){
    pair<int,int> bins = getTemplateBin(pt,fabs(eta));
    int ptBin = bins.first;
    int etaBin = bins.second;
    if( ptBin == -1 || etaBin == -1 ){ throw "Could not find pT or BDT bin"; }
    return "templ_b"+to_string(bMatch)+"_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);
  }
  else if (m_templateType == 1){
    pair<int,int> bins = getTemplateBin(pt,BDT);
    int ptBin = bins.first;
    int bdtBin = bins.second;

    if( ptBin == -1 || bdtBin == -1 ){
      throw "Could not find pT or BDT bin";
    }
    return "templ_b"+to_string(bMatch)+"_ptBin"+to_string(ptBin)+"_bdtBin"+to_string(bdtBin);
  }
  else if (m_templateType == 2){
    pair<int,int> bins = getTemplateBin(pt,fabs(eta),njet);
    int ptBin = bins.first;
    int etaBin = bins.second;
    int btag = -1;
    if (njet <= 4 ){
      if (nbjet > 0) btag = 1;
      else btag = 0;
    }
    else if (njet >= 5){
      btag = 9;
    }
    if( ptBin == -1 || etaBin == -1 || btag == -1 || njet == -1){
      throw "Could not find pT bin, eta bin, b-tag status, or njet";
    }
    return  "templ_b"+to_string(btag)+"_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin)+"_njet"+to_string(min(5,njet));
  }
  else if(m_templateType == 3){
    pair<int,int> bins = getTemplateBin(pt,fabs(eta));
    int ptBin = bins.first;
    int etaBin = bins.second;
    if( ptBin == -1 || etaBin == -1 ){ throw "Could not find pT or BDT bin"; }
    if( bMatch == 1 ){
      return "templ_b1_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);      
    }
    else if( qMatch == 1 ){
      return "templ_q1_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);
    }
    else if( gMatch == 1){
      return "templ_g1_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);
    }
    else{
      TRandom3 r=TRandom3(0);
      bool flip = r.Rndm() > 0.5;
      //      cout<<"qMatch = "<<qMatch<<" gMatch = "<<gMatch<<" flip = "<<flip<<endl;      
      if ( flip ){
	return "templ_q1_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);
      }
      else{
	return "templ_g1_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);
      }
    }
    return "";
  }
  else if(m_templateType == 4){
    pair<int,int> bins = getTemplateBin(pt,fabs(eta));
    int ptBin = bins.first;
    int etaBin = bins.second;
    if( ptBin == -1 || etaBin == -1 ){ throw "Could not find pT or BDT bin"; }
    return "templ_n"+to_string(min(3,nSubjets))+"_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);
  }
  else{
    throw "Template type not found";
  }
}
