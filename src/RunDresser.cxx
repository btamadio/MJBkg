#include "dresser.cxx"
#include <string>
#include <iostream>

using namespace std;
int main(int argc, char *argv[]){
  if (argc < 6){
    cout<<"Not enough command line arguments."<<endl;
    cout<<"usage: RunDresser <miniTreeFileName> <templateFileName> <jobName> <templateType> <toyNum> [signal to inject] [signal lumi] [MJcut to blind]"<<endl;
    return 0;
  }
  string miniTreeFileName = argv[1];
  string templateFileName = argv[2];
  string jobName = argv[3];
  int templateType = atoi(argv[4]);
  string toyNum = argv[5];
  float MJcut = 0;
  int signalNum = 0;
  float signalLumi = 0.0;
  if(argc > 6){
    if(argc < 8){
      cout<<"Must provide signal number and signal lumi"<<endl;
      exit(1);
    }
    signalNum = atoi(argv[6]);
    signalLumi = stof(argv[7]);
  }
  if (argc > 8){
    MJcut = (float)atoi(argv[8]) / 1000.0;
  }
  MJ::dresser d;
  d.setMiniTreeFileName(miniTreeFileName);
  d.setTemplateFileName(templateFileName);
  d.setTemplateType(templateType);
  string outFileName = "/project/projectdirs/atlas/btamadio/RPV_SUSY/MJBkg/output_dressed/"+jobName+"/"+jobName+"_"+toyNum+".root";
  d.setOutFileName(outFileName);
  if (MJcut > 0){ 
    d.blind(MJcut); 
    cout<<"Blinding events with MJ > "<<MJcut<<" TeV"<<endl;
  }
  if (signalNum > 0){
    d.injectSignal(signalNum,signalLumi);
    cout<<"Injecting signal with DSID = "<<signalNum<<" scaled to luminosity "<<signalLumi<<endl;
  }
  try {
    cout<<"Loading file "<<miniTreeFileName<<endl;
    d.initialize();
  }catch( const char *msg ){
    cerr<<msg<<endl;
  }
  cout<<"File loaded"<<endl;
  try{
    d.loop();
  }catch( const char *msg){
    cerr<<msg<<endl;
  }
  
  return 0;
}
