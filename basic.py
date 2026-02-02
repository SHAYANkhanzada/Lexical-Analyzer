#######################################
# IMPORTS
#######################################

from strings_with_arrows import *
import random

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
KEYWORDS = [
    'if', 'else', 'elif', 'while', 'for', 'def', 'class',
    'return', 'break', 'continue', 'pass', 'import', 'from',
    'as', 'try', 'except', 'finally', 'with', 'lambda', 'yield',
    'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is'
]

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

TT_INT       = 'INT'
TT_FLOAT     = 'FLOAT'
TT_STRING    = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD   = 'KEYWORD'
TT_PLUS      = 'PLUS'
TT_MINUS     = 'MINUS'
TT_MUL       = 'MUL'
TT_DIV       = 'DIV'
TT_LPAREN    = 'LPAREN'
TT_RPAREN    = 'RPAREN'
TT_LSQUARE   = 'LSQUARE'
TT_RSQUARE   = 'RSQUARE'
TT_COMMA     = 'COMMA'
TT_COLON     = 'COLON'
TT_EQ        = 'EQ'
TT_EQEQ      = 'EQEQ'
TT_LT        = 'LT'
TT_LTE       = 'LTE'
TT_GT        = 'GT'
TT_GTE       = 'GTE'
TT_INCREMENT = 'INCREMENT'
TT_DECREMENT = 'DECREMENT'
TT_EOF       = 'EOF'

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        return self.value if self.value is not None else self.type

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '\n':   
                self.advance()               
            elif self.current_char == '#':
                while self.current_char is not None and self.current_char not in '\n\r':
                    self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos)); self.advance()
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(self.make_plus())
            elif self.current_char == '-':
                tokens.append(self.make_minus())
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos)); self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos)); self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos)); self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos)); self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos)); self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos)); self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TT_COLON, pos_start=self.pos)); self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos)); self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        
        # Check if it's a keyword
        if id_str in KEYWORDS:
            return Token(TT_KEYWORD, id_str, pos_start, self.pos)
        else:
            return Token(TT_IDENTIFIER, id_str, pos_start, self.pos)
    
    def make_equals(self):
        """Handle = and == with lookahead"""
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '=':
            self.advance()
            return Token(TT_EQEQ, pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TT_EQ, pos_start=pos_start, pos_end=self.pos)
    
    def make_less_than(self):
        """Handle < and <= with lookahead"""
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '=':
            self.advance()
            return Token(TT_LTE, pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TT_LT, pos_start=pos_start, pos_end=self.pos)
    
    def make_greater_than(self):
        """Handle > and >= with lookahead"""
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '=':
            self.advance()
            return Token(TT_GTE, pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TT_GT, pos_start=pos_start, pos_end=self.pos)
    
    def make_plus(self):
        """Handle + and ++ with lookahead"""
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '+':
            self.advance()
            return Token(TT_INCREMENT, pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TT_PLUS, pos_start=pos_start, pos_end=self.pos)
    
    def make_minus(self):
        """Handle - and -- with lookahead"""
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '-':
            self.advance()
            return Token(TT_DECREMENT, pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TT_MINUS, pos_start=pos_start, pos_end=self.pos)
        
    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        self.advance()  # skip opening quote

        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()

        if self.current_char == '"':
            self.advance()  # skip closing quote
            return Token(TT_STRING, string, pos_start, self.pos)
        else:
            return Token(TT_STRING, string, pos_start, self.pos)  # unterminated ok for demo

#######################################
# NODES & PARSE RESULT
#######################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    def __repr__(self):
        return f'{self.tok.value}'

class VarAccessNode:
    def __init__(self, var_name):
        self.var_name = var_name
        self.pos_start = var_name.pos_start
        self.pos_end = var_name.pos_end
    def __repr__(self):
        return f'{self.var_name.value}'

class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
        return '[' + ', '.join(repr(el) for el in self.element_nodes) + ']'

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    def success(self, node):
        self.node = node
        return self
    def failure(self, error):
        self.error = error
        return self

#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return ParseResult().failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Extra stuff after expression"
            ))
        return res

    def expr(self):
        # For this demo we only accept numbers, identifiers, and lists
        return self.atom()

    def atom(self):
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return ParseResult().success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            self.advance()
            return ParseResult().success(VarAccessNode(tok))

        elif tok.type == TT_LSQUARE:
            return self.list_expr()

        elif tok.type == TT_LPAREN:
            self.advance()
            expr = self.expr()
            if expr.error: return expr
            if self.current_tok.type == TT_RPAREN:
                self.advance()
                return expr
            else:
                return ParseResult().failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        return ParseResult().failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected number, identifier, '[' or '('"
        ))

    def list_expr(self):
        pos_start = self.current_tok.pos_start
        self.advance()  # eat '['

        elements = []

        if self.current_tok.type == TT_RSQUARE:
            self.advance()
        else:
            expr = self.expr()
            if expr.error: return expr
            elements.append(expr.node)

            while self.current_tok.type == TT_COMMA:
                self.advance()
                expr = self.expr()
                if expr.error: return expr
                elements.append(expr.node)

            if self.current_tok.type != TT_RSQUARE:
                return ParseResult().failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ']'"
                ))
            self.advance()  # eat ']'

        return ParseResult().success(ListNode(elements, pos_start, self.current_tok.pos_end))

#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error, 0

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error, len(tokens) - 1  # -1 because of EOF token


if __name__ == "__main__":
    while True:
        text = input("basic > ")
        if text.strip() == "":
            continue
        
        result, error, tokens = run("<stdin>", text)

        if error:
            print(error.as_string())
        else:
            print("Result:", result)
            print("Tokens:", tokens)

