from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DataFrameLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

import os

# utils/llm_utils.py
def create_vectorstore(df, persist_dir="embeddings/"):
    # ✅ Step 1: Create a new column that combines multiple fields into readable context
    df["context"] = df.apply(
        lambda row: (
            f"On {row['Date']}, product {row['Product']} was sold in {row['Region']} "
            f"with sales of {row['Sales']}, customer age {row['Customer_Age']}, "
            f"gender {row['Customer_Gender']}, and satisfaction score {row['Customer_Satisfaction']}"
        ),
        axis=1
    )

    # ✅ Step 2: Load only the context column into the DataFrameLoader
    loader = DataFrameLoader(df[["context"]], page_content_column="context")

    # ✅ Step 3: Continue with LangChain processing
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb


def build_llm_chain(vectordb):
    """Build a LangChain RetrievalQA chain using GPT-4."""
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    retriever = vectordb.as_retriever()
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain