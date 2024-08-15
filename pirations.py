import requests, urllib.parse, base64, json, re, colorama, os, time

API_KEY = "71deea7ba87c519ac04704906a9114ac"
BASE_URL = "https://api.themoviedb.org/3"
SEARCH_URI = "/search/multi?query={0}&language=en-US&page=1&api_key={1}"
TV_URI = "/tv/{0}"
ENDING_URI = "?language=en-US&api_key={0}"
HEADERS = {"sec-fetch-dest": "iframe","referer": "https://soapertv.cc/","Host": "vidsrc.pro"}

if not os.path.exists(os.getcwd()+"/bin/"):
    os.makedirs(os.getcwd()+"/bin/")

os.system("cls")

print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Please enter a show/movie name.")
search = urllib.parse.quote(input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] "))

def getHash(types, id, szn=None, ep=None):
    if types == "tv":
        r = requests.get(f"https://vidsrc.pro/embed/tv/{id}/{szn}/{ep}",headers=HEADERS)
        if r.status_code != 200:
            exit('Show not found.')
        return json.loads(decode(json.loads(re.findall(r"{.+}",r.content.decode('utf-8'))[0])['hash']))[0]['hash']
    elif types == "movie":
        r = requests.get(f"https://vidsrc.pro/embed/movie/{id}",headers=HEADERS)
        if r.status_code != 200:
            exit('Movie not found.')
        return json.loads(decode(json.loads(re.findall(r"{.+}",r.content.decode('utf-8'))[0])['hash']))[0]['hash']

def decode(str: str):
    try:
        return base64.b64decode(str[::-1]).decode('utf-8')
    except:
        return base64.b64decode(str[::-1]+"==").decode('utf-8')

def download(hashr, selection, sznSelect=None, epSelect=None):
    r = requests.get(f"https://vidsrc.pro/api/e/{hashr}",headers=HEADERS)

    findr = re.findall(r"url=.+",r.json()['source'])
    if len(findr) == 0:
        url = r.json()['source'].replace("https://vidsrc.pro/api/proxy/viper/","https://ae.bigtimedelivery.net/").split(".png?")[0]
    else:
        url = findr[0].replace('url=','')
    if match := re.search(r"#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=4500000,RESOLUTION=1920x1080\n(.+)",requests.get(url).content.decode('utf-8')):
        data = requests.get(match.group(1)).content.decode('utf-8')
        title = cx if not ':' in (cx:=selection['name' if 'name' in selection else 'title']) else cx.replace(":","")
        open(f"bin/{title} S{sznSelect}EP{epSelect}.mpeg","w").write("") if selection['media_type'] == "tv" else open(f"bin/{title}.mpeg","w").write("")
        datlist = re.findall(r",\n.+", data)
        for i,uri in enumerate(datlist):
            os.system("cls")
            uri = uri.replace(",\n","")
            print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Building video file...")
            print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] {round(((i+1)/len(datlist))*100)}% | {i+1}/{len(datlist)} files built.")
            open(f"bin/{title} S{sznSelect}EP{epSelect}.mpeg","ab").write(requests.get(uri).content) if selection['media_type'] == "tv" else open(f"bin/{title}.mpeg","ab").write(requests.get(uri).content)
        os.system(f'start /wait cmd /k "cd dependencies && ffmpeg.exe -i "../bin/{title} S{sznSelect}EP{epSelect}.mpeg" -acodec copy -vcodec copy -f mp4 "../bin/{title} S{sznSelect}EP{epSelect}.mp4" && del "../bin/{title} S{sznSelect}EP{epSelect}.mpeg" && exit"') if selection['media_type'] == "tv" else os.system(f'start cmd /k "cd dependencies && ffmpeg.exe -i "..bin/{title}.mpeg" -acodec copy -vcodec copy -f mp4 "..bin/{title}.mp4" && del "..bin/{title}.mpeg" && exit"')

jsonEnd = json.loads(requests.get(BASE_URL+SEARCH_URI.format(search,API_KEY)).content.decode('utf-8'))

for i,result in enumerate(jsonEnd['results']):
    if not 'person' in result['media_type']:
        print(f"[{colorama.Fore.GREEN}{i}{colorama.Fore.RESET}] : {result['name' if 'name' in result else 'title']} ({result['first_air_date' if 'first_air_date' in result else 'release_date'][0:4]}) - {result['media_type']}")
    else:
        print(f"[{colorama.Fore.GREEN}{i}{colorama.Fore.RESET}] : NULL")

selection = jsonEnd['results'][int(input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] "))]

os.system("cls")

if selection['media_type'] == "tv":
    print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Please select a season.")

    r = requests.get(BASE_URL + TV_URI.format(selection['id']) + ENDING_URI.format(API_KEY))
    print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] There are {r.json()['number_of_seasons']} seasons")
    sznSelect = input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] ")
    
    os.system("cls")
    
    print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] {selection['name']} - Season {sznSelect}")
    print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Please select an episode.")

    r = requests.get(BASE_URL + TV_URI.format(selection['id'])+ f"/season/{sznSelect}" + ENDING_URI.format(API_KEY))

    eps = r.json()['episodes']
    for i,ep in enumerate(eps):
        print(f"[{colorama.Fore.GREEN}{i+1}{colorama.Fore.RESET}] : {ep['name']}")
    print(f"[{colorama.Fore.GREEN}{len(eps)+1}{colorama.Fore.RESET}] : Download whole season")

    epSelect = input(f"[{colorama.Fore.RED}?{colorama.Fore.RESET}] ")
    if epSelect == str(len(eps)+1):
        for i,_ in enumerate(eps):
            hashr = getHash(selection['media_type'],selection['id'], sznSelect, i+1)
            download(hashr, selection, sznSelect, i+1)
        exit('')

    hashr = getHash(selection['media_type'],selection['id'], sznSelect, epSelect)

    download(hashr, selection, sznSelect, epSelect)

    print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] Convering from mpeg format to mp4...")

elif selection['media_type'] == "movie":
    hashr = getHash(selection['media_type'], selection['id'])

    download(hashr, selection)
