import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query_processor import process_user_query

app = FastAPI(
    title="AI HR Assistant ", 
    description="Production RAG Backend Engine for HR policy parsing"
)

# CORS setup for safe localized frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    namespace: str = ""

class QueryResponse(BaseModel):
    answer: str
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI HR Assistant Backend Hub! Head over to /docs to test the API endpoints."}

@app.post("/api/chat", response_model=QueryResponse)
async def chat_with_hr(request: QueryRequest):
    try:
        # Calls the updated query processor with safe kwargs
        answer = process_user_query(query=request.question, namespace=request.namespace)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)