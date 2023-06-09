'''
Here are the methods used to view paragraphs in their entirety.
We will be using a pretrained summarizing model to help with the task.
Its outputs will help us judge which sentences should come first, and how
we should reorder our texts depending on the situation.

The MVP will examine the feasability of news-style inverted pyramid layouts.
However, we acknowledge that documents of different natures would highlight
different features.
'''
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, PegasusForConditionalGeneration
import pandas as pd

def summarise(full_text):

    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")

    ARTICLE_TO_SUMMARIZE = (full_text)
    inputs = tokenizer(ARTICLE_TO_SUMMARIZE, truncation=True, return_tensors="pt")

    # Generate Summary
    summary_ids = model.generate(inputs["input_ids"])
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    return summary

def scoring(summary, full_text):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    list_from_article = full_text.split(". ")
    similiarities=[]

    for sentence in list_from_article:
        embedding_1= model.encode(summary, convert_to_tensor=True)
        embedding_2 = model.encode(sentence, convert_to_tensor=True)
        similiarities.append(util.pytorch_cos_sim(embedding_1, embedding_2))

    return similiarities

def extract(score):
    score[0].item()
    new_similiarities=[]
    for i in range(len(score)):
        new_similiarities.append(score[i].item())

    return new_similiarities

def new_dataframe(new_similarities, full_text):
    summary_dictonary={"sentence":full_text.split(". "), "coefs":new_similiarities}
    df = pd.DataFrame.from_dict(summary_dictonary)
    df = df.sort_values(by='coefs',ascending=False)
    df.reset_index(drop=True,inplace=True)
    df.reset_index(names='importance',inplace=True)
    df['importance'] = df['importance'] + 1
    df = df.set_index(keys='importance',inplace=True)

    return df
