#Done By: Ayaan

import pandas as pd
import numpy as np
import spacy
import string
import streamlit as st
from spacy.lang.en.stop_words import STOP_WORDS
from mindefScholarships import *
from gensim.models import TfidfModel #We could use any model but this is good
from gensim import corpora
from gensim.similarities import MatrixSimilarity
from operator import itemgetter
from Sairam import *


global dictionary


def pre_processing(text):

    spacy_nlp = spacy.load("en_core_web_sm")

    #words to remove
    punctuations = string.punctuation
    stop_words = spacy.lang.en.stop_words.STOP_WORDS

    #Tokenize the individual words as a form of data pre-processing
        
    #tokenize the text of each scholarship
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

def createModel(body_text):

    global dictionary
    global corpus
    dictionary = corpora.Dictionary(body_text)
    corpus = [dictionary.doc2bow(tokens) for tokens in body_text]

    important_words_model = TfidfModel(corpus, normalize = True)

    return important_words_model

def scrape_website():
    text = mindefScholarship()
    text_tokenized = []
    for i in range(len(text)):
        text_tokenized.append([text[i][0], pre_processing(text[i][1])])
    international_scholarships = scrape()
    for e in range(len(international_scholarships)):
        try:
            text_tokenized.append([international_scholarships[i][0], pre_processing(international_scholarships[i][1])])
        except:
            pass
    #print("hello")
    scholarships_results_text = pd.DataFrame(text_tokenized)
    scholarships_results_text.rename(columns={0: "Link", 1: "Body"}, inplace=True)

    return scholarships_results_text

def search_function(user_input):

    scholarships_results_text = scrape_website()
    corpus_model = createModel(scholarships_results_text["Body"])

    #CHANGE CAUSE TOO SIMILAR WITH INTERNET
    corpora.MmCorpus.serialize('model_mm', corpus_model[corpus])
    scholarships_tfidf_corpus = corpora.MmCorpus('model_mm')

    scholarships_list = MatrixSimilarity(scholarships_tfidf_corpus, num_features=corpus_model.num_nnz)
    
    bowlofwords_search = dictionary.doc2bow(pre_processing(user_input))
    search_model = corpus_model[bowlofwords_search]

    scholarships_list.num_best = 6 #Change to 10

    scholarships_index = scholarships_list[bowlofwords_search]

    #scholarships_index.sort(itemgetter(1), reverse=True)
    scholarships_index.sort()

    results = []

    for e, scholarship in enumerate(scholarships_index):

        results.append(
            {
                "Relevance": round((scholarship[1] * 100),2),
                "Link": scholarships_results_text["Link"][scholarship[0]]
            }
        )

        if e == (scholarships_list.num_best-1):
            break

    pd.set_option('display.max_colwidth', None)
    results = pd.DataFrame(results, columns=["Relevance", "Link"])
    results_sorted = results.sort_values(by="Relevance", ascending=False)
    #Print out what the output is and explain to the user its descending list by 
    #Tell user what to input with example
    #Specify you need an interne

    #I sorted the results based on their relevancy score, then removed the index from them
    results_output = results_sorted["Link"].reset_index(drop=True)

    return results_output
