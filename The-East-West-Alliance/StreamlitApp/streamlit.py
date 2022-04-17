import streamlit as st
import joblib,os

import pandas as pd
import numpy as np

#NLP ackages
#NER: https://www.analyticsvidhya.com/blog/2021/06/part-10-step-by-step-guide-to-master-nlp-named-entity-recognition/
#SpaCy: https://spacy.io/
import spacy
nlp = spacy.load('en_core_web_sm') #en for english model for spacy

#
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
# Using matplotlib.use() after importing pyplot will have no effect.
# agg is the default backend which renders graphs as PNGs. There are many such backends.

#wordcloud
from wordcloud import WordCloud
from PIL import Image

##libraries for preprocessing user input
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import nltk, string, re
stop=set(stopwords.words('english'))
lemmatizer = nltk.stem.WordNetLemmatizer()
wordTokenizer = nltk.tokenize.WhitespaceTokenizer()

#get our saved models we created of the vectorizer and ML model:

 #NOT NEEDING THIS ANYMORE AFTER WE ADDED the transfomations to the models in the pkl!!  #VECTORIZER!!
#rizer = open("./models_test/final_news_cv_vectorizer.pkl", "rb") #open and read our vectorrizer model
#my moel vectorizer: ---------------------------------------------------
#rizer = open("cvec.pkl", "rb")
#news_cv = joblib.load(rizer)

  #ML MODEL to load!!
def load_prediction_models(model_file):
    loaded_models = joblib.load(open(os.path.join(model_file), "rb")) #get our model file and read it (read byte)
    return loaded_models

#lets make our classified outputs of numbers into the label we want:
def get_keys(val, my_dict):
    for key, value in my_dict.items():
    #looping through the dictionary (prediction labels). we will return key to be outputed IF its value is chosen
        if val == value:
            return key

#PREPROCESSING USERS INPUT!:
def Preprocessing(text):
    text = str(text).lower()
    text = re.sub('https?://\S+|www\.\S+', ' ', text)
    text = re.sub(' +',' ',text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', str(text))
    text = BeautifulSoup(text,  features="lxml").text
    text = re.sub('https?://\S+|www\.\S+', ' ', text)
    text = re.sub('<.*?>+', ' ', text)
    text = re.sub('\n', ' ', text)
    text = ' '.join([lemmatizer.lemmatize(w) for w in wordTokenizer.tokenize(text) if (w not in stop)])
    # text = ' '.join([token.lemma_ for token in list(nlp(text)) if (token.is_stop == False)])
    return text


def main():
    """News Classifier App with Streamlit. Is Your News Real or Fake? """

    ##st.title("News Classifier ML App: Is Your News True or Fake?") #centered the title in the next line
    st.markdown("<h1 style='text-align: center; color: white;'>News Classifier ML App: Is Your News True or Fake?</h1>", unsafe_allow_html=True)


    title_image = Image.open('fake_fact.jpeg')
    # jpeg Source: https://news.stanford.edu/2021/10/25/foil-fake-news-focus-infectiousness/
    # col1, col2, col3 = st.columns([0.2,5,0.2])
    # st.image(title_image, caption='Fake or Fact?', width = 250, use_column_width = 250)

    #centered my image!!
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')
    with col2:
        st.image(title_image, caption='Fake or Fact?', width = 250, use_column_width = 250)
    with col3:
        st.write(' ')


    st.subheader("NLP and ML App with Streamlit")
    activities = ["Prediction", "NLP"]

    choice = st.sidebar.selectbox("Choose Activity", activities)

    if choice == 'Prediction':
        st.info('Prediction with ML')

        #a place to receive our text and another to do our preprocessing

        #want to copy paste your the news article title and its body in here!
        #BASICALLY USER INPUT HERE!!
        news_text = st.text_area("Enter Text", "Type Here")
        #THEN APPLY MY PREPROCESSING:
        news_text = Preprocessing(news_text)

        #get our model.. we will make a list of models a user can choose from to classify their news ************************
        all_ml_models = ["LR", "NB", 'RFOREST','KNN', 'DT', 'SVC'] #['NB']
        #LR: Logisitc Regression ..... NB: Naive Baise...... RFOREST: random Forest... KNN: K-neighbor....DT:Decision Tree
        model_choice = st.selectbox("Choose ML Model", all_ml_models)

        #our predictiotion labels to classify FAKE(1) OR REAL(0)  .. ned to chance this laterr ***************
        prediction_labels = {"Fake":1, "Real":0}
        #prediction_labels = {'business': 0,'tech':1, 'sport':2, 'health':3, 'politics':4, 'entertainment':5}

        #WE NEED TO VECTORIZE OUR TEXT!
        if st.button("Classify"):  #IF IT IS clasify do somethingg.....
            st.text("Original test:\n{}".format(news_text))

            #we need to vectorize our inputted text to put into our ML model!

            #vect_text = news_cv.transform([news_text]).toarray()
            #since some of the models have vectorizaiton going on in them. ill this in the models dont have it going on

            #load the model based on the choice
            #NAIVE BAISE CHOICE
            if model_choice == "NB":
                #the models i got from guthub
                #predictor = load_prediction_models("./models_test/newsclassifier_Logit_model.pkl")
                #my models i made  --------------------------------------------
                #vect_text = news_cv.transform([news_text]).toarray() #not needing to transform on it anymore after adding transformation to the pkl
                #predictor = load_prediction_models("base.pkl")
                predictor = load_prediction_models("./final_models/retrain_gs_ct_mnb_np.pkl")
                prediction = predictor.predict([news_text])
                #st.write(prediction) #outputs our prediction number\
            #LOGISITC REGRESSION CHOICE
            elif model_choice == "LR":
                predictor = load_prediction_models("./final_models/gs_cvec_idf_logregV3.pkl")
                prediction = predictor.predict([news_text])

            #Decision Tree:
            elif model_choice == "DT":
                predictor = load_prediction_models("./final_models/retrain_gs_ct_dt_np.pkl")
                prediction = predictor.predict([news_text])

            #KNN
            elif model_choice == "KNN":
                predictor = load_prediction_models("./final_models/retrain_gs_ct_knn_np.pkl")
                prediction = predictor.predict([news_text])

            #RandomForestClassifier
            elif model_choice == "RFOREST":
                predictor = load_prediction_models("./final_models/retrain_gs_random_forest.pkl")
                prediction = predictor.predict([news_text])

            #Support Vector Machine Classifier (SVC) --- Model V2
            elif model_choice == "SVC":
                predictor = load_prediction_models("./final_models/gridsearchedSVCv2.pickle")
                prediction = predictor.predict([news_text])


            final_result = get_keys(prediction, prediction_labels  )
            st.success("News Categorized: {}".format(final_result))

#-----------------------------------------------------------------------
#If we want to look into the word EDA of our text!
    if choice == 'NLP': #
        st.info("Natural Language Processing")
        news_text = st.text_area("Enter Text", "Type Here")
        #the many tasks we have from here
        nlp_task = ["Tokenization", "Lemmatization"] #   "NER",, "Pattern of Speech Tags"]
        task_choice = st.selectbox("Choose NLP Task", nlp_task)
        if st.button("Analyze"):
            st.info("Original Text: \n{}".format(news_text))

            docx = nlp(news_text)
            if task_choice == "Tokenization":
                result = [token.text for token in docx]
            # elif task_choice == "NER":
            #     result = [(entity.text, entity.label) for entity in docx.ents  ]
            elif task_choice == "Lemmatization":
                result = ["'Token':{},'Lemmatized:{}'".format(token.text, token.lemma_) for token in docx]
            # elif task_choice == "Pattern of Speech Tags":
            #     result = ["'Token':{},'POS':{},'Dependency':{}".format(word.text, word.tag_, word.dep_) for word in docx]

            #output our result after going through our choice
            st.json(result)
        #lets make our output look nicer:
        if st.button("Tabulize"):
            docx = nlp(news_text)
            c_tokens = [token.text for token in docx]
            c_lemma =  [token.lemma_ for token in docx]

            #lets put these into a table pandas DataFrame
            new_df = pd.DataFrame(zip(c_tokens, c_lemma), columns=['Tokens', 'Lemma'])
            st.dataframe(new_df)

        #lets add a wordcloud!
        if st.checkbox("Wordcloud"):
            wordcloud = WordCloud().generate(news_text)
            plt.imshow(wordcloud, interpolation= 'bilinear')
            plt.axis("off")

            #
            st.set_option('deprecation.showPyplotGlobalUse', False) #to not show the warning.. need to futrue proof laterr
                                #need to not do st.pyplot() .. it needs an argument in it
            #plt.show()
            st.pyplot()



if __name__ == '__main__':
    main()
