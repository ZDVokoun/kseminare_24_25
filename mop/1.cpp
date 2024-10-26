#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

vector<int> topologicalSort(vector<vector<int>> &adj, int V) {
  vector<int> indegree(V);
  for (int i = 0; i < V; i++) {
    for (auto it : adj[i]) {
      indegree[it]++;
    }
  }

  queue<int> q;
  for (int i = 0; i < V; i++) {
    if (indegree[i] == 0) {
      q.push(i);
    }
  }
  vbool visited(V);
  vector<int> result;
  if (q.empty())
    q.push(0);
  while (!q.empty()) {
    int node = q.front();
    q.pop();
    result.push_back(node);
    visited[node] = true;

    for (auto it : adj[node]) {
      if (visited[it])
        continue;
      indegree[it]--;

      if (indegree[it] == 0)
        q.push(it);
    }
  }

  return result;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll t, o;
  cin >> t >> o;
  vector<list<pair<ll, ll>>> outedge(t);
  vector<list<pair<ll, ll>>> inedge(t);
  ll u, v, c;
  for (ll i = 0; i < o; i++) {
    cin >> u >> v >> c;
    inedge[u - 1].push_back({v - 1, c});
    outedge[v - 1].push_back({u - 1, c});
  }
  vbool visited(t);
  set<pair<ll, ll>> visited_inedge;
  set<pair<ll, ll>> visited_outedge;
  queue<ll> q;
  vll values(t);
  vbool hasvalue(t);
  // for (ll u = 0; u < t; u++)
  //   if (outedge[u].size() == 0) {
  //     q.push(u);
  //     hasvalue[u] = true;
  //     visited[u] = true;
  //   }
  if (q.empty()) {
    q.push(0);
    hasvalue[0] = true;
    visited[0] = true;
  }
  while (!q.empty()) {
    ll cur = q.front();
    q.pop();
    for (auto p : inedge[cur]) {
      if (visited_inedge.find({cur, p.first}) != visited_inedge.end())
        continue;
      if (hasvalue[p.first])
        values[p.first] = min(values[p.first], values[cur] - p.second);
      else {
        values[p.first] = values[cur] - p.second;
        hasvalue[p.first] = true;
      }
      if (!visited[p.first]) {
        q.push(p.first);
        visited[p.first] = true;
      }
      visited_inedge.insert({cur, p.first});
      visited_outedge.insert({p.first, cur});
    }
    for (auto p : outedge[cur]) {
      if (visited_outedge.find({cur, p.first}) != visited_outedge.end())
        continue;
      if (hasvalue[p.first])
        values[p.first] = max(values[p.first], values[cur] + p.second);
      else {
        values[p.first] = values[cur] + p.second;
        hasvalue[p.first] = true;
      }
      if (!visited[p.first]) {
        q.push(p.first);
        visited[p.first] = true;
      }
      visited_outedge.insert({cur, p.first});
      visited_inedge.insert({p.first, cur});
    }
  }
  for (ll u = 0; u < t; u++) {
    for (auto p : inedge[u]) {
      if (values[u] < values[p.first] + p.second) {
        cout << "nelze" << endl;
        return 0;
      }
    }
  }
  for (ll i = 0; i < t - 1; i++)
    cout << values[i] << " ";

  cout << values[t - 1] << endl;

  return 0;
}
