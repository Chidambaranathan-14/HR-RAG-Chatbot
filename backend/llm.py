import os
from openai import OpenAI
from dotenv import load_dotenv

# Force load and override any stale terminal environment variables
load_dotenv(override=True)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_response(prompt: str, context: str) -> str:
    """
    Sends the user query and retrieved context to Gemini via OpenRouter.
    """
    system_prompt = (
        "You are a helpful HR Assistant. Answer the user's question based strictly on the provided HR policy context. "
        "Provide a clear, detailed and professional answer. If the answer cannot be found in the context, "
        "state that you do not know based on the current policies."
    )
    user_content = f"Context:\n{context}\n\nQuestion: {prompt}"
    
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        # CRITICAL: Caps worst-case token size to stay within OpenRouter balance limits
        max_tokens=500  
    )
    return response.choices[0].message.content