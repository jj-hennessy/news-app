import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import eel

@eel.expose
def validateLink(url):
    if(str(url).startswith('http')):
        return True
    else:
        return False

@eel.expose
def cleanLinkList(linkList):
    newList = list()
    for link in linkList:
        if(validateLink(link)):
            newList.append(link)

    return newList

eel.init('web', {
    '_js_result_timeout': 100000
})

@eel.expose
def getArticleValues(urls):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    articleInfo = []
    for url in urls:
        try:
            articleLink = ""
            articleTitle = ""
            articleImageURL = ""
            # take in a link, then add
            html = urllib.request.urlopen(url, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')

            if(url == "https://www.nytimes.com/section/science"):
                articles = soup.findAll("h2", {"class": "e134j7ei0"})
                articleImages = soup.findAll("figure", {"class": "css-k4k3gl"})
                for i in range(len(articles)):
                    articleLink = 'https://www.nytimes.com' + articles[i].find('a')['href']
                    articleTitle = articles[i].find('a').text
                    articleImageURL = articleImages[i].find('a')
                    articleImageURL = articleImageURL.find('img')['src']
                    articleInfo.append([articleTitle, articleLink, articleImageURL])

            elif(url == "https://www.theverge.com/science"):
                articles = soup.findAll("div", {"class": "c-entry-box--compact--article"})
                for i in range(len(articles)):
                    articleLink = articles[i].find('a')['href']
                    articleTitle = articles[i].find('div', {"class": "c-entry-box--compact__title"}).find('a').text
                    articleImageURL = articles[i].find('div', {"class": "c-entry-box--compact__image"}).find('img')['src']
                    articleInfo.append([articleTitle, articleLink, articleImageURL])

        except:
            print("An exception occurred")

    return articleInfo

@eel.expose
def generateHTML(urls):
    finalHTML = '<div class="row">'

    articleInfo = getArticleValues(urls)
    print("articleInfo is this long: ", len(articleInfo))
    for article in articleInfo:
        finalHTML += '<div class="col-sm-12 col-md-4 col-lg-3 card" style="width: 18rem; margin: 15px;"><img src="'
        finalHTML += article[2]
        finalHTML += '" class="card-img-top"><div class="card-body"><h5 class="card-title">'
        finalHTML += article[0]
        finalHTML += '</h5><a href="'
        finalHTML += article[1]
        finalHTML += '" class="card-link">Read</a></div></div>'


    finalHTML += '</div>'
    return finalHTML

eel.start('gui.html')
