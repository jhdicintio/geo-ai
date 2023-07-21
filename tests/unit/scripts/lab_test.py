from src.geo_ai.scripts.lab import generate_prompt


def generate_prompt_test():
    prompt = generate_prompt("rhino")
    assert prompt == "rhino"
