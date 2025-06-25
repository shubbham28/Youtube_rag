def generate_video_summary(chunks, client):
    joined = "\n\n".join(chunks[:5])
    prompt = f"""
You are a helpful assistant. Read the following lecture content and summarize it in a structured format:

Key Topics:
- List key themes and concepts

Definitions:
- Define important terms mentioned in the lecture

Key Points:
- Break down the content into bullet points for clarity

Examples:
- Highlight any examples or case studies referenced

Content:
{joined}
"""
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
