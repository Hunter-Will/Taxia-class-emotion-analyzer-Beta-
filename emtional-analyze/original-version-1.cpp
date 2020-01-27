#include<iostream>
#include<cstdio>
#include<map>
#include<string>
#include<fstream>
#include<vector>

using namespace std;

#define maxn 5000
#define maxl 5000
#define PATH1 "../data/dic-content"
#define PATH2 "../data/emtional-words-dictionary"
int n,tot;
map<string,int>mp;
string str[maxl+10],num[100];

struct word{
    string cont;
    vector<int> evct;
}dic[maxn+10];
/*
vector<int> operator + (const word &a,const word &b){
    vector<int> c;
    for(int i=1;i<=n;i++)
	c[i]=a.evct[i]+b.evct[i];
    return c;
}
*/
vector<int> operator + (const vector<int> &a,const word &b){
    vector<int> c;
    c.resize(n+1);
    for(int i=1;i<=n;i++)
	c[i]=a[i]+b.evct[i];
    return c; 
}
/*
vector<int> operator + (const word &b,const vector<int> &a){
    vector<int> c;
    for(int i=1;i<=n;i++)
	c[i]=a[i]+b.evct[i];
    return c; 
}
*/
void init(){
    ifstream ifs(PATH1);
    for(n=1;!ifs.eof();n++){
	ifs>>num[n];
	if(num[n][0]=='$'){n--;break;}
    }
    ifs.close();
    /*cout<<n<<endl;
    for(int i=1;i<=n;i++)
    cout<<num[i]<<endl;*/
}

void ReadDic(){
    mp.clear();
    ifstream ifs(PATH2);
    for(int i=1;i<=maxn&&!ifs.eof();i++){
        ifs>>dic[i].cont;
	if(dic[i].cont[0]=='#')break;
	//cout<<dic[i].cont<<endl;
	dic[i].evct.resize(n+1);
	for(int j=1;j<=n;j++)
	    ifs>>dic[i].evct[j];
	mp[dic[i].cont]=i;
    }
    ifs.close();
}

int main(){
    int tmp;
    string wd;
    vector<int> ans;
    init();
    ReadDic();
    ans.resize(n+1);
    for(int i=1;i<=n;i++)ans[i]=0;
    for(int i=1;!cin.eof();i++){
	cin>>wd;
	if(wd[0]=='$')break;
	tmp=mp[wd];
	if(tmp)
	    ans=ans+dic[tmp];
    }
    for(int i=1;i<=n;i++)
	cout<<ans[i]<<' ';
    cout<<endl;
    return 0;
}
