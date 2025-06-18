
import json
import openai
from sentence_transformers import SentenceTransformer, util

openai.api_key = "YOUR_OPENAI_API_KEY"
model = SentenceTransformer('all-MiniLM-L6-v2')

with open("data/discourse_data.json") as f:
    documents = json.load(f)

corpus = [doc['title'] for doc in documents]
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

def get_answer(query):
    question_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(question_embedding, corpus_embeddings, top_k=2)[0]

    context = "\n\n".join([corpus[hit['corpus_id']] for hit in hits])
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful virtual TA."},
            {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"}
        ]
    )

    answer_text = response.choices[0].message.content.strip()
    links = [{"url": documents[hit['corpus_id']]['url'], "text": documents[hit['corpus_id']]['title']} for hit in hits]
    return answer_text, links
