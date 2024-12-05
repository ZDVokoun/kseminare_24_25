#include <bits/stdc++.h>
#include <functional>
#include <queue>
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

  ll n;
  string s;
  cin >> n >> s;
  vll cnt('z' - 'a' + 1);
  for (int i = 0; i < s.size(); i++)
    cnt[s[i] - 'a']++;
  priority_queue<ll, vector<ll>, less<ll>> q;
  for (ll i : cnt)
    q.push(i);
  ll fst, scnd;
  while (q.size() > 1) {
    fst = q.top();
    q.pop();
    scnd = q.top();
    q.pop();
    q.push(fst - scnd);
  }
  cout << q.top() << endl;

  return 0;
}
