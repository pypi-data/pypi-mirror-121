import os
from requests.auth import HTTPBasicAuth

from lockfilepy.exceptions import LolClientNotFound


class Lockfile:
    def __init__(self) -> None:
        self.path = (
            "C:\Riot Games\League of Legends"
            if os.name == "nt"
            else "/Applications/League of Legends.app/Contents/LoL"
        )
        try:
            with open(self.path + "/lockfile", "r") as f:
                self.data = f.readline().strip().split(":")
        except:
            raise LolClientNotFound

    @property
    def process(self) -> str:
        return self.data[0]

    @property
    def PID(self) -> int:
        return self.data[1]

    @property
    def port(self) -> int:
        return self.data[2]

    @property
    def password(self) -> str:
        return self.data[3]

    @property
    def scheme(self) -> str:
        return self.data[4]

    @property
    def url(self) -> str:
        return f"wss://riot:{self.password}@127.0.0.1:{self.port}"

    @property
    def base_url(self) -> str:
        return f"{self.scheme}://127.0.0.1:{self.port}"

    @property
    def auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth("riot", self.password)
