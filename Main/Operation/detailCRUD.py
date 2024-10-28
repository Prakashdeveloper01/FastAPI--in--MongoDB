from fastapi import APIRouter , HTTPException
from MongoDB.schema import *
from Database.db import *
from typing import List
from bson import ObjectId

detail_router = APIRouter()

@detail_router.get("/studentdetails", response_model=List[DetailsResponse])
async def read_students_Detail():
    try:
        details = []
        async for detail in detail_collection.find():
            details.append(get_details(detail))
        return details
    except:
        raise HTTPException(status_code=404,detail='Database not found')
    
@detail_router.post('/studentdetail',response_model=DetailsResponse)
async def create_detail(detail : StudentDetail):
    details_dict = detail.dict()
    result = await detail_collection.insert_one(details_dict)
    details_dict[id] = result.inserted_id
    return get_details(details_dict)

@detail_router.delete("/detail",response_model=DetailsResponse)
async def delete_detail(detail_id : str):
    result = await detail_collection.delete_one({'_id':ObjectId(detail_id)})
    
    if result.deleted_count == 0:
        raise HTTPException( status_code= 404 ,detail='Database not found')
    
    return {'Detail':'Deleted Successfully'}

@detail_router.put("/detail",response_model=DetailsResponse)
async def update_detail(detail_id : str , detail : StudentDetail):
    detail_dict = detail.dict()
    result  = await detail_collection.update_one({'_id':ObjectId(detail_id)},{'$set':detail_dict})
    
    if result.upserted_id == 0:
        raise HTTPException (status_code= 404 , detail='Detail not found')
    
    detail_dict['_id'] = detail_id
    return get_details(detail_dict)