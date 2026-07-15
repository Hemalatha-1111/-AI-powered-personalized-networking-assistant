import os
from transformers import pipeline

MODEL_DIR = "./models"
DISTILBERT_PATH = os.path.join(MODEL_DIR, "distilbert")
GPT2_PATH = os.path.join(MODEL_DIR, "gpt2")
os.makedirs(MODEL_DIR, exist_ok=True)

if os.path.exists(DISTILBERT_PATH):
    theme_classifier = pipeline("zero-shot-classification", model=DISTILBERT_PATH)
else:
    theme_classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli",local_files_only = True)

    theme_classifier.save_pretrained(DISTILBERT_PATH)

if os.path.exists(GPT2_PATH):
    prompt_generator = pipeline("text-generation", model=GPT2_PATH)
else:
    prompt_generator = pipeline("text-generation", model="gpt2")
    prompt_generator.save_pretrained(GPT2_PATH)

LOG_LEVEL_WORDS = {"info", "warning", "error", "debug", "critical", "fatal"}
DEFAULT_LABELS = ["Technology", "AI", "Machine Learning", "Business", "Marketing", 
                  "Finance", "Healthcare", "Education", "Networking", "Startup", "Product", "Sustainability"]

def extract_themes(description: str, candidate_labels: list = None):
    """DistilBERT Zero-Shot with strong filtering"""
    if not description or len(description.strip()) < 10:
        return ["General Networking"]
    
    labels_to_use = candidate_labels if candidate_labels else DEFAULT_LABELS
    
    result = theme_classifier(description, labels_to_use, multi_label=True)
    
    # Take only themes with score > 0.35 and filter log words
    themes = []
    for label, score in zip(result['labels'], result['scores']):
        if score > 0.35 and label.lower() not in LOG_LEVEL_WORDS:
            themes.append(label)
    
    return themes[:3] if themes else ["General Networking"]


def generate_prompts(theme: str, interests: str):
    """GPT-2 Text Generation"""
    if theme.lower().strip() in LOG_LEVEL_WORDS or theme == "General Networking":
        return [
            f"Hi! What are you most excited about at this event?",
            f"As someone interested in {interests}, what sessions are you attending?",
            f"I work in {interests}. What's your background?"
        ]

    input_text = f"Write 3 short networking conversation starters for someone interested in {interests} at an event about {theme}:\n1."
    outputs = prompt_generator(
        input_text, max_length=120, num_return_sequences=1,
        temperature=0.9, do_sample=True, pad_token_id=prompt_generator.tokenizer.eos_token_id
    )
    generated_text = outputs[0]['generated_text']
    prompts = [p.strip().lstrip("123456789. ") for p in generated_text.split('\n') if p.strip() and len(p) > 10]
    
    if len(prompts) < 3:
        prompts = [
            f"Hi, I'm really interested in {theme}. What brought you to this event?",
            f"As someone into {interests}, how do you see {theme} evolving in the next year?",
            f"I'd love to hear your take on {theme}. What's been your experience with it?"
        ]
    return prompts[:3]