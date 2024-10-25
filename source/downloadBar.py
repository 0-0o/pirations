from sys import stdout

class DownloadBar:
    def __init__(self, maxValue: int, message:str = None, divisions: int=10, downloadChar: str="="):
        self.divisions = divisions
        self.downloadChar = downloadChar
        self.length = 0
        self.message = message
        self.maxValue = maxValue

    def start(self):
        stdout.write(f"\r[{''.join([" " for _ in range(self.divisions)])}] {self.message}")
    
    def update(self, value: int, message: str = None):
        self.length = int(((value/self.maxValue) * self.divisions))
        if message != None:
            self.message = message

        stdout.write(f"\r[{''.join([self.downloadChar for _ in range(self.length)])}{''.join(" " for _ in range(self.divisions - self.length))}] {self.message}")