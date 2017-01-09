#define DRESSER_CXX
#include "dresser.h"
#include "TTree.h"
#include "miniTree.cxx"
#include "TRandom3.h"
#include <iostream>
using namespace std;
MJ::dresser::dresser(){
  m_MJcut = 600;
  m_blinded = false;
  m_doCorrections = false;
  m_signalInjected = false;
  m_allEventRegionNames = {"3jb0","3jb1","3jb9",
			   "3js0b0","3js0b1","3js0b9",
			   "3js1b0","3js1b1","3js1b9",
			   "3jVRb0","3jVRb1","3jVRb9",
			   "3js0VRb0","3js0VRb1","3js0VRb9",
			   "3js1VRb0","3js1VRb1","3js1VRb9",
			   "3jSRb0","3jSRb1","3jSRb9",
			   "3js0SRb0","3js0SRb1","3js0SRb9",
			   "3js1SRb0","3js1SRb1","3js1SRb9",

			   "4jb0","4jb1","4jb9",
			   "4js0b0","4js0b1","4js0b9",
			   "4js1b0","4js1b1","4js1b9",
			   "4jVRb0","4jVRb1","4jVRb9",
			   "4js0VRb0","4js0VRb1","4js0VRb9",
			   "4js1VRb0","4js1VRb1","4js1VRb9",
			   "4jSRb0","4jSRb1","4jSRb9",
			   "4js0SRb0","4js0SRb1","4js0SRb9",
			   "4js1SRb0","4js1SRb1","4js1SRb9",

			   "5jb0","5jb1","5jb9",
			   "5js0b0","5js0b1","5js0b9",
			   "5js1b0","5js1b1","5js1b9",
			   "5jVRb0","5jVRb1","5jVRb9",
			   "5js0VRb0","5js0VRb1","5js0VRb9",
			   "5js1VRb0","5js1VRb1","5js1VRb9",
			   "5jSRb0","5jSRb1","5jSRb9",
			   "5js0SRb0","5js0SRb1","5js0SRb9",
			   "5js1SRb0","5js1SRb1","5js1SRb9"};
  m_allJetRegionNames = m_allEventRegionNames;
  for(unsigned int i = 0; i < m_allEventRegionNames.size(); i++){
    m_allJetRegionNames.push_back(m_allEventRegionNames.at(i)+"bU");
    m_allJetRegionNames.push_back(m_allEventRegionNames.at(i)+"bM");
    //    cout<<m_allEventRegionNames.at(i)<<endl;
  }
  //Turn corrections and uncertainties off
  m_corr_eta1_b0 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  m_corr_eta2_b0 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  m_corr_eta3_b0 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  m_corr_eta4_b0 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  m_corr_eta1_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  m_corr_eta2_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  m_corr_eta3_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  m_corr_eta4_b1 = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  m_uncert_eta1_b0 = 0;
  m_uncert_eta2_b0 = 0;
  m_uncert_eta3_b0 = 0;
  m_uncert_eta4_b0 = 0;
  m_uncert_eta1_b1 = 0;
  m_uncert_eta2_b1 = 0;
  m_uncert_eta3_b1 = 0;
  m_uncert_eta4_b1 = 0;
}
MJ::dresser::~dresser(){
}
void MJ::dresser::blind(float mjCut){
  m_MJcut = mjCut;
  m_blinded = true;
}
void MJ::dresser::injectSignal(int signalNum, float signalLumi){
  m_signalInjected = true;
  m_signalNum = signalNum;
  m_signalLumi = signalLumi;

  if(m_signalNum == 403553){
    m_uncert_eta1_b0 =  0.0785742236138 ;
    m_uncert_eta2_b0 =  0.064249580548 ;
    m_uncert_eta3_b0 =  0.0412591729053 ;
    m_uncert_eta4_b0 =  0.0654129776769 ;
    m_uncert_eta1_b1 =  0.25697299998 ;
    m_uncert_eta2_b1 =  0.178275366047 ;
    m_uncert_eta3_b1 =  0.137180299553 ;
    m_uncert_eta4_b1 =  0.155853953026 ;
  }
  else if(m_signalNum == 403555){
    m_uncert_eta1_b0 =  0.092078359181 ;
    m_uncert_eta2_b0 =  0.0745009898683 ;
    m_uncert_eta3_b0 =  0.0439696610383 ;
    m_uncert_eta4_b0 =  0.0675131741705 ;
    m_uncert_eta1_b1 =  0.288304835371 ;
    m_uncert_eta2_b1 =  0.248771564937 ;
    m_uncert_eta3_b1 =  0.13496116668 ;
    m_uncert_eta4_b1 =  0.167862332981 ;
  }
  else if(m_signalNum == 403557){
    m_uncert_eta1_b0 =  0.0877628118615 ;
    m_uncert_eta2_b0 =  0.0703263462104 ;
    m_uncert_eta3_b0 =  0.0406460948833 ;
    m_uncert_eta4_b0 =  0.067875653102 ;
    m_uncert_eta1_b1 =  0.253996184188 ;
    m_uncert_eta2_b1 =  0.271480703474 ;
    m_uncert_eta3_b1 =  0.116542344393 ;
    m_uncert_eta4_b1 =  0.165788627718 ;
  }
  else if(m_signalNum == 403564){
    m_uncert_eta1_b0 =  0.0760983589108 ;
    m_uncert_eta2_b0 =  0.0628149197308 ;
    m_uncert_eta3_b0 =  0.03942940977 ;
    m_uncert_eta4_b0 =  0.0650079362413 ;
    m_uncert_eta1_b1 =  0.245954098902 ;
    m_uncert_eta2_b1 =  0.179324727477 ;
    m_uncert_eta3_b1 =  0.138963496328 ;
    m_uncert_eta4_b1 =  0.145486068103 ;
  }
  else if(m_signalNum==403567){
    m_uncert_eta1_b0 =  0.0729246756683 ;
    m_uncert_eta2_b0 =  0.0618618972502 ;
    m_uncert_eta3_b0 =  0.0418112570073 ;
    m_uncert_eta4_b0 =  0.0646063739277 ;
    m_uncert_eta1_b1 =  0.26233920897 ;
    m_uncert_eta2_b1 =  0.205209930226 ;
    m_uncert_eta3_b1 =  0.133307189061 ;
    m_uncert_eta4_b1 =  0.170963153465 ;
  }
  else if(m_signalNum == 403570){
    m_uncert_eta1_b0 =  0.0762503171171 ;
    m_uncert_eta2_b0 =  0.0622057203723 ;
    m_uncert_eta3_b0 =  0.0415483304151 ;
    m_uncert_eta4_b0 =  0.0626045129744 ;
    m_uncert_eta1_b1 =  0.263316169944 ;
    m_uncert_eta2_b1 =  0.182770024995 ;
    m_uncert_eta3_b1 =  0.134997674242 ;
    m_uncert_eta4_b1 =  0.15689634846 ;
  }
  else if (m_signalNum == 403587){
    m_uncert_eta1_b0 =  0.0718492945845 ;
    m_uncert_eta2_b0 =  0.061039621083 ;
    m_uncert_eta3_b0 =  0.0380999063189 ;
    m_uncert_eta4_b0 =  0.0627015045999 ;
    m_uncert_eta1_b1 =  0.262751545659 ;
    m_uncert_eta2_b1 =  0.201291052662 ;
    m_uncert_eta3_b1 =  0.137313482736 ;
    m_uncert_eta4_b1 =  0.157365571844 ;
  }
  else if(m_signalNum==403591){
    m_uncert_eta1_b0 =  0.0692154529887 ;
    m_uncert_eta2_b0 =  0.0589087257546 ;
    m_uncert_eta3_b0 =  0.0391125662931 ;
    m_uncert_eta4_b0 =  0.0637459763128 ;
    m_uncert_eta1_b1 =  0.260949183082 ;
    m_uncert_eta2_b1 =  0.174211451578 ;
    m_uncert_eta3_b1 =  0.137472869494 ;
    m_uncert_eta4_b1 =  0.163095316866 ;
  }
  else if(m_signalNum==403595){
    m_uncert_eta1_b0 =  0.0716624758545 ;
    m_uncert_eta2_b0 =  0.0614986650733 ;
    m_uncert_eta3_b0 =  0.0404930822889 ;
    m_uncert_eta4_b0 =  0.0653609347351 ;
    m_uncert_eta1_b1 =  0.25817114456 ;
    m_uncert_eta2_b1 =  0.179241725243 ;
    m_uncert_eta3_b1 =  0.134992410277 ;
    m_uncert_eta4_b1 =  0.159517096994 ;
  }
}
void MJ::dresser::initialize(){
  cout<<"Applying the following uncertainties:"<<endl;
  cout<<"    m_uncert_eta1_b0 = "<<m_uncert_eta1_b0<<endl;
  cout<<"    m_uncert_eta2_b0 = "<<m_uncert_eta2_b0<<endl;
  cout<<"    m_uncert_eta3_b0 = "<<m_uncert_eta3_b0<<endl;
  cout<<"    m_uncert_eta4_b0 = "<<m_uncert_eta4_b0<<endl;
  cout<<"    m_uncert_eta1_b1 = "<<m_uncert_eta1_b1<<endl;
  cout<<"    m_uncert_eta2_b1 = "<<m_uncert_eta2_b1<<endl;
  cout<<"    m_uncert_eta3_b1 = "<<m_uncert_eta3_b1<<endl;
  cout<<"    m_uncert_eta4_b1 = "<<m_uncert_eta4_b1<<endl;
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
  b_jet_m_dressed_shift_eta1_b0 = new vector<double>;
  b_jet_m_dressed_shift_eta2_b0 = new vector<double>;
  b_jet_m_dressed_shift_eta3_b0 = new vector<double>;
  b_jet_m_dressed_shift_eta4_b0 = new vector<double>;

  b_jet_m_dressed_shift_eta1_b1 = new vector<double>;
  b_jet_m_dressed_shift_eta2_b1 = new vector<double>;
  b_jet_m_dressed_shift_eta3_b1 = new vector<double>;
  b_jet_m_dressed_shift_eta4_b1 = new vector<double>;

  m_outTree->Branch("jet_m_dressed_nom",&b_jet_m_dressed_nom);
  m_outTree->Branch("jet_m_dressed_shift_eta1_b0",&b_jet_m_dressed_shift_eta1_b0);
  m_outTree->Branch("jet_m_dressed_shift_eta2_b0",&b_jet_m_dressed_shift_eta2_b0);
  m_outTree->Branch("jet_m_dressed_shift_eta3_b0",&b_jet_m_dressed_shift_eta3_b0);
  m_outTree->Branch("jet_m_dressed_shift_eta4_b0",&b_jet_m_dressed_shift_eta4_b0);
  m_outTree->Branch("jet_m_dressed_shift_eta1_b1",&b_jet_m_dressed_shift_eta1_b1);
  m_outTree->Branch("jet_m_dressed_shift_eta2_b1",&b_jet_m_dressed_shift_eta2_b1);
  m_outTree->Branch("jet_m_dressed_shift_eta3_b1",&b_jet_m_dressed_shift_eta3_b1);
  m_outTree->Branch("jet_m_dressed_shift_eta4_b1",&b_jet_m_dressed_shift_eta4_b1);

  //Set pT and eta binning -> at some point change this to use config file instead
  if(m_templateType == 0){
    //pt/eta/b-match binning
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};



    //ICHEP dataset
    //Turn on uncertainties derived from 4js1VRb9bU and 4js1VRb9bM
    // m_uncert_eta1_b0 =  0.0737797596282 ;
    // m_uncert_eta2_b0 =  0.0517731839566 ;
    // m_uncert_eta3_b0 =  0.0353641177501 ;
    // m_uncert_eta4_b0 =  0.0408826138381 ;
    // m_uncert_eta1_b1 =  0.142417736724 ;
    // m_uncert_eta2_b1 =  0.117140877143 ;
    // m_uncert_eta3_b1 =  0.105112534795 ;
    // m_uncert_eta4_b1 =  0.143027092743 ;

    //Pythia MC
    // m_uncert_eta1_b0 =  0.0982161391755 ;
    // m_uncert_eta2_b0 =  0.137968487372 ;
    // m_uncert_eta3_b0 =  0.0582116769559 ;
    // m_uncert_eta4_b0 =  0.102420347557 ;
    // m_uncert_eta1_b1 =  0.388618739687 ;
    // m_uncert_eta2_b1 =  0.335133822192 ;
    // m_uncert_eta3_b1 =  0.456537745303 ;
    // m_uncert_eta4_b1 =  0.307089372309 ;
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
  //Jet level histograms
  for (unsigned int i = 0; i < m_allJetRegionNames.size(); i++){
    vector<double> ptBins;
    if (m_allJetRegionNames.at(i).find("3j") != string::npos){ ptBins = m_ptBins3; }
    else if (m_allJetRegionNames.at(i).find("4j") != string::npos) { ptBins = m_ptBins4; }
    else if (m_allJetRegionNames.at(i).find("5j") != string::npos) { ptBins = m_ptBins5; }
    //Declare 1D profile hists with pt bins same as templates
    m_prof1d_kin[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_kin_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_eta1_kin[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_eta1_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_eta1_kin_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_eta2_kin[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_eta2_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_eta2_kin_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_eta3_kin[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_eta3_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_eta3_kin_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_eta4_kin[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_eta4_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_eta4_kin_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());

    m_prof1d_dress[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_dress_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_dress_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_eta1_dress[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_eta1_dress_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_eta1_dress_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_eta2_dress[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_eta2_dress_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_eta2_dress_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_eta3_dress[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_eta3_dress_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_eta3_dress_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_eta4_dress[m_allJetRegionNames.at(i)] = TProfile(("h_prof1d_eta4_dress_"+m_allJetRegionNames.at(i)).c_str(),("h_prof1d_eta4_dress_"+m_allJetRegionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());

    int nBins = 200;
    float xMin = 0;
    float xMax = 1.2;
    m_hists_m_kin[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_kin_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressNom[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressNom_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressNom_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_eta1_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_eta2_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_eta3_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_eta4_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_eta1_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_eta2_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_eta3_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressShift_eta4_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);

    m_hists_m1_kin[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_kin_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressNom[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressNom_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressNom_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_eta1_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_eta2_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_eta3_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);   
    m_hists_m1_dressShift_eta4_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_eta1_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_eta2_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressShift_eta3_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);   
    m_hists_m1_dressShift_eta4_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass1_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass1_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);

    m_hists_m2_kin[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_kin_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressNom[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressNom_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressNom_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_eta1_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_eta2_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_eta3_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_eta4_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_eta1_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_eta2_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_eta3_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressShift_eta4_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass2_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass2_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);

    xMax = 0.6;
    m_hists_m3_kin[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_kin_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressNom[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressNom_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressNom_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_eta1_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_eta2_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_eta3_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_eta4_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_eta1_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_eta2_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_eta3_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressShift_eta4_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass3_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass3_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);

    xMax = 0.4;
    m_hists_m4_kin[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_kin_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_kin_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressNom[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressNom_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressNom_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_eta1_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressShift_eta1_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_eta2_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressShift_eta2_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_eta3_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressShift_eta3_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_eta4_b0[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressShift_eta4_b0_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_eta1_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressShift_eta1_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_eta2_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressShift_eta2_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_eta3_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressShift_eta3_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressShift_eta4_b1[m_allJetRegionNames.at(i)] = TH1F(("h_jetmass4_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),("h_jetmass4_dressShift_eta4_b1_"+m_allJetRegionNames.at(i)).c_str(),nBins,xMin,xMax);
  }
  //event-level histograms
  for(unsigned int i = 0; i < m_allEventRegionNames.size(); i++){
    int nBins = 200;
    float xMin = 0;
    float xMax = 2.0;
    m_hists_MJ_kin[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_kin_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_kin_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressNom[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressNom_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressNom_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_eta1_b0[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressShift_eta1_b0_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressShift_eta1_b0_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_eta2_b0[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressShift_eta2_b0_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressShift_eta2_b0_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_eta3_b0[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressShift_eta3_b0_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressShift_eta3_b0_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_eta4_b0[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressShift_eta4_b0_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressShift_eta4_b0_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_eta1_b1[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressShift_eta1_b1_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressShift_eta1_b1_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_eta2_b1[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressShift_eta2_b1_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressShift_eta2_b1_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_eta3_b1[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressShift_eta3_b1_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressShift_eta3_b1_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressShift_eta4_b1[m_allEventRegionNames.at(i)] = TH1F(("h_MJ_dressShift_eta4_b1_"+m_allEventRegionNames.at(i)).c_str(),("h_MJ_dressShift_eta4_b1_"+m_allEventRegionNames.at(i)).c_str(),nBins,xMin,xMax);
  }
}
void MJ::dresser::loop(){
  TTree *t = m_miniTree.fChain;
  int nEntries = t->GetEntries();
  cout<<"Looping over miniTree with "<<nEntries<<" entries"<<endl;
  for(unsigned int entry = 0; entry < nEntries; entry++){
    b_jet_m_dressed_nom->clear();
    b_jet_m_dressed_shift_eta1_b0->clear();
    b_jet_m_dressed_shift_eta2_b0->clear();
    b_jet_m_dressed_shift_eta3_b0->clear();
    b_jet_m_dressed_shift_eta4_b0->clear();
    b_jet_m_dressed_shift_eta1_b1->clear();
    b_jet_m_dressed_shift_eta2_b1->clear();
    b_jet_m_dressed_shift_eta3_b1->clear();
    b_jet_m_dressed_shift_eta4_b1->clear();
    if( entry % 100000 == 0 ){
      cout<<"Processing entry "<<entry<<endl;
    }
    m_miniTree.GetEntry(entry);
    float wt = m_miniTree.weight*m_miniTree.bSF_70;
    if(m_miniTree.eventNumber==1884202){ wt = 0; }
    if(m_signalInjected and m_miniTree.mcChannelNumber > 0){
      //This is a signal event so scale up by luminosity if it's the right DSID
      if ( m_miniTree.mcChannelNumber == m_signalNum ){
	wt *= m_signalLumi;
      }
      //If it's a signal event but not from the right signal point, ignore it
      else{
	wt = 0;
	continue;
      }
    }
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
      float MJ_dressShift_eta1_b0 = 0;
      float MJ_dressShift_eta2_b0 = 0;
      float MJ_dressShift_eta3_b0 = 0;
      float MJ_dressShift_eta4_b0 = 0;
      float MJ_dressShift_eta1_b1 = 0;
      float MJ_dressShift_eta2_b1 = 0;
      float MJ_dressShift_eta3_b1 = 0;
      float MJ_dressShift_eta4_b1 = 0;
      m_regionNameList_event.clear();
      m_regionNameList_event = getEventRegionList(m_miniTree.njet,
						  m_miniTree.nbjet_Fix70,
						  m_miniTree.njet_soft,
						  m_miniTree.dEta);
      for(unsigned int i = 0; i < min(4,m_miniTree.njet); i++){
	MJ_kin += m_miniTree.jet_m->at(i);
	m_regionNameList_jet.clear();
	m_regionNameList_jet = getJetRegionList(m_miniTree.njet,
						m_miniTree.nbjet_Fix70,
						m_miniTree.njet_soft,
						m_miniTree.jet_bmatched_Fix70->at(i),
						m_miniTree.dEta);
	string templateHistName = "";
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
	vector<float> dressedMass = getDressedMass(templateHist,m_miniTree.jet_pt->at(i),m_miniTree.jet_eta->at(i),m_miniTree.jet_bmatched_Fix70->at(i),m_miniTree.isMC,m_miniTree.njet);

	MJ_dressNom += dressedMass.at(0);
	MJ_dressShift_eta1_b0 += dressedMass.at(1);
	MJ_dressShift_eta2_b0 += dressedMass.at(2);
	MJ_dressShift_eta3_b0 += dressedMass.at(3);
	MJ_dressShift_eta4_b0 += dressedMass.at(4);
	MJ_dressShift_eta1_b1 += dressedMass.at(5);
	MJ_dressShift_eta2_b1 += dressedMass.at(6);
	MJ_dressShift_eta3_b1 += dressedMass.at(7);
	MJ_dressShift_eta4_b1 += dressedMass.at(8);

	b_jet_m_dressed_nom->push_back(dressedMass.at(0));
	b_jet_m_dressed_shift_eta1_b0->push_back(dressedMass.at(1));
	b_jet_m_dressed_shift_eta2_b0->push_back(dressedMass.at(2));
	b_jet_m_dressed_shift_eta3_b0->push_back(dressedMass.at(3));
	b_jet_m_dressed_shift_eta4_b0->push_back(dressedMass.at(4));
	b_jet_m_dressed_shift_eta1_b1->push_back(dressedMass.at(5));
	b_jet_m_dressed_shift_eta2_b1->push_back(dressedMass.at(6));
	b_jet_m_dressed_shift_eta3_b1->push_back(dressedMass.at(7));
	b_jet_m_dressed_shift_eta4_b1->push_back(dressedMass.at(8));

	//Fill inclusive hists for every jet
	for( unsigned int j = 0; j < m_regionNameList_jet.size(); j++){
	  string regionName = m_regionNameList_jet.at(j);
	  m_hists_m_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),wt*unBlindEvent);
	  m_hists_m_dressNom.at(regionName).Fill(dressedMass.at(0),wt);
	  //x and y values for profile histograms
	  float xi = m_miniTree.jet_pt->at(i);
	  //If overflow in pT, put this jet into the last bin
	  if (xi >= m_prof1d_kin.at(regionName).GetXaxis()->GetBinUpEdge( m_prof1d_kin.at(regionName).GetNbinsX())){
	    xi = m_prof1d_kin.at(regionName).GetXaxis()->GetBinCenter(m_prof1d_kin.at(regionName).GetNbinsX());
	  }
	  float yi = fabs(m_miniTree.jet_eta->at(i));
	  if( m_templateType == 1 ){ yi = m_miniTree.BDTG; }
	  //Fill profile hists
	  m_prof1d_kin.at(regionName).Fill(xi,m_miniTree.jet_m->at(i),wt);
	  m_prof1d_dress.at(regionName).Fill(xi,dressedMass.at(0),wt);

	  if( fabs(m_miniTree.jet_eta->at(i)) < 0.5){
	    m_prof1d_eta1_kin.at(regionName).Fill(xi,m_miniTree.jet_m->at(i),wt);
	    m_prof1d_eta1_dress.at(regionName).Fill(xi,dressedMass.at(0),wt);
	  }
	  else if( fabs(m_miniTree.jet_eta->at(i)) < 1.0){
	    m_prof1d_eta2_kin.at(regionName).Fill(xi,m_miniTree.jet_m->at(i),wt);
	    m_prof1d_eta2_dress.at(regionName).Fill(xi,dressedMass.at(0),wt);
	  }
	  else if( fabs(m_miniTree.jet_eta->at(i)) < 1.5){
	    m_prof1d_eta3_kin.at(regionName).Fill(xi,m_miniTree.jet_m->at(i),wt);
	    m_prof1d_eta3_dress.at(regionName).Fill(xi,dressedMass.at(0),wt);
	  }
	  else if( fabs(m_miniTree.jet_eta->at(i)) < 2.0){
	    m_prof1d_eta4_kin.at(regionName).Fill(xi,m_miniTree.jet_m->at(i),wt);
	    m_prof1d_eta4_dress.at(regionName).Fill(xi,dressedMass.at(0),wt);
	    
	  }
	  m_hists_m_dressShift_eta1_b0.at(regionName).Fill(dressedMass.at(1),wt);
	  m_hists_m_dressShift_eta2_b0.at(regionName).Fill(dressedMass.at(2),wt);
	  m_hists_m_dressShift_eta3_b0.at(regionName).Fill(dressedMass.at(3),wt);
	  m_hists_m_dressShift_eta4_b0.at(regionName).Fill(dressedMass.at(4),wt);
	  m_hists_m_dressShift_eta1_b1.at(regionName).Fill(dressedMass.at(5),wt);
	  m_hists_m_dressShift_eta2_b1.at(regionName).Fill(dressedMass.at(6),wt);
	  m_hists_m_dressShift_eta3_b1.at(regionName).Fill(dressedMass.at(7),wt);
	  m_hists_m_dressShift_eta4_b1.at(regionName).Fill(dressedMass.at(8),wt);
	  //Fill exclusive hists based on jet pT order
	  if (i==0){ 
	    m_hists_m1_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),wt*unBlindEvent);
	    m_hists_m1_dressNom.at(regionName).Fill(dressedMass.at(0),wt);
	    m_hists_m1_dressShift_eta1_b0.at(regionName).Fill(dressedMass.at(1),wt);
	    m_hists_m1_dressShift_eta2_b0.at(regionName).Fill(dressedMass.at(2),wt);
	    m_hists_m1_dressShift_eta3_b0.at(regionName).Fill(dressedMass.at(3),wt);
	    m_hists_m1_dressShift_eta4_b0.at(regionName).Fill(dressedMass.at(4),wt);
	    m_hists_m1_dressShift_eta1_b1.at(regionName).Fill(dressedMass.at(5),wt);
	    m_hists_m1_dressShift_eta2_b1.at(regionName).Fill(dressedMass.at(6),wt);
	    m_hists_m1_dressShift_eta3_b1.at(regionName).Fill(dressedMass.at(7),wt);
	    m_hists_m1_dressShift_eta4_b1.at(regionName).Fill(dressedMass.at(8),wt);
	  }
	  if (i==1){ 
	    m_hists_m2_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),wt*unBlindEvent);
	    m_hists_m2_dressNom.at(regionName).Fill(dressedMass.at(0),wt);
	    m_hists_m2_dressShift_eta1_b0.at(regionName).Fill(dressedMass.at(1),wt);
	    m_hists_m2_dressShift_eta2_b0.at(regionName).Fill(dressedMass.at(2),wt);
	    m_hists_m2_dressShift_eta3_b0.at(regionName).Fill(dressedMass.at(3),wt);
	    m_hists_m2_dressShift_eta4_b0.at(regionName).Fill(dressedMass.at(4),wt);
	    m_hists_m2_dressShift_eta1_b1.at(regionName).Fill(dressedMass.at(5),wt);
	    m_hists_m2_dressShift_eta2_b1.at(regionName).Fill(dressedMass.at(6),wt);
	    m_hists_m2_dressShift_eta3_b1.at(regionName).Fill(dressedMass.at(7),wt);
	    m_hists_m2_dressShift_eta4_b1.at(regionName).Fill(dressedMass.at(8),wt);
	  }
	  if (i==2){ 
	    m_hists_m3_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),wt*unBlindEvent);
	    m_hists_m3_dressNom.at(regionName).Fill(dressedMass.at(0),wt);
	    m_hists_m3_dressShift_eta1_b0.at(regionName).Fill(dressedMass.at(1),wt);
	    m_hists_m3_dressShift_eta2_b0.at(regionName).Fill(dressedMass.at(2),wt);
	    m_hists_m3_dressShift_eta3_b0.at(regionName).Fill(dressedMass.at(3),wt);
	    m_hists_m3_dressShift_eta4_b0.at(regionName).Fill(dressedMass.at(4),wt);
	    m_hists_m3_dressShift_eta1_b1.at(regionName).Fill(dressedMass.at(5),wt);
	    m_hists_m3_dressShift_eta2_b1.at(regionName).Fill(dressedMass.at(6),wt);
	    m_hists_m3_dressShift_eta3_b1.at(regionName).Fill(dressedMass.at(7),wt);
	    m_hists_m3_dressShift_eta4_b1.at(regionName).Fill(dressedMass.at(8),wt);
	  }
	  if (i==3){ 
	    m_hists_m4_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),wt*unBlindEvent);
	    m_hists_m4_dressNom.at(regionName).Fill(dressedMass.at(0),wt);
	    m_hists_m4_dressShift_eta1_b0.at(regionName).Fill(dressedMass.at(1),wt);
	    m_hists_m4_dressShift_eta2_b0.at(regionName).Fill(dressedMass.at(2),wt);
	    m_hists_m4_dressShift_eta3_b0.at(regionName).Fill(dressedMass.at(3),wt);
	    m_hists_m4_dressShift_eta4_b0.at(regionName).Fill(dressedMass.at(4),wt);
	    m_hists_m4_dressShift_eta1_b1.at(regionName).Fill(dressedMass.at(5),wt);
	    m_hists_m4_dressShift_eta2_b1.at(regionName).Fill(dressedMass.at(6),wt);
	    m_hists_m4_dressShift_eta3_b1.at(regionName).Fill(dressedMass.at(7),wt);
	    m_hists_m4_dressShift_eta4_b1.at(regionName).Fill(dressedMass.at(8),wt);
	  }
	}
      }
      for(unsigned int j = 0; j < m_regionNameList_event.size(); j++){
	string regionName = m_regionNameList_event.at(j);
	m_hists_MJ_kin.at(regionName).Fill(MJ_kin,wt*unBlindEvent);
	m_hists_MJ_dressNom.at(regionName).Fill(MJ_dressNom,wt);
	m_hists_MJ_dressShift_eta1_b0.at(regionName).Fill(MJ_dressShift_eta1_b0,wt);
	m_hists_MJ_dressShift_eta2_b0.at(regionName).Fill(MJ_dressShift_eta2_b0,wt);
	m_hists_MJ_dressShift_eta3_b0.at(regionName).Fill(MJ_dressShift_eta3_b0,wt);
	m_hists_MJ_dressShift_eta4_b0.at(regionName).Fill(MJ_dressShift_eta4_b0,wt);
	m_hists_MJ_dressShift_eta1_b1.at(regionName).Fill(MJ_dressShift_eta1_b1,wt);
	m_hists_MJ_dressShift_eta2_b1.at(regionName).Fill(MJ_dressShift_eta2_b1,wt);
	m_hists_MJ_dressShift_eta3_b1.at(regionName).Fill(MJ_dressShift_eta3_b1,wt);
	m_hists_MJ_dressShift_eta4_b1.at(regionName).Fill(MJ_dressShift_eta4_b1,wt);
      }
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
    
  if( fabs(eta) < 0.5 and bMatch == 0) {
    m_delta = m_corr_eta1_b0.at(ptBin);
    m_uncert = m_uncert_eta1_b0;
  }
  else if( fabs(eta) < 1.0 and bMatch == 0) {
    m_delta = m_corr_eta2_b0.at(ptBin);
    m_uncert = m_uncert_eta2_b0;
  }
  else if( fabs(eta) < 1.5 and bMatch == 0) {
    m_delta = m_corr_eta3_b0.at(ptBin);
    m_uncert = m_uncert_eta3_b0;
  }
  else if( fabs(eta) < 2.0 and bMatch == 0) {
    m_delta = m_corr_eta4_b0.at(ptBin);
    m_uncert = m_uncert_eta4_b0;
  }
  if( fabs(eta) < 0.5 and bMatch == 1) {
    m_delta = m_corr_eta1_b1.at(ptBin);
    m_uncert = m_uncert_eta1_b1;
  }
  else if( fabs(eta) < 1.0 and bMatch == 1) {
    m_delta = m_corr_eta2_b1.at(ptBin);
    m_uncert = m_uncert_eta2_b1;
  }
  else if( fabs(eta) < 1.5 and bMatch == 1) {
    m_delta = m_corr_eta3_b1.at(ptBin);
    m_uncert = m_uncert_eta3_b1;
  }
  else if( fabs(eta) < 2.0 and bMatch == 1) {
    m_delta = m_corr_eta4_b1.at(ptBin);
    m_uncert = m_uncert_eta4_b1;
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
  answer = {m0,m0,m0,m0,m0,m0,m0,m0,m0};
  if( fabs(eta) < 0.5 and bMatch == 0) {
    answer.at(1) = answer.at(1)*(1+m_uncert);
  }
  else if( fabs(eta) < 1.0 and bMatch == 0){
    answer.at(2) = answer.at(2)*(1+m_uncert);
  }
  else if( fabs(eta) < 1.5 and bMatch == 0){
    answer.at(3) = answer.at(3)*(1+m_uncert);
  }
  else if( fabs(eta) < 2.0 and bMatch == 0){
    answer.at(4) = answer.at(4)*(1+m_uncert);
  }
  if( fabs(eta) < 0.5 and bMatch == 1) {
    answer.at(5) = answer.at(5)*(1+m_uncert);
  }
  else if( fabs(eta) < 1.0 and bMatch == 1){
    answer.at(6) = answer.at(6)*(1+m_uncert);
  }
  else if( fabs(eta) < 1.5 and bMatch == 1){
    answer.at(7) = answer.at(7)*(1+m_uncert);
  }
  else if( fabs(eta) < 2.0 and bMatch == 1){
    answer.at(8) = answer.at(8)*(1+m_uncert);
  }
  return answer;
}
vector<string> MJ::dresser::getJetRegionList(int nJet, int nBJet, int nSoftJet, int bMatch, float dEta){
  vector<string> eventRegionList = getEventRegionList(nJet,nBJet,nSoftJet,dEta);
  vector<string> answer = eventRegionList;
  for( unsigned int i = 0; i < eventRegionList.size(); i++){
    if (bMatch == 1){
      answer.push_back(eventRegionList.at(i)+"bM");
    }
    else{
      answer.push_back(eventRegionList.at(i)+"bU");
    }
  }
  return answer;
}
vector<string> MJ::dresser::getEventRegionList(int nJet, int nBJet, int nSoftJet, float dEta){
  vector<string> answer = {};
  string nJetStr = "3j";
  if (nJet == 4) nJetStr = "4j";
  if (nJet >= 5) nJetStr = "5j";
  answer.push_back(nJetStr+"b9");
  if(nBJet == 0) {
    answer.push_back(nJetStr+"b0");
    if(nSoftJet == 0) answer.push_back(nJetStr+"s0b0");
    else answer.push_back(nJetStr+"s1b0");
  }
  else {
    answer.push_back(nJetStr+"b1");
    if(nSoftJet == 0) answer.push_back(nJetStr+"s0b1");
    else answer.push_back(nJetStr+"s1b1");
  }
  if( nSoftJet == 0) answer.push_back(nJetStr+"s0b9");
  else answer.push_back(nJetStr+"s1b9");
  if(dEta > 1.4){
    answer.push_back(nJetStr+"VRb9");
    if(nBJet == 0) {
      answer.push_back(nJetStr+"VRb0");
      if(nSoftJet == 0) answer.push_back(nJetStr+"s0VRb0");
      else answer.push_back(nJetStr+"s1VRb0");
    }
    else {
      answer.push_back(nJetStr+"VRb1");
      if(nSoftJet == 0) answer.push_back(nJetStr+"s0VRb1");
      else answer.push_back(nJetStr+"s1VRb1");
    }
    if( nSoftJet == 0) answer.push_back(nJetStr+"s0VRb9");
    else answer.push_back(nJetStr+"s1VRb9");
  }
  else{
    answer.push_back(nJetStr+"SRb9");
    if(nBJet == 0) {
      answer.push_back(nJetStr+"SRb0");
      if(nSoftJet == 0) answer.push_back(nJetStr+"s0SRb0");
      else answer.push_back(nJetStr+"s1SRb0");
    }
    else {
      answer.push_back(nJetStr+"SRb1");
      if(nSoftJet == 0) answer.push_back(nJetStr+"s0SRb1");
      else answer.push_back(nJetStr+"s1SRb1");
    }
    if( nSoftJet == 0) answer.push_back(nJetStr+"s0SRb9");
    else answer.push_back(nJetStr+"s1SRb9");
  }
  return answer;
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
    if( ptBin == -1 || etaBin == -1 ){ throw "Could not find pT or eta bin"; }
    return "templ_n"+to_string(min(2,nSubjets))+"_ptBin"+to_string(ptBin)+"_etaBin"+to_string(etaBin);
  }
  else{
    throw "Template type not found";
  }
}
