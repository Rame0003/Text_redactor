#!/usr/bin/env python
# coding: utf-8

# In[24]:


import collections
import imp
import pytest
import nltk
from nltk import word_tokenize
import spacy
import en_core_web_sm
import redact
import importlib


def nametest():
    data="My name is Abilash. I work with Gintoki."
    (names, stats)=redact.find_names(data)
    redacted=redact.redact_text(data, names)
    assert redacted=='My name is ███████. I work with ███████.'
    assert redacted is not None
def address_test():
    data="1015 East Brooks street, Norman"
    (add, stats)=redact.find_address(data)
    (loc, stats)=redact.find_locs(data)
    data=redact.redact_text(data, add)
    data=redact.redact_text(data, loc)
    assert data=='████████████████████████ ██████, ████████'
    assert data is not None
def date_test():
    data="I blow my candles on 09/16/1996"
    (dates, stats)=redact.find_dates(data)
    data=redact.redact_text()
    assert data=='I blow my candles on ██████████'
    assert data is not None
def gender_test():
    data="He is a funny guy."
    (data, stats)=redact.concepts_gen(data)
    assert data=='██ is a funny guy .'
    assert data is not None
def mnumber_test():
    data="My number is 4055619046."
    (num, stats)=redact.find_numbers(data)
    data=redact.redact_text(data, num)
    assert data=='My number is ██████████.'
    assert data is not None

def concept_test():
    data="The Japanese celebrate new year in a grand fashion"
    (syn)=redact.concepts(data, 'Japanese')
    (data, stats)=redact.conc_red(data, syn, 'children')
    assert data=='The ████████ celebrate new year in a grand fashion'
    assert data is not None

def location_test():
    data="I live in Shibuya."
    (locs, stats)=redact.find_locs(data)
    data=redact.redact_text(data, locs)
    assert data=='I live in ███████.'
    assert data is not None

