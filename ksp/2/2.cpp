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

  int R, S;
  cin >> R >> S;
  vector<vll> graph(R, vll(S));
  for (int i = 0; i < R; i++)
    for (int j = 0; j < S; j++)
      cin >> graph[i][j];
  vector<vll> prevgraph = graph;

  vector<vbool> visited(R, vbool(S));
  queue<pint> bordering;
  for (int i = 0; i < R; i++) {
    bordering.push({i, 0});
    bordering.push({i, S - 1});
    visited[i][0] = true;
    visited[i][S - 1] = true;
  }
  for (int i = 0; i < S; i++) {
    bordering.push({0, i});
    bordering.push({R - 1, i});
    visited[0][i] = true;
    visited[R - 1][i] = true;
  }
  while (true) {
    queue<pint> q(bordering);
    bordering = {};
    vector<pint> neigh = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
    pint cur;
    while (!q.empty()) {
      cur = q.front();
      q.pop();
      // if (visited[cur.first][cur.second])
      //   continue;
      visited[cur.first][cur.second] = true;
      for (auto [di, dj] : neigh) {
        ll newi = cur.first + di;
        ll newj = cur.second + dj;
        if (newi < 0 || newi > R - 1 || newj < 0 || newj > R - 1)
          continue;
        if (visited[newi][newj])
          continue;
        if (graph[newi][newj] >= graph[cur.first][cur.second])
          q.push({newi, newj});
      }
    }
    vector<vll> components(R, vll(S, -1));
    vll values;
    ll k = 0;
    bool con = false;
    for (int i = 0; i < R; i++)
      for (int j = 0; j < S; j++) {
        if (visited[i][j])
          continue;
        con = true;
        q.push({i, j});
        values.push_back(INT64_MAX);
        while (!q.empty()) {
          cur = q.front();
          q.pop();
          if (components[cur.first][cur.second] != -1)
            continue;
          components[cur.first][cur.second] = k;
          for (auto [di, dj] : neigh) {
            ll newi = cur.first + di;
            ll newj = cur.second + dj;
            if (visited[newi][newj]) {
              values[k] = min(values[k], graph[newi][newj]);
              bordering.push({newi, newj});
            } else {
              q.push({newi, newj});
            }
          }
        }
        k++;
      }
    if (!con)
      break;
    for (int i = 0; i < R; i++)
      for (int j = 0; j < S; j++)
        if (components[i][j] != -1)
          graph[i][j] = max(values[components[i][j]], graph[i][j]);
  }
  ll res = 0;
  for (int i = 0; i < R; i++)
    for (int j = 0; j < S; j++)
      res += graph[i][j] - prevgraph[i][j];
  cout << res << endl;

  return 0;
}
