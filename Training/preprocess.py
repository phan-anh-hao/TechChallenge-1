
from typing import List, Tuple
import re
from re import sub
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from functools import reduce

sample = {
    "schema": "STATE/TERRITORY_FIELD : text_TYPE, TEXT/BACKGROUND_COLOUR_FIELD : text_TYPE, FORMAT_FIELD : text_TYPE, CURRENT_SLOGAN_FIELD : text_TYPE, CURRENT_SERIES_FIELD : text_TYPE, NOTES_FIELD : text_TYPE",
    "question": "Tell me what the notes are for South Australia fullName ",
    "sql": "SELECT  NOTES_FIELD FROM table WHERE CURRENT_SLOGAN_FIELD = 'SOUTH AUSTRALIA'"
}

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


def default_preprocessing(schema: str, question: str, sql:str="") -> Tuple[str]:
    # Remove redundant space
    schema = remove_redundant_space(schema)
    question = remove_redundant_space(question)
    sql = remove_redundant_space(sql)

    # Stemmning & Lemmatization
    schema, question, sql = lemmatize(schema, question, sql)

    # Number treatment


    #Input consistency
    schema, question, sql = consistence_schema(schema, question, sql)

    # Surround entity

    # Upper case column name in question
    schema, question, sql = upper_column_name(schema, question, sql)

   

    if sql == "":
        return schema, question

    else:
        return schema, question, sql

