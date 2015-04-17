from sys import argv
import random

class SimpleMarkovGenerator(object):
    """Takes in text input, and generates a Markov string based on that 
    input using a Markov Chain algorithm."""

    def read_text_files(self, argv):
        string_list = []

        for file_name in argv[1:]:
            text_file = open(file_name)
            text_string = text_file.read().replace("\n", " ").strip()
            string_list.append(text_string)
        return " ".join(string_list)

    def make_chains(self, argv): 
        """Takes input text as string; returns dictionary of markov chains."""

        text_string = self.read_text_files(argv)
        word_list = text_string.split()

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
        key1, key2 = rand_key
        markov_list = [key1, key2]       

        while rand_key in chains:

            rand_new_word = random.choice(chains[rand_key])
            markov_list.append(rand_new_word)
            rand_key = (rand_key[1], rand_new_word)
           
        return " ".join(markov_list)

class RemovePunctuationMixin(object):
    """Removes puncuation from your string"""

    def remove_punct(self, text_string):

        text_no_punct = ""

        for char in text_string:
            if char.isalpha() or char == " ":
                text_no_punct += char

        return text_no_punct


class SimpleMarkovGeneratorNoPunct(SimpleMarkovGenerator, RemovePunctuationMixin):
    """Takes in text input, and generates a Markov string based on that 
    input using a Markov Chain algorithm."""

    def make_chains(self, argv): 
        """Takes input text as string; returns dictionary of markov chains."""
        
        text_string = super(SimpleMarkovGeneratorNoPunct, self).read_text_files(argv)
        text_no_punct = self.remove_punct(text_string)
     
        print text_no_punct
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
        key1, key2 = rand_key
        markov_list = [key1, key2]       

        while rand_key in chains:

            rand_new_word = random.choice(chains[rand_key])
            markov_list.append(rand_new_word)
            rand_key = (rand_key[1], rand_new_word)
           
        return " ".join(markov_list) + "."





#  one way:  The TweetMarkovGenerator will have its own make_text method that inherits
#  the make_text method from the Parent class but also tweaks it so that
#  the Markov text generated ends at 140 characters.  



class TweetableMarkovGeneratorDirty(SimpleMarkovGenerator):
    """Takes in text input, and generates a tweetable (140 characters or less) 
    Markov string based on that input using a Markov Chain algorithm."""

    def make_text(self, chains): 
        """ This method generates a long-format string using the method defined in 
        the SimpleMarkovGenerator superclass, then returns a shortened version that
        is 140 characters or less."""

        unaltered_string = super(TweetableMarkovGeneratorDirty, self).make_text(chains)
        return unaltered_string[:139]

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
        key1, key2 = rand_key
        markov_list = [key1, key2]       

        while rand_key in chains:

            rand_new_word = random.choice(chains[rand_key])
            if len(" ".join(markov_list) + rand_new_word) < 139:
                markov_list.append(rand_new_word)
                rand_key = (rand_key[1], rand_new_word)
            else:   
                return " ".join(markov_list)

        return " ".join(markov_list)
            
    
if __name__ == "__main__":
      
    print "*" * 50
    
    # print "SimpleMarkovGenerator"
    # simple = SimpleMarkovGenerator()
    # print simple.make_text(simple.make_chains(argv))
    # print "\n"

    print "SimpleMarkovGeneratorNoPunct"
    punct = SimpleMarkovGeneratorNoPunct()
    print punct.make_text(punct.make_chains(argv))
    print "\n"

    # tweet = TweetableMarkovGenerator()
    # print "\n"
    # print "TweetableMarkovGenerator"
    # print tweet.make_text(tweet.make_chains(argv))
    
    # print "\n"
    # qtweet = TweetableMarkovGeneratorQuick()
    # print "TweetableMarkovGeneratorQuick"
    # print qtweet.make_text(qtweet.make_chains(argv))
