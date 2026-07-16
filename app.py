import os
import re
from collections import Counter

from flask import Flask, jsonify, render_template, request

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # The app still runs without python-dotenv; environment variables can be set normally.
    pass
app = Flask(__name__)

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have",
    "he", "in", "is", "it", "its", "of", "on", "or", "that", "the", "to", "was", "were",
    "will", "with", "this", "these", "their", "they", "we", "which", "who", "about", "after",
    "but", "not", "than", "into", "over", "more", "also", "said", "says", "new"
}
POSITIVE = {"gain", "growth", "improve", "success", "benefit", "positive", "win", "record", "strong", "rise", "agreement", "support", "progress", "safe", "hope"}
NEGATIVE = {"loss", "decline", "crisis", "risk", "war", "death", "damage", "fail", "failure", "negative", "drop", "fall", "concern", "threat", "attack", "protest"}


def words(text):
    return re.findall(r"[A-Za-z][A-Za-z'-]{1,}", text.lower())


def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 20]


def extract_keywords(text, limit=10):
    counts = Counter(w for w in words(text) if w not in STOPWORDS and len(w) > 2)
    return [word.title() for word, _ in counts.most_common(limit)]


def extract_entities(text, limit=10):
    # Lightweight named-entity approximation: consecutive capitalized terms.
    candidates = re.findall(r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}|[A-Z]{2,}(?:\s+[A-Z]{2,})*)\b", text)
    ignored = {"The", "This", "That", "These", "Those", "A", "An", "And", "But", "For", "In", "On", "At", "After", "Before"}
    counts = Counter(item for item in candidates if item not in ignored)
    return [entity for entity, _ in counts.most_common(limit)]


def local_summary(text, sentence_count=3):
    sentences = split_sentences(text)
    if not sentences:
        return text[:500]
    freq = Counter(w for w in words(text) if w not in STOPWORDS)
    scored = []
    for index, sentence in enumerate(sentences):
        sentence_words = words(sentence)
        score = sum(freq[w] for w in sentence_words if w not in STOPWORDS) / max(len(sentence_words), 1)
        # A small lead bias helps typical inverted-pyramid news articles.
        score += max(0, 0.15 - index * 0.01)
        scored.append((score, index, sentence))
    selected = sorted(sorted(scored, reverse=True)[:min(sentence_count, len(sentences))], key=lambda item: item[1])
    return " ".join(item[2] for item in selected)


def local_sentiment(text):
    all_words = words(text)
    pos = sum(word in POSITIVE for word in all_words)
    neg = sum(word in NEGATIVE for word in all_words)
    score = (pos - neg) / max(pos + neg, 1)
    if score > 0.18:
        label = "Positive"
    elif score < -0.18:
        label = "Negative"
    else:
        label = "Neutral"
    return {"label": label, "score": round(abs(score) * 100), "positive_words": pos, "negative_words": neg}


def llm_response(instruction, article):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a precise news-analysis assistant. Use only the supplied article. If the article does not contain the answer, say so plainly."},
                {"role": "user", "content": f"{instruction}\n\nARTICLE:\n{article}"},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    article = (data.get("article") or "").strip()
    if len(article) < 80:
        return jsonify({"error": "Please paste an article of at least 80 characters."}), 400

    summary = llm_response("Write a concise 3-bullet news summary. Keep facts, names, dates and figures accurate.", article)
    source = "LLM" if summary else "Local NLP"
    if not summary:
        summary = local_summary(article)
    return jsonify({
        "summary": summary,
        "summary_source": source,
        "sentiment": local_sentiment(article),
        "keywords": extract_keywords(article),
        "entities": extract_entities(article),
        "reading_time": max(1, round(len(words(article)) / 220)),
        "word_count": len(words(article)),
    })


@app.post("/api/ask")
def ask():
    data = request.get_json(silent=True) or {}
    article = (data.get("article") or "").strip()
    question = (data.get("question") or "").strip()
    if not article or not question:
        return jsonify({"error": "An article and a question are required."}), 400
    answer = llm_response(f"Answer this question in 2-4 sentences: {question}", article)
    if not answer:
        # Transparent fallback: return the most relevant source sentences rather than inventing facts.
        query_terms = set(w for w in words(question) if w not in STOPWORDS)
        ranked = sorted(split_sentences(article), key=lambda s: sum(w in query_terms for w in words(s)), reverse=True)
        answer = "Based on the article: " + " ".join(ranked[:2]) if ranked else "The article does not provide enough information to answer that."
    return jsonify({"answer": answer, "source": "LLM" if os.getenv("OPENAI_API_KEY") else "Article retrieval"})


if __name__ == "__main__":
    app.run(debug=True)
