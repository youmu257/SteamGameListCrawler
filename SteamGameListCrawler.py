# encoding=utf-8
from bs4 import BeautifulSoup
import parameter
import urllib, re, json, time, sys
from database.mysql_connect import connectMysql

def getMaxPage(soup):
    pages = str(soup.find('div', 'search_pagination_right'))
    regex = re.compile('>\d*<')
    return int(regex.findall(pages)[2][1:-1]) # find '>59<', use [1:-1] to remove '>' and '<'

def getGameInfo(soup):
    for game in soup.find_all('a'):
        #json map
        gameMap = dict()
            
        try:
            # img url
            gameMap['img_url'] = game.img['src'].replace('https://steamcdn-a.akamaihd.net/steam/apps/', '')
        except:
            # not a game
            continue
        
        # game page url
        gameMap['game_page_url'] = game['href'].replace('https://store.steampowered.com/app/', '')
        
        # game title
        gameMap['title'] = game.span.contents[0]
        
        gameSoup = BeautifulSoup(str(game), 'html.parser')
        
        # released date
        releasedDate = gameSoup.find('div', class_ = 'col search_released responsive_secondrow')
        if len(releasedDate.contents) == 0:
            # not a game
            continue
        gameMap['released_date'] = releasedDate.contents[0]
        
        # discount
        discount = gameSoup.find('div', class_ = 'col search_discount responsive_secondrow')
        try:
            gameMap['discount'] = discount.span.contents[0]
        except:
            # no discount
            continue
        
        # price
        price = gameSoup.find('div', class_ = 'col search_price discounted responsive_secondrow')
        gameMap['original_price'] = price.strike.contents[0]
        gameMap['discount_price'] = price.contents[3].replace('\t','')
        
        # reviews
        review = gameSoup.find('div', class_ = 'col search_reviewscore responsive_secondrow')
        try:
            gameMap['review'] = review.span['data-tooltip-html']
        except:
            gameMap['review'] = ""
        gameListMap['games'].append(gameMap)

def write2db():
    # connect MySQL database
    db = connectMysql()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS game_list ( id int NOT NULL AUTO_INCREMENT, " +
                         "img_url char(100)," + # CHARACTER SET utf8 COLLATE utf8_bin
                         "game_page_url char(100)," +
                         "title char(100)," +
                         "released_date char(15)," +
                         "discount char(10)," +
                         "original_price char(20)," +
                         "discount_price char(20)," +
                         "review char(100)," +
                         "PRIMARY KEY (id) )")
    # clear table
    cursor.execute("TRUNCATE TABLE game_list")
    
    insertArray = [[game['img_url'], game['game_page_url'], game['title'], game['released_date'] , game['discount'], 
                    game['original_price'], game['discount_price'], game['review'],] for game in gameListMap['games']]
    '''
    # add by iteration
    for data in insertArray:
        #cursor.execute("INSERT INTO game_list(img_url, game_page_url, title, released_date, discount, original_price, discount_price, review) values(%s,%s,%s,%s,%s,%s,%s,%s)", data)
    '''
    
    cursor.executemany("INSERT INTO game_list(img_url, game_page_url, title, released_date, discount, original_price, discount_price, review)" +
                       "values(%s,%s,%s,%s,%s,%s,%s,%s)", insertArray)
    db.commit()
    cursor.close()
    
def main():
    setting = parameter.parseArgv(sys.argv)
    
    pages = setting.pages

    global gameListMap
    gameListMap = dict()
    gameListMap['games'] = list()
    
    stime = time.time()
    while pages <= setting.maxPages:
        print('Cralwering ' + str(pages) + ' pages')
        # get the website of discount game list
        steamSearchGameList = urllib.request.urlopen('https://store.steampowered.com/search/?specials=1&page=' + str(pages))
        soup = BeautifulSoup(steamSearchGameList, 'html.parser')
        
        if setting.getMaxPages:
            setting.maxPages = getMaxPage(soup)
    
        # extract game list
        searchResult = soup.find('div', id = 'search_result_container')
        soup = BeautifulSoup(str(searchResult), 'html.parser')
        
        # add game information to gameListMap
        getGameInfo(soup)
        pages += 1
    
    print('Spend ' + str(time.time() - stime) + 's to crawler steam discount game list.')
    
    # save as json file
    if setting.saveJson:
        fout = open('result.json', 'w', encoding='utf-8')
        json.dump(gameListMap, fout)
        fout.close()
    
    # write to db
    if setting.saveDB:
        write2db()

if __name__ == '__main__':
    main()