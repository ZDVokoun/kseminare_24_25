#include <bits/stdc++.h>
#include <cstdint>
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

  int N;
  cin >> N;
  vector<ll> state(N + 1, INT64_MIN);
  state[0] = 0;
  ll mx = 0;
  for (int i = 0; i < N; i++) {
    char X;
    int t, c;
    cin >> X >> t >> c;
    if (X == 'N') {
      state[t] = max(state[t], state[0] - c);
      mx = max(mx, state[t]);
    } else {
      state[0] = max(state[0], state[t] + c);
      mx = max(mx, state[0]);
    }
  }
  cout << mx << endl;

  return 0;
}
