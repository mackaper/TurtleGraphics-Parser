# Author: Marcus Bardvall & Olle Jernström
# Lexer Luthor
import sys
import re
from copy import copy
from math import sqrt, cos, sin, pi


class DissallowedCharacterError(Exception):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(details)
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.details = details

    def as_string(self):
        result = f'{self.details}'
        result += f' File {self.pos_start.text}, line {self.pos_start.line + 1}'
        return result


class Position:
    def __init__(self, index, line, column, text):
        self.index = index
        self.line = line
        self.column = column
        self.text = text

    def advance(self, current_char):
        self.index += 1
        self.column += 1
        if current_char and current_char == '\n':
            self.line += 1
            self.column = 0


class Lexer:
    def __init__(self, text):
        self.text = text.upper()
        self.current_char = None
        self.pos = Position(-1, 1, -1, text)
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def tokenize(self):
        # keywords = ['FORW ', 'FORW\n', 'FORW\t', 'BACK ', 'BACK\n', 'BACK\t', 'LEFT ', 'LEFT\n', 'LEFT\t', 'RIGHT ', 'RIGHT\n', 'RIGHT\t',
        #             'DOWN', 'DOWN ', 'DOWN\n', 'DOWN\t', 'UP', 'UP ', 'UP\n', 'UP\t', 'COLOR ', 'COLOR\n', 'COLOR\t', 'REP ', 'REP\t', 'REP\n', 'REP%']
        self.keywords = ['FORW', 'BACK', 'LEFT',
                         'RIGHT', 'DOWN', 'UP', 'COLOR', 'REP']
        self.following_char = [' ', '\t', '\n', '%']
        self.tokens = []
        while self.current_char != None:
            if self.current_char in [" ", "\t", "\n"]:
                self.advance()
            elif self.current_char in "FBLRDUCR":
                startpos = copy(self.pos)
                word = self.construct_word()
                if word in self.keywords:
                    if word in ["DOWN", "UP"]:
                        token = Token(word, startpos, copy(self.pos))
                        self.tokens.append(token)

                    elif self.current_char in self.following_char:
                        token = Token(word, startpos, copy(self.pos))
                        self.tokens.append(token)
                    else:
                        token = Token('ERROR', startpos, copy(
                            self.pos), f"Keyword '{word}' did not match any keywords {self.keywords}, you may have forgotten a space.")
                        self.tokens.append(token)
                else:
                    token = Token('ERROR', startpos, copy(
                        self.pos), f"Keyword '{word}' did not match any keywords {self.keywords}, you may have forgotten a space.")
                    self.tokens.append(token)

            elif self.current_char in "0123456789":
                startpos = copy(self.pos)
                str_number = self.construct_number()
                int_number = int(str_number)
                if int_number != 0:
                    if self.current_char in self.following_char or self.current_char == '.':
                        token = Token('NUMBER', startpos,
                                      copy(self.pos), int_number)
                        self.tokens.append(token)
                    else:
                        token = Token('ERROR', startpos, copy(
                            self.pos), f"Number can not be 0")
                else:
                    token = Token('ERROR', startpos, copy(
                        self.pos), f"Number has to be followed by some 'space'")
            elif self.current_char == '.':
                self.tokens.append(
                    Token('PERIOD', copy(self.pos), copy(self.pos)))
                self.advance()
            elif self.current_char == "#":
                startpos = copy(self.pos)
                color = self.construct_color()
                self.tokens.append(
                    Token('HEX', startpos, copy(self.pos), color))
            elif self.current_char == '%':
                while self.current_char != '\n' and self.current_char != None:
                    self.advance()
            elif self.current_char == '"':
                token = Token('QUOTE', copy(self.pos), copy(self.pos))
                self.tokens.append(token)
                self.advance()
            else:
                token = Token('ERROR', copy(self.pos),
                              copy(self.pos), self.current_char)
                self.tokens.append(token)
                self.advance()
        try:
            eof_token = Token('EOF', copy(
                self.tokens[-1].pos_start), copy(self.tokens[-1].pos_start))
        except:
            eof_token = Token('EOF', copy(self.pos), copy(self.pos))

        self.tokens.append(eof_token)
        return self.tokens

    def construct_color(self):
        color = '#'
        self.advance()
        startpos = copy(self.pos)
        while self.current_char != None and re.match(r'[a-fA-F0-9]', self.current_char):
            color += self.current_char
            self.advance()
        if len(color) != 7:
            token = Token('ERROR', startpos, copy(self.pos),
                          f"Color must be 7 characters long including #")
            self.tokens.append(token)
        return color

    def construct_number(self):
        number = ''
        while self.current_char != None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return number

    def construct_word(self):
        word = ''
        while self.current_char != None and self.current_char.isalpha():
            word += self.current_char
            self.advance()
        # if self.current_char in self.following_char:
        #     word += self.current_char
        #     self.advance()
        return word


class Token:
    def __init__(self, type_, pos_start, pos_end, value=None):
        self.type = type_
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.value = value

    def __repr__(self):
        if self.value:
            return f'({self.type}):[{self.pos_start.line}]:{self.value}'
        return f'({self.type}:[{self.pos_start.line}])'


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.expressions = []
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = self.tokens[-1]

    def parse(self):
        while self.current_token and self.current_token.type != 'EOF':
            expression = self.parse_expression()
            if expression:
                self.expressions.append(expression)
        return self.expressions

    def parse_rep(self):
        self.advance()
        if self.current_token.type == 'NUMBER':
            number_token = self.current_token
            self.advance()
            if self.current_token.type == 'QUOTE':
                self.advance()
                inner_expressions = []
                if self.current_token.type == 'QUOTE':
                    raise DissallowedCharacterError(
                        self.current_token.pos_start, self.current_token.pos_end, f"Expected Expression, got Second QUOTE")

                while self.current_token and self.current_token.type != 'QUOTE':
                    inner_expression = self.parse_expression()
                    inner_expressions.append(inner_expression)
                if not self.current_token:
                    raise DissallowedCharacterError(
                        self.current_token.pos_start, self.current_token.pos_end, f"Expected number, got {self.current_token.type}")

                expression = NodeExpression(
                    'REP', number_token.value, inner_expressions)
                self.advance()
                return expression
            else:
                inner_expression = self.parse_expression()
                expression = NodeExpression(
                    'REP', number_token.value, [inner_expression])
                return expression
        else:
            raise DissallowedCharacterError(
                self.current_token.pos_start, self.current_token.pos_end, f"Expected number, got {self.current_token.type}")

    def parse_command(self):
        value_expression_types = ['FORW', 'BACK', 'LEFT', 'RIGHT']
        empty_expression_types = ['DOWN', 'UP']
        if self.current_token.type in value_expression_types:
            token = self.current_token
            self.advance()
            if self.current_token.type == 'NUMBER':

                number_token = self.current_token
                self.advance()
                if self.current_token.type == 'PERIOD':
                    expression = ValueExpression(
                        token.type, number_token.value)
                    self.advance()
                    return expression
                else:
                    raise DissallowedCharacterError(
                        self.current_token.pos_start, self.current_token.pos_end, f"Expected period, got {self.current_token.type}")
            else:
                raise DissallowedCharacterError(
                    self.current_token.pos_start, self.current_token.pos_end, f"Expected number, got {self.current_token.type}")

        elif self.current_token.type in empty_expression_types:
            token = self.current_token
            self.advance()
            if self.current_token.type == 'PERIOD':
                expression = EmptyExpression(token.type)
                self.advance()
                return expression
            else:
                raise DissallowedCharacterError(
                    self.current_token.pos_start, self.current_token.pos_end, f"Expected number, got {self.current_token.type}")
        elif self.current_token.type == 'COLOR':
            self.advance()
            if self.current_token.type == 'HEX':
                hex_token = self.current_token
                self.advance()
                if self.current_token.type == 'PERIOD':
                    expression = ValueExpression('COLOR', hex_token.value)
                    self.advance()
                    return expression
                else:
                    raise DissallowedCharacterError(
                        self.current_token.pos_start, self.current_token.pos_end, f"Expected number, got {self.current_token.type}")
            else:
                raise DissallowedCharacterError(
                    self.current_token.pos_start, self.current_token.pos_end, f"Expected number, got {self.current_token.type}")
        else:
            raise DissallowedCharacterError(
                self.current_token.pos_start, self.current_token.pos_end, f"Expected number, got {self.current_token.type}")

    def parse_expression(self):
        if self.current_token.type == 'REP':
            expression = self.parse_rep()
            return expression
        elif self.current_token.type == 'ERROR':
            raise DissallowedCharacterError(
                self.current_token.pos_start, self.current_token.pos_end, f"Expected number, got {self.current_token.type}")
        else:
            expression = self.parse_command()
            return expression


class NodeExpression:
    def __init__(self, instruction, value, expressions):
        self.instruction = instruction
        self.value = value
        self.expressions = expressions

    def __repr__(self):
        return f'({self.instruction}, {self.value}, {self.expressions})'


class ValueExpression:
    def __init__(self, instruction, value):
        self.instruction = instruction
        self.value = value

    def __repr__(self):
        return f'({self.instruction}, {self.value})'


class EmptyExpression:
    def __init__(self, instruction):
        self.instruction = instruction

    def __repr__(self):
        return f'({self.instruction})'


def interperete(expressions):
    color = '#0000FF'
    is_draw = False
    pos = (0, 0)
    direction = (1, 0)


class Interperator:
    def __init__(self, expr):
        self.expr = expr
        self.color = '#0000FF'
        self.draw = False
        self.pos = (0, 0)
        self.dir = (1, 0)
        self.v = 0  # degrees

    @property
    def posx(self):
        return self.pos[0]

    @property
    def posy(self):
        return self.pos[1]

    @property
    def dirx(self):
        return self.dir[0]

    @property
    def diry(self):
        return self.dir[1]

    def calc_new_pos(self, d):
        tol = 0.0000000001
        v = self.v
        x = self.posx
        y = self.posy
        new_x = round(x + d * cos((pi*v)/180), 10)
        new_x = new_x if abs(new_x) > tol else 0.0
        new_y = round((y + d * sin((pi*v)/180)), 10)
        new_y = new_y if abs(new_y) > tol else 0.0

        return (new_x, new_y)

    def interperete_expression(self, expr):
        if isinstance(expr, EmptyExpression):
            if expr.instruction == 'DOWN':
                self.draw = True

            elif expr.instruction == 'UP':
                self.draw = False

        elif isinstance(expr, ValueExpression):
            if expr.instruction == 'FORW':
                old_pos = self.pos
                new_pos = self.calc_new_pos(expr.value)
                string = f"{self.color} {old_pos[0]:.4f} {old_pos[1]:.4f} {new_pos[0]:.4f} {new_pos[1]:.4f}"
                self.pos = new_pos
                if self.draw:
                    self.lines.append(string)
            elif expr.instruction == 'BACK':
                old_pos = self.pos
                new_pos = self.calc_new_pos(-expr.value)  # Note minus
                string = f"{self.color} {old_pos[0]:.4f} {old_pos[1]:.4f} {new_pos[0]:.4f} {new_pos[1]:.4f}"
                self.pos = new_pos
                if self.draw:
                    self.lines.append(string)
            elif expr.instruction == 'LEFT':
                new_angle = expr.value
                self.v = (self.v + new_angle) % 360
            elif expr.instruction == 'RIGHT':
                new_angle = expr.value
                self.v = (self.v - new_angle) % 360
            elif expr.instruction == 'COLOR':
                new_color = expr.value
                self.color = new_color
        elif isinstance(expr, NodeExpression):
            if expr.instruction == 'REP':
                value = expr.value
                rep_expressions = expr.expressions
                for _ in range(value):
                    for rep_expr in rep_expressions:
                        self.interperete_expression(rep_expr)

    def interperete(self):
        self.lines = []
        for expr in self.expr:
            self.interperete_expression(expr)
        return self.lines


def local_run():
    import tests
    test_cases = [tests.test1, tests.test2, tests.test3, tests.test4, tests.test5, tests.test6, tests.test7,
                  tests.test8, tests.test9, tests.test10, tests.test11, tests.test12]

    for i, t in enumerate(test_cases, 1):
        print(f"------------- RUNNING TEST {i} -----------------------")
        try:
            lexer = Lexer(t)
            tokens = lexer.tokenize()
            print(tokens)
            parser = Parser(tokens)
            expressions = parser.parse()
            print(expressions)
            interperator = Interperator(expressions)
            lines = interperator.interperete()
            for l in lines:
                print(l)
        except DissallowedCharacterError as err:
            print('Syntaxfel på rad', err.pos_start.line)
        except Exception as err2:
            raise Exception
            print(err2)


def kattis_run():
    input_str = sys.stdin.read()
    try:
        lexer = Lexer(input_str)
        tokens = lexer.tokenize()
        # print(tokens)
        parser = Parser(tokens)
        expressions = parser.parse()
        # print(expressions)
        interperator = Interperator(expressions)
        lines = interperator.interperete()
        for l in lines:
            print(l)
    except DissallowedCharacterError as err:
        print('Syntaxfel på rad', err.pos_start.line)
    except Exception as err2:
        raise Exception
        print(err2)


def custom_run():
    text = '''REP 2 ""
    DOWN. 
    FORW 1.""'''
    try:
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        # print(tokens)
        parser = Parser(tokens)
        expressions = parser.parse()
        # print(expressions)
        interperator = Interperator(expressions)
        lines = interperator.interperete()
        for l in lines:
            print(l)
    except DissallowedCharacterError as err:
        print('Syntaxfel på rad', err.pos_start.line)
    except Exception as err2:
        raise Exception
        print(err2)


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    # local_run()
    # kattis_run()
    # custom_run()

    # lexer = Lexer(test)
    # tokens = lexer.tokenize()
    # print(tokens)
    # parser = Parser(tokens)
    # expressions = parser.parse()
    # print('Syntaxfel på rad', e.pos_start.line)
