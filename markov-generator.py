from sys import argv
import random
import string
class SimpleMarkovGenerator(object):
    """Takes in text input, and generates a Markov string based on that 
    input using a Markov Chain algorithm."""

    def read_text_files(self, argv):
        string_list = []

        for file_name in argv[1:]:
            text_file = open(file_name)
            text_string = text_file.read().replace("\n", " ").strip()
            clean_string = text_string.translate(None, '"#$%&\\"()*+,-/:;<=>@[\\]^_`{|}~0123456789')
            string_list.append(clean_string)

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


    def choose_first_bigram(self, chains):
        """Chooses first bigram to initiate the markov string"""

        key1 = "a"

        while not (key1[0].isupper() and key1[0].isalpha):
            rand_key = random.choice(chains.keys())        
            key1, key2 = rand_key
        
        markov_list = [key1, key2]  

        return rand_key, markov_list

    def make_text(self, chains):
        """Takes dictionary of markov chains; returns random text."""
        
        rand_key, markov_list = self.choose_first_bigram(chains)

        key1, key2 = rand_key    
        

        while rand_key in chains:

            rand_new_word = random.choice(chains[rand_key])
            markov_list.append(rand_new_word)
            rand_key = (rand_key[1], rand_new_word)
           
        return " ".join(markov_list)

###############################################################

class TweetableMarkovGenerator(SimpleMarkovGenerator):
    """Takes in text input, and generates a tweetable (140 characters or less) 
    Markov string based on that input using a Markov Chain algorithm."""

    def make_text(self, chains):
        """Takes dictionary of markov chains; returns random text that is
        140 characters long or less."""
            
        rand_key, markov_list = self.choose_first_bigram(chains)
        key1, key2 = rand_key          

        while rand_key in chains:

            rand_new_word = random.choice(chains[rand_key])
            if len(" ".join(markov_list) + rand_new_word) < 139:
                markov_list.append(rand_new_word)
                rand_key = (rand_key[1], rand_new_word)
            elif rand_new_word[-1] in '.?"!':
                # print rand_new_word[-1]
                markov_list.append(rand_new_word)
                return " ".join(markov_list)
            else:
                rand_key = (rand_key[1], rand_new_word)



###############################################################
    
if __name__ == "__main__":
      
    print "*" * 50
    
    # print "SimpleMarkovGenerator"
    # simple = SimpleMarkovGenerator()
    # print simple.make_text(simple.make_chains(argv))
    # # print simple.make_chains(argv)

    
    print "\n"
    tweet = TweetableMarkovGenerator()
    print "TweetableMarkovGenerator"
    print tweet.make_text(tweet.make_chains(argv))

