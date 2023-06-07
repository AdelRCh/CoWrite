import streamlit  as st
from txtai.pipeline import Summary
# from PyPDF2 import PdfFileReader
st.set_page_config(layout='wide')

'''
# Revolution of NLP Presents:

'''
#Title
st.title("Co-write AI")


#Extract text from PDF file using PyPDF2
# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PdfFileReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text  += page.extractText()
#     return text
# # @st.cache
# def summary_text(text):
#     summary= summary()
#     result = summary(text)
#     return result
# if st.button('Correct Sentence'):
#     st.write()

choice = st.sidebar.selectbox("Select Your Choice",  ['Grammar Check','Coreference','Paragraph reordering'])

if choice == 'Grammar Check':
    st.subheader('Grammar Check  Selected')
    input_text = st.text_area("Enter your text here")
    if st.button('Correct Sentence!'):
        col1,col2,col3=st.columns([1,1,1])
        with col1:
            st.markdown("*** YOUR OUTPUT TEXT ***")
            st.info(input_text)
        # with col3:
        #     result = summary_text(input_text)
        #     st.markdown("summarized text ")
        #     st.success(result)

elif choice == 'Coreference':
    st.subheader('Coreference Selected')
    input_text = st.text_area("Enter...")
    if st.button('Correct it!'):
        st.markdown("*** YOUR OUTPUT TEXT ***")
        st.info( input_text )



elif choice == 'Paragraph reordering':
    st.subheader('Paragraph Reordering Selected')
    input_text = st.text_area("Enter...")
    if st.button('reorder!'):
        # input_file = st.file_uploader(" Upload your document ",type=["pdf"])
        if st.button("sumarize document"):
            st.markdown("*** YOUR OUTPUT TEXT ***")
            st.info( input_text )













url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
