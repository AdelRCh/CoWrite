# CoWrite: Your Personal Writing Assistant.

CoWrite is a team project started at [Le Wagon](https://github.com/lewagon/) as part of the Data Science boot camp's curriculum during our Project Weeks.
The repository shows our progress within eight working days, after which we worked on presenting it on our Demo Day (June 16).

The individuals working on the project are as follows:  

* **The project team:** [Sarah Carr](https://github.com/Sarah-carr/), [Adel Chouadria](https://github.com/AdelRCh/), and [Agata Plucienik](https://github.com/Agataplucienik)
* **Teachers involved in the project:** Leia Grobe (GUI), [Greg Kappes (overall)](https://github.com/gkap720), Elaine Pinheiro, and Victor G. Ruiz Lopez

## About the repository:
* **/api** holds our API source file, which uses the FastAPI module (fast.py)
* **/core** contains modules, one per class. Each class has a specific task. Upon continuation, file names will change to reflect the tasks
  * **paragraph.py** contains the models used to suggest a reordering of sentences within a given paragraph and their class implementation.
  * **preprocess.py** contains our grammar model and an input pre-processing function filtering some cases of poor punctuation usage. However, in its current state, it does not handle honorifics yet (Mr., Ms., Mrs., Dr., Ph.D...).
  * **train.py** currently uses [FastCoref](https://github.com/shon-otmazgin/fastcoref) to detect coreferences across text.
  * Other files have been created for future use.
* **/streamlit** contains our GUI (built on Streamlit)
 
## Crediting the models and work used:

```
@inproceedings{Otmazgin2022FcorefFA,
  title={F-coref: Fast, Accurate and Easy to Use Coreference Resolution},
  author={Shon Otmazgin and Arie Cattan and Yoav Goldberg},
  booktitle={AACL},
  year={2022}
}

@misc{zhang2019pegasus,
    title={PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization},
    author={Jingqing Zhang and Yao Zhao and Mohammad Saleh and Peter J. Liu},
    year={2019},
    eprint={1912.08777},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

```

The project also used:  
* [Vennify's pre-trained T5 model on HuggingFace.](https://huggingface.co/vennify/t5-base-grammar-correction)
* [MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
