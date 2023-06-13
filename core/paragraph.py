'''
Here are the methods used to view paragraphs in their entirety.
We will be using a pretrained summarizing model to help with the task.
Its outputs will help us judge which sentences should come first, and how
we should reorder our texts depending on the situation.

The MVP will examine the feasability of news-style inverted pyramid layouts.
However, we acknowledge that documents of different natures would highlight
different features.
'''
from transformers import AutoTokenizer, PegasusForConditionalGeneration, AutoModel
from sentence_transformers import util
from sentence_transformers import SentenceTransformer
import torch
import gc, re
import pandas as pd
# from <path_to_hugging_face_py> import HuggingFaceAPICall

class ParagraphReorderer:

    def __init__(self,sum_env=None):
        '''
        The initialization of our ParagraphReorderer class will not take anything as input.
        That said, models need to be downloaded from HuggingFace on the first runtime.
        Afterwards, we may save them locally.

        Methods:

        - ParagraphReorder(sum_env=None):
        -- If we set sum_env='hf', we can pull summaries from HuggingFace instead.
        -- This is a kernel-saving measure for now.

        - summarize(input_text): summarizes the text you provide to it
        '''
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # if not (sum_env == 'hf'):
        #     self.sum_model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-xsum").to(self.device)
        #     self.sum_tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
        # else:
        #     self.hf_api = HuggingFaceAPICall(load=False)

        self.sum_env = sum_env

        self.scorer_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').to(self.device)
        self.scorer_tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.sum_model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum").to(self.device)
        self.sum_tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
        self.sum_env = sum_env
        self.scorer_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').to(self.device)
        self.scorer_tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')


    def summarise(self, my_text):
        '''
        my_text comes in, summarized text comes out.
        '''
        if (self.sum_env == 'hf'):
            return self.hf_api.xsum_summarize(my_text)

        tokenized_input = self.sum_tokenizer(my_text, truncation=False, padding="longest", return_tensors="pt").to(self.device)
        tokenized_output = self.sum_model.generate(**tokenized_input)
        my_summary = self.sum_tokenizer.batch_decode(tokenized_output, skip_special_tokens=True)

        #Freeing memory
        del tokenized_input, tokenized_output
        gc.collect()
        if self.device=='cuda': torch.cuda.empty_cache()

        #Sending the summary out
        return my_summary[0]
        # ARTICLE_TO_SUMMARIZE = (full_text)
        # inputs = self.sum_tokenizer(ARTICLE_TO_SUMMARIZE, truncation=True, return_tensors="pt")

        # # Generate Summary
        # summary_ids = self.sum_model.generate(inputs["input_ids"])
        # summary = self.sum_tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        # del tokenized_input, tokenized_output
        # gc.collect()

        # return summary

    def score_sentences(self, input_text, summary=None):
        # This step will be skipped if we already have a ready-made summary sentence of our own.
        if summary is None:
            summary = self.summarize(input_text)

        # Run inference & create embeddings
        payload = re.split(r'[.!?] +', input_text)
        encoded_summary = self.scorer_model.encode(summary, convert_to_tensor=True)

        # Keeping track of all similiarities
        similarities = []

        for sentence in payload:
            encoded_sentence = self.scorer_model.encode(sentence, convert_to_tensor=True)
            sim_score = util.pytorch_cos_sim(encoded_summary, encoded_sentence)
            similarities.append(sim_score[0].item())

        # Bringing it together into a DataFrame:
        summary_dictionary={"sentence":payload, "coefs":similarities}
        df = pd.DataFrame.from_dict(summary_dictionary)
        df = df.sort_values(by='coefs',ascending=False)
        df = df.reset_index(drop=True)
        df.index.names = ['importance']
        df.index = df.index + 1
        #df.set_index(keys='importance',inplace=True)
        df2 = df.to_json(orient = 'columns')

        # Cleaning up
        del payload, encoded_summary, encoded_sentence, sentence, sim_score, similarities, summary_dictionary
        gc.collect()
        if self.device=='cuda': torch.cuda.empty_cache()

        return df2

    # def scoring(self, summary, full_text):
    #     #model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    #     list_from_article = re.split(r'[.!?] +', full_text)
    #     similiarities=[]

    #     for sentence in list_from_article:
    #         embedding_1= self.scorer_model.encode(summary, convert_to_tensor=True)
    #         embedding_2 = self.scorer_model.encode(sentence, convert_to_tensor=True)
    #         similiarities.append(util.pytorch_cos_sim(embedding_1, embedding_2))

    #     return similiarities

    # def extract(score):
    #     score[0].item()
    #     new_similiarities=[]
    #     for i in range(len(score)):
    #         new_similiarities.append(score[i].item())

    #     return new_similiarities

    # def new_dataframe(new_similarities, full_text):
    #     summary_dictonary={"sentence":full_text.split(". "), "coefs":new_similiarities}
    #     df = pd.DataFrame.from_dict(summary_dictonary)
    #     df = df.sort_values(by='coefs',ascending=False)
    #     df.reset_index(drop=True,inplace=True)
    #     df.reset_index(names='importance',inplace=True)
    #     df['importance'] = df['importance'] + 1
    #     df = df.set_index(keys='importance',inplace=True)
    #     df2 = df.to_json(orient = 'columns')

    #     return df2

    # if __name__ == "__main__":
    #     summary_text = "It is a long esetablished facct that a readar will"
    #     text = "It is a long esetablished facct that a readar will be distracted by the readable contont of a page when lookng at its layout.The point of usin Lorem Ipsum is that it has a more-or-less normale distribution of letters, as opposed to using 'Content here, content here', making it look like readable English."
    #     summary = scoring(summary_text,text)
    #     print(extract(summary))
