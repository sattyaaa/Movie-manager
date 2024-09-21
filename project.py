from sys import exit
import csv
import argparse
import requests
import json
from tabulate import tabulate
from pyfiglet import Figlet

figlet = Figlet()
figlet.setFont(font="big")

from colorama import Fore, Back, Style, init
# Initialize colorama
init(autoreset=True)


def main():
    parser = argparse.ArgumentParser(description="Choose between searching and watchilist")
    parser.add_argument("-m", "--mode", default='w',
                        help="s or search for search mode \n w or watchlist for wathlist mode", type=str)
    args = parser.parse_args()

    try:
        while True:
            if (args.mode).lower() in ["s", "search"]:
                search_mode()
            elif (args.mode).lower() in ["w", "watchlist"]:
                watchlist_mode()
            else:
                exit(Fore.RED + "Not a valid mode")
    except KeyboardInterrupt:
        print(Fore.RED + "\nKeyboardInterrupt: Program terminated.")


def search_mode():
    print(figlet.renderText("movies  searcher"))

    while True:
        name = input("Enter movie name: ")
        movies = search(name)
        if movies["status"] == True:
            break
        print(Fore.RED + movies["data"])

    # prints the search results
    movies = print_search(movies)

    print("To view more about a movies type its serial number\n")
    while True:
        number = get_no(11)
        id = movies[number-1]["imdbID"]
        movie = details(id)
        if movie["status"] == True:
            break
        print(Fore.RED + movie["data"])

    movie = movie["data"]

    # prints movie details
    print_details(movie)

    action = input("\nDo you want to add this movoe in watchlist? (y/n): ")

    if action.lower() not in ["y", "yes"]:
        exit("Fore.RED + \nProgram exited")

    write_movie(movie)
    print(Fore.GREEN + "\nData Written succesfully")


def watchlist_mode():
    print(figlet.renderText("watchlist"))

    with open("watchlist.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        data_print = [{**{"S.No": i + 1}, **item} for i, item in enumerate(data)]
        print(tabulate(data_print, headers="keys", tablefmt="pretty", stralign="left"), "\n")

    print("Type the movie no to take actions")
    no = get_no(len(data)+1)
    print("What do you wnat to do?\nDelete\nWatching\nFinished")

    action = input(f"{data[no-1]["Title"]}: ")

    if action.lower() in ["d", "delete"]:
        del data[no - 1]
        print(Fore.GREEN + f"\ndeleted")

    elif action.lower() == "watching":
        data[no-1]["Status"] = "watching"
        print(Fore.GREEN + "\nUpdated")

    elif action.lower() == "finished":
        data[no-1]["Status"] = "finished"
        print(Fore.GREEN + "\nUpdated")

    else:
        exit(Fore.RED + "Invalid Action")

    with open("watchlist.csv", "w") as csvfile:
        fieldnames = ["Title", "Type", "Status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def write_movie(movie):
    with open("watchlist.csv", "a") as csvfile:
        fieldnames = ["Title", "Type", "Status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        data = {}
        for fieldname in fieldnames:
            if fieldname == "Status":
                data["Status"] = "watchlist"
                continue
            data[fieldname] = movie[fieldname]

        writer.writerow(data)


def details(id):
    url = f"http://www.omdbapi.com/?i={id}&plot=full"
    data = fetch(url)
    return data


def print_details(movie):
    ratings_data = movie.pop("Ratings")
    poster_link = movie.pop("Poster")
    plot = movie.pop("Plot")
    movie_data_list = [[key, value] for key, value in movie.items()]
    headers = ["Key", "Value"]

    print("Movie Details:")
    print(tabulate(movie_data_list, headers=headers, tablefmt="pretty", stralign="left"))

    print(f"\nPoster Link: {poster_link}")
    print(f"\nPlot: {plot}")
    print("\nRatings:")
    print(tabulate(ratings_data, headers="keys", tablefmt="pretty", stralign="left"))


def search(name):
    url = f"http://www.omdbapi.com/?s={name}&page=1"
    data = fetch(url)
    return data


def print_search(items):
    items = items["data"]["Search"]
    for item in items:
        del item["Poster"]
    movies = [{**{"S.No": i + 1}, **item} for i, item in enumerate(items)]
    print(tabulate(movies, headers="keys", tablefmt="pretty", stralign="left"), "\n")
    return movies


def fetch(url):
    api_key = "8eb341bf"
    url = f"{url}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        return {"data": f"Error: Unable to make request ({e})", "status": False}

    try:
        data = response.json()  # Parsing the response as JSON
    except json.JSONDecodeError:
        return {"data": "Error: Failed to parse response as JSON.", "status": False}

    if data.get("Response") == "False":
        return {"data": f"Error: {data.get('Error', 'Unknown error')}", "status": False}

    return {"data": data, "status": True}


def get_no(nu):
    while True:
        try:
            n = int(input("Enter: "))
            if n in range(1, nu):
                return n
        except ValueError:
            print(Fore.RED + "Invalid Value")
            continue
        print(Fore.RED + "Invalid Number")


if __name__ == "__main__":
    main()
