# Sentiment_Analysis_with_Artificial_Neural_Networks

Our project aims to collect various topics and comments on these topics from news sites. We aim to perform sentiment analysis by using artificial intelligence technologies using this collected data. That is, by processing headline and comment data from news sites, we plan to identify emotional content in texts and determine people's emotional reactions to events. Thus, we want to understand the impact of news on people and make various inferences based on these analyses. This project will use artificial intelligence and sentiment analysis methods to deeply understand and interpret the meaning of news.

# Operation of the Software Project

First, we pull the news by categories through an API and store this data in a CSV file. Next, we translate the texts in this CSV file into English; because the ready-made models used are usually trained in English. Then, we perform tokenization with the bert-base-uncased model to separate the sentences to the word level. We evaluate these words for sentiment analysis using the ready-trained textblob model and visualize the results graphically with the pyplot library.
 
