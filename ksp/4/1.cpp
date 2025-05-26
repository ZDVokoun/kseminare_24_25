#include <bits/stdc++.h>
#include <queue>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vb;
typedef pair<int, int> pint;

struct QItem {
  ll v;
  ll l;
  vint path;
  ll prev;
  bool operator<(const QItem &a) const { return l > a.l; };
};

void printVec(vint &vec) {
  for (int i = 0; i < vec.size() - 1; i++)
    cout << vec[i] << " ";
  cout << vec[vec.size() - 1] << endl;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll N, M, D;
  cin >> N >> M >> D;
  vector<vector<pint>> graph(N);
  vector<vb> visited(N, vb(N));
  for (int i = 0; i < M; i++) {
    int u, v, l;
    cin >> u >> v >> l;
    graph[u].push_back({l, v});
    graph[v].push_back({l, u});
  }
  priority_queue<QItem> q;
  q.push({D, 0, {int(D)}, D});
  bool starts = true;
  while (!q.empty()) {
    QItem cur = q.top();
    // cout << cur.v << endl;
    q.pop();
    if (!starts && cur.v == D) {
      cout << cur.path.size() << endl;
      printVec(cur.path);
      break;
    }
    starts = false;
    for (pint n : graph[cur.v]) {
      if (n.second != cur.prev && !visited[cur.v][n.second]) {
        visited[cur.v][n.second] = true;
        vint newPath = cur.path;
        newPath.push_back(n.second);
        q.push({n.second, cur.l + n.first, newPath, cur.v});
      }
    }
  }

  return 0;
}
