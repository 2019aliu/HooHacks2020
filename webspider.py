import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize

# Define constants
htmlParser = 'html5lib'
numArticles = 1

# Retrieve search page text
newsSearchUrl = "http://news.google.com/news?q=covid-19%20OR%20coronavirus&output=rss"
newsSearchResult = requests.get(newsSearchUrl).text
# Turn search page into BeautifulSoup object to access HTML tags
newsSearchSoup = BeautifulSoup(newsSearchResult, htmlParser)

# Get articles
headlines = newsSearchSoup.find_all('title')
links = newsSearchSoup.find_all('description')


for i in range(1, 1+numArticles):
    headline = headlines[i].get_text()
    # I couldn't use the .get() method, so I manually parsed it out
    # Also I can't get the <link> tag for some reason wtfffffff
    link = links[i].get_text().split()[1][6:-1]
    print("Headline %d: %s\nLink: %s\n\n" % (i, headline, link))
    articlePage = requests.get(link).text
    articleSoup = BeautifulSoup(articlePage, htmlParser)
    rawTags = articleSoup.find_all('p')
    rawTexts = [tag.get_text().strip() for tag in rawTags]
    # Filter out sentences that contain newline characters '\n' or don't contain periods.
    sentence_list = [sentence for sentence in rawTexts if not '\n' in sentence and '.' in sentence]
    # print(sentence_list)
    article = ' '.join(sentence_list)
    summary = summarize(article, ratio=0.1)
    print(summary)
    print('Statistics: Article length: %d, Summary length: %d' % (len(article), len(summary)))
    print('----------------------------------------------------------------------------------------------------')
