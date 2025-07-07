import openai
from django.conf import settings

# Set the OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def generate_insight_from_context(content):
    """
    Generates concise insights or task reminders based on a given context message.
    Returns a bullet-point list if multiple suggestions exist.
    """
    prompt = (
        "Analyze the following context and provide important task insights or reminders:\n\n"
        f"{content}\n\n"
        "Respond briefly. Use bullet points if there are multiple suggestions."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a productivity assistant that helps users identify key tasks and reminders based on context."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.5,
        )
        return response.choices[0].message['content'].strip()

    except Exception as e:
        return f"AI Insight Error: {str(e)}"


def suggest_task(context):
    """
    Generates a single actionable task suggestion based on the provided context.
    The response is a short, one-line task recommendation.
    """
    prompt = (
        "Based on the following schedule or context, suggest ONE specific task the user should do next:\n\n"
        f"{context}\n\n"
        "Respond with only one concise and actionable line."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a task suggestion assistant that recommends one actionable next step for the user."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()

    except Exception as e:
        return f"AI Task Suggestion Error: {str(e)}"
