from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client['student']  
student_collection = db['students']  
detail_collection = db['studentdetails']