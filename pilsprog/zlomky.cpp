#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

int gcd(int a, int b) {
  a = abs(a);
  b = abs(b);
  if (a < b) {
    swap(a, b);
  }
  while (b != 0) {
    int temp = a % b;
    a = b;
    b = temp;
  }
  return a;
}

void solve() {
  int v;
  cin >> v;
  cin.ignore();
  for (int _ = 0; _ < v; ++_) {
    string input;
    getline(cin, input);
    stringstream ss(input);
    string frac1, op, frac2;
    ss >> frac1 >> op >> frac2;

    int a_num, a_den, b_num, b_den;
    sscanf(frac1.c_str(), "%d/%d", &a_num, &a_den);
    sscanf(frac2.c_str(), "%d/%d", &b_num, &b_den);

    if (a_den < 0) {
      a_num = -a_num;
      a_den = -a_den;
    }
    if (b_den < 0) {
      b_num = -b_num;
      b_den = -b_den;
    }

    int lcm_den = a_den * b_den / gcd(a_den, b_den);
    int aa = a_num * (lcm_den / a_den);
    int bb = b_num * (lcm_den / b_den);

    pair<int, int> res;
    if (op == "+") {
      res = make_pair(aa + bb, lcm_den);
    } else {
      res = make_pair(aa - bb, lcm_den);
    }

    int g = gcd(res.first, res.second);
    res.first /= g;
    res.second /= g;

    if (res.second == 1) {
      cout << res.first << endl;
    } else {
      cout << res.first << "/" << res.second << endl;
    }
  }
}

signed main() {
  solve();
  return 0;
}
