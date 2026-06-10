"""Milestone 5 — Gradio query interface for the Unofficial UCSD Housing Guide.

Run:  .venv/bin/python app.py   (then open http://localhost:7860)

Type a question -> the system retrieves relevant chunks, generates a grounded
answer from them, and shows which source document(s) the answer drew from.
"""

import gradio as gr

from src.generate import ask

EXAMPLES = [
    "What do residents complain about most at Costa Verde Village?",
    "How does median 1-bedroom rent in University City compare to Mira Mesa?",
    "How crowded do students say Regents La Jolla units get?",
    "Which neighborhood is the budget option for UCSD students?",
    "What downsides do reviewers report about La Regencia?",
]


def handle_query(question):
    if not question or not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    if result["sources"]:
        sources = "\n".join(f"• {s['name']}\n  {s['url']}" for s in result["sources"])
    else:
        sources = "(No sources — the guide doesn't cover this question.)"
    return result["answer"], sources


with gr.Blocks(title="UCSD Unofficial Housing Guide") as demo:
    gr.Markdown(
        "# 🏠 The Unofficial Guide — UCSD Off-Campus Housing\n"
        "Ask about apartment complexes and neighborhoods near UC San Diego. "
        "Answers are generated **only** from collected resident reviews and housing "
        "guides — if the guide doesn't cover something, it will say so."
    )
    question = gr.Textbox(
        label="Your question",
        placeholder="e.g. What do residents say about parking at Costa Verde Village?",
    )
    ask_btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=6)
    sources = gr.Textbox(label="Sources (retrieved from)", lines=5)

    gr.Examples(EXAMPLES, inputs=question)
    ask_btn.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
