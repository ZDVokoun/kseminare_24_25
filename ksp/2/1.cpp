#include <bits/stdc++.h>
#include <queue>
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

  ll P, N, K;
  cin >> P >> N >> K;
  vll a(N), v(N), u(N);
  for (int i = 0; i < N; i++)
    cin >> a[i] >> v[i] >> u[i];
  vll cur(P + 1, -1), change(P + 1, -1);
  vector<vll> pred(K, vll(P + 1, -2));
  cur[1] = 0;
  for (int j = 0; j < K; j++) {
    for (int i = 0; i < N; i++) {
      if (cur[a[i]] == -1)
        continue;
      if (change[v[i]] < cur[a[i]] + u[i]) {
        change[v[i]] = cur[a[i]] + u[i];
        pred[j][v[i]] = i;
      }
    }
    for (int i = 1; i <= P; i++) {
      swap(cur[i], change[i]);
      change[i] = -1;
    }
  }
  vll bestpath;
  ll curv = 2;
  for (int i = K - 1; i >= 0; i--) {
    bestpath.push_back(pred[i][curv]);
    curv = a[pred[i][curv]];
  }

  for (int i = bestpath.size() - 1; i >= 0; i--)
    cout << bestpath[i] + 1 << endl;

  return 0;
}
