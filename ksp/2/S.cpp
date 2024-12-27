#include <cassert>
#include <cctype>
#include <iostream>
#include <optional>
#include <string>
#include <vector>

enum TokenType {
  // Operátory
  TK_NOT,
  TK_EQUAL,
  TK_GREATER,
  TK_LESS,
  TK_MINUS,
  TK_PLUS,
  TK_SEMICOLON,
  TK_SLASH,
  TK_STAR,
  TK_NOT_EQUAL,
  TK_EQUAL_EQUAL,
  TK_GREATER_EQUAL,
  TK_LESS_EQUAL,
  TK_LBRACE,
  TK_LPAREN,
  TK_RBRACE,
  TK_RPAREN,

  // Klíčová slova
  TK_ELSE,
  TK_FOR,
  TK_IF,
  TK_PRINT,
  TK_VAR,
  TK_WHILE,

  // literály
  TK_NAME,
  TK_NUMBER,
};

struct Token {
  TokenType type;

  // pouze u TK_NAME a TK_NUMBER, jinak ""
  std::string value;

  int row;
  int col;

  Token(TokenType t, int r = 0, int c = 0, std::string v = "")
      : type{t}, row{r}, col{c}, value{v} {}
};

std::string token_type_to_str(TokenType t) {
  switch (t) {
  case TK_NOT:
    return "NOT";
  case TK_EQUAL:
    return "EQUAL";
  case TK_GREATER:
    return "GREATER";
  case TK_LESS:
    return "LESS";
  case TK_MINUS:
    return "MINUS";
  case TK_PLUS:
    return "PLUS";
  case TK_SEMICOLON:
    return "SEMICOLON";
  case TK_SLASH:
    return "SLASH";
  case TK_STAR:
    return "STAR";
  case TK_NOT_EQUAL:
    return "NOT_EQUAL";
  case TK_EQUAL_EQUAL:
    return "EQUAL_EQUAL";
  case TK_GREATER_EQUAL:
    return "GREATER_EQUAL";
  case TK_LESS_EQUAL:
    return "LESS_EQUAL";
  case TK_LBRACE:
    return "LBRACE";
  case TK_LPAREN:
    return "LPAREN";
  case TK_RBRACE:
    return "RBRACE";
  case TK_RPAREN:
    return "RPAREN";
  case TK_ELSE:
    return "ELSE";
  case TK_FOR:
    return "FOR";
  case TK_IF:
    return "IF";
  case TK_PRINT:
    return "PRINT";
  case TK_VAR:
    return "VAR";
  case TK_WHILE:
    return "WHILE";
  case TK_NAME:
    return "NAME";
  case TK_NUMBER:
    return "NUMBER";
  }
  return "<invalid token value>";
}

struct Scanner {
  std::string source;
  bool error_occured = false;

  // Míří na znak, který bude v dalším kroku čten
  int row = 1, col = 1;

  Scanner(std::string s) : source{s} {}

  void advance(size_t i = 1) {
    if (peek() == '\n') {
      row++;
      col = 0;
    }
    col++;
    source.erase(0, i);
  }
  bool is_at_end() { return source.empty(); }

  char peek() { return source.empty() ? '\0' : source[0]; }

  bool match(char c) {
    if (peek() == c) {
      advance();
      return true;
    }
    return false;
  }

  void throw_error() {
    std::cout << "Error occured at row " << row << ", column " << col
              << std::endl;
    error_occured = true;
  }
};

std::optional<Token> match_operator_token(Scanner &sc) {
  if (sc.match('('))
    return Token(TK_LPAREN, sc.row, sc.col - 1);
  if (sc.match(')'))
    return Token(TK_RPAREN, sc.row, sc.col - 1);
  if (sc.match('['))
    return Token(TK_LBRACE, sc.row, sc.col - 1);
  if (sc.match(']'))
    return Token(TK_RBRACE, sc.row, sc.col - 1);
  if (sc.match('<')) {
    if (sc.match('=')) {
      return Token(TK_LESS_EQUAL, sc.row, sc.col - 1);
    } else {
      return Token(TK_LESS, sc.row, sc.col - 1);
    }
  }
  if (sc.match('>')) {
    if (sc.match('='))
      return Token(TK_GREATER_EQUAL, sc.row, sc.col - 1);
    else
      return Token(TK_GREATER, sc.row, sc.col - 1);
  }
  if (sc.match('!')) {
    if (sc.match('='))
      return Token(TK_NOT_EQUAL, sc.row, sc.col - 1);
    else
      return Token(TK_NOT, sc.row, sc.col - 1);
  }
  if (sc.match('=')) {
    if (sc.match('='))
      return Token(TK_EQUAL_EQUAL, sc.row, sc.col - 1);
    else
      return Token(TK_EQUAL, sc.row, sc.col - 1);
  }
  if (sc.match(';'))
    return Token(TK_SEMICOLON, sc.row, sc.col - 1);
  if (sc.match('*'))
    return Token(TK_STAR, sc.row, sc.col - 1);
  if (sc.match('-'))
    return Token(TK_MINUS, sc.row, sc.col - 1);
  if (sc.match('+'))
    return Token(TK_PLUS, sc.row, sc.col - 1);
  if (sc.match('/'))
    return Token(TK_SLASH, sc.row, sc.col - 1);
  return std::nullopt;
}

std::optional<Token> match_digit_token(Scanner &sc) {
  std::string num;
  while (std::isdigit(sc.peek())) {
    num += sc.peek();
    sc.advance();
  }
  if (num.size() > 0 && std::isalpha(sc.peek())) {
    sc.throw_error();
  }
  if (num.size() == 0)
    return std::nullopt;
  return Token(TK_NUMBER, sc.row, sc.col - 1, num);
}

std::optional<Token> match_keyword_or_name_token(Scanner &sc) {
  std::string str;
  while (std::isalpha(sc.peek())) {
    str += sc.peek();
    sc.advance();
  }
  if (str.size() == 0)
    return std::nullopt;
  if (str == "else")
    return Token(TK_ELSE, sc.row, sc.col - 1);
  if (str == "for")
    return Token(TK_FOR, sc.row, sc.col - 1);
  if (str == "if")
    return Token(TK_IF, sc.row, sc.col - 1);
  if (str == "print")
    return Token(TK_PRINT, sc.row, sc.col - 1);
  if (str == "var")
    return Token(TK_VAR, sc.row, sc.col - 1);
  if (str == "while")
    return Token(TK_WHILE, sc.row, sc.col - 1);
  return Token(TK_NAME, sc.row, sc.col - 1, str);
}

std::optional<Token> lex_one(Scanner &sc) {
  // přeskoč whitespace
  while (std::isspace(sc.peek())) {
    sc.advance();
  }

  auto o = match_operator_token(sc);
  if (o.has_value()) {
    return o;
  }

  auto d = match_digit_token(sc);
  if (d.has_value()) {
    return d;
  }

  auto k = match_keyword_or_name_token(sc);
  if (k.has_value()) {
    return k;
  }

  // jinak jsme museli narazit na konec
  if (!sc.is_at_end())
    sc.throw_error();

  return std::nullopt;
}

std::vector<Token> lex(std::string source) {
  Scanner sc = Scanner(source);
  std::vector<Token> ts;

  while (!sc.error_occured) {
    auto t = lex_one(sc);
    if (!t.has_value()) {
      break;
    }
    ts.push_back(t.value());
  }

  return ts;
}

int main() {
  std::string source =
      "var a = 42 \nfor (i = 0; i < n; i = i + 1) \na = a + 1\n";
  std::vector<Token> ts = lex(source);

  for (auto t : ts) {
    std::cout << token_type_to_str(t.type) << "(" <<
        // t.row << ", " << t.col << ", " <<
        t.value << ") ";
  }
  std::cout << '\n';
}
