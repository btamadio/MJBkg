#include "dresser.cxx"
#include <string>
#include <iostream>
using namespace std;
int main(int argc, char *argv[]){
  //argc = number of args+1
  //argv = [argc,arguments]
  if (argc < 6){
    cout<<"Not enough command line arguments."<<endl;
    cout<<"usage: RunDresser <miniTreeFileName> <templateFileName> <jobName> <templateType> <toyNum> [MJcut to blind]"<<endl;
    return 0;
  }
  string miniTreeFileName = argv[1];
  string templateFileName = argv[2];
  string jobName = argv[3];
  int templateType = atoi(argv[4]);
  //  bool blinded = atoi(argv[5]);
  string toyNum = argv[5];
  float MJcut = 0;
  if (argc > 6){
    MJcut = (float)atoi(argv[6]) / 1000.0;
  }
  MJ::dresser d;
  d.setMiniTreeFileName(miniTreeFileName);
  d.setTemplateFileName(templateFileName);
  d.setTemplateType(templateType);
  string outFileName = "/project/projectdirs/atlas/btamadio/RPV_SUSY/MJBkg/output_dressed/"+jobName+"/"+jobName+"_"+toyNum+".root";
  d.setOutFileName(outFileName);
  d.setDelta(0.05);
  if (MJcut > 0){ d.blind(MJcut); }
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
