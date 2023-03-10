import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime

tweets_df = pd.DataFrame()
st.write("# TWITTER DATA SCRAPING")
option = st.selectbox('How do you want to perform the data search? You can select either "Keyword" or "Hashtag" as the search option.',('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'Enter Text Here')
start = st.date_input("Select the Start Date", datetime.date(2022, 12, 27),key='d1')
end = st.date_input("Select the End Date", datetime.date(2023, 3, 10),key='d2')
tweet_c = st.slider('What is the quantity of tweets you desire to gather?', 0, 2000, 100)
tweets_list = []

# Scraping using the TwitterSearchScraper
if word:
    if option=='Keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>=tweet_c:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break            
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
else:
    st.warning(option,' cannot be empty')

# Creating Sidebar 
with st.sidebar:   
    st.info('DETAILS ENTERED')
    if option=='Keyword':
        st.info('Keyword is '+word)
    else:
        st.info('Hashtag is '+word)
    st.info('Starting Date is '+str(start))
    st.info('End Date is '+str(end))
    st.info("Number of Tweets "+str(tweet_c))
    st.info("Total Tweets Scraped "+str(len(tweets_df)))
    x=st.button('Show Tweets',key=1)

# DOWNLOAD In CSV Format
@st.cache # Cache is required for conversion to prevent computation on every rerun
def convert_df(df):    
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    col1, col2, col3 = st.columns(3)
    with col1: # SHOW
        y=st.button('Show Tweets',key=2)
    with col2:
        csv = convert_df(tweets_df) # CSV
        c=st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv',)        
    with col3:    # JSON
        json_string = tweets_df.to_json(orient ='records')
        j=st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string,)



if c:
    st.success("The Scraped data is Downloaded as .CSV file")  
if j:
    st.success("The Scraped data is Downloaded as .JSON file")     
if x: # DISPLAY
    st.success("The Scraped data is:")
    st.write(tweets_df)
if y: # DISPLAY
    st.balloons()
    st.success("Tweets Scraped Successfully:")
    st.write(tweets_df)
