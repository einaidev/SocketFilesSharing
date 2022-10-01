import os, platform, re
from subprocess import run, PIPE

__command__ = "ipconfig" if platform.system() == "Windows" else "ifconfig"

class allInterfaces:
    def __init__(self) -> None:
        self.command = __command__
        self.cases = {
            "ipv4": lambda x: re.compile(r"[0-9]+(?:\.[0-9]+){3}").findall(x)[0],
            "inet": lambda x: re.compile(r"[0-9]+(?:\.[0-9]+){3}").findall(x)[0]
        }
    
    @property
    def getInterfaces(self):
        interfaces = {

        }

        valid_interfaces = {

        }

        result = run([self.command], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        index = -1
        for i in result.stdout.split("\n"):
            if not i == "":
                if not i.startswith("   "):
                    index += 1
                    interfaces[index] = {"name": i}
                else:
                    if "ipv4" in i.lower():
                        interfaces[index]["ipv4"] = self.cases["ipv4"](i)
                    if "inet" in i.lower():
                        interfaces[index]["inet"] = self.cases["inet"](i)
        index = -1
        for k,v in interfaces.items():
            if "ipv4" in v:
                index += 1
                valid_interfaces[index] = {"name":v["name"], "ipv4": v["ipv4"]}

        return valid_interfaces