from bson import ObjectId
from collections import Counter


def delete_Tbd(collection):
    """
    Eliminare tuple che non hanno voti degli utenti, e moltiplicare i voti degli utenti x10
    :param collection: La collection Game del db
    """
    for score in collection.find():
        if score['user score'] == "tbd":
            collection.delete_one({"_id": ObjectId(str(score['_id']))})
        else:
            query = {"_id": ObjectId(str(score['_id']))}
            newscore = {"$mul": {'user score': 10}}
            collection.update_one(query, newscore)


def int_value(collection):
    """
    Trasformare i voti del campo user score in interi
    :param collection: La collection Game del db
    """
    for game in collection.find():
        user_score = game['user score']
        user_score = int(user_score)
        collection.update_one({"_id": ObjectId(str(game['_id']))}, {"$set": {"user score": user_score}})


def delete_duplicate_genre(collection):
    """
    Eliminare i duplicati presenti all'interno del campo genere
    :param collection: La collection Game del db
    """
    for genre in collection.find():
        input = str(genre['genre']).split(",")
        output = Counter(input)
        output = ",".join(output.keys())
        query = {"_id": ObjectId(str(genre['_id']))}
        newgenre = {"$set": {'genre': output}}
        collection.update_one(query, newgenre)


def lowercase_data(collection):
    """
    Effettuare il lower delle stringhe di nome, piattaforma, developer e genere
    :param collection: La collection Game del db
    """
    for game in collection.find():
        name = str(game["name"]).lower()
        platform = str(game["platform"]).lower()
        developer = str(game["developer"]).lower()
        genre = str(game["genre"]).lower()
        query = {"_id": ObjectId(str(game['_id']))}
        lower = {"$set": {
            'name': name,
            'platform': platform,
            'developer': developer,
            'genre': genre
        }}
        collection.update_one(query, lower)
