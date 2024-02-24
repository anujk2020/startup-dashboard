st.title("Dashboard")

st.header("First Project with Streamlit")

st.subheader("Excited to learn")

st.write("This is a normal text")

st.markdown("""
### My fav movies
- Drishyam
- 3 idiots
""")

st.code("""

def process_func(data):
    return data**2
""")

st.latex("z = (x^2 + y^2)/a^3")

st.metric("Revenue", "Rs. 3 Lakh", "+3%")

# st.json(dictionary) ; st.image(filepath) ; st.video(filepath)

# Creating Layouts or sidebars

st.sidebar.header('Sidebar Column')

col1, col2 = st.columns(2)

with col1:
    st.image('GenAI_Strategy.jpg')

with col2:
    st.image('GenAI_Strategy.jpg')

bar = st.progress(0)

for i in range(1,101):
    time.sleep(0.00000000001)
    bar.progress(i)

email = st.text_input("Enter Email")
password = st.text_input("Enter Password")