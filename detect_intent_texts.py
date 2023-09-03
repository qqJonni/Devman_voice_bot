from google.cloud import dialogflow


async def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the intent detection result with text input.
    Using the same `session_id` between requests allows continuation of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
    request={"session": session, "query_input": query_input})
