import streamlit  as st
#from txtai.pipeline import Summary
import streamlit.components.v1 as components
st.set_page_config(layout='wide')
import requests
import ast
import re
from annotated_text import annotated_text

#Title

def grammar_output_fixer(new_text):

    text_split = re.split("[.!?]+", new_text)
    punc_split = re.findall("[.!?]+", new_text)
    if text_split[-1] == '': del text_split[-1]

    repeated_sentences = []

    for i in range(1,len(text_split)):
        sent_set = set(text_split[i].split())
        prev_sent_set = set(text_split[i-1].split())

        if sent_set.issubset(prev_sent_set):
            repeated_sentences.append(i)

    for k in sorted(repeated_sentences,reverse=True):
        del text_split[k], punc_split[k]

    proc_text = ''.join([text_split[i]+punc_split[i] for i in range(len(punc_split))])

    return proc_text

def string_diff(s1: str, s2: str) -> str:
    d1, d2 = [], []
    i1 = i2 = 0
    l1 = len(s1)
    l2 = len(s2)
    while True:
        if i1 >= len(s1) or i2 >= len(s2):
            d1.extend(s1[i1:])
            d2.extend(s2[i2:])
            break
        if s1[i1] != s2[i2]:
            e1 = l1 - i1
            e2 = l2 - i2
            # if e1 > e2:
            #     d1.append((s1[i1],i1))
            #     i2 -= 1
            # elif e1 < e2:
            #     d2.append((s2[i2],i2))
            #     i1 -= 1
            # else:
            d1.append((s1[i1],s2[i2],i1))
            # d2.append((s2[i2],i2))
        i1 += 1
        i2 += 1
    d1.append((None,None,None))
    return d1

def generate_annotation(old_text,proc_text):
    old_text_tok = old_text.split()
    proc_text_tok = proc_text.split()
    differences = string_diff(old_text_tok,proc_text_tok)

    diff_index = 0
    crawled_list = []
    crawled_text = ''
    for i in range(len(old_text_tok)):

        if i == differences[diff_index][2]:

            if crawled_text != '':
                crawled_list.append(crawled_text)
                crawled_text = ''
            crawled_list.append((differences[diff_index][1],differences[diff_index][0]))
            diff_index = diff_index + 1

        else:
            crawled_text = crawled_text + old_text_tok[i]
            if i < len(old_text_tok)-1:
                crawled_text = crawled_text + ' '

        if (i == len(old_text_tok)-1) and (crawled_text != ''):
            crawled_list.append(crawled_text)

    return crawled_list

# choice = st.sidebar.selectbox("Select Your Choice",  ['Grammar Check','Coreference','Paragraph reordering'])

# if choice == 'Grammar Check':
#     st.subheader('Grammar Check  Selected')
#     input_text = st.text_area("Enter your text here")
#     if st.button('Correct Sentence!'):
#         col1,col2,col3=st.columns([1,1,1])
#         with col1:
#             st.markdown("*** YOUR OUTPUT TEXT ***")
#             st.info(input_text)
#         # with col3:
#         #     result = summary_text(input_text)
#         #     st.markdown("summarized text ")
#         #     st.success(result)

# elif choice == 'Coreference':
#     st.subheader('Coreference Selected')
#     input_text = st.text_area("Enter...")
#     if st.button('Correct it!'):
#         st.markdown("*** YOUR OUTPUT TEXT ***")
#         st.info( input_text )



# elif choice == 'Paragraph reordering':
#     st.subheader('Paragraph Reordering Selected')
#     input_text = st.text_area("Enter...")
#     if st.button('reorder!'):
#         # input_file = st.file_uploader(" Upload your document ",type=["pdf"])
#             st.markdown("*** YOUR OUTPUT TEXT ***")
#             st.info( input_text )
"""Disclaimer: this is the MVP. Some features are experimental / in need of further finetuning."""

# Sidebar

title = st.sidebar.markdown("<h1 style='text-align: center; color: #6F2694; font-size: 46px;'>CoWrite</h1>", unsafe_allow_html=True)

st.sidebar.text('Please choose what we want to do:')
selected_grammar = st.sidebar.checkbox("Check the grammar",value=True)
selected_show_corefs = False #st.sidebar.checkbox("Show coreferences",disabled=True)
selected_bad_coref = False #st.sidebar.checkbox("Spot bad coreferences",disabled=True)
selected_summary = st.sidebar.checkbox("Receive a summary",value=True)
selected_reorder = st.sidebar.checkbox("Reorder the sentences",value=True)

#set page color

initial_text = 'The Capybara is a animal that lives in South America. It is the bigest rodent in the world and look like a giant hamster. They lives near water and eat grass, plants, and vegetables. They lives in groups and have a calm and friendle nature. The Capybara is known for them swiming abilities and is often seeing taking a dip in the river. They have a dark brown fur and big round eyes. They are a loveable creature that bring joy and happines to those around them.'

st.markdown("""
    <style>
    label  {
        font-size: 25px !important;
        font-style: bold;
    }
    </style>
    """,unsafe_allow_html=True)


st.subheader("Please enter your text on the left-side panel, then click 'Generate'")
col1, col2 = st.columns(2)
col_annot = st.container()
col_summary = st.container()
col_scores = st.container()
col_coreferences = st.container()
col_bad_corefs = st.container()

with col1:
    custom_css = """
    <style>
        .transparent-button button {
            background-color: transparent !important;
            color: transparent !important;
            border: none   !important;
            outline: none !important;
        }
    </style>
    """

    components.html("",width=40, height=27)

    text_input = st.text_area("Input text:",height=300,value=initial_text)

    with col2:

        # experiment2_url = "https://cowrite-exp2-aqprprx6eq-ez.a.run.app/grammar"
        # local_url = "http://localhost:8080/grammar"
        last_working_version_url ="https://cowrite-classes-aqprprx6eq-ez.a.run.app/grammar"

        # Please add the most recent version here.
        new_version_url = "https://cowrite-aqprprx6eq-uc.a.run.app/grammar"

        # If we don't have a version, or if we revert it to None, we can use the last working version instead.
        url = last_working_version_url if new_version_url is None else new_version_url
        output_text = ''

        if st.button("Generate"):
            #If we had one before, erase all of it.

            full_text = {"full_text": text_input}
            full_request = requests.get(url,full_text).json()
            output_text = '' #Reset our output variable to fit the current purpose

            #Getting the output in the text area
            if selected_grammar:
                gram_model_output = full_request.get("grammar check","Something has gone wrong with the grammar check.")
                output_text = output_text + grammar_output_fixer(gram_model_output)
                with col_annot:
                    st.markdown('**A visual overview of the corrections that we made:**')
                    annotated_text(generate_annotation(text_input,output_text))
                    st.markdown('___')

            if selected_show_corefs:
                # Assuming "bad_corefs" is the endpoint for coreferences (please change it if that is not the case:)
                coreferences_text = full_request.get("coreferences",False)
                if coreferences_text:
                    col_coreferences.markdown(f'Coreferences (very early version): {coreferences_text}') ##We can tweak this further
                    col_coreferences.markdown('___')

            if selected_bad_coref:
                # Assuming "bad_corefs" is the endpoint for coreferences (please change it if that is not the case:)
                bad_coref_text = full_request.get("bad_corefs",False)
                if bad_coref_text:
                    col_bad_corefs.markdown(f'Too much repetition without pronoun usage on: {bad_coref_text}') ##We can tweak this further
                    col_bad_corefs.markdown('___')

            if selected_summary:
                summary_text = full_request.get("summary",False)
                if summary_text:
                    col_summary.markdown('This summary is used to infer which sentences are the most relevant:')
                    col_summary.markdown(f'**{summary_text}**')
                    col_summary.markdown('We could supply our own sentence for that in a future version.')
                    col_summary.markdown('___')

            if selected_reorder and selected_summary:
                # Assuming "similarities" is the endpoint for the scores (please change it if that is not the case:)
                my_df = full_request.get('similarities',False)
                if my_df:
                    col_scores.markdown('*Furthermore, we suggest reordering the sentences as follows:*')
                    col_scores.dataframe(data=ast.literal_eval(my_df)) #Streamlit's built-in df processor
                    col_scores.markdown('These recommendations fit a news-style approach and can be ignored otherwise.')
                    col_scores.markdown('We took your original sentences for this process in case you wished to keep them unchanged.')

            #first instance
            # url = "https://cowrite-aqprprx6eq-ey.a.run.app/grammar"
            #full_text = {"full_text": text_input}
            #request_grammar = requests.get(url,full_text)

            #experiment instance
            # experiment_url = "https://cowrite-aqprprx6eq-uc.a.run.app/grammar"
            # full_text = {"full_text": text_input}
            # request_grammar = requests.get(experiment_url,full_text)

            #experiment2 instance

            # full_text = {"full_text": text_input}
            # request_grammar = requests.get(experiment2_url,full_text)

            # classes instance
            # classes_url ="https://cowrite-classes-aqprprx6eq-ez.a.run.app/grammar"
            # full_text = {"full_text": text_input}
            # request_grammar = requests.get(classes_url,full_text)

            #run locally

            # full_text = {"full_text": text_input}
            # request_grammar = requests.get(local_url,full_text)

        text_output = st.text_area("Corrected text:",value=output_text,height=300)


# def coreference():
#     st.subheader("Coreference")
#     col1, col2 = st.columns(2)
#     with col1:
#         custom_css = """
#             <style>
#                 .transparent-button button {
#                     background-color: transparent !important;
#                     color: transparent !important;
#                     border: none !important;
#                     outline: none !important;
#                 }
#             </style>
# """


#         components.html("",width=40, height=27)


#         text_input = st.text_area("Input",height=100)

#     with col2:

#         if st.button("Generate"):
#             text_output = st.text_area("Output",value=text_input)
#             # Store the result in a variable called 'result'
#         else:
#              text_output = st.text_area("Output",height=100)


# def paragraph_reorder():
#     st.subheader("Paragraph Reorder")
#     col1, col2 = st.columns(2)

#     with col1:
#        with col1:
#         custom_css = """
#         <style>
#             .transparent-button button {
#                 background-color: transparent !important;
#                 color: transparent !important;
#                 border: none !important;
#                 outline: none !important;
#             }
#         </style>
# """

#         components.html("",width=40, height=27)


#         text_input = st.text_area("Input",height=100)

#     with col2:

#         if st.button("Generate"):
#             text_output = st.text_area("Output",value=text_input)
#             # Store the result in a variable called 'result'

#         else:
#              text_output = st.text_area("Output",height=100)


# # Main content
# if selected_option == "Grammar Check":
#     grammar_check()
# elif selected_option == "Coreference":
#     coreference()
# elif selected_option == "Paragraph Reorder":
#     paragraph_reorder()




#response_summariser = requests.get(summariser_url,result_grammar)
            #response_summariser = response_summariser.json()
            #result_summariser = response_summariser[?]


# url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
