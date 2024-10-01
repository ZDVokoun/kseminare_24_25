#include <bits/stdc++.h>
#include <cmath>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int T;
  cin >> T;
  for (int I = 0; I < T; I++) {
    int n, vp, vn, vm;
    cin >> n >> vp >> vn >> vm;
    int px, py, pz;
    cin >> px >> py >> pz;
    int curv, dz, x, y, z;
    double res = 0;
    for (int i = 0; i < n - 1; i++) {
      cin >> x >> y >> z;
      dz = z - pz;
      if (dz > 0)
        curv = vp;
      else if (dz == 0)
        curv = vn;
      else
        curv = vm;
      res += sqrt(pow(x - px, 2) + pow(y - py, 2) + pow(z - pz, 2)) / curv;
      px = x;
      py = y;
      pz = z;
    }
    cout << res << endl;
  }

  return 0;
}
