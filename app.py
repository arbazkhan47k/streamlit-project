import streamlit as st
import pyttsx3
import speech_recognition as sr

# Initialize TTS engine
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎤 Listening... Please say the university name.")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        st.success(f"✅ You said: {query}")
        return query
    except sr.UnknownValueError:
        st.error("❌ Could not understand your voice.")
    except sr.RequestError:
        st.error("❌ Speech recognition service error.")
    return None

# ------------------ University Data ------------------
universities = [
    {
        "name": "Harvard University",
        "country": "USA",
        "location": "Cambridge, Massachusetts",
        "tuition": "$50,000/year",
        "courses": ["Computer Science", "Economics", "Law", "Business"],
        "placement_rate": "92%",
        "departments": ["Engineering", "Law", "Medicine", "Business"],
        "management": "Private",
        "dorm": "On-campus housing available",
        "website": "https://www.harvard.edu"
    },
    {
        "name": "University of Oxford",
        "country": "UK",
        "location": "Oxford, England",
        "tuition": "£38,000/year",
        "courses": ["Philosophy", "Computer Science", "History"],
        "placement_rate": "89%",
        "departments": ["Humanities", "Sciences", "Law"],
        "management": "Public",
        "dorm": "Collegiate housing",
        "website": "https://www.ox.ac.uk"
    },
    {
        "name": "University of Tokyo",
        "country": "Japan",
        "location": "Tokyo, Japan",
        "tuition": "¥535,800/year",
        "courses": ["Engineering", "Physics", "Biology"],
        "placement_rate": "85%",
        "departments": ["Science", "Engineering", "Law"],
        "management": "Public",
        "dorm": "Limited on-campus dormitories",
        "website": "https://www.u-tokyo.ac.jp"
    },
    {
        "name": "Vivekananda Global University (VGU)",
        "country": "India",
        "location": "Jagatpura, Jaipur, Rajasthan",
        "tuition": "₹120,000/year",
        "courses": ["Engineering", "Management", "Law", "Design"],
        "placement_rate": "75%",
        "departments": ["Engineering", "Law", "Design", "Agriculture"],
        "management": "Private",
        "dorm": "On-campus hostels with mess, Wi-Fi, gym, and laundry",
        "website": "https://vgu.ac.in/"
    },
    {
        "name": "JECRC University",
        "country": "India",
        "location": "Sitapura, Jaipur, Rajasthan",
        "tuition": "₹110,000/year",
        "courses": ["Computer Science", "Biotech", "Civil", "MBA"],
        "placement_rate": "80%",
        "departments": ["Engineering", "Sciences", "Business"],
        "management": "Private",
        "dorm": "Hostels with AC/Non-AC rooms, mess, 24x7 security",
        "website": "https://jecrcuniversity.edu.in/"
    },
    {
        "name": "Swami Keshvanand Institute of Technology (SKIT)",
        "country": "India",
        "location": "Ramnagaria, Jagatpura, Jaipur",
        "tuition": "₹100,000/year",
        "courses": ["Mechanical Engineering", "Electronics", "CSE", "MBA"],
        "placement_rate": "78%",
        "departments": ["Engineering", "Business", "Applied Sciences"],
        "management": "Private",
        "dorm": "Separate hostels for boys and girls with Wi-Fi, mess, gym",
        "website": "https://www.skit.ac.in/"
    }
]

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="University Finder", layout="wide")
st.title("University Finder")
st.write("Explore universities and colleges with full info, including cost, placement, and dorms.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
selected_country = st.sidebar.selectbox("Select Country", ["All"] + list(set([u["country"] for u in universities])))
selected_department = st.sidebar.selectbox("Select Department", ["All"] + sorted(set(d for u in universities for d in u["departments"])))
search_name = st.sidebar.text_input("Search by University Name")

if st.sidebar.button("🎙️ Use Voice Search"):
    voice_result = recognize_speech()
    if voice_result:
        search_name = voice_result

# Apply filters
filtered_universities = universities
if selected_country != "All":
    filtered_universities = [u for u in filtered_universities if u["country"] == selected_country]
if selected_department != "All":
    filtered_universities = [u for u in filtered_universities if selected_department in u["departments"]]
if search_name:
    filtered_universities = [u for u in filtered_universities if search_name.lower() in u["name"].lower()]

# Display results
st.subheader("🎓 Universities Matching Your Criteria")

if not filtered_universities:
    st.warning("No universities found matching your criteria.")
else:
    for uni in filtered_universities:
        with st.expander(f"{uni['name']}"):
            st.markdown(f"**🌐 Website:** [Visit]({uni['website']})")
            st.markdown(f"**📍 Location:** {uni['location']}, {uni['country']}")
            st.markdown(f"**💰 Tuition Fees:** {uni['tuition']}")
            st.markdown(f"**🏛️ Management Type:** {uni['management']}")
            st.markdown(f"**🏢 Departments:** {', '.join(uni['departments'])}")
            st.markdown(f"**📚 Courses Offered:** {', '.join(uni['courses'])}")
            st.markdown(f"**💼 Placement Rate:** {uni['placement_rate']}")
            st.markdown(f"**🛏️ Hostel/Dorm Info:** {uni['dorm']}")
            if st.button(f"🔊 Speak Details - {uni['name']}"):
                message = (
                    f"{uni['name']} located in {uni['location']}, {uni['country']}. "
                    f"Tuition: {uni['tuition']}. Courses: {', '.join(uni['courses'])}. "
                    f"Departments: {', '.join(uni['departments'])}. Placement rate: {uni['placement_rate']}. "
                    f"Hostel info: {uni['dorm']}."
                )
                speak_text(message)

st.markdown("---")
st.caption("Built using Streamlit + pyttsx3 + SpeechRecognition | Demo dataset for global university exploration.")