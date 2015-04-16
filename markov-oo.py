import sys
import random



# Schematic:  
# 1.    Move functions into SimpleMarkovGenerator class (now they're methods!)
# 2.    Create a TweetMarkovGenerator subclass that has the same make_chains 
#       method as the parent class
# 3.    The TweetMarkovGenerator will have its own make_text method that inherits
#       the make_text method from the Parent class but also tweaks it so that
#       the Markov text generated ends at 140 characters.  
 

class SimpleMarkovGenerator(object):
    """Takes in text input, and generates a Markov string based on that 
    input using a Markov Chain algorithm."""

    def make_chains(self, file_name): 
        """Takes input text as string; returns dictionary of markov chains."""

        text_file = open(file_name)

        text_string = text_file.read().replace("\n", " ").lower().strip()
        text_no_punct = ""

        for char in text_string:
            if char.isalpha() or char == " ":
                text_no_punct += char

        word_list = text_no_punct.split()

        bigrams = dict() 

        for index, current_word in enumerate(word_list):
            second_word = word_list[index + 1]
            if index == len(word_list) - 2:
                break
            third_word = word_list[index + 2]

            bigrams.setdefault((current_word, second_word), [])
            bigrams[(current_word, second_word)].append(third_word)

        return bigrams

    def make_text(self, chains):
        """Takes dictionary of markov chains; returns random text."""
            
        rand_key = random.choice(chains.keys())
        rand_value_word = random.choice(chains[rand_key])
        key1, key2 = rand_key
        
        markov_string = key1 + " " + key2 + " " + rand_value_word
        
        while rand_key in chains:

            new_bigram = (key2, rand_value_word)

            if new_bigram in chains:
                rand_new_word = random.choice(chains[new_bigram])
                markov_string += " " + rand_new_word
                key2 = rand_value_word
                rand_value_word = rand_new_word 
                rand_key = new_bigram           

            else:
                markov_string += "."

                return markov_string




#  one way:  The TweetMarkovGenerator will have its own make_text method that inherits
#  the make_text method from the Parent class but also tweaks it so that
#  the Markov text generated ends at 140 characters.  
class TweetableMarkovGeneratorQuick(SimpleMarkovGenerator):
    """Takes in text input, and generates a tweetable (140 characters or less) 
    Markov string based on that input using a Markov Chain algorithm."""

    def make_text(self, chains): 
        """ This method generates a long-format string using the method defined in 
        the SimpleMarkovGenerator superclass, then returns a shortened version that
        is 140 characters or less."""

        unaltered_string = super(TweetableMarkovGenerator, self).make_text(chains)
        return unaltered_string[:139] + "." 

class TweetableMarkovGenerator(SimpleMarkovGenerator):
    """Takes in text input, and generates a tweetable (140 characters or less) 
    Markov string based on that input using a Markov Chain algorithm."""

    def make_text(self, chains): 
        """ This method generates a long-format string using the method defined in 
        the SimpleMarkovGenerator superclass, then returns a shortened version that
        is 140 characters or less."""

        unaltered_string = super(TweetableMarkovGenerator, self).make_text(chains)

        shortened_string = ""    

        if len(unaltered_string) < 140:
            return unaltered_string

        else:
            unaltered_words = unaltered_string.split(" ")

            for word in unaltered_words:
                if len(shortened_string) + len(word) + 1 >= 140:
                    shortened_string += "."
                    return shortened_string

                else:
                    shortened_string = shortened_string + " " + word




# another way uses its own completely new make_text method that does not inherit
# anything from the Parent class.  

class TweetableMarkovGeneratorQuick(SimpleMarkovGenerator):
    """Takes in text input, and generates a tweetable (140 characters or less) 
    Markov string based on that input using a Markov Chain algorithm."""

    def make_text(self, chains):
        """Takes dictionary of markov chains; returns random text that is
        140 characters long or less."""
            
        rand_key = random.choice(chains.keys())
        rand_value_word = random.choice(chains[rand_key])
        key1, key2 = rand_key
        
        markov_string = key1 + " " + key2 + " " + rand_value_word
        
        while rand_key in chains:


            new_bigram = (key2, rand_value_word)

            if new_bigram in chains:
                rand_new_word = random.choice(chains[new_bigram])
                if len(markov_string + rand_new_word) + 1 >= 140:
                    return markov_string + "."
                else:
                    markov_string += " " + rand_new_word
                    key2 = rand_value_word
                    rand_value_word = rand_new_word 
                    rand_key = new_bigram           

            else:
                markov_string += "."
                return markov_string

    




        
if __name__ == "__main__":
     
    script, file_name = sys.argv
    simple = SimpleMarkovGenerator()
    # print simple.make_text(simple.make_chains(file_name))
    # print "\n"
    # print simple.make_text(simple.make_chains(file_name))
    tweet = TweetableMarkovGenerator()
    print "\n"
    print "TweetableMarkovGenerator"
    print tweet.make_text(tweet.make_chains(file_name))
    print "\n"
    qtweet = TweetableMarkovGeneratorQuick()
    print "TweetableMarkovGeneratorQuick"
    print qtweet.make_text(qtweet.make_chains(file_name))