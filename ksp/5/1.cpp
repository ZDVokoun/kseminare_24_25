#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

bool dfs(string v, map<string, set<string>> &graph, vector<string> &res,
         map<string, bool> &visited) {
  visited[v] = true;
  if (v == "BOBER") {
    res.push_back("BOBER");
    return true;
  }
  for (string u : graph[v]) {
    if (!visited[u] && dfs(u, graph, res, visited)) {
      res.push_back(v);
      return true;
    }
  }
  return false;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int M;
  cin >> M;
  cin.ignore();
  map<string, set<string>> graph;
  map<string, bool> visited;
  for (int i = 0; i < M; i++) {
    string line;
    getline(cin, line);
    size_t dashPos = line.find('-');

    string fst = line.substr(0, dashPos);
    string scnd = line.substr(dashPos + 1);

    graph[fst].insert(scnd);
    graph[scnd].insert(fst);
    visited[fst] = false;
    visited[scnd] = false;
  }

  vector<string> res;
  dfs("ALICE", graph, res, visited);

  for (int i = res.size() - 1; i > 0; i--)
    cout << res[i] << "->";
  cout << res[0] << endl;

  return 0;
}
