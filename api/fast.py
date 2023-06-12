import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.preprocess import process_input
from core.paragraph import summarise, scoring, extract
from core.train import get_coref_outputs, prepare_for_summary
import spacy
# from core.paragraph import summarise, scoring, extract, new_dataframe
app = FastAPI()



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
    preprocess = process_input(full_text)
    coreferences = get_coref_outputs(preprocess)
    summary_prep = prepare_for_summary(preprocess, coreferences)
    #bad_coref = detect_bad_coref(coreferences,nb_sentences=1)
    summarised = summarise(summary_prep)
    scores = scoring(summarised, full_text)
    extracted = extract(scores)
    #new_df = new_dataframe(extracted, full_text)

    return {
        "grammar check": preprocess,
        "summary": summarised,
        "similarities": extracted
    }
#for stuff in bad_corefs:
#print(f'Bad coreference detected: please replace as many instances of **{stuff[0]}** as possible with adequate pronouns.')

@app.get("/")
def root():
    return {'greeting': 'Hello'}
