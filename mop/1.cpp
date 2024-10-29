#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'
#define MAX INT32_MAX

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;
typedef pair<ll, ll> pll;

void DFS(vector<vector<pll>> &graph, vbool &visited, ll u) {
  visited[u] = true;
  for (auto [v, w] : graph[u])
    if (!visited[v])
      DFS(graph, visited, v);
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll t, o;
  cin >> t >> o;
  vector<vector<pair<ll, ll>>> edge(t);
  vll indegree(t);
  ll u, v, c;
  for (ll i = 0; i < o; i++) {
    cin >> u >> v >> c;
    edge[u - 1].push_back({v - 1, -c});
    indegree[v - 1]++;
  }
  vll dist(t, MAX);
  vbool visited(t);
  for (ll i = 0; i < t; i++) {
    if (indegree[i] == 0) {
      dist[i] = 0;
      DFS(edge, visited, i);
    }
  }
  for (int u = 0; u < t; u++) {
    if (!visited[u]) {
      dist[u] = 0;
      DFS(edge, visited, u);
    }
  }

  vbool closed(t);
  bool updated = false;
  for (ll i = 1; i < t - 1; i++) {
    for (ll u = 0; u < t; u++) {
      if (dist[u] == MAX || closed[u])
        continue;
      for (pll e : edge[u]) {
        if (dist[e.first] > dist[u] + e.second) {
          updated = true;
          dist[e.first] = dist[u] + e.second;
          closed[e.first] = false;
        }
      }
      closed[u] = true;
    }
    if (!updated)
      break;
  }
  for (ll u = 0; u < t; u++) {
    if (!updated)
      break;
    if (dist[u] == MAX || closed[u])
      continue;
    for (pll e : edge[u]) {
      if (dist[e.first] > dist[u] + e.second) {
        cout << "nelze" << endl;
        return 0;
      }
    }
  }
  for (ll i = 0; i < t - 1; i++) {
    cout << dist[i] << " ";
  }
  cout << dist[t - 1] << endl;

  return 0;
}
