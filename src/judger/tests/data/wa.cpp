#include<iostream>
using namespace std;


int main(int argc, char** argv) {
    int n, a, b;
    cin >> n;
    while (n--) {
        cin >> a >> b;
        cout << a + b + 1 << endl;
    }
}