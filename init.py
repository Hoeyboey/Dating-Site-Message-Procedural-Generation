from source_messages import source_messages
   
def init():
    word_dictionary = {}
    
    for x in source_messages:
        words_in_current_message = x.split(" ")
        for y in words_in_current_message:
            if y not in word_dictionary:
                word_dictionary[y] = 1
            else:
                word_dictionary[y] = word_dictionary[y] + 1
    return word_dictionary     
