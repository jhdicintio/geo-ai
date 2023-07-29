import logging

import openai


logger = logging.Logger(__name__)

def generate_prompt(animal: str):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(animal.capitalize())


def generate_model_completion_response(animal: str):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=generate_prompt(animal),
    temperature=0.6
    )
    return response


def generate_model_chat_completion_response():
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a terse barista."},
            {"role": "user", "content": "What the best coffee you've got?"},
            {"role": "assistant", "content": "I dunno, maybe the latte. Beats me."},
            {"role": "user", "content": "What do you normally get?"}
        ]
    )
    return response