from pydantic import BaseModel
from typing import Optional, List

class Student(BaseModel):
    name: str
    age: int

class StudentDetail(BaseModel):
    location: str
    email: str
    number: str  
    student_id: str

class DetailsResponse(StudentDetail):
    id: str

class StudentResponse(Student):
    id: str  
    details: Optional[DetailsResponse] = None  

class FullResponse(Student):
    id: str  
    details: Optional[DetailsResponse] = None

def get_student(student) -> StudentResponse:
    return StudentResponse(id=str(student["_id"]), name=student["name"], age=student["age"])

def get_details(details) -> DetailsResponse:
    return DetailsResponse(
        id=str(details['_id']),
        location=details["location"],
        email=details["email"],
        number=str(details["number"]),  
        student_id=str(details["student_id"])
    )
    
def get_full_details(student) -> FullResponse:
    return FullResponse(
        id=str(student["_id"]), 
        name=student["name"], 
        age=student["age"],
        details=None  
    )


