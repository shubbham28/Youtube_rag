def generate_flashcards(topic_chunks, client):
    context = "\n\n".join(topic_chunks)
    prompt = f"""
Generate 10 interview-style flashcards from the following content in the format:

Q: ...
A: ...

Content:
{context}
"""
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content


def fallback_flashcards(topic, client):
    prompt = f"""
The topic '{topic}' was not found in the video.
Generate 5 general flashcards based on this topic in the format:

Q: ...
A: ...
"""
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
