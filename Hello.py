# Addition of two numbers
num1 = 10
num2 = 20
sum = num1 + num2
print("The sum of", num1, "and", num2, "is", sum)

# Subtraction of two numbers
difference = num1 - num2        
print("The difference between", num1, "and", num2, "is", difference)

# Multiplication of two numbers AA
product = num1 * num2       
print("The product of", num1, "and", num2, "is", product)

employee_List = ["Alice", "Bob", "Charlie", "David"]
print("Employee List:", employee_List)

def greet(name):
    print("Hello, " + name + "! Welcome to the company.")
    
greet("Alice")
greet("Bob")
greet("8")

class Employee:
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
    
    def display_info(self):
        print(f"Employee ID: {self.employee_id}, Name: {self.name}, Salary: {self.salary}")
    
    def update_salary(self, new_salary):
        self.salary = new_salary
        print(f"Salary updated to {self.salary}")
    def len(self):
        return len(self.name)

# Example usage
emp1 = Employee("AliceMargo", 101, 50000)
emp1.display_info()
emp1.update_salary(55000)
emp1.display_info()

className = emp1.__class__
print ("Class Name:", className)
ss = emp1.len()

print("Length of employee name:", ss)

class Sumit:
    pass

objSumit = Sumit()
print(objSumit)
print(isinstance(objSumit, Sumit))
print(isinstance(Employee, object))

