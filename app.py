import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="LLM API Response",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 LLM API Response Generator")
st.write("Simple Streamlit app for getting LLM responses using Perplexity API")

# Sidebar for API key input
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Enter Perplexity API Key",
        type="password",
        value=os.getenv("PERPLEXITY_API_KEY", "")
    )
    st.write("[Get API Key](https://www.perplexity.ai/settings/api)")

# Main input
user_query = st.text_area(
    "Enter your question or prompt:",
    placeholder="Ask me anything...",
    height=100
)

# Model selection
model = st.selectbox(
    "Select Model",
    ["sonar", "sonar-pro"],
    help="Choose the Perplexity model to use"
)

# Submit button
if st.button("Get Response", use_container_width=True):
    if not api_key:
        st.error("Please provide an API key")
    elif not user_query:
        st.error("Please enter a question or prompt")
    else:
        with st.spinner("Getting response..."):
            try:
                # Call Perplexity API
                url = "https://api.perplexity.ai/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "user", "content": user_query}
                    ]
                }
                
                response = requests.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data["choices"][0]["message"]["content"]
                    
                    st.success("Response received!")
                    st.markdown("### Response:")
                    st.write(assistant_message)
                    
                    # Show usage stats
                    if "usage" in data:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Input Tokens", data["usage"].get("prompt_tokens", 0))
                        with col2:
                            st.metric("Output Tokens", data["usage"].get("completion_tokens", 0))
                        with col3:
                            st.metric("Total Tokens", data["usage"].get("total_tokens", 0))
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.divider()
st.markdown(
    """
    <p style='text-align: center; color: gray;'>
    Made with ❤️ using Streamlit and Perplexity API
    </p>
    """,
    unsafe_allow_html=True
)
