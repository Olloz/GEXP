import httpx
import json
from rich.table import Table
from rich.console import Console
import time

currentTime = int(time.time()*1000)

json_data = open('private.json')
hypixeldata = json.load(json_data)

session = httpx.Client()
console = Console()

data = session.get(f'https://api.hypixel.net/guild?key={hypixeldata["hypixelKey"]}&name=Betrayed').json()
values = sorted([(member["uuid"], sum(member["expHistory"].values())) for member in data["guild"]["members"] if sum(member["expHistory"].values()) < 30000 and currentTime - member["joined"] > 691200000], key = lambda x: x[1], reverse=True)

def to_username(uuid):
        return session.get(f"https://api.hypixel.net/player?key={hypixeldata['hypixelKey']}&uuid={uuid}").json()["player"]["displayname"]

table = Table()
table.add_column("Username", width=20)
table.add_column("Total GEXP")
table.add_column("Discord")
for value in values:
    player = value[0]
    username = to_username(value[0])
    gexp = value[1]
    data2 = session.get(f"https://api.hypixel.net/player?key={hypixeldata['hypixelKey']}&uuid={player}").json()
    if not "player" in data2:
        print("Error")
        continue
    disc = "VERIFICATION REQUIRED"
    if "socialMedia" in data2['player'] and "DISCORD" in data2["player"]['socialMedia']['links']:
        disc = data2['player']['socialMedia']['links']['DISCORD']
    table.add_row(username,str(gexp),disc)
console.print(table)