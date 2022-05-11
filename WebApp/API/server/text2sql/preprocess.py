import secrets
from typing import List, Tuple
import re
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from re import sub
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from functools import reduce
import nltk as nltk
from word2number import w2n
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()


def remove_redundant_space(string):
    return " ".join(string.split())


def snake_case(string):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    string.replace('-', ' '))).split()).lower()


def lemmatize(word):
    return lemmatizer.lemmatize(word)


def is_column_name(schema, word):
    word = word.lower()
    columns = [
        property.split(' : ')[0].lower()
        for property in schema.split(', ')
    ]

    column_keywords = []
    # column must in snake_case
    for column in columns:
        column_keywords = [*column_keywords, *column.split('_')]

    lemmatized_column_keywords = [
        lemmatizer.lemmatize(keyword)
        for keyword in column_keywords
    ]

    return True if word in lemmatized_column_keywords else False


def consistence_schema(schema, question, sql):
    properties = schema.split(', ')

    properties = [
        property.split(' : ')
        for property in properties
    ]

    properties = [
        [property[0], 'TEXT' if re.search("^text", property[1]) else 'NUMBER']
        for property in properties
    ]

    properties = [
        ' : '.join([sub("[^0-9a-zA-Z]+", '_', property[0]).upper(), snake_case(property[1]).upper()])
        for property in properties
    ]

    schema = ', '.join(properties)
    question = question.lower()
    sql = sql.upper()

    return schema, question, sql


def lemmatize(schema, question, sql):
    return schema, ' '.join([lemmatizer.lemmatize(word) for word in question.split(' ') ]), sql


def upper_column_name(schema, question, sql):
    question = ' '.join([
        word.upper() if is_column_name(schema, word) else word
        for word in question.split(' ')
    ])

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


def default_preprocessing(schema: str, question: str, sql:str="") -> Tuple[str]:
    # Convert schema list to string
    schema = ", ".join(schema)

    # Remove redundant space
    schema = remove_redundant_space(schema)
    question = remove_redundant_space(question)
    sql = remove_redundant_space(sql)

    # Stemmning & Lemmatization
    schema, question, sql = lemmatize(schema, question, sql)
    schema, question, sql = stemming_process(schema, question, sql)

    # Number treatment
    schema, question, sql = number_treatment_process(schema, question, sql)

    #Input consistency
    schema, question, sql = consistence_schema(schema, question, sql)

    # Surround entity
    schema, question, sql = surrounding_entity_process(schema, question, sql)

    # Upper case column name in question
    schema, question, sql = upper_column_name(schema, question, sql)

    if sql == "":
        return schema, question

    else:
        return schema, question, sql


