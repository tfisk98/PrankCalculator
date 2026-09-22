import os
import numpy as np
import pygame


class Calculator:

    def __init__(self):
        self.priority_opps = ['sqrt', 'log_', 'ln', 'exp', 'cos', 'sin', 'tan']
        self.secondary_opps = ['*', '/', '%', '^']
        self.final_opps = ['+', '-']

        #One object containing the readily sorted opperators. Equivalent to the above but more efficient
        self.operators = ['sqrt', 'log_', 'ln', 'exp', 'cos', 'sin', 'tan', '*', '/', '%', '^','+', '-']

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            self.error_sound()
            raise ValueError("Cannot divide by zero.")
        return a / b

    def modulus(self, a, b):
        if b == 0:
            self.error_sound()
            raise ValueError("Cannot perform modulus by zero.")
        return a % b

    def power(self, a, b):
        return a ** b

    def inverse(self, a):
        if a == 0:
            self.error_sound()
            raise ValueError("Cannot take inverse of zero.")
        return 1 / a

    def squreroot(self, a):
        if a < 0:
            self.error_sound()
            raise ValueError("Cannot take square root of a negative number.")
        return a ** 0.5

    def logarithm(self, a, base):
        if a <= 0 or base <= 0 or base == 1:
            self.error_sound()
            raise ValueError("Invalid input for logarithm.")
        import math
        return math.log(a, base)

    def natural_log(self, a):
        if a <= 0:
            self.error_sound()
            raise ValueError("Invalid input for natural logarithm.")
        import math
        return math.log(a)  

    def exponential(self, a):
        import math
        return math.exp(a)

    def cosine(self, a):
        import math
        return math.cos(a)

    def sine(self, a):
        import math
        return math.sin(a)  

    def tangent(self, a):   
        import math
        return math.tan(a)

    def operate(self, operation, a, b):
        print("operating")
        print(f"Operation: {operation}, a: {a}, b: {b}")
        if operation == "+":
            return self.add(a, b)
        elif operation == "-":
            return self.subtract(a, b)
        elif operation == "*":
            return self.multiply(a, b)
        elif operation == "/":
            return self.divide(a, b)
        elif operation == "%":
            return self.modulus(a, b)
        elif operation == "^" and b == -1:
            return self.inverse(a)
        elif operation == "^":
            #print("power")
            return self.power(a, b)
        elif operation == "sqrt":
            return a*self.squreroot(b)
        elif operation == "log_":
            return self.logarithm(a, b)
        elif operation == "ln":
            return a*self.natural_log(b)
        elif operation == "exp":
            print("exp")
            return a*self.exponential(b)
        elif operation == "cos":
            return a*self.cosine(b)
        elif operation == "sin":
            return a*self.sine(b)
        elif operation == "tan":
            return a*self.tangent(b)
        else:
            self.error_sound()
            raise ValueError("Invalid operation. Please choose from '+', '-', '*', or '/'.")



    def screen_to_operation(self, screen_input):

        # Check for parentheses
        print("screen_input:", screen_input)
        if '(' in screen_input and ')' in screen_input:
            inner_expression = self.select_parentheses(screen_input)
            if inner_expression is not None:
                result = self.screen_to_operation(inner_expression)
                screen_input = screen_input.replace(f'({inner_expression})', str(result))

        operation = self.find_operation(screen_input)
        
        if operation is None:
            #print("No valid operation found in the input.")
            return float(screen_input)  # Return the number as a float if no operation is found
            #raise ValueError("Invalid operation. Please choose valid operation.")

        parts = screen_input.split(operation)
        print("parts:", parts)

        # Check if operations to perform before other opeartions
        if self.find_operation(parts[0]) is not None:
            parts[0] = self.screen_to_operation(parts[0])
        if self.find_operation(parts[1]) is not None:
            parts[1] = self.screen_to_operation(parts[1])

        #  Provides a default left part, when an operation doesn't have one 
        if parts[0] == '':
            if operation in self.priority_opps : # functions like exponential, sine, cosine, log, ...
                parts[0] = '1'  # Default to 1 for unary operations
            if operation in self.secondary_opps : # operators like *, /, % 
                return int(parts[1]) if parts[1].is_integer() else float(parts[1])
            if operation in self.final_opps : # operators like + or -
                parts[0] = '0'  # Default to 1 for unary operations
        
        while len(parts) > 2:
            parts[len(parts)-2] = self.operate(operation, float(parts[len(parts)-2]), float(parts[len(parts)-1]))
            parts.pop()


        if operation in self.final_opps and parts[0] == '':
            parts[0] = '0'  # Default to 1 for unary operations

        try:
            a = float(parts[0])
            b = float(parts[1])
        except ValueError:
            print("Invalid numbers. Please provide valid numeric values for a and b.")
            self.error_sound()
            raise ValueError("Invalid numbers. Please provide valid numeric values for a and b.")
        print("result of operation:", self.operate(operation, a, b))
        return int(self.operate(operation, a, b)) if self.operate(operation, a, b).is_integer() else self.operate(operation, a, b)

    def find_operation(self, screen_input):
        for keys in self.operators:
            if keys in screen_input:
                return keys
        return None

    def find_parentheses(self, screen_input):
        stack = []
        for i, char in enumerate(screen_input):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if not stack:
                    self.error_sound()
                    raise ValueError("Mismatched parentheses.")
                start = stack.pop()
                return start, i
        if stack:
            self.error_sound()
            raise ValueError("Mismatched parentheses.")
        return None

    def select_parentheses(self, screen_input):
        parentheses = self.find_parentheses(screen_input)
        if parentheses:
            start, end = parentheses
            return screen_input[start + 1:end]
        return None

    def error_sound(self):
        path= os.getcwd()
        effect= pygame.mixer.Sound(path + '/error.wav')
        effect.play()
        pygame.time.wait(2000)