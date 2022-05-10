from typing import List, Tuple
import re
import nltk as nltk
from word2number import w2n
from nltk.stem.wordnet import WordNetLemmatizer
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()


def default_preprocessing(schema: str, question: str, sql:str="") -> Tuple[str]:
    # For dataset builder

    if sql == "":
        return schema, question

    else:
        return schema, question, sql

# Number treatment preprocessing

def replace_text_number(text):

    tagged_number_words = 'billion/CD million/CD ten/CD thousand/CD nine/CD hundred/CD ninety/CD eight/CD seven/CD six/CD five/CD four/CD three/CD two/CD one/CD eighty/CD seventy/CD sixty/CD fifty/CD forty/CD thirty/CD twenty/CD nineteen/CD eighteen/CD seventeen/CD sixteen/CD fifteen/CD fourteen/CD thirteen/CD twelve/CD eleven/CD zero/CD'
    tagged_number_words_tuples = [nltk.tag.str2tuple(t) for t in tagged_number_words.split()]
    my_tagger = nltk.UnigramTagger([ tagged_number_words_tuples ], backoff=nltk.DefaultTagger('IGNORE'))

    my_grammar = 'NumberWord: {<CD>+}'
    parser = nltk.RegexpParser(my_grammar)
    parsed = parser.parse(my_tagger.tag(nltk.word_tokenize(text.lower())))
    #print(parsed)

    for tag in [tree.leaves() for tree in parsed.subtrees() if tree.label() == 'NumberWord']:
        ut = nltk.untag(tag)
        num = w2n.word_to_num(' '.join(ut))

        r = re.compile(re.escape(' '.join(ut)), re.IGNORECASE)
        text = r.sub(str(num), text)

    #print('-- AFTER --')
    return text

def number_treatment_process(schema = "", question = "", sql = ""):
    question_process = replace_text_number(question)
    return schema, question_process, sql


# Stemming Preprocessing
def stemming_process(schema = "", question = "", sql = ""):
    question_split = question.split()
    o = []
    for word in question_split:
        try:
            o += [str(WordNetLemmatizer().lemmatize(word,'v'))]
        except ValueError:
            o += [word] 

    question_process = ' '.join(o)
    return schema, question_process, sql


# Surrounding Preprocessing
def surrounding_entity_process(schema = "",question = "", sql = ""):
    doc = nlp(question)
    entities = doc.ents
    question_process = question
    for word in entities:
        question_process = question_process.replace(str(word),"'"+str(word)+"'")

    return schema, question_process, sql
