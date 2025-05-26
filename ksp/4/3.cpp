#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vb;
typedef pair<int, int> pint;

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int N;
  cin >> N;
  vector<vb> mgraph(N, vb(N));
  vector<vint> graph(N);
  for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++) {
      int cur;
      cin >> cur;
      mgraph[i][j] = cur;
      if (mgraph[i][j])
        graph[i].push_back(j);
    }
  vector<vint> dist_two(N, vint(N));
  vector<vint> dist_two_bridge(N, vint(N));
  for (int i = 0; i < N; i++)
    for (int j : graph[i])
      for (int k : graph[j]) {
        if (k == i)
          continue;
        dist_two[i][k]++;
        if (mgraph[i][k]) {
          cout << "TRICYKLUS " << i << " " << j << " " << k << endl;
          return 0;
        }
        if (dist_two[i][k] > 1) {
          cout << "CTYRCYKLUS " << i << " " << j << " " << k << " "
               << dist_two_bridge[i][k] << endl;
          return 0;
        }
        dist_two_bridge[i][k] = j;
      }

  cout << "NIC" << endl;

  return 0;
}
