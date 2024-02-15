# Done By: Ayaan

from Semantic_Search import *
import streamlit as st

# Requires the user to acknowledge that the disclaimer
internet_disclaimer = st.checkbox("Acknowledge that using this programme requires you to have an internet connection")

if internet_disclaimer:
    st.markdown("## Scholarship Finder - Coursework 2024")
    st.markdown('### Input the keywords of the scholarship you are looking for. Do not input what you do not want, '
                'such as "I do not want to do engineering", only input what you are searching for.')
    st.write("---")

    # Streamlit capture user input
    user_input = st.chat_input("e.g. I am looking to study engineering in Yale")

    if user_input:
        # Progress bar that is synced
        with st.spinner("Scraping website data"):
            search_output = (search_function(user_input))

        scholarships_output = search_output
        if scholarships_output.empty:
            st.write("Unfortunately we were not able to find any scholarships that satisfy your needs")
        else:
            st.markdown("### Here are the top 10 scholarships in descending order")
            st.write(scholarships_output)
