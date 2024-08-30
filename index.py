import streamlit as st
from fpdf  import FPDF
import base64


def create_pdf(name, email, phone, linkedin, address, education, work_experience, skills, projects, additional_info ):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial",size=12)

    pdf.set_font("Arial",'B',16)
    pdf.cell(200,10,txt=name,ln=True,align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200,10,txt=f"Email:{email}",ln=True,align='L')
    pdf.cell(200,10,txt=f"Phone:{phone}",ln=True,align='L')
    pdf.cell(200,10,txt=f"LinkedIn:{linkedin}",ln=True,align='L')
    pdf.cell(200,10,txt=f"Address:{address}",ln=True,align='L')
    pdf.ln(10)

    pdf.set_font("Arial",'B',14)
    pdf.cell(200,10,txt="Education",ln=True,align='L')
    pdf.set_font("Arial",size=12)
    for edu in education:
        pdf.multi_cell(0,10,f"Institution :{edu['institution']}\nPeriod: {edu['period']}\nCGPA: {edu['cgpa']}")
        pdf.ln(5)

    pdf.set_font("Arial",'B',14)
    pdf.cell(200,10,txt="Work Experience",ln=True,align='L')
    pdf.set_font("Arial",size=12)
    for exp in work_experience:
        pdf.multi_cell(0,10,f"Company :{exp['company']}\nPeriod: {exp['period']}\nRole: {exp['role']}\nDescription: {exp['description']}")
        pdf.ln(5)

    pdf.set_font("Arial",'B',14)
    pdf.cell(200,10,txt="Skills",ln=True,align='L')
    pdf.set_font("Arial",size=12)
    for skill in skills.split("\n"):
        pdf.cell(200,10,txt = f" {skill}" , ln=True, align ='L')
    pdf.ln(5)

    pdf.set_font("Arial",'B',14)
    pdf.cell(200,10,txt="Projects",ln=True,align='L')
    pdf.set_font("Arial",size=12)
    for project in projects:
        pdf.multi_cell(0,10,f"Title :{project['title']}\nDescription: {project['description']}")
        pdf.ln(5)

    pdf.set_font("Arial",'B',14)
    pdf.cell(200,10,txt="Additional Information",ln=True,align='L')
    pdf.set_font("Arial",size=12)
    pdf.multi_cell(0,10,additional_info)
    
    return pdf

def main():
        st.title("Resume Maker App")

        with st.sidebar:
            st.subheader("Personal Information")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            linkedIn = st.text_input("LinkedIn URL")
            address = st.text_area("Address")

            st.subheader("Education")
            education = []
            num_education = st.number_input("Number of Education Entries", min_value=1, max_value=10,step=1)
            for i in range(int(num_education)):
                institution = st.text_input(f"Institution {i+1}" , key = f"institution_{i}")
                period = st.text_input(f"Time period {i+1}", key = f"period_{i}")
                cgpa = st.text_input(f"CGPA {i+1}", key = f"cgpa_{i}")
                education.append({"institution" : institution , "period" : period , "cgpa" : cgpa})

            st.subheader("Work Experience")
            work_experience = []
            num_experience = st.number_input("Number of Work Experience Entries", min_value=1, max_value=10,step=1)
            for i in range(int(num_experience)):
                company = st.text_input(f"Company {i+1}" , key = f"company_{i}")
                period = st.text_input(f"Time period {i+1}", key = f"work_period_{i}")
                role = st.text_input(f"Role {i+1}", key = f"role_{i}")
                description = st.text_area(f"Description {i+1}", key = f"work_description_{i}")
                work_experience.append({"company" : company , "period" : period , "role" : role , "description" : description})

            st.subheader("Skills (Enter each skill on a new line)")
            skills = st.text_area("Skills")

            st.subheader("Projects")
            projects = []
            num_projects = st.number_input("Number of Projects", min_value=1, max_value=10,step=1)
            for i in range(int(num_projects)):
                title = st.text_input(f"Project Title {i+1}" , key = f"project_title_{i}")
                description = st.text_area(f"Description {i+1}", key = f"project_description_{i}")
                projects.append({"title" : title , "description" : description})
            
            st.subheader("Additional Information")
            additional_info = st.text_area("Additional information")

        st.write(f"## {name}")
        st.write(f"Email :  {email}")
        st.write(f"Phone : {phone}")
        st.write(f"LinkedIn :  {linkedIn}")
        st.write(f"Address :  {address}")

        st.write(f"### Education")
        for edu in education:
            st.write(f"Institution: {edu['institution']}")
            st.write(f"Period: {edu['period']}")
            st.write(f"CGPA: {edu['cgpa']}")
            st.write("")

        st.write(f"### Work Experience")
        for exp in work_experience:
            st.write(f"Company :  {exp['company']}")
            st.write(f"Period :  {exp['period']}")
            st.write(f"Role : {exp['role']}")
            st.write(f"Description : {exp['description']}")
            st.write("")

        st.write('### Skills')
        for skill in skills.split('\n'):
            st.write(f" {skill}")

        st.write(f"### Projects")
        for project  in projects:
            st.write(f"{project['title']}")
            st.write(f"Description : {project['description']}")
            st.write("")

        st.write(f"### Additional Information")
        st.write(additional_info)

        if st.button("Download Resume as PDF"):
            pdf = create_pdf(name,email,phone,linkedIn,address,education,work_experience,skills,projects,additional_info)

            pdf_output = f"{name.replace(' ',"_")}_resume.pdf"
            pdf.output(pdf_output)

            with open(pdf_output , "rb") as pdf_file:
                pdf_bytes= pdf_file.read()
                b64_pdf = base64.b64encode(pdf_bytes).decode()
            
            href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{pdf_output}"'
            #st.markdown(href, unsafe_allow_html = True)
            if (href):
                st.write("Downloaded successfully!")
            
             


if __name__ == "__main__":
    main()