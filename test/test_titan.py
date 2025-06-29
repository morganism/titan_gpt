import json
import openai
import difflib
import argparse
from cloner import create_system_prompt, load_persona

TEST_CASES_FILE = "test_cases.json"

def string_distance(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def run_test_case(api_key, system_prompt, test_input, expected_fragments):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": test_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.8
    )["choices"][0]["message"]["content"]

    results = []
    for fragment in expected_fragments:
        dist = string_distance(response, fragment)
        results.append((fragment, dist))

    return response, results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--threshold", type=float, default=0.75)

    args = parser.parse_args()
    persona = load_persona()
    system_prompt = create_system_prompt(persona)

    with open(TEST_CASES_FILE, "r") as f:
        cases = json.load(f)

    passed = 0

    for i, case in enumerate(cases):
        print(f"\n--- Test Case {i+1} ---")
        input_text = case["input"]
        expected = case["expected_fragments"]

        response, results = run_test_case(args.api_key, system_prompt, input_text, expected)
        print(f"Response:\n{response}\n")

        match_results = [dist for frag, dist in results]
        if all(d >= args.threshold for d in match_results):
            print("✅ Passed")
            passed += 1
        else:
            print("❌ Failed")
            for frag, dist in results:
                print(f"  Fragment: '{frag}' -> Similarity: {dist:.2f}")

    print(f"\n=== Titan Test Summary ===")
    print(f"{passed} / {len(cases)} passed")

if __name__ == "__main__":
    main()