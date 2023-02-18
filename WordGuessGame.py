# Portfolio 5: Word Guessing Game
# Anushka Karthikeyan
# AXK180188

import sys
import pathlib
from nltk import word_tokenize
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import randint


# PREPROCESSING FUNCTION
def preprocess(text_in):
    """
      Processes raw text into tokens; Also checks lexical diversity,
        make list of unique lemmas and
        performs pos tagging.
      Args:
        text_in: raw text from anatomy textbook
      Returns:
          List of processed tokens and nouns
    """
    # tokenize text
    tokens = " ".join(text_in)
    tokens = word_tokenize(tokens)

    # lowercase the raw text
    tokens = [t.lower() for t in tokens]

    # tokens that are only alpha and not stopwords
    tokens = [t for t in tokens if t.isalpha() and
              t not in stopwords.words('english')]

    # tokens with length > 5
    tokens1 = []
    for t in tokens:
        if len(t) > 5:
            tokens1.append(t)
    tokens = tokens1
    set1 = set(tokens1)

    # lexical diversity
    print("\nLexical diversity: %.2f" % (len(set1) / len(tokens)))

    # lemmatize tokens
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]

    # use set to make list of unique lemmas
    lemmas_unique = list(set(lemmas))
    ## print("\nThe number of unique lemmas from the anatomy textbook: ", len(lemmas_unique))

    # do pos tagging on the unique lemmas and print the first 20 tagged
    s = " ".join(lemmas_unique)
    blob = TextBlob(s)
    tagged = [x for x in blob.tags]
    print("\nThe first tagged unique lemmas from the anatomy textbook are: ", sorted(tagged)[:20])

    # create a list of only those lemmas that are nouns
    nouns = blob.noun_phrases
    ## print("Nouns: ", nouns)

    # print the number of tokens and the number of nouns
    print("\nThe number of tokens from the anatomy textbook: ", len(tokens))
    print("The number of nouns from the anatomy textbook: ", len(nouns))
    for i in nouns:
        tokens.append(i)
    print("The number of TOTAL tokens and nouns from the anatomy textbook: ", len(tokens))
    # return tokens (not unique tokens) and nouns from the function
    return tokens


# GUESSING GAME FUNCTION
def guess_game(common):
    """
    Allows user to play a guessing game from list of common tokens from anatomy textbook.
    The user will start with 5 points.
    The game will end when the user score is negative, or they guess ‘!’ as a letter
    Args:
      common: list of top 50 words from anatomy textbook
      """
    print("Let's play a word guessing game!")

    # give the user 5 points to start with;
    score = 5

    # randomly choose a word from top 50 list
    guess_word = common[randint(1, 50)]
    guess_word = list(guess_word[0])
    ## print("The word is:", guess_word)

    # output to console an “underscore space” for each letter in the word
    display_word = []
    for i, item in enumerate(guess_word):
        display_word.append('_')

    # the game ends when their total score is negative,
    while score >= 0:
        correct_guess = False
        print(' '.join(display_word))

        # ask the user for a letter
        x = input("Guess a letter: ")

        for i, item in enumerate(guess_word):
            # the game ends they guess ‘!’ as a letter
            if x == '!':
                score = -1
                print("Thanks for playing!  The word was ", ''.join(guess_word))
                break
            # if the letter is in the word, fill in all matching letter _
            elif item == x:
                correct_guess = True
                display_word[i] = x

        # if the letter is in the word, print ‘Right!’,  with the letter and add 1 point to their score
        if correct_guess:
            score += 1
            print("Right! The Score is ", score, "\n")
        # if the letter is not in the word, subtract 1 from their score, print ‘Sorry, guess again’
        elif x != '!':
            score -= 1
            print("Sorry, guess again! The Score is ", score, "\n")

        # user guessed the word correctly
        if display_word == guess_word:
            print("You solved it!\nCurrent score: ", score, "\n\nGuess another word")
            # randomly choose another word from top 50 list
            guess_word = common[randint(1, 50)]
            guess_word = list(guess_word[0])
            display_word = []
            for i, item in enumerate(guess_word):
                display_word.append('_')

        if score < 0 and x != '!':
            print("You lost! The word was ", ''.join(guess_word))


# main function to read in file, send to text for preprocessing and starts guessing game
if __name__ == '__main__':
    # sysarg for 'anat19.txt'
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    # read in file
    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read().splitlines()

    # print(text_in)
    text = preprocess(text_in)

    # sort dict by count
    counts = {t: text.count(t) for t in text}
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # print 50 most common words
    common = sorted_counts[:50]
    print("\nThe 50 most common words from the anatomy textbook are: ", common, "\n")

    # starts guessing game function
    guess_game(common)
