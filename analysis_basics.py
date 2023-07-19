"""
Script to perform some basic analysis on the bibliographic data Bibliographie18. 
"""


# === Imports === 

import re 
import seaborn as sns
from matplotlib import pyplot as plt
from os.path import join
from os.path import realpath, dirname
import os
from lxml import etree
from io import StringIO, BytesIO
from collections import Counter
import pandas as pd



# === Files and parameters === 

wdir  = realpath(dirname(__file__))
bibdatafile = join(wdir, "..", "formats", "bibliographie18_Zotero-RDF.rdf") 
#bibdatafile = join(wdir, "..", "formats", "bibliographie18_Zotero-RDF_TEST.rdf") 

namespaces = {
    "foaf" : "http://xmlns.com/foaf/0.1/",
    "bib" : "http://purl.org/net/biblio#",
    "dc" : "http://purl.org/dc/elements/1.1/",
    "z" : "http://www.zotero.org/namespaces/export#",
    "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    }



# === Functions === 

def read_json(bibdatafile): 
    bibdata = etree.parse(bibdatafile)
    return bibdata



def get_personnames(bibdata): 
    print("\npersonnames")

    # Find all the instances of persons
    personnames = []
    xpath = "//foaf:Person"
    persons = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(persons), "instances of Element 'person'")

    # Get the names (full name or first name, last name) from each person
    for item in persons: 
        if len(item) == 1: 
            personname = item[0].text
            personnames.append(personname)
        elif len(item) == 2: 
            personname = item[0].text + ", " + item[1].text 
            personnames.append(personname)    
    return personnames



def get_publishers(bibdata): 
    print("\npublisher names")

    # Find all the instances of publisher names
    publishers = []
    xpath = "//dc:publisher//foaf:name/text()"
    publishers = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(publishers))
    return publishers



def most_frequent_personnames(personnames): 
    # Count the occurrences, find the 10 most frequently mentioned persons
    personnames_counts = Counter(personnames)
    print(len(personnames_counts))
    personnames_counts = dict(sorted(personnames_counts.items(), key = lambda item: item[1], reverse=True)[:10])
    print(personnames_counts)
    for item in personnames_counts: 
        print(item)



def most_frequent_publishers(publishers):
    # Count the occurrences, find the 10 most frequently mentioned publishers
    publishernames_counts = Counter(publishers)
    print(len(publishernames_counts))
    publishernames_counts = dict(sorted(publishernames_counts.items(), key = lambda item: item[1], reverse=True)[:11])
    print(publishernames_counts)



def get_pubtypes(bibdata): 
    print("\nPublication types")

    # Find all the instances of publication types
    pubtypes = []
    xpath = "//z:itemType/text()"
    pubtypes = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(pubtypes), "instances of publication type")
    return pubtypes



def most_frequent_pubtypes(pubtypes): 
    # Count the occurrences, find the 10 most frequently mentioned persons
    pubtypes_counts = Counter(pubtypes)
    print(len(pubtypes_counts), "types of publication types")
    pubtypes_counts = dict(sorted(pubtypes_counts.items(), key = lambda item: item[1], reverse=True)[:10])
    print(pubtypes_counts)



def get_languages(bibdata): 
    print("\nLanguages")

    # Find all the instances of "language" Element and its content
    xpath = "//z:language/text()"
    languages = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(languages), "instances of language")

    # Identify frequency of languages
    languages_counts = Counter(languages)
    print(len(languages_counts), "number of different languages")
    languages_counts = dict(sorted(languages_counts.items(), key = lambda item: item[1], reverse=True)[:10])
    print(languages_counts)

    # Visualize using a simple bar chart 
    lc = pd.DataFrame.from_dict(languages_counts, orient="index", columns=["count"]).reset_index().rename({"index" : "language"}, axis=1)
    print(lc.head())
    plt.figure(figsize=(12,6))
    pal = sns.color_palette("Blues", len(lc))
    fig = sns.barplot(data=lc, x="language", y="count", palette=pal)
    fig.set_xticklabels(fig.get_xticklabels(), rotation=30)
    for i in fig.containers:
        fig.bar_label(i,)
    plt.savefig(join(wdir, "figures", "languages_counts.png"))



# === Main === 

def main(): 
    bibdata = read_json(bibdatafile)
    #pubtypes = get_pubtypes(bibdata)
    #most_frequent_pubtypes(pubtypes)
    #pubyear_count = get_pubyears(bibdata)
    #visualize_pubyears(pubyear_count)
    #personnames = get_personnames(bibdata)
    #most_frequent_personnames(personnames)
    #publishers = get_publishers(bibdata)
    #most_frequent_publishers(publishers)
    get_languages(bibdata)

main()
