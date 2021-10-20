from fastapi import FastAPI, Response
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.schemas import AKA, Title, Person, CrewMember, Rating, Episode, HelloWorld
from app.imdb import get_movie_with_id, get_cast_for_title, get_show_for_title, get_show_for_title_season_and_episode, get_episodes_for_season


app = FastAPI()
templates = Jinja2Templates(directory='templates/')


@app.get("/", response_model=HelloWorld)
async def root(request: Request):
    """
    Returns a simple message, "Hello World!"

    Returns:
        dict: The response JSON.
    """

    # Create a HelloWorld object
    data = ['hello', 'world',]
    hello_world = HelloWorld(**{key: data[i] for i, key in enumerate(HelloWorld.__fields__.keys())})

    accept = request.headers.get("accept")

    if accept.split("/")[1] == 'json':
        return hello_world
    
    if len(accept.split(",")) > 1 or accept.split("/")[1] == 'html':
        response = templates.TemplateResponse("index.html", {"request": request, "payload1": hello_world}) 
        return response


@app.get(
    "/movies/{title_id}", 
    response_model=Title, 
    summary="Get a movie.",
    response_description="A movie."
)
async def get_movies(title_id: str, request: Request):
    movie = get_movie_with_id(title_id)
    accept = request.headers.get("accept")

    if accept.split("/")[1] == 'json':
        return movie
    
    if len(accept.split(",")) > 1 or accept.split("/")[1] == 'html':
        return templates.TemplateResponse("movie.html", {"request": request, "movie": movie}) 


@app.get(
    "/cast/{title_id}",
    response_model=list[CrewMember],
    summary="Get the crew for a title_id.",
    response_description="A crew."
)
async def get_cast(title_id: str, request: Request):
    cast = get_cast_for_title(title_id)
    accept = request.headers.get("accept")

    if accept.split("/")[1] == 'json':
        return cast
    
    if len(accept.split(",")) > 1 or accept.split("/")[1] == 'html':
        return templates.TemplateResponse("cast.html", {"request": request, "cast": cast}) 


@app.get(
    "/tv/{title_id}",
    response_model=Title,
    summary="Get the tv show for the given title_id.",
    response_description="A TVShow."
)
async def get_show(title_id: str, request: Request):
    show = get_show_for_title(title_id)
    return show


@app.get(
    "/tv/{title_id}/seasons/{season_number}/episodes/{episode_number}",
    response_model=Title,
    summary="Get the episode of a specific tv show.",
    response_description="A tv show episode."
)
async def get_episode(title_id: str, season_number: int, episode_number: int, request: Request):
    episode = get_show_for_title_season_and_episode(title_id, season_number, episode_number)
    return episode


@app.get(
    "/tv/{title_id}/seasons/{season_number}/episodes",
    response_model=list[Title],
    summary="Get the episodes of a specific tv show.",
    response_description="A list of episodes."
)
async def get_episodes(title_id: str, season_number: int, request: Request):
    episodes = get_episodes_for_season(title_id, season_number)
    accept = request.headers.get("accept")

    if accept.split("/")[1] == 'json':
        return episodes
    
    if len(accept.split(",")) > 1 or accept.split("/")[1] == 'html':
        return templates.TemplateResponse("episodes.html", {"request": request, "episodes": episodes}) 
