
from langgraph.graph import StateGraph, START, END
from src.langchainagenticai.state.state import State
from src.langchainagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langchainagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode
from src.langchainagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langchainagenticai.nodes.ai_news_node import AINewsNode

class Graph_builder:

    def __init__(self,model):
        self.llm= model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):

        """
        graph is build from start to chatbot to end 
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node('chatbot',self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, 'chatbot')
        self.graph_builder.add_edge('chatbot',END)

    def chatbot_with_tools_build_graph(self):
        """
        building chat bot to chat with web and give the output
        """

        #Defining the tool and tool node

        tools = get_tools()
        tool_node = create_tool_node(tools)

        #define llm

        llm  = self.llm
        #define the chatbot node

        obj_chat_with_tool = ChatbotWithToolNode(llm) 
        chatbot_node = obj_chat_with_tool.create_chatbot(tools)
              #add nodes

        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        #define conditional edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        

    def setup_graph(self, usecase:str):

        if usecase == 'Basic Chatbot':
            self.basic_chatbot_build_graph()
        elif usecase == 'Chat with Web':
            self.chatbot_with_tools_build_graph()
        elif usecase == 'AI News':
            self.ai_news_builder_graph()

        return self.graph_builder.compile()
    
    def ai_news_builder_graph(self):

        ai_news_node = AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_results",ai_news_node.save_result)

        #Add edges

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_results")
        self.graph_builder.add_edge("save_results", END)