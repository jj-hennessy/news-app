import urllib.request, urllib.parse, urllib.error
from urllib.request import Request, urlopen
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
import ssl
import base64
import eel
import urljoin

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
def getArticleValues(websiteInformationList):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    articleInfo = []
    for website in websiteInformationList:
        try:
            articleLink = ""
            articleTitle = ""
            articleImageURL = ""
            articleSubject = website[1]
            articlePublisher = website[2]

            if(articlePublisher == "New York Times"):
                # take in a link, then add
                html = urllib.request.urlopen(website[0], context=ctx).read()
                soup = BeautifulSoup(html, 'html.parser')
                articles = soup.findAll("h2", {"class": "e134j7ei0"})
                articleImages = soup.findAll("figure", {"class": "css-k4k3gl"})
                for i in range(len(articles)):
                    articleLink = 'https://www.nytimes.com' + articles[i].find('a')['href']
                    articleTitle = articles[i].find('a').text
                    articleImageURL = articleImages[i].find('a')
                    articleImageURL = articleImageURL.find('img')['src']
                    articleInfo.append([articleTitle, articleLink, articleImageURL, articleSubject, articlePublisher])

            if(articlePublisher == "The Verge"):
                # take in a link, then add
                html = urllib.request.urlopen(website[0], context=ctx).read()
                soup = BeautifulSoup(html, 'html.parser')
                articles = soup.findAll("div", {"class": "c-entry-box--compact--article"})
                for i in range(len(articles)):
                    articleLink = articles[i].find('a')['href']
                    articleTitle = articles[i].find("h2", {"class": "c-entry-box--compact__title"})
                    articleTitle = articleTitle.find("a").text
                    articleImageURL = articles[i].find("div", {"class": "c-entry-box--compact__image"})
                    articleImageURL = articleImageURL.find("noscript").img["src"]
                    articleInfo.append([articleTitle, articleLink, articleImageURL, articleSubject, articlePublisher])

            if(articlePublisher == "Neuroscience News"):
                headers = {'User-Agent': 'Mozilla/5.0'}
                page = requests.get(website[0])
                soup = BeautifulSoup(page.text, "html.parser")
                articles = soup.findAll("article", {"class": "cb-article"})
                for i in range(len(articles)):
                    articleLink = articles[i].find("h2", {"class": "cb-post-title"})
                    articleLink = articleLink.find("a")["href"]
                    articleTitle = articles[i].find("h2", {"class": "cb-post-title"})
                    articleTitle = articleTitle.find("a").text
                    articleImageURL = articles[i].find("div", {"class": "cb-img-fw"})
                    articleImageURL = articleImageURL.find("noscript").img["src"]
                    articleInfo.append([articleTitle, articleLink, articleImageURL, articleSubject, articlePublisher])

        except:
            print("An exception occurred")

    return articleInfo

@eel.expose
def generateHTML(urls, chosenSubjects):
    subjectDictionary = {
        'tech': 'Technology',
        'science': 'Science',
        'business': 'Business'
    }
    logoDictionary = {
        'New York Times': 'https://static-s.aa-cdn.net/img/ios/284862083/9e60631d8894d77807a7bd33e2503805?v=1',
        'The Verge': 'https://cdn.freebiesupply.com/images/large/2x/the-verge-logo-transparent.png',
        'Neuroscience News': 'https://66.media.tumblr.com/avatar_69121dcd5195_128.pnj'
    }
    finalHTML = ''
    for i in range(len(chosenSubjects)):

        finalHTML += '<h1 class="text-center">'
        finalHTML += subjectDictionary[chosenSubjects[i]]
        finalHTML += ' Articles</h1><hr class="article-separator"><div class="row justify-content-center">'

        articleInfo = getArticleValues(urls)
        for article in articleInfo:
            if(article[3] == chosenSubjects[i]):

                finalHTML += '<div class="card card-image mb-3 col-sm-6 col-md-3 col-lg-3" style="margin: 15px; background-size: cover; background-image: linear-gradient(rgba(235, 1, 165, 0.5), rgba(209, 53, 49, 0.5)), url(&apos;'
                finalHTML += article[2]
                finalHTML += '&apos;)"><div class="text-white text-center d-flex align-items-center img-gradient-overlay py-5 px-4"><div><img style="display: block; margin-left: auto; margin-right: auto;" class="rounded-circle justify-content-center" height="40" width="40" src="'
                finalHTML += logoDictionary[article[4]]
                finalHTML += '"><h3 class="card-title pt-2"><strong>'
                finalHTML += article[0]
                finalHTML += '</strong></h3><a class="btn btn-deep-orange waves-effect waves-light" href="'
                print(article[1])
                finalHTML += article[1]
                finalHTML += '"><i class="far fa-clone left"></i> View article</a></div></div></div>'

        # ending div tag for row
        finalHTML += '</div>'

    return finalHTML

eel.start('welcome-screen.html')
