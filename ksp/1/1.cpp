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

  ll K, N;
  cin >> K >> N;
  vector<pair<ll, ll>> plan(2 * N);
  char ch;
  for (ll i = 0; i < N; i++) {
    ll hour, minute, second;
    cin >> hour >> ch >> minute >> ch >> second;
    plan[i].first = 3600 * hour + 60 * minute + second;
    cin >> plan[i].second;
    plan[i].second--;
    plan[i + N].first = plan[i].first + 24 * 3600;
    plan[i + N].second = plan[i].second;
  }
  vector<ll> counter(K);
  ll nonzeros = 0;
  ll i = 0;
  ll j = 0;
  ll min = INT64_MAX;
  ll beststart = -1;
  while (j < 2 * N) {
    // cout << i << " " << j << " " << counter[0] << " " << counter[1] << " "
    //      << counter[2] << endl;
    if (nonzeros == K) {
      if (plan[j].first - plan[i].first < min) {
        min = plan[j].first - plan[i].first;
        beststart = i;
      }
      counter[plan[i].second]--;
      if (counter[plan[i].second] == 0)
        nonzeros--;
      i++;
    } else {
      j++;
      if (counter[plan[j].second] == 0) {
        nonzeros++;
      }
      counter[plan[j].second]++;
    }
  }
  cout << plan[beststart].first / 3600 << ":"
       << (plan[beststart].first / 60) % 60 << ":"
       << plan[beststart].first % 3600 % 60 << " " << min << endl;

  return 0;
}
