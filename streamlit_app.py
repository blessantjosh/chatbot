import json
from datetime import datetime

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="TNPSC Prep Copilot", page_icon="📚", layout="wide")

st.title("📚 TNPSC Prep Copilot (Tamil + English)")
st.caption(
    "A single application concept for TNPSC preparation with multilingual support, "
    "study resources, syllabus tracking, and question-paper-oriented guidance."
)

with st.expander("⚠️ Important note before building", expanded=True):
    st.write(
        "A perfect *zero-error* LLM is not possible in practice. A strong and reliable TNPSC system is built "
        "with a combination of quality data curation, retrieval, evaluation, safety checks, and continuous updates."
    )

st.subheader("1) Data and exam setup")
col1, col2 = st.columns(2)

with col1:
    preferred_language = st.multiselect(
        "Primary output language",
        options=["Tamil", "English", "Tamil + English"],
        default=["Tamil + English"],
    )
    tnpsc_group = st.selectbox(
        "TNPSC exam track",
        [
            "Group 1",
            "Group 2",
            "Group 2A",
            "Group 4",
            "VAO",
            "Combined preparation",
        ],
    )
    exam_stage = st.selectbox(
        "Stage",
        ["Prelims", "Mains", "Interview", "All stages"],
        index=3,
    )

with col2:
    syllabus_topics = st.text_area(
        "Syllabus topics (comma separated)",
        placeholder="History, Polity, Economy, Geography, Aptitude, Science, Current Affairs...",
        height=100,
    )
    learning_goal = st.text_area(
        "Learning goal for this session",
        placeholder="Example: Create a 14-day mixed Tamil+English plan with daily mock tests.",
        height=100,
    )

st.subheader("2) Unified study resources")

uploaded_files = st.file_uploader(
    "Upload study materials (pdf, docs, txt, images, audio metadata, etc.)",
    type=None,
    accept_multiple_files=True,
)

youtube_links = st.text_area(
    "YouTube links (one per line)",
    placeholder="https://www.youtube.com/watch?v=...",
    height=100,
)

external_notes = st.text_area(
    "Paste extracted notes/transcripts/content",
    placeholder="Paste textbook snippets, transcript text, or key points here so the assistant can use them.",
    height=140,
)

resource_rows = []
for file in uploaded_files or []:
    resource_rows.append(
        {
            "name": file.name,
            "type": file.type or "unknown",
            "size_kb": round(file.size / 1024, 2),
        }
    )

for link in [line.strip() for line in youtube_links.splitlines() if line.strip()]:
    resource_rows.append({"name": link, "type": "youtube", "size_kb": "-"})

if resource_rows:
    st.dataframe(resource_rows, use_container_width=True)
else:
    st.info("Add files or links to build your TNPSC knowledge base context.")

st.subheader("3) Previous year papers and model tests")
qcol1, qcol2 = st.columns(2)
with qcol1:
    previous_year_focus = st.text_area(
        "Previous year question focus",
        placeholder="Mention years and sections to prioritize (e.g., Group 2A 2018-2023 GS + Aptitude).",
        height=100,
    )
with qcol2:
    mock_test_needs = st.text_area(
        "Model paper requirements",
        placeholder="Example: 50 MCQs, bilingual, medium difficulty, with explanations.",
        height=100,
    )

st.subheader("4) Ask the assistant")
openai_api_key = st.text_input("OpenAI API Key", type="password")
selected_model = st.selectbox(
    "LLM model",
    ["gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1"],
    index=0,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def build_system_prompt() -> str:
    resource_summary = json.dumps(resource_rows[:100], ensure_ascii=False, indent=2)
    prompt_parts = [
        "You are a TNPSC exam preparation assistant.",
        "Always support Tamil and English outputs where useful.",
        f"Exam track: {tnpsc_group}",
        f"Stage: {exam_stage}",
        f"Preferred language: {', '.join(preferred_language) if preferred_language else 'Tamil + English'}",
        f"Syllabus topics: {syllabus_topics or 'Not provided'}",
        f"User learning goal: {learning_goal or 'Not provided'}",
        f"Previous year focus: {previous_year_focus or 'Not provided'}",
        f"Model test needs: {mock_test_needs or 'Not provided'}",
        "Use the provided resources as context. If data is missing, clearly state assumptions.",
        "When asked for plans, include timeline, daily tasks, revision strategy, and mini tests.",
        "When asked for question papers, format in exam style and include answer key + explanation.",
        f"Resource inventory:\n{resource_summary}",
        f"Additional pasted notes:\n{external_notes or 'Not provided'}",
        "Never claim certainty when unsure; respond transparently.",
    ]
    return "\n".join(prompt_parts)


if not openai_api_key:
    st.info("Enter your OpenAI API key to start the TNPSC assistant.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)
    user_prompt = st.chat_input("Ask for notes, syllabus plans, bilingual explanations, or mock papers...")

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        chat_messages = [{"role": "system", "content": build_system_prompt()}]
        chat_messages.extend(
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        )

        with st.chat_message("assistant"):
            try:
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=chat_messages,
                    stream=True,
                )
                response = st.write_stream(stream)
            except Exception as error:
                response = (
                    "I could not generate a response right now. "
                    "Please verify your API key/model access and try again.\n\n"
                    f"Error: {error}"
                )
                st.error(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.caption(f"Last updated in app session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
