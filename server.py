from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
import base64
import json
import uuid
from pymongo import MongoClient
from urllib.parse import urlencode

# MongoDB setup
client = MongoClient("mongodb://localhost:27017") # instance of our DataBase 
db = client.redirect_service  # DB create DB directory / move to directory 
collection = db.mappings     # Directory create new table / move to this table 

app = FastAPI()              # toggleing the apies to work 

# our encoding function we feed it parametrs and it gives us back a unic code . 
def encode_params(keyword: str, src: str, creative: str) :
    data = {"k": keyword, "s": src, "c": creative}
    json_str = json.dumps(data, separators=(',', ':')) # convert into json from pyton 
    # remove spaces so it will be encoded clearly  ( , : )

    #use base64 to encode our params and make a code 
    #( first we take json into bits encode it into a code and decode it back into a string )

    b64 = base64.urlsafe_b64encode(json_str.encode()).decode()
    return b64   # return the encripted string 



# the decoding function where we feed it with our encripted code 
# and we get our 3 parameters back .
def decode_param(our_param: str) :
    try:
        #we got a string we invert it into bits decode back into our first bits and decode it back into a string . 
        json_str = base64.urlsafe_b64decode(our_param.encode()).decode()
        return json.loads(json_str)  # turn json into pyton dict 
    
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid our_param")





# API Endpoints
# the  first task get 3 parameters encode them and redirect the user to the correct url . 
@app.get("/redirect")
async def redirect_user(keyword: str, src: str, creative: str):
    # Check if params already exist in our collection 
    mapping = collection.find_one({"keyword": keyword, "src": src, "creative": creative})
    if mapping:# if you found one of the key words you will get a code that was created before . 
        our_param = mapping["our_param"]
    else: # if you did not find thouse key words we will create a new encrypted code . 
        our_param = encode_params(keyword, src, creative)
        #storing the key words and the code 
        collection.insert_one({"keyword": keyword, "src": src, "creative": creative, "our_param": our_param})

    # diffrent redirections . 
    if src.lower() == "google":
        base_url = "https://google-affiliate.com"
    elif src.lower() == "facebook":
        base_url = "https://facebook-affiliate.com"
    else:
        base_url = "https://affiliate-network.com"

    redirect_url = f"{base_url}?{urlencode({'our_param': our_param})}"
    return RedirectResponse(redirect_url)

@app.get("/retrieve_original")
async def retrieve_original(our_param: str):
    try:
        data = decode_param(our_param) # just use the base64 encoding algo to get back our params 
        return JSONResponse(content=data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid our_param")
    
    
class RefreshRequest(BaseModel):
    keyword: str
    src: str
    creative: str

# funtion that helps us create new personal code 
@app.post("/refresh_code")
async def refresh_code(req: RefreshRequest):
    new_param = str(uuid.uuid4())   # recreating new personal code 

    # Try to find existing mapping
    TheOne = collection.find_one({
        "keyword": req.keyword,
        "src": req.src,
        "creative": req.creative
    })

        # switching old code with new one 
    if TheOne:
        old_param = TheOne["our_param"]
        updates = {
            "$set": {"our_param": new_param},
            "$push": {"prev_params": old_param}
        }

        # Only set original_param if it doesn't exist yet
        if "original_param" not in TheOne:
            updates["$set"]["original_param"] = old_param

        
        # actuall updating every thing . befor it was all a setup for this one 
        collection.update_one(
            {"_id": TheOne["_id"]}, updates
        )

    else:
        # First time: set all fields // not sure needed but lets say we added this too . 
        collection.insert_one({
            "keyword": req.keyword,
            "src": req.src,
            "creative": req.creative,
            "our_param": new_param,
            "original_param": new_param,
            "prev_params": []
        })      

    return {"new_our_param": new_param}
 # some thing that was not asked , creates new code only by feeding the old Pcode    
@app.post("/refresh_by_code")
async def refresh_by_code(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    record = collection.find_one({"our_param": code})

    if not record:
        raise HTTPException(status_code=404, detail="Code not found")

    new_param = str(uuid.uuid4())
    updates = {
        "$set": {"our_param": new_param},
        "$push": {"prev_params": code}
    }

    if "original_param" not in record:
        updates["$set"]["original_param"] = code

    collection.update_one({"_id": record["_id"]}, updates)

    return {"new_our_param": new_param}


# knowing the base first created source code  is allwayes usefull . 
@app.get("/retrieve_original")
async def retrieve_original(our_param: str):
    if not our_param:
        raise HTTPException(status_code=400, detail="Missing our_param")
# using our prebuilt function to retrive function . 
    try:
        data = decode_param(our_param)
        return JSONResponse(content=data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted our_param")

