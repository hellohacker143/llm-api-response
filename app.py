import streamlit as st
import requests
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="LLM API Response & SEO Tool",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1f1f2e;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d9ff;
        margin: 10px 0;
    }
    .metric-title {
        color: #00d9ff;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: bold;
    }
    .seo-section {
        background-color: #262630;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .seo-heading h1 {
        color: #00d9ff;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .seo-heading h2 {
        color: #888;
        margin-top: 15px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 LLM API Response & SEO Content Generator")
st.write("Generate LLM responses and create SEO-optimized content with Perplexity API")

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Get API key
    def get_api_key():
        try:
            api_key = st.secrets.get("PERPLEXITY_API_KEY")
            if api_key:
                return api_key
        except:
            pass
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if api_key:
            return api_key
        return None
    
    stored_api_key = get_api_key()
    
    if stored_api_key:
        st.success("✅ API Key loaded from Streamlit Secrets!")
        show_api_input = st.checkbox("Override with manual API key?", value=False)
    else:
        show_api_input = True
    
    if show_api_input:
        api_key = st.text_input(
            "Enter Perplexity API Key",
            type="password",
            placeholder="pplx-...",
            help="Your API key will not be stored"
        )
    else:
        api_key = stored_api_key
    
    st.markdown("---")
    st.link_button(
        "🔑 Get API Key",
        "https://www.perplexity.ai/settings/api",
        use_container_width=True
    )

# Create tabs for different features
tab1, tab2 = st.tabs(["💬 LLM Response", "📝 SEO Content Generator"])

with tab1:
    st.markdown("### 💬 Ask Anything")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_query = st.text_area(
            "Your question:",
            placeholder="Ask me anything...",
            height=120,
            label_visibility="collapsed"
        )
    
    with col2:
        model = st.selectbox(
            "Model",
            ["sonar", "sonar-pro"],
            help="Choose LLM model"
        )
        max_tokens = st.slider(
            "Max Tokens",
            100, 4000, 1000, 100
        )
    
    if st.button("🚀 Get Response", use_container_width=True, type="primary"):
        if not api_key:
            st.error("❌ Please provide an API key")
            st.stop()
        
        if not user_query.strip():
            st.error("❌ Please enter a question")
            st.stop()
        
        with st.spinner("⏳ Getting response..."):
            try:
                url = "https://api.perplexity.ai/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model,
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": user_query}]
                }
                
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Get response content and remove citations
                    response_text = data["choices"][0]["message"]["content"]
                    # Remove citation markers like [2][3][6][8]
                    clean_response = re.sub(r'\[\d+\]', '', response_text)
                    
                    st.success("✅ Response received!")
                    
                    with st.expander("📤 Response", expanded=True):
                        st.markdown(clean_response)
                    
                    # Display metrics in cards
                    if "usage" in data:
                        st.markdown("### 📊 Token Usage")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">📥 Input Tokens</div>
                                <div class="metric-value">{data["usage"].get("prompt_tokens", 0)}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">📤 Output Tokens</div>
                                <div class="metric-value">{data["usage"].get("completion_tokens", 0)}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">📊 Total Tokens</div>
                                <div class="metric-value">{data["usage"].get("total_tokens", 0)}</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                elif response.status_code == 401:
                    st.error("❌ Invalid API key")
                elif response.status_code == 429:
                    st.error("⏱️ Rate limited. Try again later.")
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            
            except requests.exceptions.Timeout:
                st.error("❌ Request timeout")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.markdown("### 📝 SEO Content Generator")
    st.info("💡 Generate 1200+ words SEO-optimized content with H1, H2 headings")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        seo_keyword = st.text_input(
            "Enter SEO keyword:",
            placeholder="e.g., 'Best Python Tutorials'"
        )
    
    with col2:
        content_type = st.selectbox(
            "Content Type",
            ["Blog Post", "Product Review", "How-To Guide", "News Article"]
        )
    
    if st.button("✍️ Generate SEO Content", use_container_width=True, type="primary"):
        if not api_key:
            st.error("❌ Please provide an API key")
            st.stop()
        
        if not seo_keyword.strip():
            st.error("❌ Please enter a keyword")
            st.stop()
        
        with st.spinner("✍️ Generating SEO content (1200+ words)..."):
            try:
                # Create detailed SEO prompt
                seo_prompt = f"""
Create a comprehensive {content_type.lower()} about '{seo_keyword}' with the following structure:

1. Start with an H1 heading that includes the keyword naturally
2. Write an engaging introduction (100-150 words)
3. Create at least 4 H2 sections with relevant content (250-300 words each)
4. Each H2 section should have 2-3 paragraphs
5. Include practical examples and tips
6. End with a conclusion (100-150 words)
7. Total word count should be 1200+ words

Format the content with proper markdown headings (# for H1, ## for H2)
Make it SEO-friendly and engaging for readers.

Keyword: {seo_keyword}
Content Type: {content_type}
"""
                
                url = "https://api.perplexity.ai/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "sonar-pro",
                    "max_tokens": 3000,
                    "messages": [{"role": "user", "content": seo_prompt}]
                }
                
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    seo_content = data["choices"][0]["message"]["content"]
                    # Remove citation markers
                    clean_content = re.sub(r'\[\d+\]', '', seo_content)
                    
                    st.success("✅ SEO content generated!")
                    
                    # Display content
                    st.markdown("---")
                    st.markdown(clean_content)
                    
                    # Display metrics
                    st.markdown("---")
                    st.markdown("### 📊 Generation Stats")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">📥 Input Tokens</div>
                            <div class="metric-value">{data["usage"].get("prompt_tokens", 0)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">📤 Output Tokens</div>
                            <div class="metric-value">{data["usage"].get("completion_tokens", 0)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        word_count = len(clean_content.split())
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">📝 Word Count</div>
                            <div class="metric-value">{word_count}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download as Text",
                        data=clean_content,
                        file_name=f"seo-content-{seo_keyword.replace(' ', '-').lower()}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                elif response.status_code == 401:
                    st.error("❌ Invalid API key")
                else:
                    st.error(f"❌ Error {response.status_code}")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    Made with ❤️ using Streamlit and Perplexity API | SEO Content Generator v2.0
    </div>
    """,
    unsafe_allow_html=True
)
