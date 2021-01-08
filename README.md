# battlemetrics-utils

### Installation (windows)

```
# install python3.7 (or later)
pip3 install virtualenv
pip3 install virtualenvwrapper-win
mkvirtualenv battlemetrics
workon battlemetrics
setprojectdir .
pip3 install -r requirements.txt
# create api token: https://www.battlemetrics.com/developers
# put personal access token in token.txt
```

### Execution

```
$ python3 battlemetrics.py afkers --server-name "JOINEASYSQUAD.COM INVASION" --token-path "token.txt"
Name                             Session   Score
Keta                             39min     0pts
[EASY]122nd WB Jayy              0min      0pts
Soviet Pigeon                    11min     0pts
lil_snoopy1990                   60min     0pts
Negreta_117                      123min    0pts

$ python3 battlemetrics.py seeders --server-name "JOINEASYSQUAD.COM INVASION" --token-path "token.txt"
(EASY)Tom Hanks                  43hrs 14mins
EasyAsh™                         41hrs 52mins
EasyGroomslayer™                 40hrs 19mins
EasyDevin™                       24hrs 31mins
EasyStarkillerxfx™               22hrs 42mins
Astro Goat                       21hrs 44mins
JaggedBaLz                       17hrs 14mins
xxShinedown13Bxx                 16hrs 7mins
11B-Cogley                       12hrs 44mins
PacketLost                       12hrs 15mins
Baghdadi                         12hrs 12mins
Helen Keller                     11hrs 59mins
brushnit                         11hrs 50mins
[33rd] Vigory                    11hrs 30mins
EasyTameFroggy™                  11hrs 1mins
(Bread)PrototypeZ                10hrs 25mins
DATbod                           9hrs 50mins
Lotion Boss                      9hrs 46mins
EasyAgando™                      9hrs 40mins
GPnWhiskey                       9hrs 24mins
```
