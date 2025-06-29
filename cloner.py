import json
import openai
import os

PERSONA_FILE = "titan_persona.json"

def load_persona():
    with open(PERSONA_FILE, "r") as f:
        return json.load(f)

def create_system_prompt(persona):
    tone = persona["style"]["tone"]
    prime = persona["prime_directive"]
    context = "\n".join(persona["memory_context"])
    meta = persona["meta_behavior"]
    return f"""
You are {persona['persona']}, a custom-trained GPT personality with the following constraints:
{prime}
{meta}
Always maintain this tone: {tone}
Context: {context}
""".strip()

def get_chat_completion(api_key, messages, temperature=0.8):
    openai.api_key = api_key
    return openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=temperature
    )["choices"][0]["message"]["content"]

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--message", required=False, help="Message to test Titan persona")

    args = parser.parse_args()
    persona = load_persona()
    prompt = create_system_prompt(persona)

    messages = [
        {"role": "system", "content": prompt}
    ]

    if args.message:
        messages.append({"role": "user", "content": args.message})

    response = get_chat_completion(args.api_key, messages, temperature=persona['style']['temperature'])
    print(f"\nTitan Response:\n{response}")

if __name__ == "__main__":
    main()