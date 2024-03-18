import os
import openai
from config import apikey

openai.api_key = apikey


response = openai.Completion.create(
    model = "text-davvinci-003",
    promt = "Write an email to my boss for resignation?",
    temperature = 0.7,
    max_tokens = 256,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0
)

print(response)
'''
{
    
}
'''