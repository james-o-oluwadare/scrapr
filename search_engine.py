# extracted from jupyter notebook
# wrap code into functions and oop
# include class that reads data from url and writes to db
#    to be used in main.py

import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
import requests
import pickle
from collections import defaultdict
from math import log
import math
import time
import re
from tqdm import tqdm_notebook as tqdm
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# only needs to be run once to update for the whole package
nltk.download('stopwords')
nltk.download('wordnet')

# 
url = f"https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?ordering=publicationYearThenTitle&descending=true"
#url = f"https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/"
page = requests.get(url, verify=False).text
doc = BeautifulSoup(page, "html.parser")

num_pub = int(doc.find("li", class_="search-pager-information").text.strip().strip("/n").split()[-2])

q, r = divmod(num_pub, 50)
combined_pattern = re.compile(r"(^[A-Z][a-z]*(?:\s[A-Z][a-z]*)*,\s[A-Z][a-z]*(?:\s[A-Z][a-z]*)*(?:,\s[A-Z][a-z]*(?:\s[A-Z][a-z]*)*)*)|(^[A-Z][a-z]*(?:-[A-Z][a-z]*)*,\s[A-Z][a-z]*(?:-[A-Z][a-z]*)*(?:,\s[A-Z][a-z]*(?:-[A-Z][a-z]*)*)*)")
combined_pattern = re.compile(r"(^\w+(?:\s\w+)*,\s\w+(?:\s\w+)*(?:,\s\w+(?:\s\w+)*)*)|(^\w+(?:-\w+)*,\s\w+(?:-\w+)*(?:,\s\w+(?:-\w+)*)*)")

def to_str(string):
    return str(unicodedata.normalize('NFKD', string).encode('ascii', 'ignore'), "utf-8")

def get_authors(list_result):
    authors = []
    for i in list_result.find_all("span"):
        if combined_pattern.search(to_str(i.text)):
            authors.append(i.text)
    return authors

def get_author_link(name_links, authors):
    author_link = [None for i in range(len(authors))]
    for i in name_links:
        index = authors.index(i.text)
        author_link[index] = i.get("href")
    return author_link

def get_each_pub(list_result):
    title = list_result.find("h3", class_="title").find("a").text
    title_link = list_result.find("h3", class_="title").find("a").get("href")
    yr = int(list_result.find("span", class_="date").text.split()[-1])
    authors = get_authors(list_result)
    name_links = list_result.find_all("a", rel="Person")
    authors_link = get_author_link(name_links, authors)
    return (authors, authors_link, yr, title, title_link)

def get_pub(doc, num):
    for i in tqdm(range(num)):
        list_result = doc.find(class_="list-results").find(class_=f"list-result-item list-result-item-{i}")

        authors, authors_link, yr, title, title_link = get_each_pub(list_result)
        publications["Authors"].append(authors)
        publications["Authors_link"].append(authors_link)
        publications["Publication_Year"].append(yr)
        publications["Title"].append(title)
        publications["link"].append(title_link)

publications = {"Authors":[], "Authors_link":[], "Publication_Year":[], "Title":[], "link":[]}
for i in tqdm(range(q+1)):
    if i == 0:
        url = f"https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?ordering=publicationYearThenTitle&descending=true"
    else:
        url = f"https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?ordering=publicationYearThenTitle&descending=true&page={1}"
    
    
    page = requests.get(url, verify=False).text
    doc = BeautifulSoup(page, "html.parser")
    if i != 4:
        get_pub(doc, 50)
    else:
        get_pub(doc, r)

df = pd.DataFrame(publications)

# Connect to database (creates the database if it doesn't exist)
conn = sqlite3.connect('publications.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create Authors table
c.execute('''CREATE TABLE Authors (
                id INTEGER PRIMARY KEY,
                Name TEXT,
                Link TEXT,
                Paper INTEGER,
                FOREIGN KEY (Paper) REFERENCES Papers(id)
            )''')

# Create Papers table
c.execute('''CREATE TABLE Papers (
                id INTEGER PRIMARY KEY,
                Title TEXT,
                Link TEXT,
                PublicationYear INTEGER
            )''')

# Commit changes and close connection
conn.commit()
conn.close()

# Connect to database (creates the database if it doesn't exist)
conn = sqlite3.connect('publications.db')
# Create a cursor object to execute SQL commands
c = conn.cursor()

# Insert data into Papers table
for index, row in df.iterrows():
    c.execute('''INSERT INTO Papers (Title, Link, PublicationYear) VALUES (?, ?, ?)''', (row['Title'], row['link'], row['Publication_Year']))


# Commit changes and close connection
conn.commit()
conn.close()


# Insert data into Authors table
for index, row in df.iterrows():
    for i in zip(row['Authors'], row['Authors_link']):
        c.execute('''INSERT INTO Authors (Name, Link, Paper) VALUES (?, ?, ?)''', (i[0], i[1], index+1))
# Commit changes and close connection
conn.commit()


try:

    # connect to a databse
    conn = sqlite3.connect('publications.db')

    # If sqlite3 makes a connection with python
    # program then it will print "Connected to SQLite"
    # Otherwise it will show errors
    print("Connected to SQLite")

    # Getting all tables from sqlite_master
    sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""

    # Creating cursor object using connection object
    cursor = conn.cursor()

    # executing our sql query
    cursor.execute(sql_query)
    print("List of tables\n")

    # printing all tables list
    print(cursor.fetchall())

except sqlite3.Error as error:
    print("Failed to execute the above query", error)

finally:

    # Inside Finally Block, If connection is
    # open, we need to close it
    if conn:

        # using close() method, we will close
        # the connection
        conn.close()

        # After closing connection object, we
        # will print "the sqlite connection is
        # closed"
        print("the sqlite connection is closed")

papers = pd.read_sql_query("SELECT * FROM Papers", conn)

author = pd.read_sql_query("SELECT * FROM Authors", conn)

# Set up the database connection
conn = sqlite3.connect('publications.db')
c = conn.cursor()

# Define the pre-processing functions
stop_words = set(stopwords.words('english'))
#stemmer = PorterStemmer()
lemma = nltk.wordnet.WordNetLemmatizer()


def preprocess(text):
#     # Tokenize the text
#     tokens = text.split()
    # Remove non-alphanumeric characters and split into tokens
    tokens = re.findall(r'\w+', text)
    
    # Remove stopwords
    tokens = [token for token in tokens if token not in stop_words]
    
    # Convert the tokens to lowercase
    tokens = [token.lower() for token in tokens]
    
    # Lematize the tokens
    tokens = [lemma.lemmatize(token) for token in tokens]
    
    # Remove punctuation and special characters
    tokens = [re.sub(r'[^\w\s]', '', token) for token in tokens]
    
    # Remove single-letter tokens
    tokens = [token for token in tokens if len(token) > 1]
    
    return tokens

def create_inverted_index(table_name):
    inverted_index = {}
    if table_name == "Papers":
        c.execute("SELECT rowid, Title, PublicationYear FROM Papers")
        papers = c.fetchall()
        num_papers = len(papers)
        for paper in papers:
            paper_id = paper[0]
            title = paper[1]
            year = paper[2]
            text = title + " " + str(year)
            tokens = preprocess(text)
            for token in tokens:
                if token not in inverted_index:
                    inverted_index[token] = {}
                if paper_id not in inverted_index[token]:
                    inverted_index[token][paper_id] = 0
                inverted_index[token][paper_id] += 1
        for token in inverted_index.keys():
            df = len(inverted_index[token])
            idf = math.log(num_papers / df)
            for paper_id in inverted_index[token].keys():
                tf = inverted_index[token][paper_id]
                tfidf = tf * idf
                inverted_index[token][paper_id] = tfidf
    elif table_name == "Authors":
        c.execute("SELECT Authors.Name, Papers.rowid FROM Authors JOIN Papers ON Authors.Paper=Papers.rowid")
        author_paper_rows = c.fetchall()
        num_papers = c.execute("SELECT COUNT(DISTINCT Papers.rowid) FROM Papers").fetchone()[0]
        for row in author_paper_rows:
            author_name = row[0]
            paper_id = row[1]
            text = author_name
            tokens = preprocess(text)
            for token in tokens:
                if token not in inverted_index:
                    inverted_index[token] = {}
                if paper_id not in inverted_index[token]:
                    inverted_index[token][paper_id] = 0
                inverted_index[token][paper_id] += 1
        for token in inverted_index.keys():
            df = len(inverted_index[token])
            idf = math.log(num_papers / df)
            for paper_id in inverted_index[token].keys():
                tf = inverted_index[token][paper_id]
                tfidf = tf * idf
                inverted_index[token][paper_id] = tfidf
    else:
        print("Error: Invalid table name.")
    
    return inverted_index

inverted_index_paper = create_inverted_index("Papers")
inverted_index_author = create_inverted_index("Authors")

inverted_index_combined = {}
for token in inverted_index_paper.keys():
    if token not in inverted_index_combined:
        inverted_index_combined[token] = inverted_index_paper[token]
    else:
        inverted_index_combined[token].update(inverted_index_paper[token])
        
for token in inverted_index_author.keys():
    if token not in inverted_index_combined:
        inverted_index_combined[token] = inverted_index_author[token]
    else:
        inverted_index_combined[token].update(inverted_index_author[token])


with open('inverted_index.pkl', 'rb') as fp:
    inverted_index_combined = pickle.load(fp)


def query_inverted_index(query, inverted_index):
    if query == "":
        print("You need to enter something to search")
        return
    conn = sqlite3.connect('publications.db')
    c = conn.cursor()
    tokens = preprocess(query)
    scores = {}
    for token in tokens:
        if token in inverted_index:
            for paper_id, score in inverted_index[token].items():
                if paper_id not in scores:
                    scores[paper_id] = 0
                scores[paper_id] += score
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = []
    for paper_id, score in sorted_scores:
        c.execute("""SELECT DISTINCT Papers.Title, Papers.Link, Papers.PublicationYear, Authors.Name, Authors.Link
                     FROM Papers 
                     INNER JOIN Authors ON Papers.Id = Authors.Paper
                     WHERE Papers.Id=?""", (paper_id,))
        row = c.fetchone()
        if row:
            title, link, year, authors, authors_link = row
            results.append((title, link, year, score, authors, authors_link))
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Year: {year}")
        print(f"Author: {authors}")
        print(f"Authors Link: {authors_link}")
        print(f"Relevance Score: {score}")
        print("\n")
    conn.close()
    return #results


q = input("Enter your search: ")
print()
query_inverted_index(q, inverted_index_combined)