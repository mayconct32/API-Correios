from fastapi import APIRouter


app = APIRouter()



@app.get("/zip/{zipcode}")
async def get_by_zip_code(
    zipcode: str
):
    pass


@app.get("/city/{city}")
async def get_by_city(
    city: str,
):
    pass
