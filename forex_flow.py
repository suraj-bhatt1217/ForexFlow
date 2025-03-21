import streamlit as st

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
            st.write(user_input)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter some text in the input field.")

st.markdown(
    '<div class="footer">© 2025 ForexFlow | Exchange Without Borders, Convert Without Limits</div>',
    unsafe_allow_html=True,
)
