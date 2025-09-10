# SQL Database, sql agent, SQL Database toolkit
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ambil dari environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

# Inisialisasi database dan model hanya sekali
db = SQLDatabase.from_uri(DATABASE_URL)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="gemma2-9b-it"
)

agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True,
    handle_parsing_errors=True,
)

# Fungsi yang bisa dipanggil dari Django view
def run_sql_query(query: str) -> dict:
    try:
        response = agent.invoke(query)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}