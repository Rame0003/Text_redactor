#!/usr/bin/env python
# coding: utf-8

# In[2]:


import nltk
from nltk import word_tokenize
import spacy
import en_core_web_sm
from commonregex import CommonRegex
import glob
from nltk.corpus import wordnet
import sys
import os
import errno
import argparse
nltk.download('wordnet')

def openfiles(filename):
    with open(filename,'r') as file:
        data=file.read()
    
    return data

def redact_text(data, lst):
    if(len(lst)!=0):
        for n in lst:
            data=data.replace(n, "█"*len(n))
    return data

def find_names(data):
    names=[]
    nlp=en_core_web_sm.load()
    nltext=nlp(data)
    for word in nltext.ents:
        if word.label_=="PERSON":
                names.append(word.text)
    size=len(names)
    stats=("The number of unique names replaced in the given file is %d \n" %size)
    return names,stats

def find_locs(data):
    locs=[]
    nlp=en_core_web_sm.load()
    nltext=nlp(data)
    for word in nltext.ents:
        if word.label_=="GPE" or word.label_=="LOC":
                locs.append(word.text)
    size=len(locs)
    stats=("The number of unique locations replaced in the given file is %d \n" %size)
   
    return locs, stats


def find_dates(data):
    data1=CommonRegex(data)
    date5=[]
    if data1.dates!=0:
        for n in data1.dates:
               date5.append(n) 
    for n in date5:
            data=data.replace(n, "█"*len(n))
    size=len(date5)
   
    stats=("The number of unique dates replaced in the given file is %d \n" %size)
   
    return date5, stats


def find_address(data):
    addresses=[]
    data1=CommonRegex(data)
    if data1.street_addresses!=0:
        for n in data1.street_addresses:
            addresses.append(n)
    size=len(addresses)
   
    stats=("The number of unique addresses replaced in the given file is %d \n" %size)
   
    return addresses, stats



def find_numbers(data):
    numbers=[]
    data1=CommonRegex(data)
    if data1.phones!=0:
        for n in data1.phones:
               numbers.append(n)
    size=len(numbers)
   
    stats=("The number of unique phone numbers replaced in the given file is %d \n" %size)
   
    return numbers, stats

def concepts(data, word):
    synonyms=[]
    
    for n in wordnet.synsets(word):
        for l in n.lemmas():
            synonyms.append(l.name())
    synonyms.append(word)
    return synonyms

def conc_red(data, syns, word):
    j=0
    tokens=nltk.word_tokenize(data)
    for i in range(0,len(tokens)):
        for k in range(0,len(syns)):
            if (tokens[i].lower()==syns[k].lower()):
                tokens[i]=("█"*len(tokens[i]))
                j+=1
    data1=' '.join(map(str, tokens))
    stats=("The number of words related to %s replaced in the given file is %d \n" %(word, j))
    return data1, stats

def concepts_gen(data):
    gen=['he','she','him','her','his','hers','male','female','man','woman','men','women','He','She','Him','Her','His','Hers','Male','Female','Man','Woman','Men','Women','HE','SHE','HIM','HER','HIS','HERS','MALE','FEMALE','MAN','WOMAN','MEN','WOMEN', 'Mr.', 'Mrs.', 'Ms.']
    tokens=nltk.word_tokenize(data)
    k=0
    for i in range(0,len(tokens)):
        for j in range(0,len(gen)):
            if tokens[i]==gen[j]:
                tokens[i]=("█"*len(tokens[i]))
                k+=1
    data=' '.join(map(str, tokens))

    stats=("The number of gender based pronouns replaced in the given file is %d \n" %k)
    return data,stats

def stats_display(names, locs, date5, address, conceptstxt, nums, gens, i, opt, name):
    
    stats=("This is the stats for the document for the file named %s.redacted.txt\n"%(name))
    stats+=names
    stats+=locs
    stats+=date5
    stats+=address
    stats+=conceptstxt
    stats+=nums
    stats+=gens
    if (opt=="stdout"):
        print(stats)
    elif(opt=="store"):
        textfile = ('./stats/stats%d.txt'%i)  

        if not os.path.exists(os.path.dirname(textfile)):
            try:
                os.makedirs(os.path.dirname(textfile))
            except OSError as exc: 
                if exc.errno != errno.EEXIST:
                    raise

        with open(textfile, "w") as f:
            f.write(stats)


def file_output(data, k, file):
    text=data
    textfile = ('./%s %s.redacted.txt' %(file, k))
    with open(textfile, "w+") as f:
        f.write(data)
        f.close()
    
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("--input", required=True, action="store", type=glob.glob, nargs = '+')
    parser.add_argument("--names", action="store_true")
    parser.add_argument("--dates", action="store_true")
    parser.add_argument("--addresses", action="store_true")
    parser.add_argument("--gender", action="store_true")
    parser.add_argument("--numbers", action="store_true")
    parser.add_argument("--locations", action="store_true")
    parser.add_argument("--concepts", type=str)
    parser.add_argument("--stats",choices=( "stdout", "store"))
    parser.add_argument("--output", action="store")
    args=parser.parse_args()
    
    files=[]
    
    for i in args.input:
        files.extend(i) 
    print(files)

    for i in range(0,len(files)):
        filename=(files[i])
        data=openfiles(filename)

        if args.names==True:
            (names, namestxt)=find_names(data)
            data=redact_text(data, names)
        else:
            namestxt=("No unique names redacted\n")
        if args.dates==True:
            (dates, datetxt)=find_dates(data)
            data=redact_text(data, dates)
        else:
            datetxt=("No unique dates redacted\n")
        if args.addresses==True:
            (address, addtxt)=find_address(data)
            data=redact_text(data, address)
        else:
            addtxt=("No unique addresses redacted\n")
        if args.gender==True:
            (data, protxt)=concepts_gen(data)
        else:
            protxt=("No unique pronouns redacted\n")
        if args.numbers==True:
            (nums, numtxt)=find_numbers(data)
            (data)=redact_text(data, nums)
        else:
            numtxt=("No unique phone numbers redacted\n")
        if args.locations==True:
            (loc, loctxt)=find_locs(data)
            (data)=redact_text(data, loc)
        else:
            loctxt=("No unique locations redacted\n")
        if args.concepts:
            word=args.concepts
            syn=concepts(data, word)
            (data, contxt)=conc_red(data, syn, word)
        else:
            contxt=("No unique concept words redacted\n")
        if args.stats:
            opt=args.stats
            stats_display(namestxt, loctxt, datetxt, addtxt, contxt, numtxt, protxt, i, opt, filename)
        if args.output:
            path=args.output
            name=filename
            file_output(data, name, path)
        i+=1


