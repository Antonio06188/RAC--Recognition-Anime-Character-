import pandas as pd
from typing import Union, Any
from collections import Counter

class OpeningInformation : 
    def __init__(self, op_nb : int, op_name : str, op_artist_name : str, url : str):
        self.op_nb = op_nb
        self.op_name = op_name
        self.op_artist_name = op_artist_name
        self.url = url
        
    def __eq__(self, other):
        if not isinstance(other, OpeningInformation):
            return NotImplemented
        return self.op_nb == other.op_nb and self.op_name == other.op_name and self.op_artist_name == other.op_artist_name and self.url == other.url
    
    def __str__(self):
        returned_str = f"- Opening {self.op_nb} : {self.op_name}\n"
        returned_str += f"    x Interprète : {self.op_artist_name}\n"
        returned_str += f"    x Youtube URL : {self.url}\n"
        return returned_str
    
class AnimeInformation :
    def __init__(self, anime_name : str, list_ops : list[OpeningInformation]):
        self.anime_name = anime_name
        self.list_ops = list_ops
        
    def __eq__(self, other):
        if not isinstance(other, AnimeInformation):
            return NotImplemented
        return self.anime_name == other.anime_name and Counter(self.list_ops) == Counter(other.list_ops)
    
    def __str__(self):
        returned_str = f"Anime Name : {self.anime_name}\n"
        for op in self.list_ops :
            returned_str += f"{op}\n"
        return returned_str

class CharacterConverter:
    def arg_tools(self, x, op_arg : dict[str, str]) -> dict[str, Any]:
        #print(x)
        new_dict = {k : x[v] for k,v in op_arg.items()}
        #print(new_dict)
        return new_dict
    
    # character_path is the path of the database linking the character with the anime
    # character_columns : {"key" : with the name of the column with the name of character, "value" : with the name of the column with the name of the anime}
    # anime_path is the path of the database linking the anime with the openings
    # anime_columns is the dict with {"anime_arg" : {"anime_name" : with the name of the columns with the name of the anime}
    #                                 "op_arg" : {"op_nb" : column's name of the op_nb, "op_name" : column's name of the name of op,
    #                                             "op_artist_name" : column's name of the interpret, "url" : column's name of the youtube url}}
    def __init__(self, character_path : str, characters_columns : dict[str, str], anime_path : str, anime_arg : dict[str, Union[dict[str, str]], str]):
        df_character = pd.read_json(character_path)
        self.character_to_anime = df_character.groupby(characters_columns["key"])[characters_columns["value"]].apply(set).to_dict()
        df_anime = pd.read_json(anime_path)
        op_args = anime_arg["op_arg"]
        # print(df_anime)
        #df_anime["animeInfos"] = df_anime.apply(lambda x : OpeningInformation(**self.arg_tools(x, op_args)), axis=1)
        anime_dict = df_anime.groupby(anime_arg["anime_arg"]["anime_name"]).apply(lambda g: AnimeInformation(
            anime_name=g.name,
            list_ops=[OpeningInformation(**self.arg_tools(row, op_args)) for _, row in g.iterrows()]
        )).to_dict()
        self.anime_with_opening = anime_dict
        
    
    def getAnimes(self, character_name) :
        return self.character_to_anime.get(character_name)
    
    def getAnimeInformation(self, anime_name) -> AnimeInformation:
        return self.anime_with_opening.get(anime_name)
        