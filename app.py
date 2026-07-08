import os
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()
llm=ChatMistralAI(model="mistral-small-latest")
tavily_api_key = os.getenv("TAVILY_API_KEY")
if tavily_api_key:
    tool = TavilySearchResults(max_results=5, tavily_api_key=tavily_api_key)
else:
    class DummyNewsTool:
        def __init__(self, max_results=5):
            self.max_results = max_results
        def invoke(self, q):
            return (
                "Sample news (TAVILY_API_KEY not set):\n"
                "- Market update: Gold rises 0.5% amid safe-haven demand.\n"
                "- Economy: Inflation data expected tomorrow could move markets.\n"
                "- Commodities: Oil steady as supply concerns ease.\n"
            )
    tool = DummyNewsTool(max_results=5)
prompt=ChatPromptTemplate.from_template("""
You are an AI assistant.
Summarize the following news into one line bullet points with indexes.

{news}
""")
chain=prompt|llm|StrOutputParser()

st.set_page_config(page_title="NewsAI",layout="wide")
try:
    css=open("style.css").read()
    st.markdown(f"<style>{css}</style>",unsafe_allow_html=True)
except: pass
st.markdown("<div class='banner'>🔴 BREAKING NEWS</div>",unsafe_allow_html=True)
q=st.text_input("Search latest news","Latest gold news")
if st.button("Get Latest News"):
    with st.spinner("Fetching latest news..."):
        res=tool.invoke(q)
        out=chain.invoke({"news":res})
    st.markdown("## Latest News")
    st.write(out)
