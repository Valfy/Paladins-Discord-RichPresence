# Paladins Discord Rich Presence
[![python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/release/python-3100/) [![pyrez](https://img.shields.io/badge/Pyrez-1.1.1.1-yellow)](https://github.com/luissilva1044894/Pyrez) [![pypresence](https://img.shields.io/badge/pypresence-4.2.1-blue)](https://pypi.org/project/pypresence/)

How CLI looks like:

![CLI](https://cdn.discordapp.com/attachments/797777445537054720/1073252422157336660/image.png)

How Rich Presence looks like:

![Rich Presence](https://cdn.discordapp.com/attachments/797777445537054720/1073252674050469928/image.png)

![Rich Presence with Champion image](https://cdn.discordapp.com/attachments/797777445537054720/1073253248997265499/image.png)

### How to use

Before using this application you need to get [Access](https://fs12.formsite.com/HiRez/form48/secure_index.html) to Hi-Rez Studios API by filling out the form.

After getting access, put your credentialls into the *"devid"* and *"authkey"* fields replacing *four dashes* in ***settings.json*** file.

```json
 "Access": {
    "devid": "----",
    "authkey": "----"
  },
```

Also put you Paladins username into the *"Account"* field in the same file. 

```json
 "Account": "----",
```

Now you ready to use the application.

### How to customize rich presence text

For each in-game status you can customize text in ***settings.json*** file.

```json
  "Discord": {
    "offline": {
      "upper_text": "{player} is offline",
      "bottom_text": "Probably will launch Paladins soon",
      "image_text": "{time_rich_presence}"
    },
    
    "idle": {
    
    #
    
    "in_match": {
      "upper_text": "{player} playing as {champion}",
      "bottom_text": "On {map}",
      "image_text": "{champion} (Mastery: {mastery})"
    }
```

By using replacement words
+ `{player}` - username
+ `{title}` - in-game title
+ `{account_level}` - account level
+ `{total_hours}` - total hours played
+ `{rank}` - rank in ranked mode
+ `{champion}` - champion you are playing in live match (use it only in **"in_match"** in-game status)
+ `{mastery}` - champion mastery level (use it only in **"in_match"** in-game status)
+ `{map}` - map you are playing on (use it only in **"in_match"** in-game status)
+ `{time}` - time since game launch (with this app)
+ `{time_rich_presence}` - time since app launch

So it will be automaticly replaced by your playername and champion you playing.

### How to change app lanuguage

If you want to translate champions, maps, rank and interface of app to Russian language. Put **RU** into the *"Language"* field in ***settings.json*** file.

```json
  "Language": "EN",
```

Only English and Russian translations are available now (other lanugages will possibly be added later).

