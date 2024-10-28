from fastapi import APIRouter , HTTPException
from MongoDB.schema import *
from Database.db import *
from typing import List
from bson import ObjectId

router = APIRouter()

@router.get("/student", response_model=List[StudentResponse])
async def read_students():
    try:
        students = []
        async for student in student_collection.find():
            students.append(get_student(student))
        return students
    except:
        raise HTTPException(status_code=404,detail='Database not found')



@router.post('/student',response_model=StudentResponse)
async def create_student(student : Student):
    try:
        student_dict = student.dict()
        result = await student_collection.insert_one(student_dict)
        student_dict[id] = result.inserted_id
        return get_student(student_dict)
    except:
        raise HTTPException(status_code=404, detail='Database not found')
    

@router.delete("/delete",response_model=dict)
async def delete_student(student_id : str):
    try:
        result = await student_collection.delete_one({'_id':ObjectId(student_id)})
        
        if result.deleted_count == 0:
            raise HTTPException ( status_code=404, detail= ' Student not found')
        
        return { 'Detail' : 'Student deleted Successfully'}
    
    except:
        raise HTTPException(status_code=404 , detail= 'Database not found')

@router.put("/student",response_model=StudentResponse)
async def update_student(student_id : str, student : Student):
    try:
        student_dict = student.model_dump()
        result = await student_collection.update_one({'_id':ObjectId(student_id)},{"$set": student_dict})
        if result.upserted_id == 0 :
            raise HTTPException( status_code= 404 , detail= 'Student not found')
        student_dict["_id"] = student_id
        return get_student(student_dict)
    except : 
        raise HTTPException(status_code= 404, detail='Database not found')
    
    


@router.get("/studentdetail", response_model=List[FullResponse])
async def full_detail_students():
    try:
        students = []
        async for student in student_collection.find():
            student_data = get_full_details(student)  # Use the correct function here
            detail = await detail_collection.find_one({'student_id': student_data.id})
            student_data.details = get_details(detail) if detail else None
            students.append(student_data)
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))