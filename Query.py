import datetime
from collections import ChainMap


def insert_game(collection, name, platform, year, month, day, score, user_score, developer, genre, critics, users):
    """
    Query di inserimento con dati passati dall'utente
    """
    data = datetime.datetime(year, month, day)
    name = name.lower()
    developer = developer.lower()
    genre = genre.lower()
    collection.insert_one({
        "name": name,
        "platform": platform,
        "r-date": data,
        "score": score,
        "user score": user_score,
        "developer": developer,
        "genre": genre,
        "critics": critics,
        "users": users,
    })


def delete_game_by_name(collection, name):
    """
    Cancellazione di un gioco in base al nome
    """
    name = name.lower()
    result = collection.delete_many({
        "name": name
    })
    return result.deleted_count


def delete_game_by_name_and_platform(collection, name, platform):
    """
    Cancellazione di un gioco in base al nome e alla piattaforma
    """
    name = name.lower()
    platform = platform.lower()
    result = collection.delete_one({
        "name": name,
        "platform": platform,
    })
    return result.deleted_count


def delete_by_score(collection, score):
    """
    Cancellazione di giochi che hanno uno score minore dello score dato dall'utente
    """
    result = collection.delete_many({
        'score': {'$lte': score}
    })
    return result.deleted_count


def find_game_by_name(collection, name):
    """
    Ricerca di giochi in base al nome
    """
    name = name.lower()
    list = []
    for game in collection.find({"name": {'$regex': name}}):
        list.append(game)
    return list


def find_game_by_genre(collection, genre):
    """
    Ricerca di giochi in base al genere
    """
    genre = genre.lower()
    list = []
    for game in collection.find({"genre": {'$regex': genre}}):
        list.append(game)
    return list


def find_game_by_name_and_platform(collection, name, platform):
    """
    Ricerca di giochi in base al nome e alla piattaforma
    """
    name = name.lower()
    platform = platform.lower()
    game = collection.find_one({"$and": [{"name": {'$regex': name}}, {"platform": {'$regex': platform}}]})
    return game


def find_games_by_score(collection, score, operation, type):
    """
    Ricerca di giochi in base allo score > o < in base alla scelta dell'utente e al tipo di score scelto
    """
    list = []
    if type == "score":
        if operation == "maggiore":
            for game in collection.find({'score': {'$gte': score}}).sort("score", 1):
                list.append(game)
            return list
        elif operation == "minore":
            for game in collection.find({'score': {'$lte': score}}).sort("score", -1):
                list.append(game)
            return list
    elif type == "user score":
        if operation == "maggiore":
            for game in collection.find({'user score': {'$gte': score}}).sort("user score", 1):
                list.append(game)
            return list
        elif operation == "minore":
            for game in collection.find({'user score': {'$lte': score}}).sort("user score", -1):
                list.append(game)
            return list
    elif type == "critics":
        if operation == "maggiore":
            for game in collection.find({'critics': {'$gte': score}}).sort("critics", 1):
                list.append(game)
            return list
        elif operation == "minore":
            for game in collection.find({'critics': {'$lte': score}}).sort("critics", -1):
                list.append(game)
            return list
    elif type == "users":
        if operation == "maggiore":
            for game in collection.find({'users': {'$gte': score}}).sort("users", 1):
                list.append(game)
            return list
        elif operation == "minore":
            for game in collection.find({'users': {'$lte': score}}).sort("users", -1):
                list.append(game)
            return list


def find_games_by_developer(collection, developer):
    """
    Ricerca di giochi in base al genere
    """
    developer = developer.lower()
    list = []
    for game in collection.find({"developer": {'$regex': developer}}):
        list.append(game)
    return list


def update_game(collection, original_name, original_platform, name, platform, data, score, user_score, developer, genre,
                critics, users):
    """
    Modifica di un gioco
    """
    original_name = original_name.lower()
    original_platform = original_platform.lower()
    name = name.lower()
    platform = platform.lower()
    developer = developer.lower()
    genre = genre.lower()
    collection.update_one({'$and': [{"name": {'$regex': original_name}}, {"platform": {'$regex': original_platform}}]},
                          {"$set": {
                              "name": name,
                              "platform": platform,
                              "r-date": data,
                              "score": score,
                              "user score": user_score,
                              "developer": developer,
                              "genre": genre,
                              "critics": critics,
                              "users": users}})


def average_by_developer(collection, developer):
    """
    Funzione per il calcolo della media di score, user score, critiche e differenza score-user score di giochi di un dato developer
    """
    developer = developer.lower()
    list = []
    result = collection.aggregate([{"$match": {"developer": developer}},
                                   {"$group": {"_id": developer, "Media Score": {"$avg": "$score"},
                                               "Media Score Utenti": {"$avg": "$user score"},
                                               "Media delle Critiche": {"$avg": "$critics"}}},
                                   {"$addFields": {"Media Score": {"$round": ["$Media Score", 2]}}},
                                   {"$addFields": {"Media Score Utenti": {"$round": ["$Media Score Utenti", 2]}}},
                                   {"$addFields": {"Media delle Critiche": {"$round": ["$Media delle Critiche", 2]}}},
                                   {"$addFields": {"Differenza tra Score e Score Utenti": {"$subtract": ["$Media Score", "$Media Score Utenti"]}}},
                                   {"$addFields": {"Differenza tra Score e Score Utenti": {"$round": ["$Differenza tra Score e Score Utenti", 2]}}}])
    for i in result:
        list.append(i)
    return list


def average_by_genre(collection, genre):
    """
    Funzione per il calcolo della media di score, user score, critiche e differenza score-user score di giochi di un dato genere
    """
    genre = genre.lower()
    list = []
    result = collection.aggregate([{"$match": {"genre": {'$regex': genre}}},
                                   {"$group": {"_id": genre, "Media Score": {"$avg": "$score"},
                                               "Media Score Utenti": {"$avg": "$user score"},
                                               "Media delle Critiche": {"$avg": "$critics"}}},
                                   {"$addFields": {"Media Score": {"$round": ["$Media Score", 2]}}},
                                   {"$addFields": {"Media Score Utenti": {"$round": ["$Media Score Utenti", 2]}}},
                                   {"$addFields": {"Media delle Critiche": {"$round": ["$Media delle Critiche", 2]}}},
                                   {"$addFields": {"Differenza tra Score e Score Utenti": {"$subtract": ["$Media Score", "$Media Score Utenti"]}}},
                                   {"$addFields": {"Differenza tra Score e Score Utenti": {"$round": ["$Differenza tra Score e Score Utenti", 2]}}}])
    for i in result:
        list.append(i)
    return list


def sort_by_dates(collection, year1, year2, type):
    """
    Query per ottenere i giochi in base alla data di uscita in un range di anni specificato dall'utente
    :param year1: Anno >=
    :param year2: Anno <
    :param type: ascendente o discendente
    """
    data = datetime.datetime(year1, 1, 1)
    data2 = datetime.datetime(year2, 12, 31)
    list = []
    if type == "ascendente":
        for game in collection.find({"r-date": {"$gte": data, "$lt": data2}}).sort("r-date", 1):
            list.append(game)
    elif type == "discendente":
        for game in collection.find({"r-date": {"$gte": data, "$lt": data2}}).sort("r-date", -1):
            list.append(game)
    return list


def find_by_parameters(collection, name, platform, year, year2, score, operation_score, user_score, operation_user_score, developer, genre, critics, operation_critics, users, operation_users):
    """
    Funzione di ricerca in base ai parametri scelti dall'utente
    """
    if name is not None:
        name = name.lower()
    if platform is not None:
        platform = platform.lower()
    if developer is not None:
        developer.lower()

    if year is not None:
        data = datetime.datetime(year, 1, 1)
    if year2 is not None:
        data2 = datetime.datetime(year2, 12, 31)
    query = None
    if name is not None:
        query = {"name": {'$regex': name}}

    if platform is not None and query is not None:
        query = ChainMap(query, {"platform": {'$regex': platform}})
    elif platform is not None and query is None:
        query = {"platform": {'$regex': platform}}

    if year is not None and year2 is not None and query is not None:
        query = ChainMap(query, {"r-date": {"$gte": data, "$lt": data2}})
    elif year is not None and year2 is not None and query is None:
        query = {"r-date": {"$gte": data, "$lt": data2}}

    elif year is not None and query is not None:
        query = ChainMap(query, {"r-date": {"$gte": data}})
    elif year is not None and query is None:
        query = {"r-date": {"$gte": data}}

    if score is not None and operation_score == "maggiore" and query is not None:
        query = ChainMap(query, {'score': {'$gte': score}})
    elif score is not None and operation_score == "minore" and query is not None:
        query = ChainMap(query, {'score': {'$lte': score}})
    elif score is not None and operation_score == "maggiore" and query is None:
        query = {'score': {'$gte': score}}
    elif score is not None and operation_score == "minore" and query is None:
        query = {'score': {'$lte': score}}
    elif score is not None and operation_score is None and query is not None:
        query = ChainMap(query, {'score': score})
    elif score is not None and operation_score is None and query is None:
        query = {'score': score}

    if user_score is not None and operation_user_score == "maggiore" and query is not None:
        query = ChainMap(query, {'user score': {'$gte': user_score}})
    elif user_score is not None and operation_user_score == "minore" and query is not None:
        query = ChainMap(query, {'user score': {'$lte': user_score}})
    if user_score is not None and operation_user_score == "maggiore" and query is None:
        query = {'user score': {'$gte': user_score}}
    elif user_score is not None and operation_user_score == "minore" and query is None:
        query = {'user score': {'$lte': user_score}}
    elif user_score is not None and operation_user_score is None and query is not None:
        query = ChainMap(query, {'user score': user_score})
    elif user_score is not None and operation_user_score is None and query is None:
        query = {'user score': user_score}

    if developer is not None and query is not None:
        query = ChainMap(query, {"developer": {'$regex': developer}})
    elif developer is not None and query is None:
        query = {"developer": {'$regex': developer}}

    if genre is not None and query is not None:
        query = ChainMap(query, {"genre": {'$regex': genre}})
    elif genre is not None and query is None:
        query = {"genre": {'$regex': genre}}

    if critics is not None and operation_critics == "maggiore" and query is not None:
        query = ChainMap(query, {'critics': {'$gte': critics}})
    elif critics is not None and operation_critics == "minore" and query is not None:
        query = ChainMap(query, {'critics': {'$lte': critics}})
    if critics is not None and operation_critics == "maggiore" and query is None:
        query = {'critics': {'$gte': critics}}
    elif critics is not None and operation_critics == "minore" and query is None:
        query = {'critics': {'$lte': critics}}
    elif critics is not None and operation_critics is None and query is not None:
        query = ChainMap(query, {'critics': critics})
    elif critics is not None and operation_critics is None and query is None:
        query = {'critics': critics}

    if users is not None and operation_users == "maggiore" and query is not None:
        query = ChainMap(query, {'users': {'$gte': users}})
    elif users is not None and operation_users == "minore" and query is not None:
        query = ChainMap(query, {'users': {'$lte': users}})
    if users is not None and operation_users == "maggiore" and query is None:
        query = {'users': {'$gte': users}}
    elif users is not None and operation_users == "minore" and query is None:
        query = {'users': {'$lte': users}}
    elif users is not None and operation_users is None and query is not None:
        query = ChainMap(query, {'users': users})
    elif users is not None and operation_users is None and query is None:
        query = {'users': users}

    list = []
    for game in collection.find({"$and": [query]}):
        list.append(game)
    return list
