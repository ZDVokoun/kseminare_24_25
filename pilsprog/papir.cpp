#include <bits/stdc++.h>
#include <climits>
#include <cstdint>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

signed main(signed argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int b, s, p;
  cin >> b >> s >> p;
  vector<vector<ll>> graph(b + 1, vector<ll>(b + 1, INT32_MAX));
  for (int i = 0; i < b + 1; i++)
    graph[i][i] = 0;

  for (int i = 0; i < s; i++) {
    ll b1, b2, c;
    cin >> b1 >> b2 >> c;
    graph[b1][b2] = c;
  }
  vector<int> pp(p);
  for (int i = 0; i < p; i++) {
    cin >> pp[i];
  }
  auto newgraph = graph;
  for (int k = 1; k < b + 1; k++) {
    newgraph = graph;
    for (int i = 1; i < b + 1; i++)
      for (int j = 1; j < b + 1; j++)
        newgraph[i][j] = min(graph[i][j], graph[i][k] + graph[k][j]);
    graph = newgraph;
  }

  int mn = -1;
  ll res = INT32_MAX;
  for (int i = 1; i < b + 1; i++) {
    ll sm = 0;
    for (int x : pp) {
      sm += graph[i][x];
      sm += graph[x][i];
    }
    if (sm <= res) {
      res = sm;
      mn = i;
    }
  }
  cout << mn << " " << res << endl;

  return 0;
}
