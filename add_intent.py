import os
import json
from google.cloud import dialogflow
import argparse
from dotenv import load_dotenv, find_dotenv


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Создание Inent для dialogflow"""
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    training_answer = []
    part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_parts)
    training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
    training_phrases.append(training_phrase)
    training_answer.append(message_texts)
    text = dialogflow.Intent.Message.Text(text=training_answer)
    training_answer.pop(0)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    return response


def main():
    with open(f'{namespace}', "r") as file:
        intent_json = file.read()
    intent_data = json.loads(intent_json)

    for title, intent in intent_data.items():
        create_intent(os.environ.get('PROJECT_ID'), title, intent["questions"], intent["answer"])


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('intent_name', default='intent.json', nargs='?')

    return parser


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    parser = createParser()
    namespace = parser.parse_args()
    main()
