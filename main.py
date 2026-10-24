from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

from employee_data import INITIAL_EMPLOYEES


class EmployeeFields(BaseModel):
    name: str
    email: str
    department: str
    job_title: str


class Employee(EmployeeFields):
    id: int


app = FastAPI(title="Employee API")
employees: dict[int, Employee] = {
    employee.id: employee
    for employee in (Employee.model_validate(record) for record in INITIAL_EMPLOYEES)
}


@app.get("/employees", response_model=list[Employee])
def list_employees() -> list[Employee]:
    return list(employees.values())


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int) -> Employee:
    employee = employees.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(fields: EmployeeFields) -> Employee:
    employee_id = max(employees, default=0) + 1
    employee = Employee(id=employee_id, **fields.model_dump())
    employees[employee_id] = employee
    return employee


@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, fields: EmployeeFields) -> Employee:
    if employee_id not in employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    employee = Employee(id=employee_id, **fields.model_dump())
    employees[employee_id] = employee
    return employee


@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int) -> Response:
    if employees.pop(employee_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
