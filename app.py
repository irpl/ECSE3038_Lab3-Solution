from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import Response
from bson import ObjectId
import motor.motor_asyncio
import pydantic
import datetime

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://ecse3038-lab3-tester.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://week4:Lb30oh1KEZTEVypf@cluster0.cklfqkn.mongodb.net/?retryWrites=true&w=majority")
db = client.tanks

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

@app.get("/profile")
async def get_profile():
  profile = await db["profile"].find().to_list(1)
  if (len(profile) > 0):
    return profile[0]
  return {}

@app.post("/profile", status_code=201)
async def create_profile(request: Request):
  profile_object = await request.json()
  
  profile_object["last_updated"] = datetime.datetime.now()

  inserted_profile = await db["profile"].insert_one(profile_object)

  profile = await db["profile"].find_one({"_id": inserted_profile.inserted_id})
  return profile

@app.get("/data")
async def get_all_todos():
  tanks = await db["tanks"].find().to_list(999)
  return tanks

@app.post("/data", status_code=201)
async def create_new_todo(request: Request):
  tank_object = await request.json()

  new_tank = await db["tanks"].insert_one(tank_object)
  created_tank = await db["tanks"].find_one({"_id": new_tank.inserted_id})

  return created_tank

@app.patch("/data/{id}")
async def change_location(id: str, request: Request):
  location_update = await request.json()

  update_result = await db["tanks"].update_one({"_id": ObjectId(id)}, {"$set": location_update})

  if update_result.modified_count == 1:
    updated_tank = await db["tanks"].find_one({"_id": ObjectId(id)})
    return updated_tank
  
  raise HTTPException(status_code=404, detail=f"Tank {id} not found")

@app.delete("/data/{id}")
async def delete_tank_by_id(id: str):
  delete_result = await db["tanks"].delete_one({"_id": ObjectId(id)})

  if delete_result.deleted_count == 1:
      return Response(status_code=status.HTTP_204_NO_CONTENT)

  raise HTTPException(status_code=404, detail=f"Tank {id} not found")




