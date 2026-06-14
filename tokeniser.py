from dataclasses import dataclass
from Constants import *

@dataclass(frozen=True)
class Token:
    type : str
    value : str

    def __repr__(self):
        return f"{self.type}({self.value})"
    

def tokenise(expr : str):
    tokens = []
    
    i = 0
    while(i<len(expr)):

        if expr[i].isspace():
            i+=1
            continue

        elif expr[i].isdigit():
            nums=[]

            while i<len(expr) and (expr[i].isdigit() or expr[i] == "."):
                nums.append(expr[i])
                i+=1
            
            token = Token(NUMBER,"".join(nums)) 
            tokens.append(token)
        
        elif expr[i].isalpha():
            chars=[]

            while i<len(expr) and expr[i].isalnum():
                chars.append(expr[i])
                i+=1

            token = Token(IDENTIFIER,"".join(chars))
            tokens.append(token)
        
        elif expr[i] in "+-/*^()":
            token = Token(OPERATORS[expr[i]],expr[i])
            tokens.append(token)
            i+=1

        else:
            raise ValueError(f"Invalid character: {expr[i]}")
        
    tokens.append(Token(END,""))
    return tokens
