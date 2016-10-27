#define DRESSER_CXX
#include "dresser.h"
#include "TTree.h"
#include "miniTree.cxx"
#include "TRandom3.h"
#include <iostream>
using namespace std;
MJ::dresser::dresser(){
  m_MJcut = 0;
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
  b_jet_m_dressed_smear = new vector<double>;

  m_outTree->Branch("jet_m_dressed_nom",&b_jet_m_dressed_nom);
  m_outTree->Branch("jet_m_dressed_smear",&b_jet_m_dressed_smear);

  //Set pT and eta binning -> at some point change this to use config file instead
  if(m_templateType == 0){
    //pt/eta/b-match binning
    m_mass_corr_VR = {0.983362145257,0.984200169158,0.977797358721,0.975586979428,0.965202321645,0.971748206872,0.967629836047,0.979667146605,1.00193059003,1.00949003403,1.00232763577,1.00610321852,1.02012570449,1.02305972305,1.02047826149};
    m_mass_corr_SR = {0.93841504343,0.94891312853,0.959466634316,0.954854062213,0.956942093602,0.966843703694,0.96797316068,1.00082622301,1.00404081975,1.01879979757,1.00896991546,0.999664340742,1.03408107469,1.03983996364,1.03891668862};
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};
  }
  if(m_templateType == 1){
    //pt/BDT/b-match binning
    m_mass_corr_VR = {0.959685289567,0.957709608929,0.947837051562,0.940335033262,0.9322820971,0.933017654959,0.928334743188,0.950262690972,0.996308204029,0.988455862098,0.998695106437,1.02482723224,1.01294858582,0.987037064786,0.990726877637};
    m_mass_corr_SR = {0.923421968046,0.923686365314,0.935026497931,0.919090223557,0.929793760039,0.925617188694,0.952878954078,0.984055586603,1.02224369428,1.04107465795,1.03994203767,1.02630570584,1.03837595079,1.04730864121,1.02766402224};
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {-1.0,0.0,0.3,1.0};
  }
  if(m_templateType == 2){
    //ICHEP binning (soft jets + b-tag)
    m_mass_corr_VR = {0.980540972943,0.970721504435,0.960668549837,0.972736355391,1.00519312687,0.99959476931,1.0087786744,1.01870688226};
    m_mass_corr_SR = {0.953294883664,0.950459331057,0.959022698708,0.979696945942,1.00168405958,1.01372029197,1.004838362,0.995798837315};
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
  //Setup output histograms
  vector<string> regionNames = {"3jVRb0","3jVRb1","3jVRb9","3jVRbM","3jVRbU",
				"3jSRb0","3jSRb1","3jSRb9","3jSRbM","3jSRbU",
				"4jVRb0","4jVRb1","4jVRb9","4jVRbM","4jVRbU",
				"4jSRb0","4jSRb1","4jSRb9","4jSRbM","4jSRbU",
				"5jVRb0","5jVRb1","5jVRb9","5jVRbM","5jVRbU",
				"5jSRb0","5jSRb1","5jSRb9","5jSRbM","5jSRbU"};
  for (unsigned int i = 0; i < regionNames.size(); i++){
    vector<double> ptBins;
    if (regionNames.at(i).find("3j") != string::npos){ ptBins = m_ptBins3; }
    else if (regionNames.at(i).find("4j") != string::npos) { ptBins = m_ptBins4; }
    else if (regionNames.at(i).find("5j") != string::npos) { ptBins = m_ptBins5; }
    //Declare 1D profile hists with pt bins same as templates
    m_prof1d_kin[regionNames.at(i)] = TProfile(("h_prof1d_kin_"+regionNames.at(i)).c_str(),("h_prof1d_kin_"+regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_dressUp[regionNames.at(i)] = TProfile(("h_prof1d_dressUp_"+regionNames.at(i)).c_str(),("h_prof1d_dressUp_"+regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_dressNom[regionNames.at(i)] = TProfile(("h_prof1d_dressNom_"+regionNames.at(i)).c_str(),("h_prof1d_dressNom_"+regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());
    m_prof1d_dressDown[regionNames.at(i)] = TProfile(("h_prof1d_dressDown_"+regionNames.at(i)).c_str(),("h_prof1d_dressDown_"+regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data());

    //Declare 2D profile hists with 2d binning same as templates
    m_prof2d_kin[regionNames.at(i)] = TProfile2D(("h_prof2d_kin_"+regionNames.at(i)).c_str(),("h_prof2d_kin_"+regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data(),m_yBins.size()-1,m_yBins.data());
    m_prof2d_dressUp[regionNames.at(i)] = TProfile2D(("h_prof2d_dressUp_"+regionNames.at(i)).c_str(),("h_prof2d_dressUp_"+regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data(),m_yBins.size()-1,m_yBins.data());
    m_prof2d_dressNom[regionNames.at(i)] = TProfile2D(("h_prof2d_dressNom_"+regionNames.at(i)).c_str(),("h_prof2d_dressNom_"+regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data(),m_yBins.size()-1,m_yBins.data());
    m_prof2d_dressDown[regionNames.at(i)] = TProfile2D(("h_prof2d_dressDown_"+regionNames.at(i)).c_str(),("h_prof2d_dressDown_"+regionNames.at(i)).c_str(),ptBins.size()-1,ptBins.data(),m_yBins.size()-1,m_yBins.data());

    int nBins = 200;
    float xMin = 0;
    float xMax = 1.2;
    m_hists_m_kin[regionNames.at(i)] = TH1F(("h_jetmass_kin_"+regionNames.at(i)).c_str(),("h_jetmass_kin_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressNom[regionNames.at(i)] = TH1F(("h_jetmass_dressNom_"+regionNames.at(i)).c_str(),("h_jetmass_dressNom_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressUp[regionNames.at(i)] = TH1F(("h_jetmass_dressUp_"+regionNames.at(i)).c_str(),("h_jetmass_dressUp_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressDown[regionNames.at(i)] = TH1F(("h_jetmass_dressDown_"+regionNames.at(i)).c_str(),("h_jetmass_dressDown_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);


    m_hists_m1_kin[regionNames.at(i)] = TH1F(("h_jetmass1_kin_"+regionNames.at(i)).c_str(),("h_jetmass1_kin_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressNom[regionNames.at(i)] = TH1F(("h_jetmass1_dressNom_"+regionNames.at(i)).c_str(),("h_jetmass1_dressNom_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressUp[regionNames.at(i)] = TH1F(("h_jetmass1_dressUp_"+regionNames.at(i)).c_str(),("h_jetmass1_dressUp_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressDown[regionNames.at(i)] = TH1F(("h_jetmass1_dressDown_"+regionNames.at(i)).c_str(),("h_jetmass1_dressDown_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);

    m_hists_m2_kin[regionNames.at(i)] = TH1F(("h_jetmass2_kin_"+regionNames.at(i)).c_str(),("h_jetmass2_kin_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressNom[regionNames.at(i)] = TH1F(("h_jetmass2_dressNom_"+regionNames.at(i)).c_str(),("h_jetmass2_dressNom_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressUp[regionNames.at(i)] = TH1F(("h_jetmass2_dressUp_"+regionNames.at(i)).c_str(),("h_jetmass2_dressUp_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressDown[regionNames.at(i)] = TH1F(("h_jetmass2_dressDown_"+regionNames.at(i)).c_str(),("h_jetmass2_dressDown_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);

    xMax = 0.6;
    m_hists_m3_kin[regionNames.at(i)] = TH1F(("h_jetmass3_kin_"+regionNames.at(i)).c_str(),("h_jetmass3_kin_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressNom[regionNames.at(i)] = TH1F(("h_jetmass3_dressNom_"+regionNames.at(i)).c_str(),("h_jetmass3_dressNom_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressUp[regionNames.at(i)] = TH1F(("h_jetmass3_dressUp_"+regionNames.at(i)).c_str(),("h_jetmass3_dressUp_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressDown[regionNames.at(i)] = TH1F(("h_jetmass3_dressDown_"+regionNames.at(i)).c_str(),("h_jetmass3_dressDown_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);

    xMax = 0.4;
    m_hists_m4_kin[regionNames.at(i)] = TH1F(("h_jetmass4_kin_"+regionNames.at(i)).c_str(),("h_jetmass4_kin_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressNom[regionNames.at(i)] = TH1F(("h_jetmass4_dressNom_"+regionNames.at(i)).c_str(),("h_jetmass4_dressNom_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressUp[regionNames.at(i)] = TH1F(("h_jetmass4_dressUp_"+regionNames.at(i)).c_str(),("h_jetmass4_dressUp_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressDown[regionNames.at(i)] = TH1F(("h_jetmass4_dressDown_"+regionNames.at(i)).c_str(),("h_jetmass4_dressDown_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    
    xMax = 2.0;
    m_hists_MJ_kin[regionNames.at(i)] = TH1F(("h_MJ_kin_"+regionNames.at(i)).c_str(),("h_MJ_kin_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressNom[regionNames.at(i)] = TH1F(("h_MJ_dressNom_"+regionNames.at(i)).c_str(),("h_MJ_dressNom_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressUp[regionNames.at(i)] = TH1F(("h_MJ_dressUp_"+regionNames.at(i)).c_str(),("h_MJ_dressUp_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressDown[regionNames.at(i)] = TH1F(("h_MJ_dressDown_"+regionNames.at(i)).c_str(),("h_MJ_dressDown_"+regionNames.at(i)).c_str(),nBins,xMin,xMax);
  }
}
void MJ::dresser::loop(){
  TTree *t = m_miniTree.fChain;
  int nEntries = t->GetEntries();
  //  nEntries = 100;
  cout<<"Looping over miniTree with "<<nEntries<<" entries"<<endl;
  for(unsigned int entry = 0; entry < nEntries; entry++){
    b_jet_m_dressed_nom->clear();
    b_jet_m_dressed_smear->clear();

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
      float MJ_dressShift = 0;
      //regionName 0 based only on njet and dEta
      string regionName0 = getRegionName(m_miniTree.njet,m_miniTree.dEta);
      //b-inclusive region name
      string regionName=regionName0+"b9";
      //b-tag/b-veto region name
      string regionNameB = regionName0;
      if( m_miniTree.nbjet_Fix70 > 0 ) regionNameB += "b1"; 
      else regionNameB += "b0";
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
					     m_miniTree.BDTG,
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
	bool correct = true;
	if(m_miniTree.njet == 3){
	  correct = false;
	}
	pair<float,float> dressedMass = getDressedMass(templateHist,m_miniTree.jet_pt->at(i),m_miniTree.dEta, correct);
	MJ_dressNom += dressedMass.first;
	MJ_dressShift += dressedMass.second;
	b_jet_m_dressed_nom->push_back(dressedMass.first);
	b_jet_m_dressed_smear->push_back(dressedMass.second);

	//Fill inclusive hists for every jet
	m_hists_m_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	m_hists_m_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	m_hists_m_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);

	m_hists_m_dressNom.at(regionName).Fill(dressedMass.first,m_miniTree.weight);
	m_hists_m_dressNom.at(regionNameB).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressNom.at(regionNameM).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);

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
	m_prof1d_kin.at(regionNameB).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);
	m_prof1d_kin.at(regionNameM).Fill(xi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);
	m_prof2d_kin.at(regionName).Fill(xi,yi,m_miniTree.jet_m->at(i),m_miniTree.weight);
	m_prof2d_kin.at(regionNameB).Fill(xi,yi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);
	m_prof2d_kin.at(regionNameM).Fill(xi,yi,m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70);

	m_prof1d_dressNom.at(regionName).Fill(xi,dressedMass.first,m_miniTree.weight);
	m_prof1d_dressNom.at(regionNameB).Fill(xi,dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	m_prof1d_dressNom.at(regionNameM).Fill(xi,dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	m_prof2d_dressNom.at(regionName).Fill(xi,yi,dressedMass.first,m_miniTree.weight);
	m_prof2d_dressNom.at(regionNameB).Fill(xi,yi,dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	m_prof2d_dressNom.at(regionNameM).Fill(xi,yi,dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);

	if( dressedMass.second > dressedMass.first ){
	  m_hists_m_dressUp.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	  m_hists_m_dressUp.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m_dressUp.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof1d_dressUp.at(regionName).Fill(xi,dressedMass.second,m_miniTree.weight);
	  m_prof1d_dressUp.at(regionNameB).Fill(xi,dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof1d_dressUp.at(regionNameM).Fill(xi,dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof2d_dressUp.at(regionName).Fill(xi,yi,dressedMass.second,m_miniTree.weight);
	  m_prof2d_dressUp.at(regionNameB).Fill(xi,yi,dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof2d_dressUp.at(regionNameM).Fill(xi,yi,dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);

	}
	else{
	  m_hists_m_dressDown.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	  m_hists_m_dressDown.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m_dressDown.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof1d_dressDown.at(regionName).Fill(xi,dressedMass.second,m_miniTree.weight);
	  m_prof1d_dressDown.at(regionNameB).Fill(xi,dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof1d_dressDown.at(regionNameM).Fill(xi,dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof2d_dressDown.at(regionName).Fill(xi,yi,dressedMass.second,m_miniTree.weight);
	  m_prof2d_dressDown.at(regionNameB).Fill(xi,yi,dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  m_prof2d_dressDown.at(regionNameM).Fill(xi,yi,dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	}
	//Fill exclusive hists based on jet pT order
	if (i==0){ 
	  m_hists_m1_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m1_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m1_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m1_dressNom.at(regionName).Fill(dressedMass.first,m_miniTree.weight);
	  m_hists_m1_dressNom.at(regionNameB).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m1_dressNom.at(regionNameM).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	  if(dressedMass.second > dressedMass.first){
	    m_hists_m1_dressUp.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	    m_hists_m1_dressUp.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	    m_hists_m1_dressUp.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  }
	  else{
	    m_hists_m1_dressDown.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	    m_hists_m1_dressDown.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	    m_hists_m1_dressDown.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  }
	}
	if (i==1){ 
	  m_hists_m2_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m2_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m2_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m2_dressNom.at(regionName).Fill(dressedMass.first,m_miniTree.weight);
	  m_hists_m2_dressNom.at(regionNameB).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressNom.at(regionNameM).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	  if(dressedMass.second > dressedMass.first){
	    m_hists_m2_dressUp.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	    m_hists_m2_dressUp.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	    m_hists_m2_dressUp.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  }
	  else{
	    m_hists_m2_dressDown.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	    m_hists_m2_dressDown.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	    m_hists_m2_dressDown.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  }
	}
	if (i==2){ 
	  m_hists_m3_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m3_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m3_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m3_dressNom.at(regionName).Fill(dressedMass.first,m_miniTree.weight);
	  m_hists_m3_dressNom.at(regionNameB).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressNom.at(regionNameM).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	  if(dressedMass.second > dressedMass.first){
	    m_hists_m3_dressUp.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	    m_hists_m3_dressUp.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	    m_hists_m3_dressUp.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  }
	  else{
	    m_hists_m3_dressDown.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	    m_hists_m3_dressDown.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	    m_hists_m3_dressDown.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  }
	}
	if (i==3){ 
	  m_hists_m4_kin.at(regionName).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*unBlindEvent);
	  m_hists_m4_kin.at(regionNameB).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m4_kin.at(regionNameM).Fill(m_miniTree.jet_m->at(i),m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
	  m_hists_m4_dressNom.at(regionName).Fill(dressedMass.first,m_miniTree.weight);
	  m_hists_m4_dressNom.at(regionNameB).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressNom.at(regionNameM).Fill(dressedMass.first,m_miniTree.weight*m_miniTree.bSF_70);
	  if(dressedMass.second > dressedMass.first){
	    m_hists_m4_dressUp.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	    m_hists_m4_dressUp.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	    m_hists_m4_dressUp.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  }
	  else{
	    m_hists_m4_dressDown.at(regionName).Fill(dressedMass.second,m_miniTree.weight);
	    m_hists_m4_dressDown.at(regionNameB).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	    m_hists_m4_dressDown.at(regionNameM).Fill(dressedMass.second,m_miniTree.weight*m_miniTree.bSF_70);
	  }
	}
      }
      //      cout<<"MJ_kin = "<<MJ_kin<<"\t MJ_dressNom = "<<MJ_dressNom<<"\t MJ_dressShift = "<<MJ_dressShift<<endl;
      m_hists_MJ_kin.at(regionName).Fill(MJ_kin,m_miniTree.weight*unBlindEvent);
      m_hists_MJ_kin.at(regionNameB).Fill(MJ_kin,m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
      m_hists_MJ_dressNom.at(regionName).Fill(MJ_dressNom,m_miniTree.weight);
      m_hists_MJ_dressNom.at(regionNameB).Fill(MJ_dressNom,m_miniTree.weight*m_miniTree.bSF_70);
      if( MJ_dressShift > MJ_dressNom){
	m_hists_MJ_dressUp.at(regionName).Fill(MJ_dressShift,m_miniTree.weight);
	m_hists_MJ_dressUp.at(regionNameB).Fill(MJ_dressShift,m_miniTree.weight*m_miniTree.bSF_70);
      }
      else{
	m_hists_MJ_dressDown.at(regionName).Fill(MJ_dressShift,m_miniTree.weight);
	m_hists_MJ_dressDown.at(regionNameB).Fill(MJ_dressShift,m_miniTree.weight*m_miniTree.bSF_70);
      }

    }
    m_outTree->Fill();
  }
  m_outFile->Write();
}
pair<float,float> MJ::dresser::getDressedMass(TH1F *h, float pt, float dEta, bool correct){
  pair<int,int> bins;
  if(m_templateType==2){
    string histName = string(h->GetName());
    if(histName.find("njet3") != string::npos){
      bins = getTemplateBin(pt,0.0,3);
    }
    else if(histName.find("njet4") != string::npos){
      bins = getTemplateBin(pt,0.0,4);
    }
    else if(histName.find("njet5") != string::npos){
      bins = getTemplateBin(pt,0.0,5);
    }
    else{
      cout<<"Bin Not found!"<<endl;
      exit(1);
    }
  }
  else{
    bins = getTemplateBin(pt,0.0,3);
  }
  int ptBin = bins.first;
  float massCorr = 1;
  if (m_doCorrections and correct){
    if(dEta < 1.4){
      massCorr = m_mass_corr_SR.at(ptBin-1);
    }
    else{
      massCorr = m_mass_corr_VR.at(ptBin-1);
    }
  }
  gRandom->SetSeed(0);
  pair<float,float> answer;
  float r0 = h->GetRandom();
  TRandom3 tRandom(0);
  float r1 = tRandom.Gaus(0,m_delta);
  answer.first = pt*exp(r0)*massCorr;
  answer.second = pt*exp(r0)*(1+r1)*massCorr;
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
    if( qMatch == 1){
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
