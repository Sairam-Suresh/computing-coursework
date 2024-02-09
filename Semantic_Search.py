#Done By: Ayaan (408)

#import packages
import pickle
import os
import pandas as pd
import numpy as np
import spacy
import string
import streamlit as st
from time import *
from spacy.lang.en.stop_words import STOP_WORDS
from Scrape_Mindef_Scholarships import *
from gensim.models import TfidfModel #We could use other models but this is better for tasks such as document retrieval based on keyword matching.
from gensim import corpora
from gensim.similarities import MatrixSimilarity
from operator import itemgetter
from Sairam import *


#We use pickle instead of json, as pickle is better for python
scholarships_cache = "scholarships_cache.pkl"

global dictionary
global scholarships_results_text


def pre_processing(text):

    spacy_nlp = spacy.load("en_core_web_sm")

    #Words to remove
    punctuations = string.punctuation
    stop_words = spacy.lang.en.stop_words.STOP_WORDS

    #Tokenize the individual words as a form of data pre-processing
        
    #Tokenize the text of each scholarship
    tokens = spacy_nlp(text)

    result_tokens = []


    for word in tokens:
        word = word.lemma_
        word = word.lower()
        word = word.strip()
        if len(word)>=3 and word not in stop_words and word not in punctuations:
            try:
                result_tokens.append(word)
            except:
                print("error")

    return result_tokens

def create_model(body_text):
    #We calculate a Term Frequency-Inverse Document Frequency (TFIDF) weight for each of the individual tokens in the bowl of words representation that we create

    global dictionary
    global corpus
    dictionary = corpora.Dictionary(body_text)
    corpus = [dictionary.doc2bow(tokens) for tokens in body_text]

    important_words_model = TfidfModel(corpus, normalize = True)

    return important_words_model

def scrape_website():
    st.title("NO WAY")
    #This function gathers all the scraped data from the websites

    text_tokenized = []

    text = mindefScholarship()
    for i in range(len(text)):
        text_tokenized.append([text[i][0], pre_processing(text[i][1])])

    """ #ToDo: Rename this cause its funny
    international_scholarships = scrape()
    for e in range(len(international_scholarships)):
        try:
            text_tokenized.append([international_scholarships[i][0], pre_processing(international_scholarships[i][1])])
        except:
            pass
    """

    #Casts the tokenized array of words in each scholarship, into a Pandas dataframe as this makes it easier to create a tfidf model
    scholarships_results_text = pd.DataFrame(text_tokenized)
    scholarships_results_text.rename(columns={0: "Link", 1: "Body"}, inplace=True)

    #save file to cache
    with open(scholarships_cache, "wb") as f:
        pickle.dump(scholarships_results_text, f)

    return scholarships_results_text

def search_function(user_input):

    try:
        with open(scholarships_cache, "rb") as f:
            scholarships_results_text = pickle.load(f)
    except:
        scholarships_results_text = scrape_website()
    
    #Create a model using the body text of all the scholarships
    corpus_model = create_model(scholarships_results_text["Body"])

    #Save the models to the computer
    corpora.MmCorpus.serialize('scholarships_model', corpus_model[corpus])
    tfidf_corpus = corpora.MmCorpus('scholarships_model')

    scholarships_list = MatrixSimilarity(tfidf_corpus, num_features=corpus_model.num_nnz)
    
    bowlofwords_search = dictionary.doc2bow(pre_processing(user_input))
    search_model = corpus_model[bowlofwords_search]

    scholarships_list.num_best = 10

    scholarships_index = scholarships_list[bowlofwords_search]

    #scholarships_index.sort(itemgetter(1), reverse=True)
    scholarships_index.sort()

    results = []

    for e, scholarship in enumerate(scholarships_index):

        results.append({"Relevance": round((scholarship[1] * 100),2), "Link": scholarships_results_text["Link"][scholarship[0]]})
        if e == (scholarships_list.num_best-1):
            break

    pd.set_option('display.max_colwidth', None)
    results = pd.DataFrame(results, columns=["Relevance", "Link"])
    results_sorted = results.sort_values(by="Relevance", ascending=False)

    #I sorted the results based on their relevancy score, then removed the index from them
    results_output = results_sorted["Link"].reset_index(drop=True)

    return results_output
