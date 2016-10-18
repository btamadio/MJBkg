#include "dresser.cxx"
#include <string>
#include <iostream>
using namespace std;
int main(int argc, char *argv[]){
  //argc = number of args+1
  //argv = [argc,arguments]
  if (argc < 6){
    cout<<"Not enough command line arguments."<<endl;
    cout<<"usage: RunDresser <miniTreeFileName> <templateFileName> <jobName> <templateType> <toyNum>"<<endl;
    return 0;
  }
  string miniTreeFileName = argv[1];
  string templateFileName = argv[2];
  string jobName = argv[3];
  int templateType = atoi(argv[4]);
  string toyNum = argv[5];
  MJ::dresser d;
  d.setMiniTreeFileName(miniTreeFileName);
  d.setTemplateFileName(templateFileName);
  d.setTemplateType(templateType);
  d.setOutFileName("output_dressed/"+jobName+"_"+toyNum+".root");
  d.setDelta(0.2);
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
