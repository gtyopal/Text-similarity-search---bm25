# coding: utf-8
import pandas as pd
import numpy as np
import re
import string
import nltk
from sklearn.utils import shuffle
from bs4 import BeautifulSoup
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    r = re.compile(r'<[^>]+>', re.S)
    text = r.sub('', text)
    text = re.sub(r'&(nbsp;)', ' ', text)
    text = re.sub(r'<[^>]+', '', text)
    text = re.sub('\&lt[;]', ' ', text)
    text = re.sub('\&gt[;]', ' ', text)
    return text

def remove_punctuation(text):
    text = re.sub(r'[^\x00-\x7f]',r' ',text)
    text = re.sub("["+string.punctuation+"]", " ", text)
    new_words = []
    words = word_tokenize(text)
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return " ".join(new_words)

def remove_non_ascii(text):
    """ remove non-asccii """
    words = word_tokenize(text)
    new_words = []
    for word in words:
        if re.findall(r'[^a-z0-9\,\.\?\:\;\"\'\[\]\{\}\=\+\-\_\)\(\^\&\$\%\#\@\!\`\~ ]', word):
            continue
        new_words.append(word)
    return " ".join(new_words)

def remove_others(text):
    """ remove url """
    text = re.sub(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', ' spamurl ' , text)
    """ remove email """
    text = re.sub(r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)', ' email ', text)
    """ remove phone numbers """
    text = re.sub(r'[\@\+\*].?[014789][0-9\+\-\.\~\(\) ]+.{6,}', ' phone ', text)
    """ remove digits """
    text = re.sub(r'[0-9\.\%]+', ' digit ', text)
    return text

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def stem_words(words):
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def denoise_text(text):
    text = text.lower()
    text = strip_html(text)
    text = remove_punctuation(text)
#     text = remove_others(text)
#     text = remove_non_ascii(text)
    words = word_tokenize(text)
    words = to_lowercase(words)
    words = remove_stopwords(words)
#     words = stem_words(words)
    # words = lemmatize_verbs(words)
    text = " ".join(words)
    if not text.strip():
        text = " "
    return text
