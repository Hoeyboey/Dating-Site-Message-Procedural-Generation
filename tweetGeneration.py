import random
import difflib
from init import init
from PyDictionary import PyDictionary

#This function will select a base tweet that will be mashed up with another on the first runthrough
def select_base_tweet(source_messages):
    index_of_base_tweet = random.randint(0, len(source_messages)-1)
    base_tweet = source_messages[index_of_base_tweet]
    return base_tweet
    
#In this function, the base tweet is split, and a word is chosen based on its frequency in source_messages.py to be the bridging point between two messages, returning the first half of the split tweet, the word that was used for the split, and an updated blacklist 
def splitting_tweet(tweet, freq_words_in_tweet, total_freq, words_in_tweet, blacklist):
    word_split_on = ""
    checking_if_successful = False
    while checking_if_successful == False:
        index_of_word_split_on = 0
        for x in words_in_tweet:
            index_of_word_split_on = index_of_word_split_on + 1
            if x != words_in_tweet[0] and x not in blacklist:
                current_probability = freq_words_in_tweet[x]/total_freq
                random_number = random.random()
                if random_number < current_probability:
                    tweet = words_in_tweet[0]
                    for index_of_words_putting_back_together_for_base_tweet in range(1, index_of_word_split_on-1):
                        tweet = tweet + " " + words_in_tweet[index_of_words_putting_back_together_for_base_tweet]
                    tweet = tweet + " "
                    word_split_on = x
                    blacklist.append(word_split_on)
                    checking_if_successful = True
                    break
    splitting_tweet_output = [tweet, word_split_on, blacklist]
    return splitting_tweet_output
    
#Here, we use difflib to get similar words to the splitting word, and find messages in source_messages.py that can be swapped in
def selecting_splitting_word_and_possible_second_messages(word_split_on, word_dictionary_for_markov_chain, source_messages):
    splitting_word_and_similar = difflib.get_close_matches(word_split_on, list(word_dictionary_for_markov_chain), 10, 0.4)
    possible_messages = {}
    possible_messages_list = []
    for x in source_messages:
        for y in splitting_word_and_similar:
            y = " " + y + " " 
            if y in x:
                possible_messages[x] = y
                possible_messages_list.append(x)
    output_for_this = [possible_messages, possible_messages_list]
    return output_for_this

#This is the main function, which makes up the bulk of what happens. It needs to be split up into seperate functions honestly.
def tweetGeneration(tweet, number_of_runthroughs, source_messages, blacklist):    
    for runthrough_number in range(0, number_of_runthroughs):
        word_dictionary_for_markov_chain = init()
        total_words_in_chain = len(word_dictionary_for_markov_chain)    
        words_in_tweet = tweet.split(" ")
        total_freq = 0
        freq_words_in_tweet = {}
        
        for x in words_in_tweet:
            if freq_words_in_tweet.get(x) == None:
                freq_words_in_tweet[x] = word_dictionary_for_markov_chain[x]
                total_freq = total_freq + word_dictionary_for_markov_chain[x]
                
        splitting_tweet_output = splitting_tweet(tweet, freq_words_in_tweet, total_freq, words_in_tweet, blacklist)    
        tweet, word_split_on, blacklist = splitting_tweet_output
        
        selecting_splitting_word_output = selecting_splitting_word_and_possible_second_messages(word_split_on, word_dictionary_for_markov_chain.keys(), source_messages)
        possible_messages, possible_messages_list = selecting_splitting_word_output
        second_message = random.choice(possible_messages_list)
        if second_message.count(" " + possible_messages[second_message] + " ") > 1:
            place_to_split_second_message = random.randint(1, second_message.count(" " + possible_messages[second_message] + " "))
            second_message = second_message.split(possible_messages[second_message], place_to_split_second_message)
            second_message = second_message[-1]
        else: 
            second_message = second_message.split(possible_messages[second_message])
            second_message = second_message[1]
        tweet = tweet + word_split_on + " " + second_message
        print("Printing output " + str(runthrough_number+1))
        print(tweet)
    return tweet

#This function will check the length of a tweet - if it's over 140 characters, it will remove random words until it is below 140 characters.
def check_length(tweet):
    while len(tweet) > 140:
        tweet_list_of_words = tweet.split(" ")
        word_to_remove = random.randint(0, len(tweet_list_of_words)-1)
        tweet_list_of_words.remove(tweet_list_of_words[word_to_remove])
        tweet = tweet_list_of_words[0]
        for x in range(1, len(tweet_list_of_words)):
            tweet = tweet + " " + tweet_list_of_words[x]
    return tweet

#Obvious what this does
def print_final_output(tweet):
    print("Printing final output:")
    print(tweet)

#This is the start of the noun swapping process
# def identify_nouns(tweet):
#     dictionary=PyDictionary()