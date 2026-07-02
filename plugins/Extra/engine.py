# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import openai
from info import OPENAI_API

async def ai(query):
    openai.api_key = OPENAI_API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful movie assistant bot. Provide concise responses."},
            {"role": "user", "content": query}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
     
async def ask_ai(client, m, message):
    try:
        question = message.text.split(" ", 1)[1]
        # Generate response using OpenAI API
        response = await ai(question)
        # Send response back to user
        await m.edit(f"{response}")
    except Exception as e:
        # Handle other errors
        error_message = f"An error occurred: {e}"
        await m.edit(error_message)
