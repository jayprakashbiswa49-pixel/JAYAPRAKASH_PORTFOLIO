"""Generate an authentic, professional PDF resume for Jayaprakash Biswal."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch

def generate_resume(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    story = []
    styles = getSampleStyleSheet()

    # Colors
    c_primary = colors.HexColor('#202936')
    c_secondary = colors.HexColor('#4568DC')
    c_muted = colors.HexColor('#556070')
    c_line = colors.HexColor('#D1D8E0')

    # Custom styles
    style_name = ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=0
    )
    style_title = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_secondary
    )
    style_contact = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_muted
    )
    style_section_heading = ParagraphStyle(
        'ResumeHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_secondary,
        spaceAfter=3,
        spaceBefore=7
    )
    style_item_title = ParagraphStyle(
        'ResumeItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_primary
    )
    style_item_sub = ParagraphStyle(
        'ResumeItemSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=c_muted
    )
    style_body = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_primary
    )
    style_bullet = ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_primary,
        leftIndent=12
    )

    # 1. Header
    story.append(Paragraph("JAYAPRAKASH BISWAL", style_name))
    story.append(Paragraph("Python Developer | Web Developer | Data Analyst | Aspiring Data Scientist", style_title))
    story.append(Spacer(1, 2))
    
    contact_text = (
        "Bhubaneswar, Odisha, India &nbsp;|&nbsp; "
        "Email: jayprakashbiswa49@gmail.com &nbsp;|&nbsp; "
        "GitHub: github.com/jayprakashbiswa49-pixel &nbsp;|&nbsp; "
        "LinkedIn: linkedin.com/in/jayaprakash-biswal-bb1937414"
    )
    story.append(Paragraph(contact_text, style_contact))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=c_line, spaceBefore=2, spaceAfter=4))

    # 2. Education
    story.append(Paragraph("EDUCATION", style_section_heading))
    edu_table_data = [
        [
            Paragraph("<b>BSc in Information Technology Management</b> — NIIS Group of Institutions", style_item_title),
            Paragraph("<b>Bhubaneswar, Odisha</b>", style_item_sub)
        ],
        [
            Paragraph("Third Year Undergraduate &nbsp;|&nbsp; <b>CGPA: 8.14</b>", style_item_sub),
            Paragraph("Expected 2027", style_item_sub)
        ]
    ]
    t_edu = Table(edu_table_data, colWidths=[400, 140])
    t_edu.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_edu)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_line, spaceBefore=2, spaceAfter=4))

    # 3. Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", style_section_heading))
    skills_data = [
        [Paragraph("<b>Programming Languages:</b>", style_body), Paragraph("Python, Java, C, SQL, JavaScript", style_body)],
        [Paragraph("<b>Web Development:</b>", style_body), Paragraph("HTML5, CSS3, Flask, Jinja2, REST APIs", style_body)],
        [Paragraph("<b>Data Analysis & BI:</b>", style_body), Paragraph("Pandas, NumPy, Matplotlib, Seaborn, MS Excel, Power BI", style_body)],
        [Paragraph("<b>Machine Learning:</b>", style_body), Paragraph("Scikit-learn, Data Preprocessing, Machine Learning Fundamentals", style_body)],
        [Paragraph("<b>Developer Tools:</b>", style_body), Paragraph("Git, GitHub, VS Code, Jupyter Notebook, Anaconda", style_body)],
    ]
    t_skills = Table(skills_data, colWidths=[140, 400])
    t_skills.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_skills)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_line, spaceBefore=2, spaceAfter=4))

    # 4. Featured Projects
    story.append(Paragraph("FEATURED PROJECTS", style_section_heading))

    # Project 1: Glint
    story.append(Paragraph("<b>Glint: AI-Powered Placement Portal</b> &nbsp;|&nbsp; <i>Python, Flask, SQLAlchemy, PostgreSQL</i>", style_item_title))
    story.append(Paragraph("• Built an AI-oriented placement portal to manage student credentials, detect skill gaps, and match candidates with placement workflows.", style_bullet))
    story.append(Paragraph("• Implemented relational schemas with SQLAlchemy and connected PostgreSQL persistence deployed on Render.", style_bullet))
    story.append(Spacer(1, 3))

    # Project 2: Customer Churn Prediction
    story.append(Paragraph("<b>Customer Churn Prediction</b> &nbsp;|&nbsp; <i>Python, Flask, Pandas, Scikit-learn</i>", style_item_title))
    story.append(Paragraph("• Engineered an end-to-end machine learning application predicting customer churn based on subscription and demographic features.", style_bullet))
    story.append(Paragraph("• Handled exploratory data analysis, feature encoding, model evaluation, and created a Flask web inference interface.", style_bullet))
    story.append(Spacer(1, 3))

    # Project 3: Sales Data Analysis
    story.append(Paragraph("<b>Sales Data Analysis</b> &nbsp;|&nbsp; <i>Python, Pandas, Matplotlib</i>", style_item_title))
    story.append(Paragraph("• Cleaned and analyzed comprehensive retail transaction records to identify sales patterns, regional performance, and peak revenue drivers.", style_bullet))
    story.append(Spacer(1, 3))

    # Project 4: Amazon Books Analysis
    story.append(Paragraph("<b>Amazon Books Analysis</b> &nbsp;|&nbsp; <i>Python, Pandas, Data Visualization</i>", style_item_title))
    story.append(Paragraph("• Evaluated Amazon bestseller trends, analyzing pricing distributions, author rankings, and sentiment-to-rating correlations.", style_bullet))
    story.append(Spacer(1, 3))

    # Project 5: IPL Data Analysis
    story.append(Paragraph("<b>IPL Data Analysis</b> &nbsp;|&nbsp; <i>Python, Pandas, Matplotlib</i>", style_item_title))
    story.append(Paragraph("• Explored multi-season IPL tournament statistics, toss decisions vs match outcomes, and individual player performance analytics.", style_bullet))
    story.append(Spacer(1, 3))

    # Project 6: Python Hands-on Projects
    story.append(Paragraph("<b>Python Hands-on Projects Suite</b> &nbsp;|&nbsp; <i>Python, REST APIs, PyPDF2</i>", style_item_title))
    story.append(Paragraph("• Implemented a suite of practical utilities including real-time News API scraper, desktop water reminder, quiz engine, and automated PDF merger.", style_bullet))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_line, spaceBefore=2, spaceAfter=4))

    # 5. Certifications
    story.append(Paragraph("CERTIFICATIONS", style_section_heading))
    cert_text = (
        "• <b>Job Ready Data Science</b> — CodeWithHarry &nbsp;&nbsp;|&nbsp;&nbsp; "
        "• <b>Python Bootcamp</b> — CodeWithHarry<br/>"
        "• <b>AI Excel</b> — SkillCourse &nbsp;&nbsp;|&nbsp;&nbsp; "
        "• <b>Power BI</b> — Great Learning / SkillCourse &nbsp;&nbsp;|&nbsp;&nbsp; "
        "• <b>Web Development</b> — Apna College"
    )
    story.append(Paragraph(cert_text, style_body))

    doc.build(story)
    print(f"Successfully generated resume at {output_path}")

if __name__ == '__main__':
    target = os.path.join(os.path.dirname(__file__), 'app', 'static', 'files', 'resume.pdf')
    generate_resume(target)
