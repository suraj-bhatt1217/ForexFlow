import streamlit as st
import os
import json
import requests

from openai import OpenAI
from dotenv import load_dotenv
from typing import Tuple, Dict


model_name = "gpt-3.5-turbo"

load_dotenv()

OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

EXCHANGERATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    response = json.loads(requests.get(url).text)
    return (base, target, amount, f'{response["conversion_result"]:.2f}')


def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
    The output from the LLM should be a JSON (dfrom dotenv import load_dotenv
    import dotenvict) with the base, amount and target
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": textbox_input,
                },
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=100,
            model=model_name,
        )

    except Exception as e:
        print(f"Exception {e} for {text}")
    else:
        return response.choices[0].message.content


def run_pipeline():
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    if True:  # tool_calls
        # Update this
        st.write(
            f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}'
        )

    elif True:  # tools not used
        # Update this
        st.write(f"(Function calling not used) and response from the model")
    else:
        st.write("NotImplemented")


st.set_page_config(
    page_title="ForexFlow",
    page_icon="💱",
    layout="centered",
)

st.markdown(
    """
    <style>
        .main-header {
            font-size: 3.5rem;
            font-weight: bold;
            color: #004085;
            text-align: center;
            margin-bottom: 1rem;
            padding-top: 2rem;
            text-shadow: 2px 2px #cce5ff;
        }
        .tagline {
            font-size: 1.4rem;
            color: #555;
            text-align: center;
            font-style: italic;
            margin-bottom: 2rem;
            text-shadow: 1px 1px #d4d4d4;
        }
        .input-section {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .output-section {
            background-color: #e6f2ff;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin-top: 1rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.8rem;
            color: #666;
        }
        .stButton > button {
            display: block;
            margin: 0 auto;
            width: 50%;
            padding: 0.8rem 0;
            font-size: 1rem;
            font-weight: bold;
            background-color: #007bff;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">ForexFlow</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tagline">Real-Time Rates, Effortless Conversions</div>',
    unsafe_allow_html=True,
)

with st.container():
    user_input = st.text_input(
        "Enter your query or amount to convert:",
        placeholder="Example: Convert 100 USD to EUR",
    )
    submit_button = st.button("Submit")
    st.markdown("</div>", unsafe_allow_html=True)

if submit_button:
    if user_input:
        with st.container():
            st.subheader("Your Input:")
            st.write(call_llm(user_input))
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter some text in the input field.")

st.markdown(
    '<div class="footer">© 2025 ForexFlow | Exchange Without Borders, Convert Without Limits</div>',
    unsafe_allow_html=True,
)
