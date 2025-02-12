import streamlit as st
import openai

# --- Function to generate resume using OpenAI ---
def generate_resume(name, email, phone, linkedin, objective, skills, experience, education):
    """Generates a resume using OpenAI based on user inputs."""

    try:
        # Construct the prompt for OpenAI
        prompt = f"""
        Generate a professional and well-structured resume for:

        Personal Information:
        Name: {name}
        Email: {email}
        Phone: {phone}
        LinkedIn: {linkedin}

        Objective:
        {objective}

        Skills:
        {skills}

        Experience:
        {experience}

        Education:
        {education}

        Instructions:
        * Use a professional tone.
        * Highlight key achievements and responsibilities in the experience section.
        * Structure the resume for readability and impact.
        * Keep it concise and focused on the most relevant information.
        * Limit the resume to one page, if possible.
        """

        # Call the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or a more suitable model
            prompt=prompt,
            max_tokens=500,  # Adjust as needed
            n=1,
            stop=None,
            temperature=0.7, # Adjust for creativity vs. accuracy
        )

        resume_text = response.choices[0].text.strip()
        return resume_text

    except Exception as e:
        return f"Error generating resume: {e}"


# --- Streamlit UI ---
def main():
    st.title("AI-Powered Resume Generator")

    # --- OpenAI API Key Input ---
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    openai.api_key = openai_api_key # Set the OpenAI API key

    # --- User Input Fields ---
    with st.form("resume_form"):
        st.subheader("Personal Information")
        name = st.text_input("Name:", placeholder="John Doe")
        email = st.text_input("Email:", placeholder="john.doe@example.com")
        phone = st.text_input("Phone:", placeholder="123-456-7890")
        linkedin = st.text_input("LinkedIn Profile URL:", placeholder="linkedin.com/in/johndoe")

        st.subheader("Summary/Objective")
        objective = st.text_area("Objective:", placeholder="Highly motivated professional seeking a challenging role...")

        st.subheader("Skills")
        skills = st.text_area("Skills (separate with commas):", placeholder="Python, Data Analysis, Communication...")

        st.subheader("Experience")
        experience = st.text_area("Experience (Describe your job roles, responsibilities, and achievements.  Separate each job experience with a double line break '\\n\\n'):",
                                placeholder="Job Title: Software Engineer\nCompany: Acme Corp\nDates: 2020-2023\nResponsibilities: Developed and maintained web applications...\n\nJob Title: Intern\nCompany: Beta Inc\nDates: 2019\nResponsibilities: Assisted with data analysis...")

        st.subheader("Education")
        education = st.text_area("Education (Separate each education entry with a double line break '\\n\\n'):",
                                 placeholder="Degree: Bachelor of Science in Computer Science\nUniversity: Example University\nDates: 2016-2020\n\nDegree: High School Diploma\nSchool: Example High School\nDates: 2012-2016")


        submitted = st.form_submit_button("Generate Resume")

    # --- Resume Generation and Display ---
    if submitted:
        if not openai_api_key:
            st.error("Please enter your OpenAI API Key.")
        else:
            with st.spinner("Generating Resume..."):
                resume_text = generate_resume(name, email, phone, linkedin, objective, skills, experience, education)

            st.subheader("Generated Resume:")
            st.code(resume_text, language="text")  # Display as code for better formatting

            # --- Download Button ---
            st.download_button(
                label="Download Resume (TXT)",
                data=resume_text,
                file_name="resume.txt",
                mime="text/plain",
            )


if __name__ == "__main__":
    main()