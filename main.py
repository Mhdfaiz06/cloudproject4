from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI()

# In-memory databases
students = {}
classes = {}
class_students = {}

# Models
class Student(BaseModel):
    first_name: str
    last_name: str
    middle_name: str = ""
    age: int
    city: str

class Class(BaseModel):
    class_name: str
    description: str
    start_date: date
    end_date: date
    hours: int

# Endpoints

# 1. Capture student details
@app.post("/students")
def create_student(student: Student):
    student_id = len(students) + 1
    students[student_id] = student
    return {"student_id": student_id, "student": student}

# 2. Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = updated
    return {"student_id": student_id, "student": updated}

# 3. Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted"}

# 4. Create class
@app.post("/classes")
def create_class(cls: Class):
    class_id = len(classes) + 1
    classes[class_id] = cls
    class_students[class_id] = []
    return {"class_id": class_id, "class": cls}

# 5. Update class
@app.put("/classes/{class_id}")
def update_class(class_id: int, updated: Class):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    classes[class_id] = updated
    return {"class_id": class_id, "class": updated}

# 6. Delete class
@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    del classes[class_id]
    del class_students[class_id]
    return {"message": "Class deleted"}

# 7. Register student to class
@app.post("/classes/{class_id}/students/{student_id}")
def register_student(class_id: int, student_id: int):
    if class_id not in classes or student_id not in students:
        raise HTTPException(status_code=404, detail="Class or student not found")
    class_students[class_id].append(student_id)
    return {"message": f"Student {student_id} registered to class {class_id}"}

# 8. Get students in class
@app.get("/classes/{class_id}/students")
def list_students_in_class(class_id: int):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    student_list = [students[sid] for sid in class_students[class_id]]
    return {"students": student_list}
