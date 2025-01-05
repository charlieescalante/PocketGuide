import streamlit as st
from openai import OpenAI
from streamlit_geolocation import streamlit_geolocation

# Set your OpenAI API key
client = OpenAI(api_key=st.secrets['OPENAI_API_Key'])

st.title("Hello and Welcome to PocketGuide!")

# Initialize session states
if "tour_started" not in st.session_state:
    st.session_state.tour_started = False

if "messages" not in st.session_state:
    # We’ll start with a 'system' role message that sets up the behavior of the AI
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a tour guide. You give insights into people's surroundings "
                "using their GPS coordinates. It will be a 1-sided tour; you won't "
                "receive questions from the user. You will simply speak about the area "
                "as though you've lived there your whole life, providing rich detail "
                "and history."
            ),
        }
    ]

# Create a "Start Tour" button
if st.button("Start Tour"):
    st.session_state.tour_started = True

# If user clicked on "Start Tour", retrieve location and call GPT
if st.session_state.tour_started:
    location = streamlit_geolocation()

    if location:
        st.success("Geolocation Retrieved Successfully!")
        lat = location["latitude"]
        lon = location["longitude"]

        st.write(f"**Latitude:** {lat}")
        st.write(f"**Longitude:** {lon}")

        # Prepare a user role message with the lat-lon info
        user_message = f"My current GPS coordinates are: Latitude {lat}, Longitude {lon}."
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Call OpenAI ChatCompletion
        with st.spinner("Generating your tour guide narration..."):
            chatresponse = client.chat.completions.create(
                model='chatgpt-4o-latest',
                messages= st.session_state.messages,
                temperature=1,
                n=1,
                stream=True
            )

        # Extract and display the assistant’s response
        tour_guide_text = chatresponse["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": tour_guide_text})

        st.write("---")
        st.markdown("#### Your PocketGuide says:")
        st.write(tour_guide_text)

    else:
        st.warning("Click the button to fetch your geolocation.")
