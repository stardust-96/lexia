from openai import OpenAI
from config import OPENAI_API_KEY, GROQ_API_KEY
from settings import load_settings

# Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def rewrite_text_with_gpt(original_text: str, tone: str = "Neutral", num_alternatives: int = None, model_override: str = None) -> list[str]:
    settings = load_settings()
    if num_alternatives is None:
        num_alternatives = settings.get("num_alternatives", 3)
    model = model_override if model_override else settings.get("model", "gpt-4")
    temperature = settings.get("temperature", 0.7)
    if not original_text.strip():
        return ["No text provided."]

    try:
        # Determine if it's a preset tone or custom instruction
        is_preset_tone = tone in ["Neutral", "Formal", "Friendly", "Professional", "Concise", "Creative"]
        
        if model == "llama-4-scout":
            # Llama-specific prompt that works better with its format
            if is_preset_tone:
                system_prompt = f"You are a helpful assistant that rewrites text to improve grammar, clarity, and tone. Use a {tone.lower()} tone."
            else:
                system_prompt = f"You are a helpful assistant that rewrites text according to specific instructions. Follow the user's rewriting requirements precisely."
            
            user_prompt = f"""Rewrite the following text in {num_alternatives} different ways. Label each version clearly as 'Version 1:', 'Version 2:', etc.

Original text: {original_text}

{f"Rewriting instruction: {tone}" if not is_preset_tone else f"Use a {tone.lower()} tone."}

Please provide exactly {num_alternatives} rewritten versions."""
        else:
            # GPT prompt with separator
            if is_preset_tone:
                system_prompt = f"You are a helpful assistant that rewrites text to improve grammar, clarity, and tone. Use a {tone.lower()} tone. Provide {num_alternatives} different alternative rewrites, each with a slightly different approach or style while maintaining the {tone.lower()} tone."
            else:
                system_prompt = f"You are a helpful assistant that rewrites text according to specific instructions. Follow the user's rewriting requirements precisely while providing {num_alternatives} different variations."
            
            user_prompt = f"""Rewrite the following text in {num_alternatives} different ways:

{original_text}

{f"Rewriting instruction: {tone}" if not is_preset_tone else f"Use a {tone.lower()} tone."}

Please provide {num_alternatives} alternatives, separated by '---ALTERNATIVE---' markers."""

        # Select the appropriate client and model based on settings
        if model == "llama-4-scout":
            client = groq_client
            actual_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            client = openai_client
            actual_model = model
        
        response = client.chat.completions.create(
            model=actual_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        
        content = response.choices[0].message.content.strip()
        
        # Try to split by the expected separator first
        alternatives = content.split('---ALTERNATIVE---')
        alternatives = [alt.strip() for alt in alternatives if alt.strip()]
        
        # If we didn't get enough alternatives, try to parse Llama's format
        if len(alternatives) < 2 and model == "llama-4-scout":
            # Parse Llama's format with **Version X:** or similar patterns
            import re
            # Look for patterns like "Version 1:", "Alternative 1:", etc.
            version_pattern = r'\*\*(?:Version|Alternative|Option)\s*\d+:.*?\*\*\s*(.*?)(?=\*\*(?:Version|Alternative|Option)\s*\d+:|$)'
            matches = re.findall(version_pattern, content, re.DOTALL)
            
            if matches:
                alternatives = [match.strip() for match in matches]
            else:
                # Fallback: split by double newlines if we have them
                parts = content.split('\n\n')
                if len(parts) >= num_alternatives:
                    alternatives = parts[:num_alternatives]
                else:
                    # Last resort: just return the whole response as one alternative
                    alternatives = [content]
        
        # Ensure we have the requested number of alternatives
        if len(alternatives) < num_alternatives:
            while len(alternatives) < num_alternatives:
                alternatives.append(alternatives[0] if alternatives else original_text)
        
        return alternatives[:num_alternatives]

    except Exception as e:
        return [f"Error: {str(e)}"]
