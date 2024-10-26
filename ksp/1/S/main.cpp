#include <print>
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

  OP_BRANCH,
  OP_NOT,
  OP_EQ,
  OP_LT,
};

struct Instruction {
  // typ instrukce
  Opcode op;

  // některé instrukce si potřebují
  // pamatovat další hodnoty
  variant<monostate, int, string> value = monostate{};
};

vector<Instruction> instruction;
vector<int> stack;
unordered_map<string, int> variables;
int ip;

void interpret(vector<Instruction> const &instruction, vector<int> &stack,
               unordered_map<string, int> &variables) {
  int ip = 0; // index aktuální instrukce
              // (instruction pointer)
  while (true) {
    if (!(ip >= 0 && ip < ssize(instruction)))
      break;

    auto ins = instruction.at(ip);

    switch (ins.op) {
    case OP_PRINT: {
      println("PRINT: {}", stack.back());
    } break;

    case OP_LOAD: {
      stack.push_back(variables[get<string>(ins.value)]);

    } break;

    case OP_STORE: {
      variables[get<string>(ins.value)] = stack.back();
      stack.pop_back();
    } break;

    case OP_PUSH: {
      stack.push_back(get<int>(ins.value));
    } break;

    case OP_ADD: {
      int y = stack.back();
      stack.pop_back();
      int x = stack.back();
      stack.pop_back();
      stack.push_back(x + y);
      // TODO
    } break;
    case OP_SUB: {
      int y = stack.back();
      stack.pop_back();
      int x = stack.back();
      stack.pop_back();
      stack.push_back(x - y);
      // TODO
    } break;
    case OP_MUL: {
      int y = stack.back();
      stack.pop_back();
      int x = stack.back();
      stack.pop_back();
      stack.push_back(x * y);
      // TODO
    } break;
    case OP_DIV: {
      int y = stack.back();
      stack.pop_back();
      int x = stack.back();
      stack.pop_back();
      stack.push_back(x / y);
      // TODO
    } break;
    case OP_DUP: {
      // TODO
      stack.push_back(stack.back());
    } break;
    case OP_BRANCH: {
      int x = stack.back();
      stack.pop_back();
      if (x)
        ip = get<int>(ins.value) - 1;
    } break;
    case OP_NOT: {
      int x = stack.back();
      stack.pop_back();
      stack.push_back(!x);
    } break;
    case OP_EQ: {
      int y = stack.back();
      stack.pop_back();
      int x = stack.back();
      stack.pop_back();
      stack.push_back(x == y);
    } break;
    case OP_LT: {
      int y = stack.back();
      stack.pop_back();
      int x = stack.back();
      stack.pop_back();
      stack.push_back(x < y);
    } break;
    }
    ip += 1;
  }
}

int main() {
  vector<int> stack = {5};
  vector<Instruction> instruction({
      Instruction{.op = OP_STORE, .value = "in"},
      Instruction{.op = OP_PUSH, .value = 0},
      Instruction{.op = OP_STORE, .value = "it"},
      Instruction{.op = OP_PUSH, .value = 1},
      //
      Instruction{.op = OP_LOAD, .value = "it"},
      Instruction{.op = OP_PUSH, .value = 1},
      Instruction{.op = OP_ADD},
      Instruction{.op = OP_DUP},
      Instruction{.op = OP_STORE, .value = "it"},
      Instruction{.op = OP_MUL},
      //
      Instruction{.op = OP_LOAD, .value = "it"},
      Instruction{.op = OP_LOAD, .value = "in"},
      Instruction{.op = OP_LT},
      Instruction{.op = OP_BRANCH, .value = 4},
  });
  unordered_map<string, int> variables;

  interpret(instruction, stack, variables);
  for (auto i : stack)
    println("{}", i);
}
