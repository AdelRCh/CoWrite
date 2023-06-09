'''
We will have our preprocessing routines grouped here for ease of use.
- Grammar correction: data loading and cleaning
- Grammar correction: input processing (if necessary)
- Coreference identifier: data loading and cleaning
- Coreference identifier: input processing
- Summarizer: initializing the model, loading the data, and training it further
'''
import re
import gc
from happytransformer import HappyTextToText
from happytransformer import TTSettings


#make beam settings and happy t5 a class

def process_input(full_text):
    beam_settings = TTSettings(num_beams=5, min_length=1, max_length=100)
    happy_t5 = HappyTextToText('TS',"vennify/t5-base-grammar-correction")
    #Separate the paragraph
    paragraphs = full_text.split('\n')
    corrected_paragraphs = []
    corrections = []
    for para in paragraphs:
        #a.candy.is.a.3.5 candy. => a. candy. is. a.3.5 candy.
        #I want to find all instances of these periods and fix them.
        search = re.findall(r'\.[a-zA-Z]', para)

        for bad_dot in search:
            location = para.find(bad_dot)
            #I want to include the period in the sentence before splitting.
            para = para[:location+1] + ' ' + para[location+1:]

        #We will split each paragraph into sentences and correct each one.
        #split_sentences = para.split(sep='. ')
        split_sentences =re.split("[.!?]+", para)
        for sentence in split_sentences:
            #happy_t5 is the model variable after loading. Must be renamed, I think.
            #Alert: preventing an error when people do two line carries in a row ("one of the paragraphs is empty? What sorcery is this.")
            #It's the equivalent of the "you KICK Miette?" meme tweet, except for the model.
            if sentence: #Not a line carry
                prelim_result = happy_t5.generate_text(sentence, args=beam_settings)
                corrections.append(prelim_result.text.capitalize())
            else:
                corrections.append(sentence)

        result = ' '.join(corrections)
        corrected_paragraphs.append(result)

    return '\n'.join(corrected_paragraphs)
