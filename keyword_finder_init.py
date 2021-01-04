# Import libraries and modules
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import string
wn = nltk.WordNetLemmatizer() #Lemmatizer
stopword = nltk.corpus.stopwords.words('english') #Stopwords in English language


def matching_keywords(job_posting, resume):

    
    def clean_the_text(text):
        """
        Function to clean and tokenize the text.
        Input: 
            job_posting: text file
            resume: text_file
        Output: 
            text: cleaned and tekenized body of text        
        """
        
        #Replace non-word characters with empty space
        text = re.sub('[^A-Za-z0-9\s]', ' ', text)
        
        #Remove punctuation
        text = ''.join([word for word in text if word not in string.punctuation])
        
        #Bring text to lower case
        text = text.lower()
        
        #Tokenize the text
        tokens = re.split('\W+', text)
        
        #Remove stopwords
        text = [word for word in tokens if word not in stopword]
        
        #Lemmatize the words
        text = [wn.lemmatize(word) for word in text]
        
        #Return text
        return text
    
    #Read the files
    with open(job_posting, 'r') as f: 
        job_posting = f.read()

    with open(resume, 'r') as f:  
        resume = f.read()
        
        
    #Apply clean_the_text function to the text files   
    list_1 = clean_the_text(job_posting)
    list_2 = clean_the_text(resume)
    
    
    def common_words(l_1, l_2):
        """
        Input: 
            l_1: list of words
            l_2: list_of words
        Output: 
            matching_words: set of common words exist in l_1 and l_2        
        """
        matching_words = set.intersection(set(l_1), set(l_2))
        return matching_words
    
    #Apply common_words function to the lists
    common_keywords = common_words(list_1, list_2)
    
    #Print number of matching words
    print('The number of common words in your resume and the job posting is: {}'.format(len(common_keywords)),'\n')
    
    #Print the percentage of matching words
    print('{:.0%} of the words in your resume are in the job description'.format(len(common_keywords)/len(list_2)), '\n')    
    
    # Create an empty dictionary
    freq_table = {}
    
    # Create frequency table for the words that are not in the list_2 but in the list_1
    for word in list_1:
        if not word in list_2:
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1
    
    # Sort the dictionary by values in descending order
    freq_table = dict(sorted(freq_table.items(), key=lambda item: item[1], reverse=True))
    
    # Create a pandas dataframe from the dictionary
    pd.set_option('display.max_rows', 300)
    df = pd.DataFrame.from_dict(freq_table.items())
    
    # Rename columns
    df.columns = ['word','count']
    
    print('You can choose some words in the job posting from the table below to add your resume.')
    return df