# Project 1: Text Redactor 
----
### By Abilash Ramesh
--------
### Contents:

* Introduction
* How to run?
* Available flags
* How do they work?
* Stats: What do they do?
* Output: What do we get?

## Introduction:

This project aims to provide the user with an automated redactor where the user can provide input about what type of file formats to be taken in, what type of words need to be redacted, how many words have been redacted and finally specify where the output files need to be stored. This project will assist people to redact specific text that the user sees as sensitive information. 

## How to run?:

The code can be run in the following format:
```python
pipenv run python redact.py --input *.txt --names --dates --locations --gender --numbers --concepts 'word' 
--output trial/ --stats "store"
```
The table below lists the types of input that is required to be given to the flags:
|Flag|Input|
|--|:----:|
|--input| file format (\*.txt,\*.md)|
|--concepts|"concept word"|
|--stats|"stdout" or "store"|
|--output|"foldername"+/|

The other flags are provided as input to redact specific texts which have a specific labels. The flags are clearly explained in the section below.

## Available flags:

The available flags for this program are as follows
* --names
* --gender
* --dates
* --numbers
* --addresses
* --location
* --concepts

All of the flags are made to work in the same way. Once the flag is added into the run commmand. the program recognizes it and proceeds to collect the words that are marked with a certain label. The words are collected into a list and they are replaced with the unicode charecter '█'. We will delve into the working of the functions in the next heading.

## Internal working of code:

For labelling the input text, we use both the NLTK and SpaCy packages. I used SpaCy due to its capabilities to detect organizations and locations better. I found out that the use of Stanford NLP package provided us with better results but the issue was that we needed to provide it with a few extra credentials such as jar file location for the package and other such filepath inputs. I used NLTK in places where tokenization of words individually was required. 

The input flag gives the input to the glob module which extracts a list of all files present in the directory that the program is stored in. Once the text file names are taken in, the files are appended to a list for reference. Each file is passed and the data is extracted from it. The data is stored and passed on for further processing. 

The redaction process depends on the flags provided to it. The input flag is a compulsary one hence the program requires it to be given while running the above mentioned command. The rest of the flags are given by the user. Each flag activates a function which redacts a particular type of text. The functions performed by the available flags are given below:

1. --names: This flag allows the user to redact names. I used the SpaCy package to perform the labelling operation. I found the SpaCy package to be useful when first names, last names are involved in the text. 

2. --gender: For this flag, I specified a list of pronouns that are gender-specific. The text is tokenized using NLTK tokenizer and each text is compared with the pronouns in the list. If a pronoun is found, it is replaced with the '█' charecter. 

3. --dates: For this flag, I used a package called CommonRegex which allowed me to extract any dates that had the format "mm/dd/yyyy", "Mon dd yyyy" or "Month dd yyyy". Using the replace function, I collected the dates in the text and replaced them in the main text. 

4. --numbers: This flag also uses the CommonRegex package. Numbers in the format "xxxxxxxxxx" or "(xxx)-xxx-xxxx" or "+x(xxx)-xxx-xxxx" are detected. The numbers are detected, appended to a list and redacted using the replace option. 

5. --addresses: Addresses are obtained from the CommonRegex package. The address format needs to be "xxxx street name". 
>I would suggest using the location flag along with addresses to improve the redaction process. 

6. --location: This flag redacts the location names. I used the SpaCy package for this process. The function finds out the words with the label GPE or LOC and redacts them using the replace function. 

7. --concepts: This is a special flag which uses the Wordnet module. The flag is given a word which acts as a clue to what kind of words we need to be looking into. The word is sent to the function and a list of synonyms or words related to the given word are returned. These words are then redacted by comparing with the tokenized words from the given text file. The  words that are found to match with the list's contents are replaced with the '█' charecter. 

## Stats: What do they do?
The stats flag gives us an overview of the number of each flag that has been redacted in the document. The stats can either display on the screen or write the stats for each file labelled "stats_#.txt" in a separate stats folder. The flag will see if there is a stats folder otherwise it will create the folder for us. The files are redacted with the corrosponding file name on top of the text. 

## Output: What do we get?
The output flag takes in the location where the user wants their files to be stored. A proper location should be given to the flag in the format "foldername/". The redacted file is written in the format that it is taken from the parent directory and the filename given to it is its position in the directory. For example, a file that is the first in the directory is redacted and written as "file_#.redacted.txt". 
