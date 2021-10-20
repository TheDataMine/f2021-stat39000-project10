import sqlite3
from fastapi import HTTPException
from .database import queries, database_path
from .schemas import Title, Genre, CrewMember

def get_movie_with_id(title_id: str) -> Title:
    # Get the movie info from the database, and close
    # the database connection
    conn = sqlite3.connect(database_path)
    result = queries.get_movie_with_id(conn, title_id = title_id)
    conn.close()
    
    # If the result wasn't a movie, raise an exception
    if result[1] != 'movie':
        raise HTTPException(status_code=422, detail=f"Title with title_id '{title_id}' is not a movie, it is a {result[1]}.")
    
    # Split the genres by comma, and create a list of Genre objects
    listed_genres = result[8].split(',')
    genres = []
    for genre in listed_genres:
        genres.append(Genre(**{key: genre for _, key in enumerate(Genre.__fields__.keys())}))
    
    # Create a Title object, but manually set the genres entry in the Title object
    # to our list of Genres objects.
    movie = {key: result[i] for i, key in enumerate(Title.__fields__.keys())}
    movie['genres'] = genres
    movie = Title(**movie)

    return movie


def get_cast_for_title(title_id: str) -> list[CrewMember]:
    # Get the cast for the movie, and close the database connection
    conn = sqlite3.connect(database_path)
    results = queries.get_cast_for_title(conn, title_id = title_id)
    conn.close()

    print(results)
    # Create a list of dictionaries, where each dictionary is a cast member
    cast = []
    for member in results:
        cast.append(CrewMember(**{key: member[i] for i, key in enumerate(CrewMember.__fields__.keys())}))

    return cast


def get_show_for_title(title_id: str) -> Title:
    # Get the tv info from the database, and close
    # the database connection
    conn = sqlite3.connect(database_path)
    result = queries.get_show_with_id(conn, title_id = title_id)
    conn.close()
    
    # If the result wasn't a tv series, raise an exception
    if result[1] != 'tvSeries':
        raise HTTPException(status_code=422, detail=f"Title with title_id '{title_id}' is not a tv series, it is a {result[1]}.")

    # Split the genres by comma, and create a list of Genre objects
    listed_genres = result[8].split(',')
    genres = []
    for genre in listed_genres:
        genres.append(Genre(**{key: genre for _, key in enumerate(Genre.__fields__.keys())}))

    # Create a Title object, but manually set the genres entry in the Title object
    # to our list of Genres objects.
    show = {key: result[i] for i, key in enumerate(Title.__fields__.keys())}
    show['genres'] = genres
    show = Title(**show)

    return show


def get_show_for_title_season_and_episode(title_id: str, season_number: int, episode_number: int) -> Title:
    # Get the episode info from the database, and close
    # the database connection
    conn = sqlite3.connect(database_path)
    result = queries.get_episode_for_title_season_number_episode_number(conn, title_id = title_id, season_number = season_number, episode_number = episode_number)
    title_type = queries.get_title_type(conn, title_id = title_id)
    seasons_in_show = queries.get_seasons_in_show(conn, title_id = title_id)
    episodes_in_season = queries.get_episodes_in_season(conn, title_id = title_id, season_number = season_number)
    conn.close()

    # If the result wasn't a tv series, raise an exception
    if title_type != 'tvSeries':
        raise HTTPException(status_code=422, detail=f"Title with title_id '{title_id}' is not a tv series, it is a {title_type}.")

    # If the season requested doesn't exist
    if seasons_in_show < 1 or season_number > seasons_in_show:
        raise HTTPException(status_code=422, detail=f"There are only {seasons_in_show} seasons for this show, you requested information about season {season_number}.")

    # If the season requested has < 1 episodes or more than the number of episodes in the season
    if episode_number < 1 or episode_number > episodes_in_season:
        raise HTTPException(status_code=422, detail=f"Season {season_number} only {episodes_in_season} episodes and you requested episode {episode_number}.")

    # Split the genres by comma, and create a list of Genre objects
    listed_genres = result[8].split(',')
    genres = []
    for genre in listed_genres:
        genres.append(Genre(**{key: genre for _, key in enumerate(Genre.__fields__.keys())}))

    # Create a Title object, but manually set the genres entry in the Title object
    # to our list of Genres objects.
    episode = {key: result[i] for i, key in enumerate(Title.__fields__.keys())}
    episode['genres'] = genres
    episode = Title(**episode)

    return episode


def get_episodes_for_season(title_id: str, season_number) -> list[Title]:
    # Get the episode info from the database, and close
    # the database connection
    conn = sqlite3.connect(database_path)
    results = queries.get_episodes_for_season(conn, title_id = title_id, season_number = season_number)
    title_type = queries.get_title_type(conn, title_id = title_id)
    seasons_in_show = queries.get_seasons_in_show(conn, title_id = title_id)
    conn.close()

    print(results)

    # If the result wasn't a tv series, raise an exception
    if title_type != 'tvSeries':
        raise HTTPException(status_code=422, detail=f"Title with title_id '{title_id}' is not a tv series, it is a {title_type}.")

    # If the season requested doesn't exist
    if seasons_in_show < 1 or season_number > seasons_in_show:
        raise HTTPException(status_code=422, detail=f"There are only {seasons_in_show} seasons for this show, you requested information about season {season_number}.")

    episodes = []
    for result in results:
        # Split the genres by comma, and create a list of Genre objects
        listed_genres = result[8].split(',')
        genres = []
        for genre in listed_genres:
            genres.append(Genre(**{key: genre for _, key in enumerate(Genre.__fields__.keys())}))

        # Create a Title object, but manually set the genres entry in the Title object
        # to our list of Genres objects.
        episode = {key: result[i] for i, key in enumerate(Title.__fields__.keys())}
        episode['genres'] = genres
        episodes.append(Title(**episode))

    return episodes