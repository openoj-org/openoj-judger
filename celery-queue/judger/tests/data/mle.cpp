#include<iostream>
using namespace std;


int main(int argc, char** argv) {
    // int big_cache[1024 * 1024];
    // int* SegmentationFault;
    // *SegmentationFault = 0;
    int* big_cache = new int[1024 * 1024];

    for (int i = 0; i < 1024 * 1024; ++i) {
        big_cache[i] = i;
    }
    int n, a, b;
    cin >> n;
    while (n--) {
        cin >> a >> b;
        cout << a + b << endl;
    }
    delete[] big_cache;
}