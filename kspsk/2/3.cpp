#include <bits/stdc++.h>
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

  ll n, p, t;
  cin >> n >> t >> p;
  vll v(n), s(n);
  for (int i = 0; i < n; i++)
    cin >> s[i] >> v[i];
  ll res = 0;
  ll succ = 0;
  ll not_succ = 0;
  for (int i = 0; i < n; i++) {
    if (succ >= p)
      break;
    ll time_to_arrive = ceil(double(s[i]) / double(v[i]));
    if (time_to_arrive > t)
      not_succ++;
    else {
      succ++;
      res += not_succ;
    }
  }
  if (succ < p)
    cout << -1 << endl;
  else
    cout << res << endl;

  return 0;
}
