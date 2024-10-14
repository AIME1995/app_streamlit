import pandas as pd   
import numpy as np      
import streamlit as st 
import plotly.express as px 
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt  
# python -m streamlit run app.py

st.title("Streamlit Analysis of tweets of US Airlines")
st.sidebar.title("Streamlit Analysis of tweets of US Airlines")

st.markdown("This application is a streamlit dashboard to analyze the sentiments of tweets ❤️")

st.sidebar.markdown("This application is a streamlit dashboard to analyze the sentiments of tweets ❤️")

data_url = "C:/Users/adjeg/OneDrive/Documents/STREAMLIT_PROJECT/Tweets.csv"


def load_data():
    data = pd.read_csv(data_url)
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data()

st.sidebar.subheader("Show random tweets")
random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet' )[["text"]].sample(n=1) .iat[0,0])


st.sidebar.markdown("### Number of tweet by sentiment")
select = st.sidebar.selectbox('Visualization type', ["Histogram", "Pie plot"], key = "1")

sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({"Sentiment": sentiment_count.index, "Tweets":sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiments")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x="Sentiment", y="Tweets", color="Tweets", height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values="Tweets", names='Sentiment')
        st.plotly_chart(fig)


st.sidebar.subheader("When and where our users tweeting from ?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data["tweet_created"].dt.hour == hour] 
if not st.sidebar.checkbox("Close", True, key='close_checkbox'):
    st.markdown("### Tweet Locations based on the time of day") 
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False, key='show_raw_data'):
        st.write(modified_data)


        

st.sidebar.subheader("Breakdown airline tweets by sentiments")
choice = st.sidebar.multiselect('Pick airlines', ("US Airways", "United", "Américan", "Southwest", 'Delta', "Virgin América"), key= '0')
if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x= "airline", y = "airline_sentiment", histfunc='count', color='airline_sentiment',
                              
                              facet_col="airline_sentiment", labels={"airline_sentiment": "tweets"}, height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display word Cloud for what sentiments ?", ("positive",  "neutral", "negative",))

if not st.sidebar.checkbox("Close", True, key= '3'):
    st.header('word cloud for %s sentiment'% (word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ''.join(df['text'])
    processed_word = ''.join([word for word in words.split() if 'htpp' not in word and not word.startswith("@") and word != 'RT'])
    wordcloud = wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_word)
    # Crée une figure et un axe explicitement
    fig, ax = plt.subplots()

    # Crée ton nuage de mots et affiche-le sur l'axe
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Supprime les axes pour une meilleure visualisation

    # Passe la figure à st.pyplot
    st.pyplot(fig)
    

