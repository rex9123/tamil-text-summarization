# -*- coding: utf-8 -*-
import os
import wikipedia
import re
from nltk.tokenize import sent_tokenize, word_tokenize

wikipedia.set_lang("ta")

TOPICS = [
    "சென்னை",
    "பெங்களூர்",
    "தில்லி",
    "கொல்கத்தா",
    "மும்பை"
]

SUMMARY_PATH = "../test/summaries"
ARTICLE_PATH = "../test/data"
TITLE_PATH = "../test/title"

ELIMINATION_THRESHOLD = 0.1
PARAGRAPH_THRESHOLD = 15
SUMMARY_SIZE = 8

# Create directories if they do not exist
os.makedirs(SUMMARY_PATH, exist_ok=True)
os.makedirs(ARTICLE_PATH, exist_ok=True)
os.makedirs(TITLE_PATH, exist_ok=True)

def getContentRichParagraphs(d):
    wordCount = {}
    paragraph = re.split("\n{1,}", d)

    for i in range(len(paragraph)):
        wordCount[i] = len(word_tokenize(paragraph[i]))

    maxWordCount = max(wordCount.values())

    # Filtering the very small lines
    selectedParagraphs = list(filter(lambda l: float(wordCount[l]) / maxWordCount >= ELIMINATION_THRESHOLD, wordCount.keys()))

    return "\n".join([paragraph[l] for l in selectedParagraphs[0:PARAGRAPH_THRESHOLD]])


def cleanContent(d, contentRich=False):
    if isinstance(d, bytes):
        d = d.decode('utf-8')  # Decode bytes to string if necessary

    d = re.sub(r'[a-zA-Z\(\)\'\"\[\]\*]', '', d)

    d = (d if not contentRich else getContentRichParagraphs(d))
    d = re.sub('\s{2,}', ' ', d)
    d = re.sub('\n{3,}', '\n\n', d)

    d = re.sub('[\.\s]?\.+', '.', d)

    # HOT FIXES
    d = re.sub(r'\xe0\xae\x95\xe0\xae\xbf\.\xe0\xae\xaa\xe0\xae\xbf\.','\xe0\xae\x95\xe0\xae\xbf\.\xe0\xae\xaa\xe0\xae\xbf', d)
    d = re.sub(r'\xe0\xae\x95\xe0\xae\xbf\.\xe0\xae\xae\xe0\xaf\x80\.','\xe0\xae\x95\xe0\xae\xbf\.\xe0\xae\xAE\xe0\xaf\x80', d)
    d = re.sub(r'\xe0\xae\x95\xe0\xae\xbf\.\xe0\xae\xAE\xe0\xaf\x81\.','\xe0\xae\x95\xe0\xae\xbf\.\xe0\xae\xAE\xe0\xaf\x81', d)

    return d


def cleanSummary(d):
    return "\n".join(sent_tokenize(cleanContent(d))[0:SUMMARY_SIZE])


def filterSummaryFromContent(content, summary):
    return content.replace(summary, '')


for i in range(len(TOPICS)):
    wiki = wikipedia.page(TOPICS[i])
    fileName = "article-" + str(i + 1)

    summary = wiki.summary
    content = filterSummaryFromContent(wiki.content, wiki.summary)
    title = wiki.title

    # Write summaries and articles directly as strings
    with open(os.path.join(SUMMARY_PATH, fileName), "w+", encoding='utf-8') as f:
        f.write(cleanSummary(summary))  # No need to encode

    with open(os.path.join(ARTICLE_PATH, fileName), "w+", encoding='utf-8') as f:
        f.write(cleanContent(content, contentRich=True))  # No need to encode

    with open(os.path.join(TITLE_PATH, fileName), "w+", encoding='utf-8') as f:
        f.write(cleanContent(title))  # No need to encode

    print(TOPICS[i])
