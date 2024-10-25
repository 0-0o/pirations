import requests, os, json, base64, re
from source.downloadBar import DownloadBar

API_KEY = "71deea7ba87c519ac04704906a9114ac"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36','origin': 'https://embed.su','referer': 'https://embed.su/'}

class Movie:
    def __init__(self, movieID: int):
        self.movieID = movieID

    def getHash(self):
        HASH_HEADERS = {"sec-fetch-dest": "iframe","referer": "https://soapertv.cc/","Host": "embed.su"}
        url = f"https://embed.su/embed/movie/{self.movieID}"
        r = requests.get(url,headers=HASH_HEADERS)
        JsonObject = json.loads(base64.b64decode(re.findall(r"`.+`",r.content.decode('utf-8'))[0].replace("`","")))
        if r.status_code != 200:
            exit('Movie not found.')
        try:
            decoded = base64.b64decode(JsonObject['hash'][::-1]).decode('utf-8')
        except:
            decoded = base64.b64decode(JsonObject['hash'][::-1]+"==").decode('utf-8')
        return json.loads(decoded)[0]['hash']
    
    def getMovieData(self):
        r = requests.get(f"https://api.themoviedb.org/3/movie/{self.movieID}?language=en-US&api_key={API_KEY}")

        return r.json()

    def download(self, parentFolder: str, printDownloadInfo: bool = False):
        try:
            movieName = self.getMovieData()['title']

            if not os.path.exists(parentFolder):
                os.mkdir(parentFolder)
            r = requests.get(f"https://embed.su/api/e/{self.getHash()}", headers=HEADERS)
            qualitiesM3U8 = r.json()['source']

            # get highest quality (kinda bodge but has 100% success rate so)

            r = requests.get(qualitiesM3U8)
            if match := re.search(r"#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=4500000,RESOLUTION=1920x1080\n(.+)", r.content.decode('utf-8')):
                urlsM3U8 = requests.get("https://embed.su"+match.group(1)).content.decode('utf-8')
                urlsList = re.findall(r",\n.+", urlsM3U8)

                if printDownloadInfo:
                    print(f"Downloading {movieName}...")
                    downloadBar = DownloadBar(len(urlsList),"0%", 25)
                    downloadBar.start()

                for i,url in enumerate(urlsList):
                    mpegDataSlice = requests.get(url.replace(",\n",""), headers=HEADERS).content
                    open(f"{parentFolder}/{movieName}.mpeg","ab").write(mpegDataSlice)
                    if printDownloadInfo:
                        downloadBar.update(i+1,f"{round((((i+1)/(len(urlsList))) * 100), 1)}%")

                return {"success":True, "path": os.path.abspath(os.getcwd())+f"\\bin\\{movieName}.mpeg"}
        except: 
            exit("File path specified is not writable.") 