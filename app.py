import streamlit  as st
#from txtai.pipeline import Summary
import streamlit.components.v1 as components
st.set_page_config(layout='wide')
import requests

#Title




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
"""Deisgn No. 2"""

# Sidebar

title = st.sidebar.markdown("<h1 style='text-align: center; color: #6F2694; font-size: 46px;'>CoWrite</h1>", unsafe_allow_html=True)

selected_option = st.sidebar.selectbox("Select an option", ["Grammar Check", "Coreference", "Paragraph Reorder"])

#set page color



st.markdown("""
    <style>
    label  {
        font-size: 25px !important;
        font-style: bold;
    }
    </style>
    """,unsafe_allow_html=True)


def grammar_check():
    st.subheader("Grammar Check")
    col1, col2 = st.columns(2)

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

        text_input = st.text_area("Input",height=300)

    with col2:
        if st.button("Generate"):
            #first instance
            # url = "https://cowrite-aqprprx6eq-ey.a.run.app/grammar"
            #full_text = {"full_text": text_input}
            #request_grammar = requests.get(url,full_text)

            #experiment instance
            # experiment_url = "https://cowrite-aqprprx6eq-uc.a.run.app/grammar"
            # full_text = {"full_text": text_input}
            # request_grammar = requests.get(experiment_url,full_text)

            #experiment2 instance
            # experiment2_url = "https://cowrite-exp2-aqprprx6eq-ez.a.run.app/grammar"
            # full_text = {"full_text": text_input}
            # request_grammar = requests.get(experiment2_url,full_text)

            #classes instance
            classes_url ="https://cowrite-classes-aqprprx6eq-ez.a.run.app/grammar"
            full_text = {"full_text": text_input}
            request_grammar = requests.get(classes_url,full_text)

            #run locally
            # local_url = "http://localhost:8080/grammar"
            # full_text = {"full_text": text_input}
            # request_grammar = requests.get(local_url,full_text)
            st.write(request_grammar)
            response_grammar = request_grammar.json()

            results = response_grammar["summary"]
            text_output = st.text_area("Output",value=results)
        else:
             text_output = st.text_area("Output",height=300)




def coreference():
    st.subheader("Coreference")
    col1, col2 = st.columns(2)
    with col1:
        custom_css = """
            <style>
                .transparent-button button {
                    background-color: transparent !important;
                    color: transparent !important;
                    border: none !important;
                    outline: none !important;
                }
            </style>
"""


        components.html("",width=40, height=27)


        text_input = st.text_area("Input",height=100)

    with col2:

        if st.button("Generate"):
            text_output = st.text_area("Output",value=text_input)
            # Store the result in a variable called 'result'
        else:
             text_output = st.text_area("Output",height=100)


def paragraph_reorder():
    st.subheader("Paragraph Reorder")
    col1, col2 = st.columns(2)

    with col1:
       with col1:
        custom_css = """
        <style>
            .transparent-button button {
                background-color: transparent !important;
                color: transparent !important;
                border: none !important;
                outline: none !important;
            }
        </style>
"""

        components.html("",width=40, height=27)


        text_input = st.text_area("Input",height=100)

    with col2:

        if st.button("Generate"):
            text_output = st.text_area("Output",value=text_input)
            # Store the result in a variable called 'result'

        else:
             text_output = st.text_area("Output",height=100)


# Main content
if selected_option == "Grammar Check":
    grammar_check()
elif selected_option == "Coreference":
    coreference()
elif selected_option == "Paragraph Reorder":
    paragraph_reorder()







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
