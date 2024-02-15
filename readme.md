# ScholarFinder (Coursework 2024)
Presented to you by Sairam from S401 and Ayaan and Lohith from S408

## Introduction
ScholarFinder is a web application that helps students find a scholarship that they would like 
to pursue without having to go through the hassle of searching for scholarships on different websites.

## Features
**Search**: Users can search for scholarships based on their preferences, with a chat-like interface

**Caching**: The application searches online for scholarships and downloads them to a database, so
that future queries are much faster

## Installation
1. Obtain a copy of this source code
2. Install the required dependencies using this command:
```bash
pip3 install selenium webdriver_manager pandas numpy spacy gensim scikit_learn streamlit beautifulsoup4 watchdog
spacy download en_core_web_sm
```
3. Run the application using this command in the folder where the source code is located:
```bash
python3 -m streamlit run user_interface.py
```
4. Open the link provided in the terminal to access the application
5. Enjoy!

## Note!
When you run the application and give it a query for the very first time it will take up to 
**12 minutes** to complete, so please be patient! Subsequent answering times will be much faster
afterwards

Make sure to have a stable internet connection when running the application, and not to put in any
negative terms when searching for scholarships, as the model is currently unable to handle them at
the moment