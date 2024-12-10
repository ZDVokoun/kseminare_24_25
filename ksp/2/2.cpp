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
  visited[0][0] = true;
  visited[0][S - 1] = true;
  visited[R - 1][0] = true;
  visited[R - 1][S - 1] = true;

  priority_queue<pair<ll, pint>, vector<pair<ll, pint>>,
                 greater<pair<ll, pint>>>
      bordering;
  for (int i = 1; i < R - 1; i++) {
    bordering.push({graph[i][0], {i, 0}});
    bordering.push({graph[i][S - 1], {i, S - 1}});
    visited[i][0] = true;
    visited[i][S - 1] = true;
  }
  for (int i = 1; i < S - 1; i++) {
    bordering.push({graph[0][i], {0, i}});
    bordering.push({graph[R - 1][i], {R - 1, i}});
    visited[0][i] = true;
    visited[R - 1][i] = true;
  }
  ll res = 0;

  while (!bordering.empty()) {
    auto cr = bordering.top();
    bordering.pop();
    // if (visited[cr.second.first][cr.second.second])
    //   continue;
    pint cur;
    queue<pint> q;
    q.push(cr.second);
    ll height = cr.first;
    vector<pint> neigh = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
    while (!q.empty()) {
      cur = q.front();
      q.pop();
      res += height - graph[cur.first][cur.second];
      visited[cur.first][cur.second] = true;
      for (auto [di, dj] : neigh) {
        ll newi = cur.first + di;
        ll newj = cur.second + dj;
        if (newi < 0 || newi > R - 1 || newj < 0 || newj > S - 1)
          continue;
        if (visited[newi][newj])
          continue;
        if (graph[newi][newj] <= height) {
          q.push({newi, newj});
          res += height - graph[newi][newj];
          graph[newi][newj] = height;
        } else {
          bordering.push({graph[newi][newj], {newi, newj}});
        }
        visited[newi][newj] = true;
      }
    }
  }

  cout << res << endl;

  return 0;
}
