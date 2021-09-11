"""
WikiTrivia - The Free and Radnom trivia games

Backend for generating questions

"""
#Prerequisites 
import wikipedia
import random
import re
from wikipedia.wikipedia import WikipediaPage
import nltk

#Download natural language packages
path = './nltk_modules'
nltk.data.path.append(path)
nltk.download('punkt', download_dir=path)
nltk.download('wordnet', download_dir=path)
nltk.download('averaged_perceptron_tagger', download_dir=path)
nltk.download('maxent_ne_chunker', download_dir=path)
nltk.download('words', download_dir=path)


BLANK_SPACE = "______"


def strip_brackets(text):
    return re.sub('\(.*\)', "", text)

def fetch_named_entities(text):
    names = []
    for sentence in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
            if hasattr(chunk, 'label'):
                #print(chunk.label(), ' '.join(c[0] for c in chunk))
                names.append((chunk.label(), chunk[0][0]))

    return names


def remove_subject(subject, text):
    text = strip_brackets(text)

    subject_list = fetch_named_entities(text)

    for item in subject_list:
        if item[0] == 'PERSON': #TODO: Generalise to all types
            if nltk.corpus.wordnet.synsets(item[1]):
                #print(item, "!!!!!!!")
                text = text.replace(item[1], BLANK_SPACE)
                    
    subject_split = subject.split(" ")
    for token in subject_split:
        text = text.replace(token, BLANK_SPACE)
        
    return text


def generate_question():
    """
    Generates a question

    returns:

    (answer (str), question (str)) : tuple of answer and question 
                                     stored as strings
    """
    Question = ""
    Answer = ""

    #Load the page with the list of pages
    page = wikipedia.page(title="Wikipedia:Multiyear ranking of most viewed pages")
    links = page.links

    #Try load a page and keep trying till you get one
    pageLoaded = False
    while pageLoaded == False:
        try:
            random_page = random.choice(links)
            question_page = wikipedia.page(title=random_page,auto_suggest=False)
            pageLoaded = True
        except:
            pageLoaded = False
    
    page_title = strip_brackets(question_page.title)
    print(page_title)


    summary = remove_subject(page_title, question_page.summary)
    summary = summary.split('. ')[0]



    print(summary)

    return (page_title,summary)

generate_question()

