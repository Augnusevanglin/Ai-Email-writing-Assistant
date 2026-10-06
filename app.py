import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time

# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="AI Email Writing Assistant",
    page_icon="✉️",
    layout="centered"
)

st.title("✉️ AI Email Writing Assistant")
st.write("Generate professional emails easily using Artificial Intelligence.")
st.divider()

# --------------------------------------------------
# CHECK API KEY
# --------------------------------------------------

if not API_KEY:
    st.error("GEMINI_API_KEY is missing in the .env file.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# EMAIL INPUT SECTION
# --------------------------------------------------

st.subheader("📧 Email Details")

col1, col2 = st.columns(2)

with col1:
    sender = st.text_input(
        "Who is writing?",
        placeholder="Example: Student"
    )

with col2:
    receiver = st.text_input(
        "Who is receiving?",
        placeholder="Example: Professor"
    )

subject = st.text_input(
    "Email Subject / Purpose",
    placeholder="Example: Request for leave"
)

content = st.text_area(
    "What do you want to say?",
    placeholder="Enter the details you want to include in the email...",
    height=150
)

# --------------------------------------------------
# TONE AND LENGTH
# --------------------------------------------------

col3, col4 = st.columns(2)

with col3:
    tone = st.selectbox(
        "Choose Email Tone",
        [
            "Professional",
            "Formal",
            "Polite",
            "Friendly",
            "Apologetic"
        ]
    )

with col4:
    length = st.selectbox(
        "Choose Email Length",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )

st.divider()

# --------------------------------------------------
# GENERATE EMAIL
# --------------------------------------------------

if st.button("✨ Generate Email", use_container_width=True):

    # Check required fields
    if not sender or not receiver or not content:

        st.warning(
            "Please fill in Who is writing, Who is receiving, "
            "and What do you want to say."
        )

    else:

        # --------------------------------------------------
        # AI PROMPT
        # --------------------------------------------------

        prompt = f"""
You are an AI Email Writing Assistant.

Write a high-quality email using the following information:

Sender: {sender}
Receiver: {receiver}
Purpose/Subject: {subject}
Details: {content}
Tone: {tone}
Length: {length}

Requirements:
1. Create a suitable email subject.
2. Use an appropriate greeting.
3. Write a clear and grammatically correct email.
4. Keep the tone {tone}.
5. Keep the email {length}.
6. Include a professional closing.
7. Do not add explanations outside the email.
8. Make the email sound natural and human-written.

Return the complete email.
"""

        # --------------------------------------------------
        # CALL GEMINI AI
        # --------------------------------------------------

        try:

            with st.spinner("🤖 AI is writing your email..."):

                response = None

                # Try 3 times if Gemini is temporarily busy
                for attempt in range(3):

                    try:

                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt
                        )

                        break

                    except Exception as e:

                        error_message = str(e)

                        if "503" in error_message and attempt < 2:

                            time.sleep(8)

                        else:

                            response = None
                            break

            # --------------------------------------------------
            # IF GEMINI SUCCESSFULLY GENERATES EMAIL
            # --------------------------------------------------

            if response is not None:

                email = response.text

                st.success("Email generated successfully! 🎉")

                st.subheader("📨 Generated Email")

                st.text_area(
                    "Your AI-generated email:",
                    value=email,
                    height=350
                )

                st.download_button(
                    label="⬇️ Download Email",
                    data=email,
                    file_name="generated_email.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            # --------------------------------------------------
            # FALLBACK EMAIL IF GEMINI IS BUSY
            # --------------------------------------------------

            else:

                demo_email = f"""Subject: {subject if subject else "Regarding Your Request"}

Dear {receiver},

I am writing to you regarding {subject if subject else "the matter mentioned"}.

{content}

I would appreciate your consideration. Please let me know if any further information is required.

Regards,
{sender}
"""

                st.warning(
                    "⚠️ Gemini AI is temporarily busy. "
                    "Showing a demo email for presentation."
                )

                st.subheader("📨 Demo Email")

                st.text_area(
                    "Sample email:",
                    value=demo_email,
                    height=350
                )

                st.download_button(
                    label="⬇️ Download Email",
                    data=demo_email,
                    file_name="demo_email.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        # --------------------------------------------------
        # OTHER ERRORS
        # --------------------------------------------------

        except Exception as e:

            st.error(
                "Unable to generate the email right now. "
                "Please try again."
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Email Writing Assistant | Built with Python, Streamlit and Gemini AI"
)
