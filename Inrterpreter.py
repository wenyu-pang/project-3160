#wenyu pang
#Class Initialization
import re

class Interpreter:
    def __init__(it):
        it.variables = {}
#make the program run
    def run(it, program):
        l = program.split("\n")
        for line in l:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            if not it.assignment(line):
                print("error: Missing semicolon at the end of line.")
                return
        it.print_variables()
#make the function Assignments
    def assignment(it, l):
        if not l.endswith(";"):  # Check for missing semicolon
            print("error: Missing semicolon at the end of line.")
            return False
        l = l[:-1].strip()  # Remove semicolon
        p = l.split("=", 1)
        if len(p) != 2:
            print("error: Invalid assignment format.")
            return False
        
        identifier, expression = p[0].strip(), p[1].strip()
        if not it.identifier(identifier):
            print("error: Invalid identifier")      
            return False
        
        value = it.expression(expression)
        if value is None:
            print("error: Invalid expression")  
            return False
        
        it.variables[identifier] = value
        return True
    #make the function identifier
    def identifier(it, identifier):
        return re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", identifier) is not None
    #make the function Expressions
    def  expression (self, expression):
        try:
            value = self.evaluate_add_sub(expression)
            return value
        except:
            return None
    #make the function Handling Addition and Subtraction
    def evaluate_add_sub(it, expression):
        terms = re.split(r"(?=\+)|(?=\-)", expression)
        result = it.evaluate_term(terms[0].strip())
        if result is None:
            raise ValueError("Invalid term")
        
        for term in terms[1:]:
            term = term.strip()
            if term.startswith("+"):
                result += it.evaluate_term(term[1:].strip())
            elif term.startswith("-"):
                result -= it.evaluate_term(term[1:].strip())
        
        return result
    #make the function Handling Multiplication
    def evaluate_term(it, term):
        factors = term.split("*")
        result = it.factor(factors[0].strip())
        if result is None:
            raise ValueError("Invalid factor")
        
        for factor in factors[1:]:
            factor_value = it.factor(factor.strip())
            if factor_value is None:
                raise ValueError("Invalid factor")
            result *= factor_value
        
        return result
    #make the function Evaluating Individual Factors
    def factor(it, factor):
        factor = factor.strip()

        # Literal check
        if re.match(r"^\d+$", factor):
            if factor.startswith("0") and len(factor) > 1:
                raise ValueError("Invalid literal with leading zero")
            return int(factor)
        
        # Identifier check
        if it.identifier(factor):
            return it.get_variable_value(factor)
        
        # Parentheses
        if factor.startswith("(") and factor.endswith(")"):
            return it.expression(factor[1:-1])
        
        # Unary operations
        if factor.startswith("-"):
            return -it.factor(factor[1:].strip())
        if factor.startswith("+"):
            return it.factor(factor[1:].strip())
        
        raise ValueError("Invalid factor")

    def get_variable_value(it, identifier):
        if identifier in it.variables:
            return it.variables[identifier]
        raise ValueError("Uninitialized variable")

    def print_variables(it):
        for name, value in it.variables.items():
            print(f"{name} = {value}")

# Example usage
interpreter = Interpreter()

# Sample inputs
program1 = "x = 001;"
program2 = "x_2 = 0;"
program3 = "x = 0\ny = x;\nz = ---(x+y);"
program4 = "x = 1;\ny = 2;\nz = ---(x+y)*(x+-y);"
#Output all the answer
print("Input 1")
print(program1)
interpreter.run(program1)  # Output: error

print("\nInput 2")
print(program2)
interpreter.run(program2)  # Output: x_2 = 0

print("\nInput 3")
print(program3)
interpreter.run(program3)  # Output: error

print("\nInput 4")
print(program4)
interpreter.run(program4)  # Output: