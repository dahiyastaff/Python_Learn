from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Query
from pydantic import BaseModel,EmailStr

from employee_data import INITIAL_EMPLOYEES


class EmployeeFields(BaseModel):
    name: str
    email: EmailStr
    department: str
    job_title: str
    salary: float


class Employee(EmployeeFields):
    id: int


app = FastAPI(title="Employee API")
employees: dict[int, Employee] = {
    employee.id: employee
    for employee in (Employee.model_validate(record) for record in INITIAL_EMPLOYEES)
}


@app.get("/employees", response_model=list[Employee])
def sort_employees(
    sort_by: str = Query(default="id", description="Field to sort by: id, name, email, department, job_title, salary"),
    order: str = Query(default="asc", description="Sort order: asc or desc"),
) -> list[Employee]:
    if sort_by not in {"id", "name", "email", "department", "job_title", "salary"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sort_by must be one of: id, name, email, department, job_title, salary",
        )
    if order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order must be either asc or desc",
        )

    return sorted(employees.values(), key=lambda employee: getattr(employee, sort_by), reverse=order == "desc")


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
