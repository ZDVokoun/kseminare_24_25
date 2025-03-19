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

  int r;
  cin >> r;
  vector<string> s(r);
  vector<vector<bool>> cnt_n(r, vector<bool>(10));
  vector<vbool> cnt_ch(r, vector<bool>(26));
  for (int i = 0; i < r; i++) {
    cin >> s[i];
    for (char ch : s[i]) {
      if (ch < 'A')
        cnt_n[i][ch - '0'] = true;
      else
        cnt_ch[i][ch - 'A'] = true;
    }
  }
  int d;
  cin >> d;
  for (int i = 0; i < d; i++) {
    string q;
    cin >> q;
    vector<string> res;
    for (int j = 0; j < r; j++) {
      bool match = true;
      for (char ch : q) {
        if (ch < 'A')
          match &= cnt_n[j][ch - '0'];
        else
          match &= cnt_ch[j][ch - 'A'];
      }
      if (match)
        res.push_back(s[j]);
    }
    if (res.size() == 0) {
      cout << "nenalezeno" << endl;
      continue;
    }
    for (int j = 0; j < res.size() - 1; j++)
      cout << res[j] << ", ";
    cout << res[res.size() - 1] << endl;
  }

  return 0;
}
