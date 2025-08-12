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

  int N;
  cin >> N;
  vector<vector<int>> table(N, vector<int>(N));
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      cin >> table[i][j];
    }
  }
  vector<map<int, int>> degree(N);
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      if (i == j)
        continue;
      degree[i][table[i][j]]++;
    }
  }
  bool run = true;
  vector<pint> edges;
  while (run) {
    run = false;
    for (int i = 0; i < N; i++) {
      if (degree[i].size() == 1) {
        degree[i].clear();
        run = true;
        for (int j = 0; j < N; j++) {
          if (degree[j].find(table[j][i]) == degree[j].end())
            continue;
          degree[j][table[j][i]]--;
          if (degree[j][table[j][i]] == 0) {
            degree[j].erase(table[j][i]);
            edges.push_back({i + 1, j + 1});
          }
        }
        break;
      }
    }
  }
  for (pint p : edges) {
    cout << p.first << " " << p.second << endl;
  }

  return 0;
}
