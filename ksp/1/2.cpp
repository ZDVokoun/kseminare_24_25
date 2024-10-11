#include <bits/stdc++.h>
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

  int rows, columns;
  cin >> rows >> columns;
  vector<string> map(rows);
  for (int i = 0; i < rows; i++)
    cin >> map[i];

  pair<int, int> start;
  for (int y = 0; y < rows; y++)
    for (int x = 0; x < columns; x++)
      if (map[y][x] == 'H')
        start = {x, y};

  queue<pair<int, int>> q;
  q.push(start);

  vector<pair<int, int>> neighs = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
  vector<vector<bool>> visited(rows, vector<bool>(columns));
  vector<pair<int, int>> res;
  visited[start.second][start.first] = true;

  if (rows < 3 || columns < 3) {
    cout << 0 << endl;
    return 0;
  }

  while (!q.empty()) {
    auto cur = q.front();
    q.pop();
    if (cur.first > 0 && cur.first < columns - 1 &&
        map[cur.second][cur.first] == '.' &&
        map[cur.second][cur.first - 1] == '#' &&
        map[cur.second][cur.first + 1] == '#') {
      res.push_back(cur);
      continue;
    }
    if (cur.second > 0 && cur.second < rows - 1 &&
        map[cur.second][cur.first] == '.' &&
        map[cur.second - 1][cur.first] == '#' &&
        map[cur.second + 1][cur.first] == '#') {
      res.push_back(cur);
      continue;
    }
    for (auto neigh : neighs) {
      int newx = cur.first + neigh.first;
      int newy = cur.second + neigh.second;
      if (newx < 0 || newx >= columns || newy < 0 || newy >= rows)
        continue;
      if (map[newy][newx] == '.' && !visited[newy][newx]) {
        q.push({newx, newy});
        visited[newy][newx] = true;
      }
    }
  }

  cout << res.size() << endl;
  for (auto p : res)
    cout << p.first + 1 << " " << p.second + 1 << endl;

  return 0;
}
