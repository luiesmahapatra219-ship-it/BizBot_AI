
import streamlit as st
import csv
import os
from datetime import datetime

st.set_page_config(
    page_title="BizBot AI",
    page_icon="🤖"
)

# Demo business information
BUSINESS_NAME = "BizBot Store"
BUSINESS_HOURS = "Monday to Saturday, 9 AM to 6 PM"
BUSINESS_EMAIL = "support@example.com"

PRODUCTS = {
    "laptop": 45000,
    "headphones": 1500,
    "keyboard": 800
}

# Chatbot logic
def get_response(message):
    message = message.lower().strip()

    if any(word in message for word in ["hello", "hi", "hey"]):
        return "Hello! Welcome to BizBot AI. How can I help you?"

    elif "hour" in message or "timing" in message:
        return f"Our business hours are {BUSINESS_HOURS}."

    elif "contact" in message or "email" in message:
        return f"Contact us at {BUSINESS_EMAIL}."

    elif "product" in message or "catalog" in message:
        return "We sell laptops, headphones and keyboards."

    elif "price" in message or "cost" in message:
        return "\n".join(
            f"{name.title()}: Rs. {price:,}"
            for name, price in PRODUCTS.items()
        )

    elif "laptop" in message:
        return f"Our laptop costs Rs. {PRODUCTS['laptop']:,}."

    elif "headphone" in message:
        return f"Headphones cost Rs. {PRODUCTS['headphones']:,}."

    elif "keyboard" in message:
        return f"Our keyboard costs Rs. {PRODUCTS['keyboard']:,}."

    elif "refund" in message or "return" in message:
        return "Please contact our support team about returns."

    elif "thank" in message:
        return "You're welcome! Is there anything else I can help with?"

    else:
        return (
            "Sorry, I don't know that answer yet. "
            "Try asking about products, prices, timings or contact details."
        )

# Page design
st.title("🤖 BizBot AI")
st.subheader("Smart Business Assistant")
st.write("Ask questions about our products and services.")

st.sidebar.title("Business Details")
st.sidebar.write(BUSINESS_NAME)
st.sidebar.write(BUSINESS_HOURS)
st.sidebar.write(BUSINESS_EMAIL)

# Keep the conversation on the page
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! How can I help you today?"
        }
    ]

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Type your question...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    answer = get_response(prompt)

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# Customer enquiry form
st.divider()
st.subheader("📩 Contact Our Business")

with st.form("enquiry_form"):
    name = st.text_input("Your name")
    contact = st.text_input("Your email or phone")
    enquiry = st.text_area("Your question")
    consent = st.checkbox("I agree to submit my enquiry")

    submitted = st.form_submit_button("Submit Enquiry")

    if submitted:
        if not name.strip() or not contact.strip() or not enquiry.strip():
            st.error("Please fill in all fields.")
        elif not consent:
            st.warning("Please give consent before submitting.")
        else:
            file_exists = os.path.exists("enquiries.csv")

            with open(
                "enquiries.csv",
                "a",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow([
                        "Date", "Name", "Contact", "Enquiry"
                    ])

                writer.writerow([
                    datetime.now().isoformat(timespec="seconds"),
                    name.strip(),
                    contact.strip(),
                    enquiry.strip()
                ])

            st.success("Your enquiry was saved successfully!")
            st.info("This demo saves enquiries locally; it does not send emails.")
