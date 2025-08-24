#CONSOLE LINE CALCULATOR

class Calculations:
    def add(n, m):
        return n + m
    def subtract(n, m):
        return n - m
    def multiply(n, m):
        return n * m
    def divide(n, m):
        return n / m
    def power(n, m):
        return pow(n, m)
    def floor_division(n , m):
        return n // m
    def remainder(n, m):
        return n % m

class Operations:
    @staticmethod
    def run():
        operators = input("Choose operation (+, -, ^, /, **, //, %): ")
        try:
            n = float(input("Enter 1st number: "))
            m = float(input("Enter 2nd number: "))
        except ValueError:
            print("Please enter valid numbers.")
            return

        match operators:
            case "+":
                print(n, "+", m, "=", Calculations.add(n, m))
            case "-":
                print(n, "-", m, "=", Calculations.subtract(n, m))
            case "*":
                print(n, "*", m, "=", Calculations.multiply(n , m))
            case "/":
                print(n, "/", m, "=", Calculations.divide(n, m))
            case "**" | "^":
                print(n, "**", m, "=", Calculations.power(n, m))
            case "//":
                print(n, "//", m, "=", Calculations.floor_division(n, m))
            case "%":
                print(n, "%", m, "=", Calculations.remainder(n, m))
            case _:
                print("INVALID OPERATOR")

Operations.run()