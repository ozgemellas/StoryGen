from fpdf import FPDF
import tempfile
import gradio as gr
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from pathlib import Path
from datetime import datetime
import sqlite3
import random
from fastapi.staticfiles import StaticFiles

# === LOAD MODEL ===
model_path = "../out-storygen/final"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

past_stories = []

# === GENERATE TEXT ===
def story_model_generate(start_sentence):
    inputs = tokenizer(start_sentence, return_tensors="pt", padding=True)
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    max_length = min(300, input_ids.shape[1] + 100)

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

    return tokenizer.decode(output[0], skip_special_tokens=True).strip()

# === SAVE STORY TO DATABASE ===
def save_to_database(prompt, story, pdf_path):
    Path("database").mkdir(exist_ok=True)
    conn = sqlite3.connect("database/stories.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            story TEXT,
            pdf_path TEXT,
            timestamp TEXT
        )
    """)
    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO stories (prompt, story, pdf_path, timestamp) VALUES (?, ?, ?, ?)",
        (prompt, story, pdf_path, timestamp)
    )
    conn.commit()
    conn.close()

# === SAVE FEEDBACK TO DATABASE ===
def save_feedback(rating, comment):
    Path("database").mkdir(exist_ok=True)
    conn = sqlite3.connect("database/feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating TEXT,
            comment TEXT,
            timestamp TEXT
        )
    """)
    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO feedback (rating, comment, timestamp) VALUES (?, ?, ?)",
        (rating, comment, timestamp)
    )
    conn.commit()
    conn.close()
    return gr.update(value="", visible=False), gr.update(value=None)

# === LAST 5 STORIES TABLE ===
def get_last_5_stories_table():
    db_path = Path("database/stories.db")
    if not db_path.exists():
        return "<p>No stories found.</p>"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT prompt, pdf_path, timestamp FROM stories ORDER BY timestamp DESC LIMIT 5"
    )
    rows = cursor.fetchall()
    conn.close()

    html = """
    <table style="width:100%; border-collapse: collapse;">
      <tr>
        <th style='text-align:left; padding:8px; border-bottom:1px solid #ccc;'>Prompt</th>
        <th style='text-align:left; padding:8px; border-bottom:1px solid #ccc;'>Date</th>
        <th style='text-align:left; padding:8px; border-bottom:1px solid #ccc;'>PDF</th>
      </tr>
    """

    for prompt, pdf_path, timestamp in rows:
        filename = Path(pdf_path).name
        date_str = timestamp[:19].replace("T", " ")
        html += f"""
        <tr>
          <td style='padding:8px; border-bottom:1px solid #eee;'>{prompt}</td>
          <td style='padding:8px; border-bottom:1px solid #eee;'>{date_str}</td>
          <td style='padding:8px; border-bottom:1px solid #eee;'>
              <a href="/saved_pdfs/{filename}" target="_blank">📥 {filename}</a>
          </td>
        </tr>
        """

    html += "</table>"
    return html

# === GENERATE STORY ===
def generate_story(start_sentence):
    if not start_sentence.strip():
        return "Please enter a starting sentence.", gr.update(visible=False)

    full_story = story_model_generate(start_sentence)
    past_stories.append(full_story)

    pdf_dir = Path("saved_pdfs")
    pdf_dir.mkdir(exist_ok=True)
    suffix = random.randint(100000, 999999)
    pdf_filename = f"story{suffix}.pdf"
    pdf_path = str(pdf_dir / pdf_filename)

    pdf = FPDF()
    pdf.add_page()

    # Default Arial font for PDF
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(50, 10, "Your Story Begins With:", ln=0)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"{start_sentence} ", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    for line in full_story.split('\n'):
        pdf.multi_cell(0, 8, line)

    pdf.output(pdf_path)
    save_to_database(start_sentence, full_story, pdf_path)

    return full_story, gr.update(value=pdf_path, visible=True)

# === RESET ===
def clear():
    return "", "", gr.update(value=None, visible=False)

# === THEME ===
custom_css = """
body {
    background-color: #0F1C2E;
}
.gradio-container {
    background-color: #0F1C2E;
    color: #F5F0E1;
}
h1, h2, h3, .output-markdown p {
    color: #FFD700;
}
textarea, input, .output-textbox, .input-textbox {
    background-color: #F5F0E1 !important;
    color: #000000 !important;
}
button {
    background-color: #FFD700 !important;
    color: #000000 !important;
    border: none;
}
"""

# === INTERFACE ===
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("<h1>📚 Story Completion System</h1>")
    gr.Markdown("Enter a starting sentence and let the model complete the story:")

    start_sentence = gr.Textbox(label="Starting Sentence", placeholder="E.g.: John woke up in the morning...")
    generate_button = gr.Button("📖 Generate Story")

    output = gr.Textbox(label="📝 Completed Story", lines=10)
    file_output = gr.File(label="📥 Download as PDF", visible=False)

    gr.Markdown("### 📣 Feedback")
    rating = gr.Radio(["👍 Like", "👎 Dislike"], label="How did you find the story?")
    comment = gr.Textbox(label="Write your comment", placeholder="Write your feedback here...", visible=False)
    send_button = gr.Button("Submit", visible=False)

    def show_comment_box(rating_value):
        return gr.update(visible=True), gr.update(visible=True)

    rating.change(fn=show_comment_box, inputs=rating, outputs=[comment, send_button])
    send_button.click(fn=save_feedback, inputs=[rating, comment], outputs=[comment, rating])

    reset_button = gr.Button("🔄 New Story")
    gr.Markdown("### 📚 Last 5 Stories")
    recent_box = gr.HTML(get_last_5_stories_table)

    generate_button.click(
        generate_story,
        inputs=[start_sentence],
        outputs=[output, file_output]
    ).then(
        get_last_5_stories_table,
        outputs=[recent_box]
    )

    reset_button.click(
        clear,
        outputs=[start_sentence, output, file_output]
    ).then(
        get_last_5_stories_table,
        outputs=[recent_box]
    )

# === PDF SERVICE ===
demo.app.mount("/saved_pdfs", StaticFiles(directory="saved_pdfs"), name="saved_pdfs")

demo.launch()
