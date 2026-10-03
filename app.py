import hashlib
import json
from pathlib import Path

import streamlit as st

from agent import AIAgent
from tools import search_products

st.set_page_config(page_title="Agentic AI Assistant", page_icon="🤖", layout="wide")

APP_DIR = Path(__file__).resolve().parent
USER_DB_PATH = APP_DIR / "users.json"


@st.cache_resource
def get_agent():
    return AIAgent()


def load_users():
    if not USER_DB_PATH.exists():
        return {}
    try:
        data = json.loads(USER_DB_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def save_users(users):
    USER_DB_PATH.write_text(json.dumps(users, indent=2), encoding="utf-8")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(full_name, username, email, password):
    users = load_users()
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."
    if username in users:
        return False, "That username is already registered."
    users[username] = {
        "full_name": full_name.strip(),
        "email": email.strip(),
        "password": hash_password(password),
    }
    save_users(users)
    return True, "Registration successful. Please sign in."


def authenticate_user(username, password):
    users = load_users()
    user = users.get(username.strip())
    if not user:
        return None
    if user.get("password") == hash_password(password):
        return user
    return None


agent = get_agent()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "default_budget" not in st.session_state:
    st.session_state.default_budget = 800
if "preferred_focus" not in st.session_state:
    st.session_state.preferred_focus = "Balanced"
if "selected_laptop" not in st.session_state:
    st.session_state.selected_laptop = None
if "checkout_order" not in st.session_state:
    st.session_state.checkout_order = None
if "profile" not in st.session_state:
    st.session_state.profile = "Student"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Chat"


st.markdown(
    """
    <style>
    .main { background: #07111f; }
    .block-container { padding-top: 2rem; }
    .small-muted { color: #9fb0c7; }
    .card { padding: 1rem; border-radius: 12px; border: 1px solid #24364d; margin-bottom: .8rem; }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c1728 0%, #111d2d 100%);
    }
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.25);
        background: rgba(15, 23, 42, 0.75);
        color: #e2e8f0;
        font-weight: 600;
        padding: 0.7rem 0.8rem;
        margin: 0.18rem 0;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        border-color: rgba(96, 165, 250, 0.7);
        background: rgba(30, 41, 59, 0.9);
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border-color: rgba(96, 165, 250, 0.8);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.18);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if not st.session_state.authenticated:
    st.title("🤖 Agentic AI Assistant")
    st.caption("Create an account or sign in to access your AI assistant.")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Login")

        if login_submit:
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = {"username": username.strip(), **user}
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab_register:
        with st.form("register_form"):
            full_name = st.text_input("Full name")
            username = st.text_input("Create username")
            email = st.text_input("Email")
            password = st.text_input("Create password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            register_submit = st.form_submit_button("Create account")

        if register_submit:
            if not full_name or not username or not email or not password:
                st.error("Please complete all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(full_name, username, email, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

    st.stop()


with st.sidebar:
    st.title("🤖 Agentic AI Assistant")
    st.caption(f"Welcome, {st.session_state.current_user.get('full_name', st.session_state.current_user.get('username', 'User'))}")
    st.divider()

    nav_items = [
        ("💬 Chat", "Chat"),
        ("� Checkout", "Checkout"),
        ("�🕘 History", "History"),
        ("⚙️ Settings", "Settings"),
        ("ℹ️ About", "About"),
    ]

    for label, page_name in nav_items:
        if st.button(label, key=f"nav_{page_name}", use_container_width=True, type="primary" if st.session_state.current_page == page_name else "secondary"):
            st.session_state.current_page = page_name
            st.rerun()

    st.divider()

    if st.button("🚪 Sign out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.messages = []
        st.session_state.current_page = "Chat"
        st.rerun()

    st.divider()
    st.success("Agent Online")
    st.caption("Using ML + Tools + Data Analysis")


page = st.session_state.current_page

if page == "Chat":
    st.title("Chat with Your AI Agent")
    st.caption("Ask questions, request analysis, or get help with real-world tasks.")

    st.subheader("Quick prompts")
    quick_prompts = [
        "Best laptop under £800 for a computer science student",
        "Portable laptop with long battery life under £900",
        "Laptop for programming and multitasking",
        "Preferable value laptop for university",
        "Superior Business Laptop for video conferecing and office work or remote work",
        "Recommended Laptop for day to day use and general purpose",
    ]
    cols = st.columns(len(quick_prompts))
    for col, prompt in zip(cols, quick_prompts):
        if col.button(prompt[:28] + "..." if len(prompt) > 28 else prompt, key=f"quick_{prompt[:10]}"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            result = agent.process(prompt)
            st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
            st.session_state.history.append({"prompt": prompt, "response": result["answer"], "intent": result["intent"], "confidence": round(result["confidence"], 2)})
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask me anything...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        result = agent.process(prompt)

        with st.chat_message("assistant"):
            st.markdown(result["answer"])

            with st.expander("🔎 Show agent reasoning / workflow"):
                for i, step in enumerate(result["steps"], 1):
                    st.markdown(f"**{i}. {step['title']}**")
                    st.write(step["detail"])

            with st.expander("🛠️ Tools used"):
                for tool in result["tools"]:
                    st.write(f"✅ {tool}")

        st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
        st.session_state.history.append(
            {
                "prompt": prompt,
                "response": result["answer"],
                "intent": result["intent"],
                "confidence": round(result["confidence"], 2),
            }
        )

    st.divider()
    st.subheader("Smart laptop finder")
    profile = st.session_state.profile

    with st.form("laptop_preferences"):
        col_a, col_b = st.columns(2)
        with col_a:
            budget = st.slider("Budget", min_value=400, max_value=1500, value=st.session_state.default_budget, step=50)
        with col_b:
            profile = st.selectbox("User profile", ["Student", "Developer", "Business", "General use"], index=["Student", "Developer", "Business", "General use"].index(profile))
        preference = st.selectbox("Priority", ["Balanced", "Performance", "Battery", "Value", "Portability"], index=["Balanced", "Performance", "Battery", "Value", "Portability"].index(st.session_state.preferred_focus))
        submitted = st.form_submit_button("Find my best match")

    if submitted:
        st.session_state.default_budget = budget
        st.session_state.profile = profile
        st.session_state.preferred_focus = preference
        query = f"Best {profile.lower()} laptop for {preference.lower()} use under £{budget}"
        result = agent.process(query)
        st.markdown(result["answer"])

    st.divider()
    st.subheader("Browse laptop options")

    budget_for_cards = st.session_state.default_budget
    focus = st.session_state.preferred_focus

    filtered = search_products(f"under £{budget_for_cards}")
    matching = filtered[:6]

    if not matching:
        st.info("No matches found in this budget range. Try increasing the budget.")
    else:
        for product in matching:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {product['name']}")
                    st.write(f"**Price:** £{product['price']}")
                    st.write(f"**CPU:** {product['cpu']}")
                    st.write(f"**RAM:** {product['ram']} | **Storage:** {product['storage']}")
                    st.write(f"**Display:** {product['display']} | **Battery:** {product['battery']}")
                    st.write(f"**Why it stands out:** {product['pros']}")
                    st.write(f"**Trade-off:** {product['cons']}")
                with col2:
                    st.metric("Profile", profile)
                    if st.button("Buy now", key=f"select_{product['name']}"):
                        st.session_state.selected_laptop = product
                        st.session_state.checkout_order = None
                        st.session_state.current_page = "Checkout"
                        st.session_state.messages.append({"role": "assistant", "content": f"Added to checkout: **{product['name']}** for a **{profile.lower()}** profile with a **{focus.lower()}** priority."})
                        st.toast(f"Added {product['name']} to checkout")
                        st.rerun()

            st.write("")

elif page == "Checkout":
    st.title("Checkout")

    if not st.session_state.selected_laptop:
        st.info("No laptop selected yet. Choose a device from the chat recommendations and then complete checkout here.")
        if st.button("Back to recommendations"):
            st.session_state.current_page = "Chat"
            st.rerun()
        st.stop()

    laptop = st.session_state.selected_laptop
    subtotal = float(laptop["price"])
    shipping = 0 if subtotal >= 900 else 25
    tax = round(subtotal * 0.2, 2)
    total = round(subtotal + shipping + tax, 2)

    st.subheader("Your selected laptop")
    with st.container(border=True):
        st.markdown(f"### {laptop['name']}")
        st.write(f"**Price:** £{laptop['price']}")
        st.write(f"**CPU:** {laptop['cpu']}")
        st.write(f"**RAM:** {laptop['ram']} | **Storage:** {laptop['storage']}")
        st.write(f"**Display:** {laptop['display']}")
        st.write(f"**Battery:** {laptop['battery']}")

    st.divider()

    with st.form("checkout_form"):
        customer_name = st.text_input("Full name", value=st.session_state.current_user.get("full_name", "") if st.session_state.current_user else "")
        email = st.text_input("Email address", value=st.session_state.current_user.get("email", "") if st.session_state.current_user else "")
        shipping_address = st.text_area("Shipping address", height=110, placeholder="Street, city, postcode, country")
        delivery_option = st.radio("Delivery option", ["Standard (3-5 days)", "Express (1-2 days)"], index=0)
        payment_method = st.selectbox("Payment method", ["Visa", "Mastercard", "PayPal", "Apple Pay"])

        st.subheader("Order summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Laptop: {laptop['name']}")
            st.write(f"Subtotal: £{subtotal:.2f}")
            st.write(f"Shipping: £{shipping:.2f}")
            st.write(f"VAT: £{tax:.2f}")
        with col2:
            st.metric("Total", f"£{total:.2f}")
            st.write(f"Delivery: {delivery_option}")
            st.write(f"Payment: {payment_method}")

        confirm_order = st.form_submit_button("Confirm purchase")

    if confirm_order:
        if not customer_name or not email or not shipping_address:
            st.error("Please complete all checkout details before confirming your order.")
        else:
            st.session_state.checkout_order = {
                "customer_name": customer_name,
                "email": email,
                "shipping_address": shipping_address,
                "delivery_option": delivery_option,
                "payment_method": payment_method,
                "laptop": laptop["name"],
                "total": total,
            }
            st.success("Purchase confirmed! Your order has been placed successfully.")
            st.balloons()
            st.write("### Order confirmation")
            st.write(f"**Customer:** {customer_name}")
            st.write(f"**Laptop:** {laptop['name']}")
            st.write(f"**Total paid:** £{total:.2f}")
            st.write(f"**Delivery:** {delivery_option}")
            st.write(f"**Payment method:** {payment_method}")

            if st.button("Start new purchase"):
                st.session_state.selected_laptop = None
                st.session_state.checkout_order = None
                st.session_state.current_page = "Chat"
                st.rerun()

elif page == "History":
    st.title("Conversation History")
    if not st.session_state.history:
        st.info("No chat history yet. Ask the agent a question from the Chat page.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history), 1):
            with st.container(border=True):
                st.markdown(f"**{idx}. Prompt:** {item['prompt']}")
                st.write(f"**Intent:** {item['intent']} | **Confidence:** {item['confidence']:.0%}")
                st.write(item['response'])

        if st.button("Clear history"):
            st.session_state.history = []
            st.rerun()

elif page == "Settings":
    st.title("Settings")
    st.session_state.default_budget = st.slider("Default laptop budget", 400, 1500, st.session_state.default_budget, step=50)
    st.session_state.preferred_focus = st.radio(
        "Default laptop focus",
        ["Balanced", "Performance", "Battery", "Value", "Portability"],
        index=["Balanced", "Performance", "Battery", "Value", "Portability"].index(st.session_state.preferred_focus),
    )
    st.session_state.profile = st.selectbox("Default user profile", ["Student", "Developer", "Business", "General use"], index=["Student", "Developer", "Business", "General use"].index(st.session_state.profile))

    st.checkbox("Enable auto-saving of chat history", value=True)
    st.checkbox("Compact dashboard layout", value=False)

    st.subheader("Quick actions")
    if st.button("Reset app state"):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.selected_laptop = None
        st.rerun()

elif page == "About":
    st.title("About this app")
    st.markdown(
        """
        This app demonstrates an agentic AI workflow using:

        - ML intent classification
        - product search and filtering
        - recommendation scoring
        - a simple chat experience

        It is designed as a hackathon MVP and can be extended with live APIs, a real LLM, vector search, or persistent storage.
        """
    )

    st.subheader("Recommended prompts")
    st.code("What are the best laptops for computer univeristy science students under £800?")
    st.code("Recommend a portable laptop with strong battery life under £900.")
    st.code("Which laptop is best for programming and multitasking?")
    st.code("Best performing Laptop for business use for conferencing/office work/remote work")
    st.code("Recommended Laptop for general purpose and everyday use")
    
    if st.session_state.selected_laptop:
        st.success(f"Currently selected: {st.session_state.selected_laptop}")
