from openai import OpenAI
from test_example import search_query

client = OpenAI()

def chat(query, chat_history):
    context = search_webpage_final(query)
    prompt_with_context = f"Context: {context}\n\nUser input: {query}"

    chat_history.append({"role": "user", "content": prompt_with_context})

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06", 
        messages=chat_history,
        stream=True
    )

    complete_response = ""

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            complete_response += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content

    chat_history.append({"role": "assistant", "content": complete_response})

