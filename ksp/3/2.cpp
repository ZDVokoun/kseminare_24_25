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

  string a, b;
  getline(cin, a);
  getline(cin, b);
  int m = a.size();
  int n = b.size();

  vector<vll> dp(b.size() + 1, vll(a.size() + 1, INT32_MAX));
  vector<vector<string>> ops(b.size() + 1, vector<string>(a.size() + 1));
  vector<vector<pint>> back(n + 1, vector<pint>(m + 1));
  dp[n][m] = 0;
  dp[n - 1][m] = 2;
  dp[n][m - 1] = 2;
  ops[n - 1][m] = "2x\n3iaa" + b.substr(n - 1, n);
  ops[n][m - 1] = "2iaa\n3x";
  ops[n - 1][m - 1] = "l";

  back[n][m] = {-1, -1};
  back[n - 1][m] = {m, n};
  back[n][m - 1] = {m, n};
  back[n - 1][m - 1] = {m, n};

  if (a[m - 1] != b[n - 1]) {
    dp[n - 1][m - 1] = 2;
    ops[n - 1][m - 1] = "3i" + b.substr(n - 1, 1) + "aa\nh\nh\n3x";
  } else
    dp[n - 1][m - 1] = 0;

  for (int i = n; i >= 0; i--) {
    for (int j = m; j >= 0; j--) {
      if (j >= m - 1 && i >= n - 1)
        continue;
      // no change
      if (j < m && i < n && a[j] == b[i] && dp[i + 1][j + 1] < dp[i][j]) {
        dp[i][j] = dp[i + 1][j + 1];
        ops[i][j] = "l";
        back[i][j] = {j + 1, i + 1};
      }
      // 2i
      if (i + 2 <= n && 1 + dp[i + 2][j] < dp[i][j]) {
        dp[i][j] = 1 + dp[i + 2][j];
        ops[i][j] = "2i" + b.substr(i, 2);
        back[i][j] = {j, i + 2};
      }
      // 3i
      if (i + 3 <= n && 1 + dp[i + 3][j] < dp[i][j]) {
        dp[i][j] = 1 + dp[i + 3][j];
        ops[i][j] = "3i" + b.substr(i, 3);
        back[i][j] = {j, i + 3};
      }
      // 2x
      if (j + 2 <= m && 1 + dp[i][j + 2] < dp[i][j]) {
        dp[i][j] = 1 + dp[i][j + 2];
        ops[i][j] = "2x";
        back[i][j] = {j + 2, i};
      }
      // 3x
      if (j + 3 <= m && 1 + dp[i][j + 3] < dp[i][j]) {
        dp[i][j] = 1 + dp[i][j + 3];
        ops[i][j] = "3x";
        back[i][j] = {j + 3, i};
      }
    }
  }

  pint cur = {0, 0};
  while (cur != make_pair(m, n)) {
    cout << ops[cur.second][cur.first] << endl;
    cur = back[cur.second][cur.first];
  }
  cout << ":wq" << endl;

  return 0;
}
