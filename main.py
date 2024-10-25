from source.movies import Movie
from source.shows import Show
import requests, colorama, urllib, os

API_KEY = "71deea7ba87c519ac04704906a9114ac"
OUT_FOLDER = "bin"

print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Please enter a show/movie name.")
search = urllib.parse.quote(input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] "))

os.system("cls")

searchJson = requests.get(f"https://api.themoviedb.org/3/search/multi?query={search}&language=en-US&page=1&api_key={API_KEY}").json()
for i,result in enumerate(searchJson['results']):
    if result['media_type'] in ['tv','movie']:
        print(f"[{colorama.Fore.GREEN}{i}{colorama.Fore.RESET}] : {result['name' if 'name' in result else 'title']} ({result['first_air_date' if 'first_air_date' in result else 'release_date'][0:4]}) - {result['media_type']}")
    else:
        print(f"[{colorama.Fore.GREEN}{i}{colorama.Fore.RESET}] : NULL")

try:
    selection = searchJson['results'][int(input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] "))]
    os.system("cls")
    if selection['media_type'] == "tv":
        print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Please select a season.")

        show = Show(selection['id'])

        print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] There are {show.getShowData()['number_of_seasons']} seasons")
        sznSelect = input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] ")
        
        show.season = int(sznSelect)

        os.system("cls")
        
        print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] {selection['name']} - Season {sznSelect}")
        print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Please select an episode.")

        seasonInfo = requests.get(f"https://api.themoviedb.org/3/tv/{selection['id']}/season/{sznSelect}?language=en-US&api_key={API_KEY}").json()

        eps = seasonInfo['episodes']
        for i,ep in enumerate(eps):
            print(f"[{colorama.Fore.GREEN}{i+1}{colorama.Fore.RESET}] : {ep['name']}")

        epSelect = input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] ")

        show.episode = int(epSelect)

        os.system("cls")

        showDownloadResult = show.download(OUT_FOLDER, True)
        if showDownloadResult.get("success"):
            os.system("cls")
            print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Successfully downloaded, do you want to open it [Y/N]")
            openFolder = input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] ")
            if openFolder.lower() == "y" or openFolder.lower() == "yes":
                os.system(f"explorer {showDownloadResult.get("path")}")
    else:
        movie = Movie(selection['id']).download(OUT_FOLDER, True)
        if movie.get("success"):
            os.system("cls")
            print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Successfully downloaded, do you want to open it [Y/N]")
            openFolder = input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] ")
            if openFolder.lower() == "y" or openFolder.lower() == "yes":
                os.system(f"explorer {movie.get("path")}")
except:
    exit("Improper value entered.")
