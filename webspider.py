import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize

# Define constants
htmlParser = 'html5lib'
numArticles = 10
sampleQuery = "covid-19%20OR%20coronavirus%20when:2d"

def generateDigest(query):
    """
    Generates a roughly one-minute digest of recent articles for the given query

    Args:
        query: The query to generate a digest for
    
    Returns:
        A 1-minute digest in the form of a list of strings
    """
    # Retrieve search page text: covid-19 or coronavirus, last 48 hours
    newsSearchUrl = "http://news.google.com/news?q=%s&output=rss" % query
    newsSearchResult = requests.get(newsSearchUrl).text
    # Turn search page into BeautifulSoup object to access HTML tags
    newsSearchSoup = BeautifulSoup(newsSearchResult, htmlParser)

    # Get articles
    headlines = newsSearchSoup.find_all('title')
    links = newsSearchSoup.find_all('description')

    bigsummary = ""
    for i in range(1, 1+numArticles):
        # Scrape the data from the article
        headline = headlines[i].get_text()
        # I couldn't use the .get() method, so I manually parsed it out
        # Also I can't get the <link> tag for some reason wtfffffff
        link = links[i].get_text().split()[1][6:-1]
        articlePage = requests.get(link).text
        articleSoup = BeautifulSoup(articlePage, htmlParser)
        rawTags = articleSoup.find_all('p')
        rawTexts = [tag.get_text().strip() for tag in rawTags]

        # Filter out sentences that contain newline characters '\n' or don't contain periods.
        sentence_list = [sentence for sentence in rawTexts if not '\n' in sentence and '.' in sentence]
        article = ' '.join(sentence_list)

        # summarize the individual articles
        summary = summarize(article, ratio=0.1)
        bigsummary += summary + "\n"

    # Finally, generate the daily digest using the summarization tool on all individual summaries.
    dailydigest = summarize(bigsummary, ratio=0.1)
    # print(dailydigest.split("\n"))
    # return dailydigest
    return dailydigest.split("\n")
        

# print(generateDigest(sampleQuery))