from fastapi import FastAPI, HTTPException
from typing import List
from MongoDB.schema import * 
from Database.db import *
from Operation.studentCRUD import *
from Operation.detailCRUD import*

app = FastAPI()
app.include_router(router)
app.include_router(detail_router)