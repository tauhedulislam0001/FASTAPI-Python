from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "jhon",
        "age": 17,
        "class": "year 12"
    },
    2: {
        "name": "salman",
        "age": 27,
        "class": "year 19"
    }
}


class Student(BaseModel):
    name: str
    age: int
    year: str

    class Config:
        arbitrary_types_allowed = True

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

# gt = greaterthen
# lt = lessthen
# ge = greaterthen or equal
# le = lessthen or equal

@app.get("/")
def index():
    return {"name": "First Data"}


@app.get("/get-students/{student_id}")
def get_student(student_id: int = Path(..., description="This ID of the student you want to view", gt=0)):
    return students.get(student_id)


# query parameter
# google.com/results?search=Python

@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None, test : int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}


# request body and the post method
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exist"}

    students[student_id] = student
    return students[student_id]


# request put method
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error:", "Student Doesn't exit"}

    student_data = students[student_id]  # Get the existing student data
    if student.name is not None:
        student_data["name"] = student.name
    if student.age is not None:
        student_data["age"] = student.age
    if student.year is not None:
        student_data["year"] = student.year

    return student_data  # Return the updated student data


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exit"}

    del students[student_id]
    return {"Message:" "Student deleted successfully!"}