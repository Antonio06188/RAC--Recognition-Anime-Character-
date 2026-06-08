import model.characterConverter as cc
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import base64

ROOT_DATASET_PATH = "Dataset/Animes/"
character_path = "characters_to_animes.json"
opening_path = "animes_to_openings.json"
characterConverter = cc.CharacterConverter(character_path=ROOT_DATASET_PATH+character_path,
                                           characters_columns={"key" : "character_name", "value":"anime"},
                                           anime_path=ROOT_DATASET_PATH+opening_path,
                                           anime_arg={"anime_arg" : {"anime_name":"anime"},
                                                      "op_arg":{"op_nb":"opening_nb", "op_name":"opening_name",
                                                                "op_artist_name":"opening_artists","url":"opening_youtube_url"}})

print("*****************************************")
print("Character to Anime")
print(characterConverter.getAnimes("Midoriya Izuku"))
print("*******************************************")
print("Animes with Opening")
#print(df_anime)
print(characterConverter.getAnimeInformation("My Hero Academia"))

class Opening(BaseModel):
    op_number : int
    op_name : str
    op_artist : str
    youtube_url : str

class ResultTestPredict(BaseModel):
    original_img : str
    box_img : str
    crop_img : str
    character_name : str
    character_ref_img : str
    anime_name : str
    anime_ref_img : str
    openings : list[Opening]
    
def img_to_base64(img: Image.Image) -> str :
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

app = FastAPI()

# POST endpoint
@app.post("/predict-test/", response_model=ResultTestPredict)
async def predictTest(file : UploadFile = File(...)):
    original_img_byte = await file.read()
    original_img = Image.open(BytesIO(original_img_byte)).convert("RGB")
    
    original_img.show()
    
    box_img = Image.open("img2.jpg")
    crop_img = Image.open("img3.jpg")
    character_img = Image.open("izuku-midoriya.webp")
    anime_img = Image.open("my_hero_academia.jpg")
    character_name = "Midoriya Izuku"
    animes = list(characterConverter.getAnimes(character_name))

    anime_name = animes[0] if animes else None
    openings = characterConverter.getAnimeInformation(anime_name).list_ops
    
    return {
        "original_img" : img_to_base64(original_img),
        "box_img" : img_to_base64(box_img),
        "crop_img" : img_to_base64(crop_img),
        "character_name" : character_name,
        "character_ref_img" : img_to_base64(character_img),
        "anime_name" : anime_name,
        "anime_ref_img" : img_to_base64(anime_img),
        "openings" : [{"op_number":o.op_nb,
                               "op_name":o.op_name, 
                               "op_artist":o.op_artist_name,
                               "youtube_url":o.url} for o in openings]
    }

