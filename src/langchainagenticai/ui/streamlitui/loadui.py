from src.langchainagenticai.ui.configfile import Config
import streamlit as st
import os


class Loadstreamlitui:

    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout='wide')
        st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked =False

        with st.sidebar:
            #get options from config
            llm_options = self.config.get_llm_options()
            usecase_options =self.config.get_usecase_options()

            #select llm 
            self.user_controls['Selected_llm'] = st.selectbox('Select LLM', llm_options)

            if self.user_controls['Selected_llm'] == 'Groq':

                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox('Select Model',model_options)
                self.user_controls['GROQ_API_KEY'] =st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type = "password")

                #vaidate api key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your GROQ API to proceed.")


            self.user_controls["selected_usecase"] = st.selectbox('Select Usecase', usecase_options)

            if self.user_controls["selected_usecase"] == "Chat with Web" or self.user_controls["selected_usecase"] == "AI News":

                self.user_controls["TAVILY_API_KEY"] = st.text_input(
                "TAVILY API Key",
                type="password"
                )

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your Tavily API key")
                else:
                    os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"]

            if self.user_controls["selected_usecase"] == "AI News":

                st.subheader("AI News Explorer")

                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select Time Frame",
                        {"Daily", "Weekly", "Monthly"},
                        index=0
                    )
                
                if st.button("Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame



        return self.user_controls


