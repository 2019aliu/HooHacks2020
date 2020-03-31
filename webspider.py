import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize
import random

# Define constants
htmlParser = 'html5lib'
numArticles = 10
sampleQuery = "covid-19%20OR%20coronavirus%20when:2d"
summarizationRatio = 0.1
previewWordLimit = 100

def scrapeSummarize(link):
    """
    Scrapes and summarizes a news article

    Args:
        link: the link to the news article
    
    Returns:
        A summary of the article
    """
    articlePage = requests.get(link).text
    articleSoup = BeautifulSoup(articlePage, htmlParser)
    rawTags = articleSoup.find_all('p')
    rawTexts = [tag.get_text().strip() for tag in rawTags]

    # Filter out sentences that contain newline characters '\n' or don't contain periods.
    sentence_list = [sentence for sentence in rawTexts if not '\n' in sentence and '.' in sentence]
    article = ' '.join(sentence_list)

    # summarize the individual articles
    summary = summarize(article, ratio=summarizationRatio)
    return summary

def newsSearch(query):
    """
    Performs a Google News search

    Args:
        query: the query to enter into Google News
    
    Returns:
        Tuple containing a list of headlines in the first element, and a list of links in the second element. 
        A headline corresponds to a link with the same index
    """
    # Retrieve search page text: covid-19 or coronavirus, last 48 hours
    newsSearchUrl = "http://news.google.com/news?q=%s&output=rss" % query
    newsSearchResult = requests.get(newsSearchUrl).text
    # Turn search page into BeautifulSoup object to access HTML tags
    newsSearchSoup = BeautifulSoup(newsSearchResult, htmlParser)

    # Get articles
    headlines = newsSearchSoup.find_all('title')
    links = newsSearchSoup.find_all('description')
    return (headlines, links)

def generatePreview(query):
    """
    Generates a preview of the daily digest of recent articles for a query

    Args:
        query: The query to generate a preview for
    
    Returns:
        A short paragraph previewing the news in the form of a string
    """
    (headlines, links) = newsSearch(query)
    summary = ""
    while len(summary) <= 0:
        randomIndex = random.randint(1, numArticles)
        # Scrape the data from the article
        headline = headlines[randomIndex].get_text()
        link = links[randomIndex].get_text().split()[1][6:-1]
        summary = scrapeSummarize(link)
    summaryWords = summary.split()
    if len(summaryWords) > previewWordLimit:
        return ' '.join(summaryWords[:previewWordLimit])
    return summary

# preview = generatePreview(sampleQuery)
# print(type(preview))
# print("%s\n\nPreview length: %d" % (preview, len(preview)))

def generateDigest(query):
    """
    Generates a roughly one-minute digest of recent articles for a query

    Args:
        query: The query to generate a digest for
    
    Returns:
        A 1-minute digest in the form of a list of strings
    """
    (headlines, links) = newsSearch(query)

    bigsummary = ""
    for i in range(1, 1+numArticles):
        # Scrape the data from the article
        headline = headlines[i].get_text()
        # I couldn't use the .get() method, so I manually parsed it out
        # Also I can't get the <link> tag for some reason wtfffffff
        link = links[i].get_text().split()[1][6:-1]
        summary = scrapeSummarize(link)
        bigsummary += summary + "\n"

    # Finally, generate the daily digest using the summarization tool on all individual summaries.
    dailydigest = summarize(bigsummary, ratio=summarizationRatio)
    return dailydigest.split("\n")

# print(generateDigest(sampleQuery))
