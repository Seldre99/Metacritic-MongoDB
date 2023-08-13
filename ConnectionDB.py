from pymongo import MongoClient


def get_database():
    """
    Funzione per effettuare l'accesso a mongodb, in CONNECTION_STRING inserire la path di connessione a MongoDB
    :return: database Metacritic_VideoGames
    """
    CONNECTION_STRING = "" 
    client = MongoClient(CONNECTION_STRING)
    return client['Metacritic_VideoGames']
