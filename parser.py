from expressions import *
from tokeniser import *

class Parser:
    def __init__(self,tokens : list):
        self.tokens = tokens
        self.pos = 0
    
    def consume(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    
    def peek(self) -> Token:
        return self.tokens[self.pos]
    
    def expect(self,type):
        token = self.consume()

        if(token.type != type):
            raise ValueError(f"Expected {type}, got {token.type}({token.value})")
        return token
    
    def parse(self):
        result = self.parse_expr()
        self.expect(END)
        return result

    def primary(self):
        token = self.consume()

        if token.type == NUMBER:
            return Const(float(token.value))
        
        elif token.type == IDENTIFIER:
            if self.peek().type != LPAREN:
                if token.value == "e":
                   return Const(E)
                return Var(token.value)
            
            else:
                self.consume()
                arg = self.parse_expr()
                self.expect(RPAREN)

                name = token.value.lower()
                if name in FUNCTION_MAP:
                    return FUNCTION_MAP[name](arg)
                else:
                    raise ValueError(f"Unexpected Token:{token}")
        
        elif token.type == LPAREN:
            expr = self.parse_expr()
            self.expect(RPAREN)
            return expr
        
        else:
            raise ValueError(f"Unexpected Token {token}")
        
    def parse_power(self):
        left = self.primary()
            
        if(self.peek().type == POW):
            self.consume()
            right = self.parse_unary()
            return Pow(left,right)
        
        return left
        
    def parse_unary(self):
        if(self.peek().type == MINUS):
            self.consume()
            right = self.parse_unary()
            return Neg(right)
        
        else:
            return self.parse_power()

    def parse_term(self):
        left = self.parse_unary()
        
        while self.peek().type == MUL or self.peek().type == DIV:
            operator = self.consume()
            right = self.parse_unary()

            if operator.type == MUL:
                left = Mul(left,right)
            else:
                left = Div(left,right)

        return left

    def parse_expr(self):
        left = self.parse_term()

        while self.peek().type == PLUS or self.peek().type == MINUS:
            operator = self.consume()
            right = self.parse_term()

            if operator.type == PLUS:
                left = Add(left,right)
            else:
                left = Sub(left,right)
            
        return left
