#include "testlib.h"

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    int n = inf.readInt();
    for (int i = 0; i < n; ++i) {
        if (ouf.readInt() != ans.readInt()) {
            quitf(_wa, "Wrong Answer");
        }
    }
    quitf(_ok, "Accepted");
}