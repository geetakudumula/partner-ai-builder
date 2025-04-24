import gradio as gr
import os
from PIL import Image

# Define static blueprint data (extend as needed)
blueprint_data = {
    ("AI Chatbot", "Retail"): {
        "services": ["Azure OpenAI", "Azure CosmosDB", "Logic Apps", "App Service"],
        "prompt": "Act as a friendly shopping assistant for retail customers...",
        "summary": "A chatbot for retail uses Azure OpenAI for LLMs, CosmosDB for customer data, and Logic Apps for order fulfillment.",
    },
    ("Document Summarizer", "Finance"): {
        "services": ["Azure OpenAI", "Form Recognizer", "Blob Storage"],
        "prompt": "Summarize financial statements from scanned documents.",
        "summary": "This pipeline uses OpenAI for text understanding, Form Recognizer to extract fields, and Blob Storage for archiving.",
    },
    ("Translator", "Healthcare"): {
        "services": ["Azure OpenAI", "Azure Translator", "Azure API Management"],
        "prompt": "Translate discharge summaries and prescriptions into Spanish.",
        "summary": "Healthcare solution using OpenAI and Translator API to serve multilingual medical content securely.",
    },
}

# Dynamic generation function
def generate_blueprint(use_case, industry):
    key = (use_case, industry)
    data = blueprint_data.get(key)

    if not data:
        return "Error", "Error", "Error", None

    # Sanitize file name: lowercase, replace spaces
    diagram_file = f"{use_case.lower().replace(' ', '_')}_{industry.lower().replace(' ', '_')}.png"
    diagram_path = os.path.join("diagrams", diagram_file)

    try:
        image = Image.open(diagram_path)
    except FileNotFoundError:
        image = None

    return (
        "\n".join(data["services"]),
        data["prompt"],
        data["summary"],
        image
    )

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("🧠 **PartnerAIBuilder: Azure AI Blueprint Generator**")

    with gr.Row():
        use_case = gr.Dropdown(["AI Chatbot", "Document Summarizer", "Translator"], label="Use Case")
        industry = gr.Dropdown(["Retail", "Finance", "Healthcare"], label="Industry")

    generate_btn = gr.Button("Generate Blueprint")

    services = gr.Textbox(label="Recommended Azure Services")
    prompt = gr.Textbox(label="Prompt Engineering Example")
    summary = gr.Textbox(label="Solution Summary")
    diagram = gr.Image(label="Architecture Diagram")

    generate_btn.click(fn=generate_blueprint,
                       inputs=[use_case, industry],
                       outputs=[services, prompt, summary, diagram])

# Launch app
demo.launch()
