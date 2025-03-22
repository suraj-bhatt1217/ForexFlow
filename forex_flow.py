import streamlit as st
import os
import json
import requests

from openai import OpenAI
from dotenv import load_dotenv
from typing import Tuple, Dict

model_name = "gpt-3.5-turbo"

load_dotenv()

EXCHANGERATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

# Streamlit App Title, Header, and Styling
st.set_page_config(page_title="ForexFlow", page_icon="💱", layout="centered")

st.markdown(
    """
    <style>
        .main-header { font-size: 3.5rem; font-weight: bold; color: #004085; text-align: center; margin-bottom: 1rem; padding-top: 2rem; text-shadow: 2px 2px #cce5ff; }
        .tagline { font-size: 1.4rem; color: #555; text-align: center; font-style: italic; margin-bottom: 2rem; text-shadow: 1px 1px #d4d4d4; }
        .input-section { background-color: #f8f9fa; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto; }
        .footer { text-align: center; margin-top: 2rem; font-size: 0.8rem; color: #666; }
        .stButton > button { display: block; margin: 0 auto; width: 50%; padding: 0.8rem 0; font-size: 1rem; font-weight: bold; background-color: #007bff; border: none; border-radius: 10px; color: white; cursor: pointer; transition: background-color 0.3s ease; }
        .stButton > button:hover { background-color: #0056b3; }
        
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">ForexFlow</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tagline">Real-Time Rates, Effortless Conversions</div>',
    unsafe_allow_html=True,
)

# User Input for OpenAI API Key
api_key = st.text_input("Enter your OpenAI API Key", type="password")
if api_key:
    client = OpenAI(api_key=api_key)
    st.success("API Key saved successfully! You can now make API calls.")
else:
    st.warning("Please enter your OpenAI API key to proceed.")


# Function for Exchange Rate API Call
def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    response = requests.get(url).json()
    return (base, target, amount, f'{response["conversion_result"]:.2f}')


# Function for LLM (ChatGPT) Call
def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt."""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "exchange_rate_function",
                "description": "Convert a given amount of money from one currency to another. Each currency will be represented as a 3-letter code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "base": {"type": "string", "description": "The base currency."},
                        "target": {
                            "type": "string",
                            "description": "The target currency",
                        },
                        "amount": {
                            "type": "string",
                            "description": "Amount of money to convert.",
                        },
                    },
                    "required": ["base", "target", "amount"],
                    "additionalProperties": False,
                },
            },
        }
    ]

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": textbox_input},
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=100,
            model=model_name,
            tools=tools,
        )
    except Exception as e:
        st.error(f"API call failed: {e}")
    else:
        return response


# Run Pipeline Based on User Input
def run_pipeline(user_input):
    response = call_llm(user_input)
    if response and response.choices[0].finish_reason == "tool_calls":
        response_arguments = json.loads(
            response.choices[0].message.tool_calls[0].function.arguments
        )
        base = response_arguments["base"]
        target = response_arguments["target"]
        amount = response_arguments["amount"]
        _, _, _, conversion_result = get_exchange_rate(base, target, amount)
        st.write(f"{base} {amount} is {target} {conversion_result}")

    elif response and response.choices[0].finish_reason == "stop":
        st.write(f"(Function calling not used) {response.choices[0].message.content}")
    else:
        st.warning("No valid response from the model.")


# User Input Field for Conversion Query
user_input = st.text_input(
    "Enter your query or amount to convert:",
    placeholder="Example: Convert 100 USD to EUR",
)
if st.button("Submit"):
    if user_input and api_key:
        run_pipeline(user_input)
    elif not api_key:
        st.warning("Please enter your OpenAI API key.")
    else:
        st.warning("Please enter some text in the input field.")

# Footer
st.markdown(
    '<div class="footer">© 2025 ForexFlow | Exchange Without Borders, Convert Without Limits</div>',
    unsafe_allow_html=True,
)
