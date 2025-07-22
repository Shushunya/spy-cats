from fastapi import HTTPException
import httpx

async def validate_cat_breed(breed: str):
    
    if not breed:
        breed = "abys"
    else:
        breed = breed.lower()

    async with httpx.AsyncClient() as client:
        breed_API_URL = f"https://api.thecatapi.com/v1/breeds/{breed}"
        response = await client.get(breed_API_URL)
        
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid cat breed")

    return response.json()
