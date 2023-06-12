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
#import lance


def get_coref_outputs(corrected_text, model):
    nlp = spacy.load("en_core_web_lg")
    nlp_model = nlp.add_pipe("fastcoref")
    #Get the coreference indexes from our input
    doc = model(corrected_text)

    coref_words = []
    for index, coref in enumerate(doc._.coref_clusters):
        coref_words.append([])
        for word in coref:
            coref_words[index].append(corrected_text[word[0]:word[1]])

    # My function returns the coordinates and the words.
    # We can use the coordinates to highlight text on Streamlit if needed,
    # and we can use the words directly for other things.
    coreferences = {
        'nb_corefs': len(doc._.coref_clusters),
        'word_boundaries':doc._.coref_clusters,
        'words':coref_words
    }

    return coreferences


def prepare_for_summary(corrected_text, coreferences):

    # Creating a separate variable (bad memories from C++)
    processed_text = corrected_text

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
    for row in coref_df.iterrows():
        processed_text = processed_text[:row.start] + row.replacement + processed_text[row.stop:]

    # for index, row in coref_df.iterrows():
    #     processed_text = processed_text[:row.start] + row.replacement + processed_text[row.stop:]

    # And we're home free from there
    return processed_text

        #This function takes an output from "get_coref_output" running on a full paragraph,
#as well as the number of sentences in a paragraph (1 by default).

#I need to refine the output here.
# def detect_bad_coref(coreferences, full_text):
#     # An extremely barbaric implementation of pronouns.
#     #nb_sentences = calc_num_sentences(full_text):
#     return len(re.split(r'[.!?] +', full_text))
#     pronoun_list = ['I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'mine', 'yours', 'his', 'hers', 'its', 'ours', 'theirs']
#     pronoun_caps = [i.upper() for i in pronoun_list]
#     bad_coref_log = []

#     nb_corefs = coreferences.get('nb_corefs',0)
#     for coref_idx in range(nb_corefs):
#         longest_coref = sorted(coreferences['words'][coref_idx],key=len,reverse=True)[0]
#         coref_list = [i.upper() for i in coreferences['words'][coref_idx]]
#         count_pronouns = len([i for i in coref_list if i in pronoun_caps])

#         factor = (len(coref_list) - count_pronouns + 2)
#         if factor <= 0: factor = 1
#         score = nb_sentences / factor

#         #We need to refine the threshold. For now, must send the notebook as is.
#         threshold = 1

#         #If we have less than 1 pronoun in a situation where we have over two sentences,
#         #or we refer to the topic too much, we need to make a callout.

#         if score <= threshold:
#             bad_coref_log.append((longest_coref,coref_idx+1))

#     return bad_coref_log

# if __name__ == "__main__":
#     nlp = spacy.load("en_core_web_lg")
#     nlp_model = nlp.add_pipe("fastcoref")
#     corefs = get_coref_outputs({"text": "this is a sentence, hes a bad box"}, nlp_model)
#     print(corefs)
