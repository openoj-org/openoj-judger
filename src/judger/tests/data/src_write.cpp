#include<iostream>
#include<fstream>
using namespace std;


int main(int argc, char** argv) {
    int n, a, b;
    cin >> n;
    ofstream fout("my_out.txt");
    fout << "This message should not be successfully written to the file";
    fout.close();
    while (n--) {
        cin >> a >> b;
        cout << a + b << endl;
    }
}