import psutil
from requests.auth import HTTPBasicAuth
from typing import Optional

from lockfilepy.exceptions import LolClientNotFound


class Lockfile:
    def __init__(self, path: Optional[str] = None) -> None:
        if not path:
            process = [
                p
                for p in psutil.process_iter(attrs=["pid", "name"])
                if p.info["name"] == "LeagueClient.exe"
            ]
            if not process:
                raise LolClientNotFound

            self.path = process[0].cmdline()[0].rsplit("/", 1)[0]
            with open(self.path + "/lockfile", "r") as f:
                self.data = f.readline().strip().split(":")

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
