from src.geo_ai.scripts.lab import generate_prompt, generate_model_chat_completion_response, generate_model_completion_response


def generate_prompt_test():
    prompt = generate_prompt("rhino")
    assert prompt == "rhino"


def generate_model_completion_response_test():
    response = generate_model_completion_response()
    print(response)


def generate_model_chat_completion_test():
    response = generate_model_chat_completion_response()
    print(response)
