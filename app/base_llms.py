import os
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from botocore.config import Config
import boto3
from langchain_openai import ChatOpenAI

load_dotenv()

def llm_llama():
    
    config = Config(read_timeout=120)
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_ACCESS_KEY= os.getenv("AWS_ACCESS_KEY_ID")

    client = boto3.client('bedrock-runtime', region_name='us-west-2',config=config, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,)
 
    llm = ChatBedrock(
        client=client,
        model_id="arn:aws:bedrock:us-west-2:585008056358:inference-profile/us.meta.llama3-3-70b-instruct-v1:0",
        provider="meta",
        model_kwargs={"temperature": 0},
        region="us-west-2"
    )

    return llm

def llm_4o():
    llm  = ChatOpenAI(model="gpt-4o-2024-11-20", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    return llm

def llm_o1_mini():
    llm = ChatOpenAI(model="o1-mini", api_key=os.getenv("OPENAI_API_KEY"))
    return llm