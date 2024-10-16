
from footy_data import footy_db
from match import match
from typing import List, Tuple, Callable, Any

def get_player(footy: Tuple[str, str, int, int, int]) -> str:
    return footy[0] 


def get_team(footy: Tuple[str, str, int, int, int]) -> str:
    return footy[1]


def get_mins(footy: Tuple[str, str, int, int, int]) -> int:
    return footy[2] 


def get_goals(footy: Tuple[str, str, int, int, int]) -> List[str]:
    return footy[3] 

def get_assists(footy: Tuple[str, str, int, int, int]) -> List[str]:
    return footy[4]



def players_by_team(matches: List[str]) -> List[str]:
    team = (matches[0])
    result = []
    for footy in footy_db:
        if get_team(footy) == team:
            result.append(get_team(footy))
    return result

def player_by_goal_range(matches: List[str]) -> List[str]:
    goal_start = int(matches[0])
    goal_end = int(matches[1])
    result = []
    for footy in footy_db:
        if(get_goals(footy) >= goal_start and get_year(footy) <= goal_end):
            result.append(get_player(footy))
    return result

# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# The pattern-action list for the natural language query system A list of tuples of
# pattern and action It must be declared here, after all of the function definitions
pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("what players play on _"), players_by_team),
    (str.split("what players scored goals between _ and _"), player_by_goal_range),
    # (str.split("what movies were made before _"), title_before_year),
    # (str.split("what movies were made after _"), title_after_year),
    # (str.split("who directed %"), director_by_title),
    # (str.split("who was the director of %"), director_by_title),
    # (str.split("what movies were directed by %"), title_by_director),
    # (str.split("who acted in %"), actors_by_title),
    # (str.split("when was % made"), year_by_title),
    # (str.split("in what movies did % appear"), title_by_actor),
    (["bye"], bye_action),
]


def search_pa_list(src: List[str]) -> List[str]:
    for pat, act in pa_list:
        val = match(pat, src)
        if val is not None: 
            result = act(val)
            if result:  
                return result
            else:
                return ["No answers"]
    return ["I don't understand"]


def query_loop() -> None:
    """The simple query loop. The try/except structure is to catch Ctrl-C or Ctrl-D
    characters and exit gracefully.
    """
    print("Welcome to the EPL database!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for answer in answers:
                print(answer)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nSo long!\n")


# uncomment the following line once you've written all of your code and are ready to try
# it out. Before running the following line, you should make sure that your code passes
# the existing asserts.
query_loop()