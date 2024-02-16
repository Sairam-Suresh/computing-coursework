# This script was created in full by Ayaan Jain from S408

# import packages
import pandas as pd
import spacy
import string
from spacy.lang.en.stop_words import STOP_WORDS
import concurrent.futures
# We could use other models but this is better for tasks such as document retrieval based on keyword matching.
from gensim.models import TfidfModel
from gensim import corpora
from gensim.similarities import MatrixSimilarity
import pickle
import streamlit as st

# import the web scrapers
from Scraping_Brightsparks import brightsparks
from Scraping_Mindef_Scholarships import mindef_scholarships
from Scraping_Scholarshipportal import scrape
from Scraping_Scholars4Dev import Scholars4Dev

# We use pickle instead of json, as pickle is better for python
scholarships_cache = "scholarships_cache.pkl"

global dictionary
global scholarships_results_text


def mindef_scraper_function():
    data = mindef_scholarships()
    return data


def scholarshipportal_scraper_function():
    data = scrape()
    return data


def scholars4dev_scraper_function():
    data = Scholars4Dev()
    return data


def brightsparks_scraper_function():
    try:
        data = brightsparks()
        return data
    except:
        print("Brightsparks scraper is down")
        return None


def pre_processing(text):
    spacy_nlp = spacy.load("en_core_web_sm")

    # Words to remove
    punctuations = string.punctuation
    stop_words = spacy.lang.en.stop_words.STOP_WORDS

    # Tokenize the individual words as a form of data pre-processing

    # Tokenize the text of each scholarship
    tokens = spacy_nlp(text)

    result_tokens = []

    for word in tokens:
        word = word.lemma_
        word = word.lower()
        word = word.strip()
        if len(word) >= 3 and word not in stop_words and word not in punctuations:
            try:
                result_tokens.append(word)
            except:
                print("error")

    return result_tokens


def create_model(body_text):
    # We calculate a Term Frequency-Inverse Document Frequency (TFIDF) weight for each of the individual tokens in
    # the bowl of words representation that we create

    global dictionary
    global corpus
    dictionary = corpora.Dictionary(body_text)
    corpus = [dictionary.doc2bow(tokens) for tokens in body_text]

    important_words_model = TfidfModel(corpus, normalize=True)

    return important_words_model


def scrape_website():
    # This function gathers all the scraped data from the websites
    text_tokenized = []

    # The following code was added by Sairam from S401: Parallel scraping of websites using
    # concurrent.futures.ProcessPoolExecutor The following functions are used to submit work to the ProcessPoolExecutor

    # Execute all scrapers in parallel using ProcessPoolExecutor
    # and append the results to the text_tokenized list
    with concurrent.futures.ProcessPoolExecutor() as executor:
        scrapers = [
            executor.submit(scholarshipportal_scraper_function),
            executor.submit(mindef_scraper_function),
            executor.submit(brightsparks_scraper_function),
            executor.submit(scholars4dev_scraper_function)
        ]

        for data in concurrent.futures.as_completed(scrapers):
            result = data.result()

            if result is not None:
                for e in range(len(result)):
                    text_tokenized.append([result[e][0], pre_processing(result[e][1])])
            else:
                # A scraper returned None, so we skip it
                continue

    # Sairam's code ends here

    # Casts the tokenized array of words in each scholarship, into a Pandas dataframe as this makes it easier to
    # create a tfidf model
    scholarships_results_dataframe = pd.DataFrame(text_tokenized)
    scholarships_results_dataframe.rename(columns={0: "Link", 1: "Body"}, inplace=True)

    # Save file to cache
    with open(scholarships_cache, "wb") as f:
        pickle.dump(scholarships_results_dataframe, f)

    return scholarships_results_dataframe


def search_function(user_input):
    try:
        with open(scholarships_cache, "rb") as f:
            scholarships_results_text = pickle.load(f)
            if scholarships_results_text is not None:
                st.write("Data loaded from cache successfully")
            else:
                scholarships_results_text = scrape_website()
    except:
        scholarships_results_text = scrape_website()

    # Create a model using the body text of all the scholarships
    corpus_model = create_model(scholarships_results_text["Body"])

    # Save the models to the computer
    corpora.MmCorpus.serialize('scholarships_search_model', corpus_model[corpus])
    tfidf_corpus = corpora.MmCorpus('scholarships_search_model')

    scholarships_list = MatrixSimilarity(tfidf_corpus, num_features=corpus_model.num_nnz)

    bowl_of_words_search = dictionary.doc2bow(pre_processing(user_input))
    search_model = corpus_model[bowl_of_words_search]

    scholarships_list.num_best = 5

    scholarships_index = scholarships_list[bowl_of_words_search]

    # scholarships_index.sort(itemgetter(1), reverse=True)
    scholarships_index.sort()

    results = []

    for e, scholarship in enumerate(scholarships_index):

        results.append(
            {"Relevance": round((scholarship[1] * 100), 2), "Link": scholarships_results_text["Link"][scholarship[0]]})
        if e == (scholarships_list.num_best - 1):
            break

    pd.set_option('display.max_colwidth', None)
    results = pd.DataFrame(results, columns=["Relevance", "Link"])
    results_sorted = results.sort_values(by="Relevance", ascending=False)

    # I sorted the results based on their relevancy score, then removed the index from them
    results_output = results_sorted["Link"].reset_index(drop=True)

    return results_output
