'''
The routines which will help us train three components:
- Grammar checking
- Coreference identification
- Summarizer

If we get to that point, we will also have a function to train our stylebook
checker depending on our stylebook du jour.
'''
from fastcoref import spacy_component
import spacy
import pandas as pd
import re

class CorefModel:

    # Initializing model
    def __init__(self):
        # Loading the model and creating a pipeline
        self.nlp = spacy.load("en_core_web_lg")
        self.nlp.add_pipe("fastcoref")


    def get_coref_outputs(self,input_text):
        '''
        We want to get the coreference outputs on a paragraph-by-paragraph basis,
        after we do the grammar correction, but before everything else.

        Input:
        - input_text (str)

        Output:
        - a dictionary with the following syntax {
                'nb_corefs': the amount of fields that have a coreference,
                'word_boundaries': the string positions for each coreference's start/end,
                'words': the words within said boundaries
        }
        '''
        #Get the coreference indexes from our input
        doc = self.nlp(input_text)

        coref_words = []
        for index, coref in enumerate(doc._.coref_clusters):
            coref_words.append([])
            for word in coref:
                coref_words[index].append(input_text[word[0]:word[1]])

        # The function returns the coordinates and the words.
        # We can use the coordinates to highlight text on Streamlit if needed,
        # and we can use the words directly for other things.
        return {
            'nb_corefs': len(doc._.coref_clusters),
            'word_boundaries':doc._.coref_clusters,
            'words':coref_words
        }

    def prepare_for_summary(self,text,coreferences=None):
        '''
        The function receives a 'text' argument - our initial input.
        Coreferences is the result of processing our input through the coreference checker.
        We do not recommend having "None", but the function is built to account for such scenarios.

        This function returns an edited version of our input, one that makes more sense for a summary model.
        '''

        # Creating a separate variable (bad memories from C++)
        processed_text = text

        # If we didn't bother running this part (NOT RECOMMENDED), this is a fallback:
        if coreferences is None:
            coreferences = self.get_coref_outputs(text)

        # Initializing the list of corefs
        nb_corefs = coreferences.get('nb_corefs',0)
        full_coref_list = []

        if nb_corefs == 0: return processed_text

        # Gathering all the coreferences into a DataFrame (Start, Stop, replace that space by)
        for coref_idx in range(nb_corefs):

            # Find the coreference with the biggest word length for any given coref:
            longest_coref = sorted(coreferences['words'][coref_idx],key=len,reverse=True)[0]

            # Associate the locations of old words with their upcoming replacement:
            for boundary in coreferences['word_boundaries'][coref_idx]:
                full_coref_list.append([boundary[0],boundary[1],longest_coref])

        # Making the dataframe and sorting by their starting spots
        coref_df = pd.DataFrame(full_coref_list,columns=['start','stop','replacement'])
        coref_df.sort_values(by='start',ascending=False,inplace=True)
        coref_df.reset_index(drop=True,inplace=True)

        # Changing the words - going from last coreference to first.
        # If we start with the first one, the positions get bounced all over the place.
        # We get the string before the coreference we need to replace, put the replacement, then continue
        for index, row in coref_df.iterrows():
            processed_text = processed_text[:row.start] + row.replacement + processed_text[row.stop:]

        # And we're home free from there
        return processed_text

    def detect_bad_coref(self,text,coreferences=None):
        '''
        This function takes the output from "get_coref_output" running on a full paragraph (coreferences),
        as well as the summarized version of the text.
        It will return tuples of coreferences that have too much repetition to them or that lack pronoun usage,
        as well as how many references we are making to it.

        Note: coreferences can be left empty, but we do not recommend that. Only do that if you know what you're doing.
        '''

        if coreferences is None:
            coreferences = self.get_coref_outputs(text)
        # An extremely barbaric implementation of pronouns.
        pronoun_list = ['I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'mine', 'yours', 'his', 'hers', 'its', 'ours', 'theirs']
        pronoun_caps = [i.upper() for i in pronoun_list]
        bad_coref_log = []

        nb_sentences = len(re.split(r'[.!?] +', text))

        nb_corefs = coreferences.get('nb_corefs',0)
        for coref_idx in range(nb_corefs):
            longest_coref = sorted(coreferences['words'][coref_idx],key=len,reverse=True)[0]
            coref_list = [i.upper() for i in coreferences['words'][coref_idx]]
            count_pronouns = len([i for i in coref_list if i in pronoun_caps])

            factor = (len(coref_list) - count_pronouns + 2)
            if factor <= 0: factor = 1
            score = nb_sentences / factor

            #We need to refine the threshold. For now, must send the notebook as is.
            threshold = 1

            #If we have less than 1 pronoun in a situation where we have over two sentences,
            #or we refer to the topic too much, we need to make a callout.

            if score <= threshold:
                bad_coref_log.append((longest_coref,len(coref_list)))

        return bad_coref_log
