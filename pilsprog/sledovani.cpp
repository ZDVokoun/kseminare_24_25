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

  int s;
  cin >> s;
  vector<pint> sensors(s);
  for (int i = 0; i < s; i++) {
    cin >> sensors[i].first >> sensors[i].second;
  }
  int u;
  cin >> u;
  for (int i = 0; i < u; i++) {
    vector<double> vals(s);
    for (int j = 0; j < s; j++)
      cin >> vals[j];
    double x1 = sensors[0].first, x2 = sensors[1].first, x3 = sensors[2].first,
           x4 = sensors[3].first, y1 = sensors[0].second,
           y2 = sensors[1].second, y3 = sensors[2].second,
           y4 = sensors[3].second;
    double t1 = vals[0], t2 = vals[1], t3 = vals[2], t4 = vals[3];
    double x =
        0.5 *
        ((t4 * y3 - t3 * y4) * t1 * t1 +
         (t1 * (y3 - y4) - t4 * y3 + t3 * y4) * t2 * t2 +
         (t2 * (y3 - y4) - t4 * y3 + t3 * y4) * x1 * x1 -
         (t1 * (y3 - y4) - t4 * y3 + t3 * y4) * x2 * x2 +
         (t2 * (y3 - y4) - t4 * y3 + t3 * y4) * y1 * y1 +
         ((t3 - t4) * y1 - t1 * (y3 - y4) + t4 * y3 - t3 * y4) * y2 * y2 +
         (t3 * t3 * y4 - x3 * x3 * y4 - y3 * y3 * y4 -
          (t4 * t4 - x4 * x4 - y4 * y4) * y3) *
             t1 -
         (t1 * t1 * (y3 - y4) + t3 * t3 * y4 - x3 * x3 * y4 - y3 * y3 * y4 -
          (t4 * t4 - x4 * x4 - y4 * y4) * y3) *
             t2 -
         (t2 * t2 * (t3 - t4) + t3 * t3 * t4 - (t3 - t4) * x2 * x2 -
          t4 * x3 * x3 - t4 * y3 * y3 -
          (t3 * t3 - t4 * t4 - x3 * x3 + x4 * x4 - y3 * y3 + y4 * y4) * t2 -
          (t4 * t4 - x4 * x4 - y4 * y4) * t3) *
             y1 +
         (t1 * t1 * (t3 - t4) + t3 * t3 * t4 - (t3 - t4) * x1 * x1 -
          t4 * x3 * x3 - (t3 - t4) * y1 * y1 - t4 * y3 * y3 -
          (t3 * t3 - t4 * t4 - x3 * x3 + x4 * x4 - y3 * y3 + y4 * y4) * t1 -
          (t4 * t4 - x4 * x4 - y4 * y4) * t3) *
             y2) /
        ((x4 * y3 - x3 * y4) * t1 - (x4 * y3 - x3 * y4) * t2 +
         (t2 * (y3 - y4) - t4 * y3 + t3 * y4) * x1 -
         (t1 * (y3 - y4) - t4 * y3 + t3 * y4) * x2 +
         ((t3 - t4) * x2 - t2 * (x3 - x4) + t4 * x3 - t3 * x4) * y1 -
         ((t3 - t4) * x1 - t1 * (x3 - x4) + t4 * x3 - t3 * x4) * y2);
    double y =
        -0.5 *
        ((t4 * x3 - t3 * x4) * t1 * t1 +
         (t1 * (x3 - x4) - t4 * x3 + t3 * x4) * t2 * t2 +
         (t2 * (x3 - x4) - t4 * x3 + t3 * x4) * x1 * x1 +
         ((t3 - t4) * x1 - t1 * (x3 - x4) + t4 * x3 - t3 * x4) * x2 * x2 -
         ((t3 - t4) * x2 - t2 * (x3 - x4) + t4 * x3 - t3 * x4) * y1 * y1 +
         ((t3 - t4) * x1 - t1 * (x3 - x4) + t4 * x3 - t3 * x4) * y2 * y2 +
         (t3 * t3 * x4 - x3 * x3 * x4 - x4 * y3 * y3 -
          (t4 * t4 - x4 * x4 - y4 * y4) * x3) *
             t1 -
         (t1 * t1 * (x3 - x4) + t3 * t3 * x4 - x3 * x3 * x4 - x4 * y3 * y3 -
          (t4 * t4 - x4 * x4 - y4 * y4) * x3) *
             t2 -
         (t2 * t2 * (t3 - t4) + t3 * t3 * t4 - t4 * x3 * x3 - t4 * y3 * y3 -
          (t3 * t3 - t4 * t4 - x3 * x3 + x4 * x4 - y3 * y3 + y4 * y4) * t2 -
          (t4 * t4 - x4 * x4 - y4 * y4) * t3) *
             x1 +
         (t1 * t1 * (t3 - t4) + t3 * t3 * t4 - (t3 - t4) * x1 * x1 -
          t4 * x3 * x3 - t4 * y3 * y3 -
          (t3 * t3 - t4 * t4 - x3 * x3 + x4 * x4 - y3 * y3 + y4 * y4) * t1 -
          (t4 * t4 - x4 * x4 - y4 * y4) * t3) *
             x2) /
        ((x4 * y3 - x3 * y4) * t1 - (x4 * y3 - x3 * y4) * t2 +
         (t2 * (y3 - y4) - t4 * y3 + t3 * y4) * x1 -
         (t1 * (y3 - y4) - t4 * y3 + t3 * y4) * x2 +
         ((t3 - t4) * x2 - t2 * (x3 - x4) + t4 * x3 - t3 * x4) * y1 -
         ((t3 - t4) * x1 - t1 * (x3 - x4) + t4 * x3 - t3 * x4) * y2);
    cout << round(x) << " " << round(y) << endl;
  }

  return 0;
}
