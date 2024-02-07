from Semantic_Search import *
import time

#TODO:
#Explan why the medicine scholarship doesn't show up

#Streamlit
internet_disclaimer = st.checkbox("Acknowledge that using this programme requires you to have an internet connection")

if internet_disclaimer:
    st.markdown("## Scholarship Finder - Coursework 2024")
    st.markdown('### Input the keywords of the scholarship you are looking for. Do not input what you do not want, such as "I do not want to do engineering", only input what you are searching for.')
    st.write("---")

    #Streamlit capture user input
    user_input = ""
    user_input = st.chat_input("e.g. I am looking to study engineering in Yale")

    if user_input:
        progress_bar = st.progress(0, "Finding scholarships")
        for percentages_completion in range(100):
            time.sleep(0.7)
            progress_bar.progress(percentages_completion + 1, "Finding scholarships")
        scholarships_output = (search_function(user_input))
        if scholarships_output.empty:
            st.write("Unfortunately we were not able to find any scholarships that satisfy your needs")
        else:
            st.write(scholarships_output) 