from openai import OpenAI
from text_example import search_query

client = OpenAI()

def chat(query):
    context = search_query(query)
    prompt_with_context = f"Context: {context}\n\nUser input: {query}"

    response = client.chat.completions.create( 
        model="gpt-4o-2024-08-06", 
        messages=[{"role": "user", "content": prompt_with_context}],
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content

test = "Ege Ihracatci Birliklerinde en guncel 5 duyuru ne hakkinda?"
for chunk in chat("Ege Ihracatci Birliklerinde afyonkarahisar blok mermer fuari ne zaman duzenlenecek"):
    print(chunk, end='', flush=True)
