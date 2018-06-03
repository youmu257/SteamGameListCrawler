# Steam game list crawler

## Introduction
- Crawler special game list on [Steam](https://store.steampowered.com/search/?specials=1)
- Save as json file or write to database by simple command

## Requirements
If you want run this project, the requirements are as follows:
- Python 3
- MySQL

## Usage
If you want write data to database, you need to change the login information of database/config.ini
Then, jsut run the command like: ```python SteamGameListCrawler.py --page 1 --json --db```

Parameter:

| parameter                     | comment                                                                                 |
| ------------------------------|-----------------------------------------------------------------------------------------|
| "--page start_page (end_page)"| setting search start page and end page. It will search total page if not input end page | 
| "--json"                      | save result as a json file named result.json                                            |
| "--db"                        | save result into database                                                               |

## Database Schema

Table: steam_game_list (default)

| filed nmae    | field type(length)| comment              | auto_increment?  |
| --------------|-------------------|----------------------|----------------- |
| id            | int primary key   | id of each game in list           | yes |
| img_url       | char(100)         | the image url of the game         | no  |
| game_page_url | char(100)         | the url of game page              | no  |
| title         | char(100)         | the name of the game              | no  |
| released_date | char(15)          | the realeased date of the game    | no  |
| discount      | char(10)          | the discount of the game now      | no  |
| original_price| char(20)          | the original price of the game    | no  |
| discount_price| char(20)          | the discount price of the game now| no  |
| review        | char(100)         | the reviews of the game           | no  |