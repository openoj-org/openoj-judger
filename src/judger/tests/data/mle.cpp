#include<iostream>
using namespace std;


int main(int argc, char** argv) {
    // int big_cache[1024 * 1024];
    int* SegmentationFault;
    
    *SegmentationFault = 0;
    int n, a, b;
    cin >> n;
    while (n--) {
        cin >> a >> b;
        cout << a + b << endl;
    }
}