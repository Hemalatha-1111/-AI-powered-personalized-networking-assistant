from transformers import pipeline
class TopicGenerator:
    def __init__(self):
        # Human-like responses kosam gpt2 small text-generation setup
        self.generator = pipeline("text-generation", model="gpt2")

    def generate_prompts(self, theme: str, interests: str) -> list:
        prompt = f"At a networking event about {theme}, a professional interested in {interests} can say: \""
        
        outputs = self.generator(prompt, max_length=60, num_return_sequences=3, pad_token_id=50256)
        
        starters = []
        for output in outputs:
            text = output['generated_text']
            # Clean context extraction
            clean_text = text.replace(prompt, "").split('"')[0].strip()
            if clean_text and clean_text not in starters:
                starters.append(clean_text)
                
        # Backup static responses simple text errors prevent cheyadanki
        if len(starters) < 2:
            starters = [
                f"Hi! I saw the event focuses on {theme}. What brought you here today?",
                f"As someone keen on {interests}, I'm loving the insights on {theme}. What's your take on it?"
            ]
        return starters