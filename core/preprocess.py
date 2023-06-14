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
from happytransformer import HappyTextToText, TTSettings



#make beam settings and happy t5 a class


class GrammarModel:
    '''This class contains our grammar model.'''

    def __init__(self, env_from=None):
        '''
        The initialization of our GrammarModel class calls an environment string from where
        we load the model. Different environment variables will be invoked, depending on
        env_from's value:

        - 'hf' or None: HuggingFace (by default)
        - 'gc': Google Cloud (will need to pull from environment variables)
        - 'mlflow': form MLFlow (if applicable)
        - 'local': On the local VM/environment

        '''
        # if env_from == None or env_from == 'hf':
        #     self.model = self.load_model('hf')
        # else:
        #     pass # model.load from checkpoint
        self.model = HappyTextToText('TS',"vennify/t5-base-grammar-correction")
        self.beam_settings = TTSettings(num_beams=20)
        # self.beam_settings = TTSettings(num_beams=20, min_length=1, max_length=int(len(input)*(3)))

    def check_grammar(self, input):
        '''
        The input of this function is a **preprocessed** string that we wish to correct.
        The output is a string with corrections (hopefully).
        If we don't like the output, we might want to tune the model some more.
        '''
        gc.collect()

        if not input:
            return input

        new_text=input.split('. ')
        #grammar_model = self.model.generate_text(input, args=self.beam_settings)

        new_sample_text=[]
        for sentence in new_text:
            result = self.model.generate_text(sentence, args=self.beam_settings)
            new_sample_text.append(result.text)

        super_text=" ".join(new_sample_text)

        return super_text


# def process_input(full_text):
#     beam_settings = TTSettings(num_beams=5, min_length=1, max_length=100)
#     happy_t5 = HappyTextToText('TS',"vennify/t5-base-grammar-correction")
#     #Separate the paragraph
#     paragraphs = full_text.split('\n')
#     corrected_paragraphs = []
#     corrections = []
#     for para in paragraphs:
#         #a.candy.is.a.3.5 candy. => a. candy. is. a.3.5 candy.
#         #I want to find all instances of these periods and fix them.
#         search = re.findall(r'\.[a-zA-Z]', para)

#         for bad_dot in search:
#             location = para.find(bad_dot)
#             #I want to include the period in the sentence before splitting.
#             para = para[:location+1] + ' ' + para[location+1:]

#         #We will split each paragraph into sentences and correct each one.
#         #split_sentences = para.split(sep='. ')
#         split_sentences =re.split("[.!?]+", para)
#         for sentence in split_sentences:
#             #happy_t5 is the model variable after loading. Must be renamed, I think.
#             #Alert: preventing an error when people do two line carries in a row ("one of the paragraphs is empty? What sorcery is this.")
#             #It's the equivalent of the "you KICK Miette?" meme tweet, except for the model.
#             if sentence: #Not a line carry
#                 prelim_result = happy_t5.generate_text(sentence, args=beam_settings)
#                 corrections.append(prelim_result.text.capitalize())
#             else:
#                 corrections.append(sentence)

#         result = ' '.join(corrections)
#         corrected_paragraphs.append(result)

#     return '\n'.join(corrected_paragraphs)

# if __name__ == "__main__":
#     text = "It is a long esetablished facct that a readar will be distracted by the readable contont of a page when lookng at its layout.The point of usin Lorem Ipsum is that it has a more-or-less normale distribution of letters, as opposed to using 'Content here, content here', making it look like readable English."
#     summary = process_input(text)
#     print(summary)
