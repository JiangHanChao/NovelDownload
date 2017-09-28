#include<iostream>
#include<fstream>
#include<string>
using namespace std;

int main()
{
	ifstream fs;
	ofstream fp;
	string temp;
	fs.open("ipAgency.txt");
	fp.open("ip.txt");
	while(!fs.eof()){
		getline(fs,temp);
		fp<<temp<<" ";
	}
	fs.close();
	fp.close();
	return 0;
}
