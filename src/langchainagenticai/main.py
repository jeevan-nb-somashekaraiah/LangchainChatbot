import streamlit as st
from src.langchainagenticai.ui.streamlitui.loadui import Loadstreamlitui
from src.langchainagenticai.LLMs.groqLlm import GroqLlm
from src.langchainagenticai.graph.graph_builder import Graph_builder
from src.langchainagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():

    ui = Loadstreamlitui()
    user_input = ui.load_streamlit_ui()
    

    if not user_input:
        st.error("failed to load model ")
        return
    
    #Text input for user message
    if st.session_state.IsFetchButtonClicked:
         user_message = st.session_state.timeframe
    else:
         user_message =st.chat_input("Enter your message:")

    if user_message:
        try:
        #configure the llm

            obj_llm_config = GroqLlm(user_control_inputs=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("LLM model could not be initiated")
                return
            # Initialize and set up the graph based on use case
            usecase=user_input.get("selected_usecase")

            if not usecase:
                    st.error("Error: No use case selected.")
                    return
        
            graph_builder = Graph_builder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()

            except Exception as e:
                st.error(f"Error: graph set up failed - {e}")
                return
        except Exception as e:
                st.error(f"Error: graph set up failed - {e}")
                return