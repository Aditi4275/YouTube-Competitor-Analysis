import streamlit as st
import base64
import os
import io
import re
import fitz  # PyMuPDF
import matplotlib.pyplot as plt
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ------------------------------
# Helper Functions
# ------------------------------
def get_gemini_response(input, pdf_content, prompt):
    """Get response from Gemini model."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    """Convert uploaded PDF to an image and base64 string."""
    if uploaded_file is not None:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_doc:
            first_page = pdf_doc[0].get_pixmap()
            img_byte_arr = io.BytesIO(first_page.tobytes("jpeg"))
            return Image.open(img_byte_arr), base64.b64encode(img_byte_arr.getvalue()).decode()
    else:
        raise FileNotFoundError("No file uploaded")

def extract_match_percentage(response_text):
    """Extract match percentage from Gemini response."""
    match = re.search(r"Match Percentage:\s*(\d+)%", response_text)
    return int(match.group(1)) if match else 0

def draw_pie_chart(match_percentage):
    """Draw a pie chart for match percentage."""
    fig, ax = plt.subplots()
    labels = ['Match', 'Remaining']
    sizes = [match_percentage, 100 - match_percentage]
    colors = ['#4CAF50', '#FF5733']
    explode = (0.1, 0)
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.axis('equal')
    return fig

def draw_bar_chart(skills, ratings):
    """Draw a bar chart for skills and ratings."""
    fig, ax = plt.subplots()
    ax.barh(skills, ratings, color='#4CAF50')
    ax.set_xlabel('Rating (Out of 10)')
    ax.set_title('Skill Ratings')
    return fig

# ------------------------------
# UI Configuration
# ------------------------------
def set_custom_ui():
    """Set custom CSS and page configuration."""
    st.set_page_config(page_title="Technical ATS Resume Expert", page_icon="📄", layout="wide")
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://www.transparenttextures.com/patterns/always-grey.png');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextArea>textarea {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 10px;
        }
        .stFileUploader>div>div>div>div {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 10px;
        }
        .stMarkdown h1 {
            text-align: center;
            color: #4CAF50;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .stMarkdown h2 {
            color: #333;
            font-size: 1.8em;
            margin-bottom: 15px;
        }
        .stMarkdown h3 {
            color: #4CAF50;
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .stMarkdown p {
            color: #555;
            font-size: 1.1em;
            line-height: 1.6;
        }
        .stImage img {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stPlotlyChart {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True
    )

# ------------------------------
# Page Layout
# ------------------------------
def display_header():
    """Display the header section."""
    st.markdown("<h1>📄 Technical Resume Expert</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p style='text-align: center; color: #666; font-size: 1.4em;'>
            Upload your resume and job description to get a detailed analysis and improvement suggestions.
        </p>
    """, unsafe_allow_html=True)

def display_inputs():
    """Display input fields for job description and resume upload."""
    col1, col2 = st.columns(2)
    with col1:
        input_text = st.text_area("📝 **Job Description:**", height=200, key="input", placeholder="Paste the job description here...")
    with col2:
        uploaded_file = st.file_uploader("📂 **Upload your resume (PDF):**", type=["pdf"], help="Upload your resume in PDF format.")
    return input_text, uploaded_file

def display_buttons():
    """Display action buttons."""
    col1, col2, col3 = st.columns(3)
    with col1:
        submit1 = st.button("🔍 Analyse Resume")
    with col2:
        submit2 = st.button("📈 Improve Skills")
    with col3:
        submit3 = st.button("📊 Match Resume with Job Description")
    return submit1, submit2, submit3

# ------------------------------
# Main Function
# ------------------------------
def main():
    set_custom_ui()
    display_header()
    input_text, uploaded_file = display_inputs()
    submit1, submit2, submit3 = display_buttons()

    if uploaded_file is not None:
        st.success("✅ PDF Uploaded Successfully!")

    if submit1:
        if uploaded_file is not None:
            pdf_image, pdf_base64 = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, [{"mime_type": "image/jpeg", "data": pdf_base64}], input_prompt1)
            st.subheader("📊 Analysis")
            st.write(response)
        else:
            st.warning("⚠️ Please upload your resume!")

    elif submit2:
        if uploaded_file is not None:
            pdf_image, pdf_base64 = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, [{"mime_type": "image/jpeg", "data": pdf_base64}], input_prompt2)
            st.subheader("📈 Improvement Suggestions")
            st.write(response)
        else:
            st.warning("⚠️ Please upload your resume!")

    elif submit3:
        if uploaded_file is not None:
            pdf_image, pdf_base64 = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, [{"mime_type": "image/jpeg", "data": pdf_base64}], input_prompt3)
            match_percentage = extract_match_percentage(response)
            col1, col2 = st.columns(2)
            with col1:
                st.image(pdf_image, caption="Resume First Page", use_container_width=True)
            with col2:
                st.subheader("📊 Match Percentage")
                pie_chart = draw_pie_chart(match_percentage)
                st.pyplot(pie_chart)
            st.subheader("📝 Detailed Analysis")
            st.write(response)

            # Additional Bar Chart for Skill Ratings
            skills = ["Python", "Data Analysis", "Machine Learning", "Communication"]
            ratings = [8, 7, 6, 9]
            st.subheader("📊 Skill Ratings")
            bar_chart = draw_bar_chart(skills, ratings)
            st.pyplot(bar_chart)
        else:
            st.warning("⚠️ Please upload your resume!")

# ------------------------------
# Prompts
# ------------------------------
input_prompt1 = """
You are an experienced Technical HR Manager with expertise in talent acquisition and recruitment for technology, finance, and business roles. Your task is to conduct a detailed evaluation of the provided resume against the job description.

Alignment with Job Requirements: Analyze the resume to identify key skills, qualifications, and experiences that match the job requirements. Highlight areas where the candidate excels in fulfilling the role's technical, financial, or business-related expectations.

Strengths: Enumerate the candidate's core strengths, including technical skills, domain knowledge, certifications, achievements, or relevant experiences that align closely with the job description.

Weaknesses: Point out any notable gaps or areas where the candidate's profile does not meet the job requirements, such as missing skills, insufficient experience, or lack of relevant certifications.

Overall Fit: Provide a professional assessment of how well the candidate fits the role, considering both strengths and weaknesses. Offer an overall recommendation (e.g., highly suitable, moderately suitable, not suitable) and explain your reasoning.

Ensure your evaluation is specific, clear, and actionable, taking into account the nuances of the job role and industry requirements.
"""

input_prompt2 = """
You are a highly experienced Technical Career Advisor with deep expertise in the fields of Data Science, Web Development, Big Data Engineering, DevOps, and other technical domains. Your task is to provide detailed, actionable, and personalized guidance to help the individual improve their skills and advance their career based on the provided resume and job description.

1. **Skill Gap Analysis**: Identify the specific skills, technologies, tools, or certifications that are missing from the candidate's resume but are crucial for excelling in the specified job role.

2. **Recommended Learning Path**: Suggest practical steps the candidate can take to acquire the missing skills, such as:
   - Online courses or certifications (e.g., Coursera, Udemy, or official vendor certifications like AWS, Azure, or Google Cloud).
   - Projects or hands-on experiences that can help them gain expertise.
   - Open-source contributions or internships for real-world exposure.

3. **Emerging Trends and Technologies**: Highlight any emerging trends, tools, or frameworks in the industry that the candidate should explore to stay competitive and future-proof their career.

4. **Improvement in Soft Skills**: If applicable, suggest areas where the candidate can improve soft skills (e.g., communication, teamwork, or leadership) that are essential for success in their chosen domain.

5. **Overall Guidance**: Provide a summary of the top three actionable steps the candidate should prioritize to achieve significant improvement in their profile.

Ensure that your response is specific to the candidate's field and the role described in the job description. Provide clear, concise, and actionable advice that the candidate can immediately apply to improve their skills and career prospects.
"""

input_prompt3 = """
You are a skilled and advanced ATS (Applicant Tracking System) scanner, designed with deep functionality and specialized expertise in roles such as Data Science, Web Development, Big Data Engineering, and DevOps. Your task is to evaluate the provided resume against the job description thoroughly.

Matching Percentage: Analyze the resume and provide a precise percentage score indicating how well the candidate's profile aligns with the job description.

Missing Keywords: Identify and list any critical skills, technologies, tools, certifications, or keywords mentioned in the job description that are absent from the resume.

Final Thoughts: Provide a brief, insightful summary of your evaluation, including the candidate's overall suitability for the role, highlighting both key strengths and gaps.

Output Structure:

Match Percentage(bold): XX%
Missing Keywords(bold): 
[List missing skills/tools/keywords]
Final Thoughts(bold): 
[Provide a short summary of strengths and weaknesses and a recommendation if possible.]
"""

# Run the app
if __name__ == "__main__":
    main()