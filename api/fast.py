#import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.preprocess import GrammarModel
from core.paragraph import ParagraphReorderer
from core.train import CorefModel
#import spacy
#from core.paragraph import summarise, scoring, extract, new_dataframe
app = FastAPI()

grammar_model= GrammarModel()
reorder = ParagraphReorderer()
comodel = CorefModel()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
 )

@app.get("/grammar")
def grammar(full_text):
    preprocess = grammar_model.check_grammar(full_text)
    coreferences = comodel.get_coref_outputs(preprocess)
    summary_prep = comodel.prepare_for_summary(preprocess, coreferences)
    bad_coref = comodel.detect_bad_coref(preprocess, coreferences)
    summarised = reorder.summarise(summary_prep)
    df_similarities = reorder.score_sentences(full_text, summarised)
    #extracted = extract(scores)
    #new_df = new_dataframe(extracted, full_text)

    return {
        "grammar check": preprocess,
        "summary": summarised,
        "similarities": df_similarities
    }
#for stuff in bad_corefs:
#print(f'Bad coreference detected: please replace as many instances of **{stuff[0]}** as possible with adequate pronouns.')

@app.get("/")
def root():
    return {'greeting': 'Hello'}
