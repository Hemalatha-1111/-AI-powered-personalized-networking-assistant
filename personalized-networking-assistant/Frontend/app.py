import streamlit as st
import requests

# FASTAPI_URL = "http://localhost:8000"
BACKEND_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="Personalized Networking Assistant", layout="wide", page_icon="🤝")
st.title("🤝 Personalized AI Networking Assistant")

tab1, tab2, tab3 = st.tabs(["💡 Generate Starters", "🔍 Fact Verification", "⏳ Strategy History"])

# Tab 1: Generating Smart Starters
with tab1:
    st.header("Generate Tailored Conversation Starters")
    event_desc = st.text_area("Enter Event Description:", placeholder="e.g., AI for Sustainable Cities tech summit...")
    user_interests = st.text_input("Enter Your Specific Interests:", placeholder="e.g., climate change, urban planning")
    if st.button("🚀 Generate Starters", use_container_width=True):
        if not event_desc or not user_interests:
            st.error("Fill both fields!")
        else:
            with st.spinner("Analyzing..."):
                try:
#                     # Call Orchestration API
                    res = requests.post(f"{BACKEND_URL}/generate", json={
                        "description": event_desc, "interests": user_interests
                    })
                    res.raise_for_status()
                    data = res.json()
                    st.success(f"*Identified Theme:* {data['theme']}")
                    st.subheader("💬 Output Display")
                    for i, prompt in enumerate(data['prompts']):
                        st.info(f"*Option {i+1}:* {prompt}")
            
                    if st.button(f"👍 Save ({i+1})", key=f"up_{i}"):
                        requests.post(f"{BACKEND_URL}/feedback", json={"prompt": prompt, "feedback": "Liked"})
                        st.toast("Saved!")
                except Exception as e:
                    st.error(f"Backend offline: {e}")
                
       

# Tab 2: Quick Fact Verification
with tab2: 
    st.subheader("🔍 Real-Time Fact Verification Engine")
    search_topic = st.text_input("Enter a concept or topic to query (e.g., 'blockchain in healthcare'):")
    if st.button("Query Wikipedia"):
        res = requests.get(f"{BACKEND_URL}/verify", params={"topic": search_topic}).json()
        if res.get("verified"):
            st.success("✅ Verified")
            st.write(res.get("summary"))
            st.caption(f"[Read more]({res.get('url')})")
        else:
            st.warning(res.get("summary"))

# Tab 3: History & Analysis
with tab3:
    st.subheader("Previous Strategy Assessment Logs")
    if st.button("Refresh Historical Records",type = "primary"):
        try:
            res = requests.get(f"{BACKEND_URL}/history",timeout = 10)
            history = res.json()
            if history:
                for entry in reversed(history):
                    timestamp = entry.get('timestamp','No date')
                    description = entry.get('description','N/A')

                    interests = entry.get('interests','N/A')
                    # theme = entry.get('theme',[entry.get('theme','N/A')])
                    theme = entry.get('theme','N/A')
                    prompts = entry.get('prompts',entry.get('starters',[]))
                    
                    with st.expander(f"Session Log - {timestamp}"): #[:16]
                        st.write(f"**Event Context:** {description}")
                        st.write(f"**Interests:** {interests}")
                        st.write(f"**Extracted Categories:** {theme}")      #', '.join('themes')}")
                        st.write("**Generated Options:**")
                        for p in prompts:
                            st.write(f"- {p}")
            else:
                st.info("No history found yet")
        except Exception as e:
            st.error("failed to fetch history:{e}")