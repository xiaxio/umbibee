# Simple Streamlit UI for AI Web Scraper.

"""
Security note:
- Do NOT hardcode credentials in source. Use environment variables or
  Streamlit's secrets management. If credentials were previously
  committed, rotate them immediately (change passwords/tokens) and
  purge them from git history (see repo admin notes).
"""

import os
import credentials
import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
    login_to_sso,
)
from parse import parse_with_ollama


st.title("AI Web Scraper")

# Input URL
url = st.text_input("Enter the URL to scrape:")

if st.button("Scrape Site"):
    st.write("Scraping Page Source:", url)
    page_source = scrape_website(url)
    body_content = extract_body_content(page_source)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)


st.markdown("---")
st.write("Scrape SSO (use env vars or enter credentials interactively)")

# Prefer environment variables or Streamlit secrets for credentials.
# Environment variables: SSO_USER and SSO_PASS
# Alternatively, set these in Streamlit `secrets.toml` and access via st.secrets
env_user = os.getenv("SSO_USER")
env_pass = os.getenv("SSO_PASS")

# Inline inputs are available but are not stored in source control.
interactive_user = st.text_input("SSO username (leave blank to use SSO_USER env)")
interactive_pass = st.text_input("SSO password (leave blank to use SSO_PASS env)", type="password")

# Choose credentials: prefer env, then interactive inputs.
username = env_user if env_user else (interactive_user or "")
password = env_pass if env_pass else (interactive_pass or "")

if st.button("Scrape SSO"):
    if not url:
        st.warning("Please enter a URL first.")
    else:
        if not username or not password:
            st.warning(
                "No SSO credentials supplied. Set SSO_USER/SSO_PASS environment variables or enter them above."
            )
        else:
            # Do not log or display credentials
            st.write("Scraping SSO-protected page...")
            # Use credentials from credentials.py for testing/development only
            page_source = login_to_sso(url, credentials.username, credentials.password)
            body_content = extract_body_content(page_source)
            cleaned_content = clean_body_content(body_content)

            st.session_state.dom_content = cleaned_content

            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_description = st.text_area("Enter parsing description:", height=100)

    if st.button("Parse DOM Content"):
        if parse_description:
            st.write("Parsing DOM Content with description")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_output = parse_with_ollama(dom_chunks, parse_description)
            st.write("Parsed Output:", parsed_output)
