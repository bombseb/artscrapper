# artscrapper

## Description

This program automatically downloads artworks and turns them into icons for artist's directories containing albums and audiofiles.

For the moment, the supported file manager is Dolphin. For each selected directories The image is searched on fanart.tv. If the search is unsuccessful, a second search is performed on Deezer. The image is then downloaded and saved in the artist's directory. A **.directory** file is then created. This file is specific to Dolphin and is used to define the downloaded image as the directory icon.

## Installation

```
cp artscrapper.py ~/.local/bin
chmod +x ~/.local/bin/artscrapper.py
cp artscrapper.desktop ~/.local/share/kio/servicemenus/
chmod +x ~/.local/share/kio/servicemenus/artscrapper.py
```

## Use

In dolphin, select the directories, right-click and select "Download artwork".
A terminal window will open, in which you can follow the progress of your work.

Exemple :
![Screenshot](https://raw.githubusercontent.com/bombseb/artscrapper/master/img/Screenshot1.png)

![Logo du projet](https://raw.githubusercontent.com/bombseb/artscrapper/master/img/Screenshot2.png)
