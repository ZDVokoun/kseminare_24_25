#include <cassert>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <variant>
#include <vector>

using namespace std;

enum Opcode {
  OP_PRINT,
  OP_PUSH,

  OP_LOAD,
  OP_STORE,

  OP_ADD,
  OP_SUB,
  OP_MUL,
  OP_DIV,
  OP_DUP,

  OP_NOT,
  OP_EQ,
  OP_LT,

  OP_BRANCH,
  OP_POP,
};

struct Instruction {
  // typ instrukce
  Opcode op;

  // některé instrukce si potřebují
  // pamatovat další hodnoty
  variant<monostate, int, string> value = monostate{};
};

int pop(vector<int> &zasobnik) {
  assert(!empty(zasobnik));
  int v = zasobnik.back();
  zasobnik.pop_back();
  return v;
}

void chyba(const string &msg, int ip, const vector<int> &zasobnik,
           const unordered_map<string, int> &promenne) {
  printf("Chyba na instrukci %d: %s\n", ip, msg.c_str());
  printf("Zasobnik: ");
  for (auto x : zasobnik) {
    printf("%d ", x);
  }
  printf("\n");
  printf("Promenne:\n");
  for (auto [k, v] : promenne) {
    printf("  %s: %d\n", k.c_str(), v);
  }

  throw std::runtime_error("Chyba v interpretru");
}

void interpret(vector<Instruction> const &instrukce, vector<int> &zasobnik,
               unordered_map<string, int> &promenne) {
  int ip = 0; // index aktuální instrukce
              // (instruction pointer)
  while (true) {
    if (!(ip >= 0 && ip < instrukce.size()))
      break;

    auto ins = instrukce.at(ip);

    switch (ins.op) {
    case OP_PRINT: {
      if (empty(zasobnik))
        chyba("Prázdný zásobník", ip, zasobnik, promenne);
      printf("PRINT: %d\n", zasobnik.back());
    } break;

    case OP_LOAD: {
      auto promenna = get<string>(ins.value);
      if (promenne.find(promenna) == promenne.end()) {
        chyba("Nedefinovaná proměnná", ip, zasobnik, promenne);
      }
      zasobnik.push_back(promenne[promenna]);

    } break;

    case OP_STORE: {
      if (empty(zasobnik))
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      promenne[get<string>(ins.value)] = pop(zasobnik);
    } break;

    case OP_PUSH: {
      zasobnik.push_back(get<int>(ins.value));
    } break;

    case OP_ADD: {
      if (size(zasobnik) < 2)
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      int b = pop(zasobnik);
      int a = pop(zasobnik);
      zasobnik.push_back(a + b);
    } break;
    case OP_SUB: {
      if (size(zasobnik) < 2)
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      // odebere nejdříve b, pak teprve a, aby
      // PUSH(30) PUSH(10) SUB dávalo 20
      int b = pop(zasobnik);
      int a = pop(zasobnik);
      zasobnik.push_back(a - b);
    } break;
    case OP_MUL: {
      if (size(zasobnik) < 2)
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      int b = pop(zasobnik);
      int a = pop(zasobnik);
      zasobnik.push_back(a * b);
    } break;
    case OP_DIV: {
      if (size(zasobnik) < 2)
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      int b = pop(zasobnik);
      int a = pop(zasobnik);
      if (b == 0) {
        chyba("Dělení nulou", ip, zasobnik, promenne);
      }
      zasobnik.push_back(a / b);
    } break;
    case OP_DUP: {
      if (empty(zasobnik))
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      zasobnik.push_back(zasobnik.back());
    } break;
    case OP_NOT: {
      if (empty(zasobnik))
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      int a = pop(zasobnik);
      zasobnik.push_back(a == 0 ? 1 : 0);
    } break;
    case OP_EQ: {
      if (size(zasobnik) < 2)
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      int b = pop(zasobnik);
      int a = pop(zasobnik);
      zasobnik.push_back(a == b ? 1 : 0);
    } break;
    case OP_LT: {
      if (size(zasobnik) < 2)
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      int b = pop(zasobnik);
      int a = pop(zasobnik);
      zasobnik.push_back(a < b ? 1 : 0);
    } break;
    case OP_BRANCH: {
      if (empty(zasobnik))
        chyba("Prázdný zásobník", ip, zasobnik, promenne);

      int a = pop(zasobnik);
      if (a != 0) {
        ip = get<int>(ins.value);
        continue;
      }
    } break;
    case OP_POP: {
      pop(zasobnik);
    } break;
    }

    ip += 1;
  }
}
// int main() {
//   vector<int> zasobnik;
//   vector<Instruction> instrukce(
//       {Instruction{.op = OP_PUSH, .value = 8},
//
//        // var fac = 1
//        Instruction{.op = OP_PUSH, .value = 1},
//        Instruction{.op = OP_STORE, .value = "fac"},
//
//        // while: if (i<2) goto break;
//        Instruction{.op = OP_DUP},
//        Instruction{.op = OP_PUSH, .value = 2},
//        Instruction{.op = OP_LT},
//        Instruction{.op = OP_BRANCH, .value = 15},
//
//        // fac *=i
//        Instruction{.op = OP_DUP}, // jump target
//        Instruction{.op = OP_LOAD, .value = "fac"},
//        Instruction{.op = OP_MUL},
//        Instruction{.op = OP_STORE, .value = "fac"},
//
//        // i -= 1
//        Instruction{.op = OP_PUSH, .value = -1},
//        Instruction{.op = OP_ADD},
//
//        // if (1) goto while:
//        Instruction{.op = OP_PUSH, .value = 1},
//        Instruction{.op = OP_BRANCH, .value = 3},
//        // break:
//
//        Instruction{.op = OP_LOAD, .value = "fac"},
//        Instruction{.op = OP_PRINT}});
//   unordered_map<string, int> promenne;
//
//   interpret(instrukce, zasobnik, promenne);
// }
//
