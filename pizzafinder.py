import os
import json
import base64
import streamlit as st
import openai
import requests

# —————————————————————————————————————————————————————————————
# Configuration
# —————————————————————————————————————————————————————————————
st.set_page_config(page_title="Pizza Finder", layout="centered")

# Load keys from environment for security
client = openai.OpenAI(api_key="{replace with your API}")


YELP_API_KEY = "{replace with your API}"  # Put your actual Yelp API key here
headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

# —————————————————————————————————————————————————————————————
# Helper Functions
# —————————————————————————————————————————————————————————————
def clean_json(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
    first = text.find("{")
    last = text.rfind("}")
    if first != -1 and last != -1 and last > first:
        text = text[first:last+1]
    return text


def encode_image_file(uploaded_file) -> str:
    return base64.b64encode(uploaded_file.read()).decode("utf-8")


def get_pizza_data(uploaded_file, user_text):
    b64 = encode_image_file(uploaded_file)

    # Image Agent (vision model)
    image_prompt = (
        "You are a pizza expert. Based on this image, return a JSON object with:\n"
        "- 'tags': list of ≥10 descriptors\n"
        "- 'review': 2–3 sentence summary of the pizza’s quality\n"
        "Return ONLY valid JSON."
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": image_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]
            }],
            max_tokens=500
        )
        raw = resp.choices[0].message.content
        image_data = json.loads(clean_json(raw))
    except Exception as e:
        st.error(f"🍕 Error extracting image data: {e}")
        image_data = {}

    # Flavor Agent
    flavor_prompt = (
        "Extract pizza flavor characteristics from the user's description.\n"
        "Return JSON with keys: cheesiness, greasiness, spiciness, sweetness, saltiness,\n"
        "sourness, umami, bitterness, sauciness, herbiness, tanginess.\n"
        "Assign 'low', 'medium', 'high' or descriptive text.\n"
        f"User: '{user_text}'\n"
        "Return ONLY valid JSON."
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": flavor_prompt}],
            max_tokens=300
        )
        raw = resp.choices[0].message.content
        flavor_data = json.loads(clean_json(raw))
    except Exception as e:
        st.error(f"⚠️ Failed to parse flavor profile: {e}")
        flavor_data = {}

    return {
        "image_data": image_data.get("tags", []),
        "flavor_data": {k: v for k, v in flavor_data.items() if k in [
            "cheesiness","greasiness","spiciness","sweetness","saltiness",
            "sourness","umami","bitterness","sauciness","herbiness","tanginess"]
        }
    }


def get_pizza_places(pizza_data, location, radius_miles):
    tags = pizza_data.get("image_data", [])
    profile = pizza_data.get("flavor_data", {})
    if not tags and not profile:
        st.error("No tags or flavor data to search for.")
        return []

    pool = tags + list(profile.keys())
    results = []
    for term in pool:
        params = {
            "term": term,
            "location": location,
            "radius": int(radius_miles * 1609),
            "limit": 5,
            "categories": "pizza",
            "sort_by": "rating"
        }
        try:
            res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
            results.extend(res.json().get("businesses", []))
        except Exception as e:
            st.error(f"🍕 Error searching Yelp: {e}")

    unique = []
    seen = set()
    for biz in results:
        if biz["id"] not in seen:
            seen.add(biz["id"])
            unique.append(biz)
    return unique

# UI: Streamlit App
st.title("Welcome to Pizza Finder!")
st.write("Upload a pizza image and describe your flavors to get personalized pizza spot ideas.")
st.write("---")

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if 'user_text' not in st.session_state:
    st.session_state['user_text'] = ''

# File uploader
uploaded_file = st.file_uploader("🍕 Upload a pizza image:", type=["jpg", "jpeg", "png"], key="image_file")
if uploaded_file:
    st.session_state['uploaded_file'] = uploaded_file
    st.image(uploaded_file, caption="Your Pizza", width=600)


# Flavor description input
user_text = st.text_area(
    "📝 Describe your pizza experience:",
    value=st.session_state['user_text'],
    key='user_text'
)

# Automatically process data when both image and text are present
if st.session_state['uploaded_file'] and user_text.strip():
    pizza_data = get_pizza_data(st.session_state['uploaded_file'], user_text)
    st.session_state['pizza_data'] = pizza_data
    st.success("Data processed successfully!")

    # Display image tags
    tags = pizza_data.get("image_data", [])
    if tags:
        st.subheader("🍕 Image Tags")
        st.write(", ".join(tags))

    # Display flavor profile
    flavors = pizza_data.get("flavor_data", {})
    if flavors:
        st.subheader("🍕 Flavor Profile")
        emoji_map = {
            "cheesiness": "🧀",
            "greasiness": "🛢️",
            "spiciness": "🌶️",
            "sweetness": "🍬",
            "saltiness": "🧂",
            "sourness": "🍋",
            "umami": "🍄",
            "bitterness": "☕",
            "sauciness": "🍅",
            "herbiness": "🌿",
            "tanginess": "🍋"
        }
        for k, v in flavors.items():
            st.markdown(f"{emoji_map.get(k, '')} **{k.capitalize()}**: {v}")

st.write("---")
st.header("🍕 Find Top Pizza Places Nearby")
location = st.text_input("Enter a location:", "Manhattan, NY")
radius_miles = st.slider("Search radius (miles):", 1, 25, 3)

# Search button retained
if st.button("Search for Pizza Places"):
    # Check if pizza_data is available in session state
    pizza_data = st.session_state.get('pizza_data', {})

    if not pizza_data:
        st.warning("Please upload an image and describe the flavor first!")
    else:
        with st.spinner("Searching Yelp…"):
            businesses = get_pizza_places(pizza_data, location, radius_miles)
            if businesses:
                st.markdown("### 🍕 Recommended Pizza Places", unsafe_allow_html=True)
                for i in range(0, len(businesses), 2):
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        biz1 = businesses[i]
                        st.subheader(f"🍕 {biz1['name']}")
                        st.write(f"📍 **Address:** {' '.join(biz1['location']['display_address'])}")
                        st.write(f"⭐ **Rating:** {biz1['rating']} stars ({biz1['review_count']} reviews)")
                        st.write(f"📞 **Phone:** {biz1.get('display_phone', 'N/A')}")
                        st.markdown(f"[🔗 View on Yelp]({biz1['url']})", unsafe_allow_html=True)

                        if biz1.get("image_url"):
                            st.image(biz1["image_url"], caption=f"Image of {biz1['name']}")

                        reviews = biz1.get("reviews", [])
                        if reviews:
                            st.write(f"💬 **Review:** {reviews[0]['text']}")

                    if i + 1 < len(businesses):
                        with col2:
                            biz2 = businesses[i + 1]
                            st.subheader(f"🍕 {biz2['name']}")
                            st.write(f"📍 **Address:** {' '.join(biz2['location']['display_address'])}")
                            st.write(f"⭐ **Rating:** {biz2['rating']} stars ({biz2['review_count']} reviews)")
                            st.write(f"📞 **Phone:** {biz2.get('display_phone', 'N/A')}")
                            st.markdown(f"[🔗 View on Yelp]({biz2['url']})", unsafe_allow_html=True)

                            if biz2.get("image_url"):
                                st.image(biz2["image_url"], caption=f"Image of {biz2['name']}")


                            reviews = biz2.get("reviews", [])
                            if reviews:
                                st.write(f"💬 **Review:** {reviews[0]['text']}")

                    st.markdown("---")

            else:
                st.error("No pizza places found. Try adjusting your input!")
