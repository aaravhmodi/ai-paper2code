import streamlit as st
import requests

st.title("🧬 AI Paper-to-Code Generator")
query = st.text_input("Ask about a model (e.g. 'Implement CLIP training loop'): ")

if st.button("Generate Code"):
    if not query:
        st.error("Please enter a query before generating code.")
    else:
        try:
            # set a timeout so the UI doesn't hang forever
            res = requests.post("http://localhost:8000/generate", json={"query": query}, timeout=30)
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        else:
            # If response isn't 2xx, show status and body for debugging
            if not res.ok:
                st.error(f"Server returned status {res.status_code}")
                st.text("Response body:\n" + (res.text or "<empty>"))
            else:
                # Try to parse JSON, but handle non-JSON gracefully
                try:
                    data = res.json()
                except ValueError:
                    st.error("Server returned non-JSON response")
                    st.text("Response body:\n" + (res.text or "<empty>"))
                else:
                    # Safely extract result key
                    code = data.get("result") if isinstance(data, dict) else None
                    if not code:
                        st.error("Response JSON did not contain a 'result' field")
                        st.write(data)
                    else:
                        st.code(code, language="python")
