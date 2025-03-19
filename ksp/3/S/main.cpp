/*
 * Kód k tomuto dílu seriálu se nachází v tomto souboru, ve zbylých je jen
 * řešení minulých dílů
 */

#include "interpret.hpp"
#include "token.hpp"
#include <cctype>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

struct TokenScanner {
  std::vector<Token> source;

  TokenScanner(std::vector<Token> s) : source{s} {}

  bool isAtEnd() { return source.empty(); }

  Token peek() { return source.empty() ? Token(TK_EOF) : source[0]; }

  void advance() { source.erase(source.begin()); }

  bool check(TokenType type) {
    if (isAtEnd())
      return false;
    return peek().type == type;
  }

  bool match(TokenType type) { return match(std::vector<TokenType>{type}); }

  bool match(std::vector<TokenType> types) {
    for (TokenType type : types) {
      if (check(type)) {
        advance();
        return true;
      }
    }
    return false;
  }

  void consume(TokenType type, const string &message) {
    if (!match(type)) {
      error(message);
    }
  }

  void error(const string &message) {
    if (isAtEnd()) {
      std::cerr << "Error at the end: ";
    } else {
      Token token = peek();
      std::cerr << "Error on token " << token_type_to_str(token.type) << "("
                << token.value << ")" << " at " << token.row << ":"
                << token.column << ": ";
    }
    std::cerr << message << "\n";
    std::exit(1);
  }
};

enum ExprType {
  ET_LITERAL,
  ET_NAME,
  // binární operátory
  ET_MULTIPLY,
  ET_DIVIDE,
  ET_ADD,
  ET_SUBTRACT,
  ET_LESS,
  ET_LESS_EQUAL,
  ET_GREATER,
  ET_GREATER_EQUAL,
  ET_EQUAL,
  ET_NOT_EQUAL,
  ET_ASSIGN,

  // unární operátory
  ET_NEGATE,
  ET_NOT,

  // příkazy
  ET_BLOCK,
  ET_PRINT,
  ET_VAR,
  ET_IF,
  ET_WHILE,
  ET_FOR,
};

struct Expr {
  Expr(ExprType t, std::vector<Expr> ch) : type{t}, children{ch} {}

  Expr(ExprType t, std::string v) : type{t}, value{v} {}

  ExprType type;
  std::vector<Expr> children;
  std::string value; // pokud je number nebo name
};

/*
 * Úkol 1
 */

void printExpr(Expr ex) {
  cout << "(";
  switch (ex.type) {
  case ET_LITERAL:
    cout << ex.value;
    break;
  case ET_NAME:
    cout << ex.value;
    break;
  case ET_MULTIPLY:
    printExpr(ex.children[0]);
    cout << " * ";
    printExpr(ex.children[1]);
    break;
  case ET_DIVIDE:
    printExpr(ex.children[0]);
    cout << " / ";
    printExpr(ex.children[1]);
    break;
  case ET_ADD:
    printExpr(ex.children[0]);
    cout << " + ";
    printExpr(ex.children[1]);
    break;
  case ET_SUBTRACT:
    printExpr(ex.children[0]);
    cout << " - ";
    printExpr(ex.children[1]);
    break;
  case ET_LESS:
    printExpr(ex.children[0]);
    cout << " < ";
    printExpr(ex.children[1]);
    break;
  case ET_LESS_EQUAL:
    printExpr(ex.children[0]);
    cout << " <= ";
    printExpr(ex.children[1]);
    break;
  case ET_GREATER:
    printExpr(ex.children[0]);
    cout << " > ";
    printExpr(ex.children[1]);
    break;
  case ET_GREATER_EQUAL:
    printExpr(ex.children[0]);
    cout << " >= ";
    printExpr(ex.children[1]);
    break;
  case ET_EQUAL:
    printExpr(ex.children[0]);
    cout << " == ";
    printExpr(ex.children[1]);
    break;
  case ET_NOT_EQUAL:
    printExpr(ex.children[0]);
    cout << " != ";
    printExpr(ex.children[1]);
    break;
  case ET_ASSIGN:
    printExpr(ex.children[0]);
    cout << " = ";
    printExpr(ex.children[1]);
    break;
  case ET_NOT:
    cout << "!";
    printExpr(ex.children[0]);
    break;
  case ET_NEGATE:
    cout << "-";
    printExpr(ex.children[0]);
    break;
  case ET_BLOCK:
    for (auto e : ex.children)
      printExpr(e);
    break;
  case ET_IF:
    cout << "IF";
    printExpr(ex.children[0]);
    printExpr(ex.children[1]);
    break;
  case ET_FOR:
    cout << "FOR";
    for (auto e : ex.children)
      printExpr(e);
    break;
  case ET_PRINT:
    cout << "PRINT";
    printExpr(ex.children[0]);
    break;
  case ET_WHILE:
    cout << "WHILE";
    printExpr(ex.children[0]);
    printExpr(ex.children[1]);
    break;
  case ET_VAR:
    cout << "VAR ";
    for (auto e : ex.children)
      printExpr(e);
    break;
  default:
    cout << "UNDEF" << "(";
    for (auto e : ex.children)
      printExpr(e);
    cout << ")";
    break;
  }
  cout << ")";
}

void printExprLn(Expr ex) {
  printExpr(ex);
  cout << endl;
}

Expr expression(TokenScanner &ts);
Expr unary(TokenScanner &ts);

Expr primary(TokenScanner &ts) {
  auto token = ts.peek();

  if (ts.match(TK_NUMBER)) {
    return Expr(ET_LITERAL, token.value);
  }

  if (ts.match(TK_NAME)) {
    return Expr(ET_NAME, token.value);
  }

  if (ts.match(TK_LPAREN)) {
    // návrat zpět na začátek řetězce funkcí
    Expr e = expression(ts);
    ts.consume(TK_RPAREN, "Expected ')'");
    return e;
  }

  ts.error("Unexpected token");
}

Expr unary(TokenScanner &ts) {
  if (ts.match(TK_MINUS))
    return Expr(ET_NEGATE, {unary(ts)});
  else if (ts.match(TK_NOT))
    return Expr(ET_NOT, {unary(ts)});
  else
    return primary(ts);
}

Expr multiplication(TokenScanner &ts) {
  Expr expr = unary(ts);

  while (ts.check(TK_STAR) || ts.check(TK_SLASH)) {
    Token op = ts.peek();
    ts.advance();
    Expr right = unary(ts);
    ExprType type = (op.type == TK_STAR) ? ET_MULTIPLY : ET_DIVIDE;
    expr = Expr(type, {expr, right});
  }

  return expr;
}

/*
 * Úkol 2
 */

Expr addition(TokenScanner &ts) {
  Expr e = multiplication(ts);

  while (ts.check(TK_PLUS) || ts.check(TK_MINUS)) {
    Token op = ts.peek();
    ts.advance();
    Expr right = multiplication(ts);
    ExprType type = (op.type == TK_PLUS) ? ET_ADD : ET_SUBTRACT;
    e = Expr(type, {e, right});
  }

  return e;
}

// Dávám prioritu operátorům porovnání před == a !=, což dělám pomocí rozdělení
// do dvou funkcí

Expr comparison(TokenScanner &ts) {
  Expr e = addition(ts);

  while (ts.check(TK_GREATER) || ts.check(TK_LESS) ||
         ts.check(TK_GREATER_EQUAL) || ts.check(TK_LESS_EQUAL)) {
    Token op = ts.peek();
    ts.advance();
    Expr right = addition(ts);
    ExprType type;
    switch (op.type) {
    case TK_GREATER_EQUAL:
      type = ET_GREATER_EQUAL;
      break;
    case TK_LESS_EQUAL:
      type = ET_LESS_EQUAL;
      break;
    case TK_GREATER:
      type = ET_GREATER;
      break;
    case TK_LESS:
      type = ET_LESS;
      break;
    default:
      break;
    }
    e = Expr(type, {e, right});
  }

  return e;
}

Expr equals(TokenScanner &ts) {
  Expr e = comparison(ts);

  while (ts.check(TK_EQUAL_EQUAL) || ts.check(TK_NOT_EQUAL)) {
    Token op = ts.peek();
    ts.advance();
    Expr right = comparison(ts);
    ExprType type = (op.type == TK_EQUAL_EQUAL) ? ET_EQUAL : ET_NOT_EQUAL;
    e = Expr(type, {e, right});
  }

  return e;
}

Expr assignment(TokenScanner &ts) {
  Expr left = equals(ts);
  if (ts.match(TK_EQUAL)) {
    Expr right = assignment(ts);
    return Expr(ET_ASSIGN, {left, right});
  }
  return left;
}

Expr expression(TokenScanner &ts) { return assignment(ts); }

Expr printStatement(TokenScanner &ts) {
  Expr value = expression(ts);
  ts.consume(TK_SEMICOLON, "Expected ';' after value.");
  return Expr(ET_PRINT, {value});
}

/*
 * Úkol 3
 */

Expr varStatement(TokenScanner &ts) {
  Expr value = assignment(ts);
  if (value.children[0].type != ET_NAME)
    ts.error("Expected variable name after 'VAR'.");
  ts.consume(TK_SEMICOLON, "Expected ';' after value.");
  return Expr(ET_VAR, {value});
}

Expr statement(TokenScanner &ts) {
  if (ts.match(TK_PRINT))
    return printStatement(ts);
  if (ts.match(TK_VAR))
    return varStatement(ts);
  // TODO
}

Expr parse(TokenScanner &ts) {
  std::vector<Expr> statements;

  while (!ts.isAtEnd()) {
    statements.push_back(statement(ts));
  }

  return Expr(ET_BLOCK, statements);
}

/*
 * Úkol 4
 */

void emit(std::vector<Instruction> &program, Expr &expr,
          std::unordered_set<string> &variables) {
  // Kontrolu definic proměnných neřeším za běhu, ale během převodu do
  // instrukcí, aktuálně všechny proměnné mají globální scope
  if (expr.type == ET_VAR) {
    variables.insert(expr.children[0].children[0].value);
  }
  if (expr.type != ET_ASSIGN)
    for (auto &operand : expr.children) {
      emit(program, operand, variables);
    }

  switch (expr.type) {
  case ET_ADD: {
    program.push_back(Instruction{.op = OP_ADD});
  } break;
  case ET_MULTIPLY: {
    program.push_back(Instruction{.op = OP_MUL});
  } break;
  case ET_SUBTRACT: {
    program.push_back(Instruction{.op = OP_SUB});
  } break;
  case ET_DIVIDE: {
    program.push_back(Instruction{.op = OP_DIV});
  } break;
  case ET_BLOCK:
    break;
  case ET_NOT: {
    program.push_back(Instruction{.op = OP_NOT});
  } break;
  case ET_EQUAL: {
    program.push_back(Instruction{.op = OP_EQ});
  } break;
  case ET_NOT_EQUAL: {
    program.push_back(Instruction{.op = OP_EQ});
    program.push_back(Instruction{.op = OP_NOT});
  } break;
  case ET_NEGATE: {
    program.push_back(Instruction{.op = OP_PUSH, .value = -1});
    program.push_back(Instruction{.op = OP_MUL});
  } break;
  case ET_IF: {
    // TODO
  } break;
  case ET_FOR: {
    // TODO
  } break;
  case ET_NAME: {
    program.push_back(Instruction{.op = OP_LOAD, .value = expr.value});
  } break;
  case ET_VAR: {
    program.push_back(Instruction{.op = OP_POP});
  } break;
  case ET_PRINT: {
    program.push_back(Instruction{.op = OP_PRINT});
    program.push_back(Instruction{.op = OP_POP});
  } break;
  case ET_WHILE: {
    // TODO
  } break;
  case ET_ASSIGN: {
    if (variables.find(expr.children[0].value) == variables.end()) {
      std::cerr << "Variable " << expr.children[0].value << " was not defined."
                << endl;
      std::exit(1);
    }
    emit(program, expr.children[1], variables);

    program.push_back(Instruction{.op = OP_DUP});
    program.push_back(
        Instruction{.op = OP_STORE, .value = expr.children[0].value});
  } break;
  case ET_LESS: {
    program.push_back(Instruction{.op = OP_LT});
  } break;
  case ET_LESS_EQUAL: {
    program.push_back(Instruction{.op = OP_PUSH, .value = 1});
    program.push_back(Instruction{.op = OP_ADD});
    program.push_back(Instruction{.op = OP_LT});
  } break;
  case ET_GREATER_EQUAL: {
    program.push_back(Instruction{.op = OP_LT});
    program.push_back(Instruction{.op = OP_NOT});
  } break;
  case ET_GREATER: {
    program.push_back(Instruction{.op = OP_PUSH, .value = 1});
    program.push_back(Instruction{.op = OP_ADD});
    program.push_back(Instruction{.op = OP_LT});
    program.push_back(Instruction{.op = OP_NOT});
  } break;
  case ET_LITERAL: {
    // Tady konečně naparsujeme číslo ze stringu
    // :)
    int value = std::stoi(expr.value);
    program.push_back(Instruction{.op = OP_PUSH, .value = value});
  } break;
  }
}

int main() {
  string source =
      "var a = 1 + 2 * 9 / -3; print a; var b = 0; print ((a = 10) * (b = 4)) "
      "/ a / b;print (a = 0) >= a; print !(b > (b = 0));";
  cout << source << endl;
  std::vector<Token> tokens = lex(source);

  TokenScanner ts(tokens);

  Expr ex = parse(ts);

  printExprLn(ex);

  vector<Instruction> program;
  unordered_set<string> defs;
  emit(program, ex, defs);

  vector<int> stack;
  unordered_map<string, int> variables;
  interpret(program, stack, variables);
}
