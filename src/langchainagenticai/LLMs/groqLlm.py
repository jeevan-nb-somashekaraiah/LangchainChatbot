from langchain_groq import ChatGroq
import os
import streamlit as st

class GroqLlm:

    def __init__(self,user_control_inputs):
        self.user_control_inputs = user_control_inputs
    
    def get_llm_model(self):

        try:

            groq_api_key = self.user_control_inputs['GROQ_API_KEY']
            selected_groq_model = self.user_control_inputs['selected_groq_model']
            if groq_api_key =='' and os.environ['GROQ_API_KEY'] == '':
                st.error("please enter API key")

            llm = ChatGroq(api_key = groq_api_key,model = selected_groq_model)

        except Exception as e:
            raise ValueError(f'Error Ocuured with Exception: {e}')
        return llm                                                   

