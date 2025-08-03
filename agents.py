from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(os.getenv("GROQ_API_KEY"))

def country_extractor(user_query):
    prompt = f"The user query is :- {user_query}.\n If the place to visit is a city then return as 'I got city'."
    completion = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
        {
            "role": "system",
            "content": "You are a Country or a State extractor. You will get a prompt to plan a trip somewhere. You have to return only the country or state in which user wants to go. If the user wants to go to a city than return 'I got city' in your answer. If you get state or country then return the state or country in your answer. Only return the name of the state or country in your response and nothing else."
        },
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response

def cities_decider(user_query, cities_list):
    prompt = f"The user wants: {user_query}\nHere is a cities data where I am providing city name with its alternate name and a little about the city if available:\n"
    for i, city in enumerate(cities_list):
        prompt+= f"{i+1}. {city['name']} ({city['alt_name']}) :- {city['description']}\n"
    prompt += """Your response should be all the cities with their description as provided priority wise. Dont give anything else. Include all the cities provided in the prompt but priority wise."""
    completion = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
        {
            "role": "system",
            "content": "You are a trip planner city recommender. You will be given a list of cities or a single city and a user prompt. You have to recommend the user for which cities to visit. You have to do this task by analysing the user input and see which cities aligns with the user's interest and then prepare a priority wise order list."
        },
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response.strip('\n').split('\n')