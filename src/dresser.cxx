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
  b_jet_m_dressed_up = new vector<double>;
  b_jet_m_dressed_down = new vector<double>;

  m_outTree->Branch("jet_m_dressed_nom",&b_jet_m_dressed_nom);
  m_outTree->Branch("jet_m_dressed_up",&b_jet_m_dressed_up);
  m_outTree->Branch("jet_m_dressed_down",&b_jet_m_dressed_down);

  //Set pT and eta binning -> at some point change this to use config file instead
  if(m_templateType == 0){
    //pt/eta/b-match binning
    m_mass_corr_VR = {0.983362145257,0.984200169158,0.977797358721,0.975586979428,0.965202321645,0.971748206872,
		      0.967629836047,0.979667146605,1.00193059003,1.00949003403,1.00232763577,1.00610321852,
		      1.02012570449,1.02305972305,1.02047826149};
    m_mass_corr_SR = {0.93841504343,0.94891312853,0.959466634316,0.954854062213,0.956942093602,0.966843703694,
		      0.96797316068,1.00082622301,1.00404081975,1.01879979757,1.00896991546,0.999664340742,
		      1.03408107469,1.03983996364,1.03891668862};
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};
    m_deltas = {0.0371466145457,0.0154280783421,0.0160572721911,0.0240760491119,0.0299535602059,0.039231082425,
		0.00199592278433,-0.026907728043,-0.0320283666982,0.0069393626982,-0.0200608240752,0.011357223687,
		-0.0184557814035,0.00478771247814,0.0195624416068};
  }
  if(m_templateType == 1){
    //pt/BDT/b-match binning
    m_mass_corr_VR = {0.959685289567,0.957709608929,0.947837051562,0.940335033262,0.9322820971,0.933017654959,
		      0.928334743188,0.950262690972,0.996308204029,0.988455862098,0.998695106437,1.02482723224,
		      1.01294858582,0.987037064786,0.990726877637};
    m_mass_corr_SR = {0.923421968046,0.923686365314,0.935026497931,0.919090223557,0.929793760039,0.925617188694,
		      0.952878954078,0.984055586603,1.02224369428,1.04107465795,1.03994203767,1.02630570584,
		      1.03837595079,1.04730864121,1.02766402224};
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {-1.0,0.0,0.3,1.0};
    m_deltas = {0.0585043703441,0.043513427165,0.0491962013015,0.060436197281,0.0706835895406,0.0812131220089,
		0.0538541298782,-0.00377991353078,-0.0188052356295,0.014580446044,-0.0151503024595,0.0173123959725,
		-0.0126822261856,0.0234683678931,0.0461984329114};
  }
  if(m_templateType == 2){
    //ICHEP binning (soft jets + b-tag)
    m_mass_corr_VR = {0.980540972943,0.970721504435,0.960668549837,0.972736355391,1.00519312687,0.99959476931,
		      1.0087786744,1.01870688226};

    m_mass_corr_SR = {0.953294883664,0.950459331057,0.959022698708,0.979696945942,1.00168405958,1.01372029197,
		      1.004838362,0.995798837315};
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.244,0.293,0.364,0.445,0.52,0.6,0.733,0.896};
    m_ptBins5 = {0.2,0.244,0.293,0.364,0.445,0.52,0.6,0.733};
    m_yBins = {0,0.5,1.0,1.5,2.0};
    m_deltas = {0.0336980753354,0.0271277693625,0.0364305828916,0.00341274767482,-0.00456456660634,-0.0109712645649,
		-0.00055156675562,0.0324697574121};
  }
  if(m_templateType == 3){
    //pt/eta/qg-match binning
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};
    m_deltas = {0.0471695473558,0.0304516268889,0.0335215541859,0.0329496220836,0.0422938064581,0.0578954494051,
		0.0243979729581,-0.00405051313814,-0.0101216716535,0.013697267464,-0.0160694137165,0.0200395992595,
		-0.0142660184474,0.0125795539467,0.0216193438483};
  }
  if(m_templateType == 4){
    //pt/eta/n_subjet binning
    m_ptBins3 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins4 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_ptBins5 = {0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896};
    m_yBins = {0,0.5,1.0,1.5,2.0};
    m_deltas = {0.0170027553852,0.0100065136381,0.0124197901228,0.0266207036167,0.0199546560232,0.0195558821268,
		0.024030486192,-0.0269327037104,-0.0132908865516,0.00391776024267,-0.000315987815234,0.0231868794928,
		-0.00519994041148,0.0058088500764,0.0231153582394};
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
    m_hists_m_dressUp[m_regionNames.at(i)] = TH1F(("h_jetmass_dressUp_"+m_regionNames.at(i)).c_str(),("h_jetmass_dressUp_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m_dressDown[m_regionNames.at(i)] = TH1F(("h_jetmass_dressDown_"+m_regionNames.at(i)).c_str(),("h_jetmass_dressDown_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);


    m_hists_m1_kin[m_regionNames.at(i)] = TH1F(("h_jetmass1_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass1_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass1_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass1_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressUp[m_regionNames.at(i)] = TH1F(("h_jetmass1_dressUp_"+m_regionNames.at(i)).c_str(),("h_jetmass1_dressUp_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m1_dressDown[m_regionNames.at(i)] = TH1F(("h_jetmass1_dressDown_"+m_regionNames.at(i)).c_str(),("h_jetmass1_dressDown_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);

    m_hists_m2_kin[m_regionNames.at(i)] = TH1F(("h_jetmass2_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass2_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass2_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass2_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressUp[m_regionNames.at(i)] = TH1F(("h_jetmass2_dressUp_"+m_regionNames.at(i)).c_str(),("h_jetmass2_dressUp_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m2_dressDown[m_regionNames.at(i)] = TH1F(("h_jetmass2_dressDown_"+m_regionNames.at(i)).c_str(),("h_jetmass2_dressDown_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);

    xMax = 0.6;
    m_hists_m3_kin[m_regionNames.at(i)] = TH1F(("h_jetmass3_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass3_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass3_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass3_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressUp[m_regionNames.at(i)] = TH1F(("h_jetmass3_dressUp_"+m_regionNames.at(i)).c_str(),("h_jetmass3_dressUp_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m3_dressDown[m_regionNames.at(i)] = TH1F(("h_jetmass3_dressDown_"+m_regionNames.at(i)).c_str(),("h_jetmass3_dressDown_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);

    xMax = 0.4;
    m_hists_m4_kin[m_regionNames.at(i)] = TH1F(("h_jetmass4_kin_"+m_regionNames.at(i)).c_str(),("h_jetmass4_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressNom[m_regionNames.at(i)] = TH1F(("h_jetmass4_dressNom_"+m_regionNames.at(i)).c_str(),("h_jetmass4_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressUp[m_regionNames.at(i)] = TH1F(("h_jetmass4_dressUp_"+m_regionNames.at(i)).c_str(),("h_jetmass4_dressUp_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_m4_dressDown[m_regionNames.at(i)] = TH1F(("h_jetmass4_dressDown_"+m_regionNames.at(i)).c_str(),("h_jetmass4_dressDown_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    
    xMax = 2.0;
    m_hists_MJ_kin[m_regionNames.at(i)] = TH1F(("h_MJ_kin_"+m_regionNames.at(i)).c_str(),("h_MJ_kin_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressNom[m_regionNames.at(i)] = TH1F(("h_MJ_dressNom_"+m_regionNames.at(i)).c_str(),("h_MJ_dressNom_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressUp[m_regionNames.at(i)] = TH1F(("h_MJ_dressUp_"+m_regionNames.at(i)).c_str(),("h_MJ_dressUp_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
    m_hists_MJ_dressDown[m_regionNames.at(i)] = TH1F(("h_MJ_dressDown_"+m_regionNames.at(i)).c_str(),("h_MJ_dressDown_"+m_regionNames.at(i)).c_str(),nBins,xMin,xMax);
  }
}
void MJ::dresser::loop(){
  TTree *t = m_miniTree.fChain;
  int nEntries = t->GetEntries();
  //  nEntries = 100;
  cout<<"Looping over miniTree with "<<nEntries<<" entries"<<endl;
  for(unsigned int entry = 0; entry < nEntries; entry++){
    b_jet_m_dressed_nom->clear();
    b_jet_m_dressed_up->clear();
    b_jet_m_dressed_down->clear();

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
      float MJ_dressUp = 0;
      float MJ_dressDown = 0;
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
	vector<float> dressedMass = getDressedMass(templateHist,m_miniTree.jet_pt->at(i),m_miniTree.dEta,correct);
	MJ_dressNom += dressedMass.at(0);
	MJ_dressUp += dressedMass.at(1);
	MJ_dressDown += dressedMass.at(2);
	b_jet_m_dressed_nom->push_back(dressedMass.at(0));
	b_jet_m_dressed_up->push_back(dressedMass.at(1));
	b_jet_m_dressed_down->push_back(dressedMass.at(2));

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
	m_hists_m_dressUp.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	m_hists_m_dressUp.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	m_hists_m_dressUp.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressUp.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);

	m_hists_m_dressDown.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	m_hists_m_dressDown.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	m_hists_m_dressDown.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	m_hists_m_dressDown.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);

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

	  m_hists_m1_dressUp.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m1_dressUp.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m1_dressUp.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m1_dressUp.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);

	  m_hists_m1_dressDown.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m1_dressDown.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m1_dressDown.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m1_dressDown.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);

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
	  m_hists_m2_dressUp.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m2_dressUp.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m2_dressUp.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressUp.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressDown.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m2_dressDown.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m2_dressDown.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m2_dressDown.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
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

	  m_hists_m3_dressUp.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m3_dressUp.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m3_dressUp.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressUp.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);

	  m_hists_m3_dressDown.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m3_dressDown.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m3_dressDown.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m3_dressDown.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);

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

	  m_hists_m4_dressUp.at(regionName).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m4_dressUp.at(regionNameS).Fill(dressedMass.at(1),m_miniTree.weight);
	  m_hists_m4_dressUp.at(regionNameB).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressUp.at(regionNameM).Fill(dressedMass.at(1),m_miniTree.weight*m_miniTree.bSF_70);

	  m_hists_m4_dressDown.at(regionName).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m4_dressDown.at(regionNameS).Fill(dressedMass.at(2),m_miniTree.weight);
	  m_hists_m4_dressDown.at(regionNameB).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);
	  m_hists_m4_dressDown.at(regionNameM).Fill(dressedMass.at(2),m_miniTree.weight*m_miniTree.bSF_70);

	}
      }
      m_hists_MJ_kin.at(regionName).Fill(MJ_kin,m_miniTree.weight*unBlindEvent);
      m_hists_MJ_kin.at(regionNameS).Fill(MJ_kin,m_miniTree.weight*unBlindEvent);
      m_hists_MJ_kin.at(regionNameB).Fill(MJ_kin,m_miniTree.weight*m_miniTree.bSF_70*unBlindEvent);
      m_hists_MJ_dressNom.at(regionName).Fill(MJ_dressNom,m_miniTree.weight);
      m_hists_MJ_dressNom.at(regionNameS).Fill(MJ_dressNom,m_miniTree.weight);
      m_hists_MJ_dressNom.at(regionNameB).Fill(MJ_dressNom,m_miniTree.weight*m_miniTree.bSF_70);

      m_hists_MJ_dressUp.at(regionName).Fill(MJ_dressUp,m_miniTree.weight);
      m_hists_MJ_dressUp.at(regionNameS).Fill(MJ_dressUp,m_miniTree.weight);
      m_hists_MJ_dressUp.at(regionNameB).Fill(MJ_dressUp,m_miniTree.weight*m_miniTree.bSF_70);
      
      m_hists_MJ_dressDown.at(regionName).Fill(MJ_dressDown,m_miniTree.weight);
      m_hists_MJ_dressDown.at(regionNameS).Fill(MJ_dressDown,m_miniTree.weight);
      m_hists_MJ_dressDown.at(regionNameB).Fill(MJ_dressDown,m_miniTree.weight*m_miniTree.bSF_70);
    }
    m_outTree->Fill();
  }
  m_outFile->Write();
}
vector<float> MJ::dresser::getDressedMass(TH1F *h, float pt, float dEta, bool correct){
  int ptBin = -1;
  //need to know from which pT bin to get delta
  if(m_templateType==2){ ptBin= getTemplateBin(pt,0.0,4).first-1; }
  else{ ptBin = getTemplateBin(pt,0.0,3).first-1; }
  m_delta = m_deltas.at(ptBin);
  gRandom->SetSeed(0);
  vector<float> answer;
  float r0 = h->GetRandom();
  TRandom3 tRandom(0);
  //nominal dressed mass and shifted up and down masses
  answer.push_back( pt*exp(r0) );
  answer.push_back( pt*exp(r0)*(1+m_delta) );
  answer.push_back( pt*exp(r0)*(1-m_delta) );
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
