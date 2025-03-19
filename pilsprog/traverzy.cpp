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

ll solve(int l, int r, vector<int> &lst) {
  if (l == r - 1)
    return 0;
  ll res = INT32_MAX;
  for (int i = l + 1; i < r; i++) {
    res = min(res, solve(l, i, lst) + solve(i, r, lst) + lst[r] - lst[l]);
    cout << solve(l, i, lst) + solve(i, r, lst) + lst[r] - lst[l] << " " << l
         << r << " " << i << endl;
  }
  return res;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int t;
  cin >> t;
  for (int I = 0; I < t; I++) {
    int d, r;
    cin >> d >> r;
    vector<int> lst(r + 2);
    for (int i = 0; i < r; i++)
      cin >> lst[i + 1];
    lst[0] = 0;
    lst[r + 1] = d;
    vector<vll> dp(r + 2, vll(r + 2, INT32_MAX));
    // cout << solve(0, r + 1, lst) << endl;
    for (int i = 0; i < r + 2; i++) {
      dp[i][i] = 0;
    }
    for (int i = 0; i < r + 1; i++) {
      dp[i][i + 1] = 0;
    }
    for (int i = 2; i < r + 2; i++) {
      for (int j = 0; j < r + 2 - i; j++) {
        for (int k = 1; k < i; k++) {
          // cout << j << " " << j + i << endl;
          // cout << dp[j][j + k] + dp[j + k][j + i] + lst[j + i] - lst[j] <<
          // endl;
          dp[j][j + i] = min(dp[j][j + i], dp[j][j + k] + dp[j + k][j + i] +
                                               lst[j + i] - lst[j]);
        }
      }
    }
    cout << dp[0][r + 1] << endl;
    // for (auto line : dp) {
    //   for (auto n : line)
    //     cout << n << " ";
    //   cout << endl;
    // }
  }

  return 0;
}
