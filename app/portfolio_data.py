"""Centralized Portfolio Data Repository for Jayaprakash Biswal.

All personal details, project metadata, skill taxonomy, educational history,
and certifications are maintained here as typed Python data structures.
"""

PROFILE_DATA = {
    "name": "Jayaprakash Biswal",
    "short_name": "Jayaprakash",
    "monogram": "JB",
    "title": "Python Developer | Web Developer | Data Analyst | Aspiring Data Scientist",
    "headline": "Building useful digital experiences with Python, data, and AI.",
    "bio_summary": (
        "I'm Jayaprakash Biswal, an IT Management student passionate about Python development, "
        "data analysis, and practical AI-powered applications."
    ),
    "about_text": (
        "I am currently in my third year pursuing a BSc in Information Technology Management at NIIS "
        "Group of Institutions, Bhubaneswar, maintaining a CGPA of 8.14. My journey centers on "
        "practical, project-based engineering — combining clean Python code with intuitive web interfaces "
        "and robust data pipelines. Whether architecting backend routes with Flask, unearthing trends with "
        "Pandas and Matplotlib, or training predictive models with Scikit-learn, I focus on building software "
        "that solves genuine problems."
    ),
    "location": "Bhubaneswar, Odisha, India",
    "email": "jayprakashbiswa49@gmail.com",
    "github_url": "https://github.com/jayprakashbiswa49-pixel",
    "linkedin_url": "https://www.linkedin.com/in/jayaprakash-biswal-bb1937414",
    "stats": [
        {"label": "Academic CGPA", "value": "8.14", "detail": "BSc IT Management (3rd Year)"},
        {"label": "Featured Projects", "value": "7+", "detail": "Web, ML & Analytics"},
        {"label": "Certifications", "value": "5", "detail": "Data Science & Development"},
        {"label": "Core Focus", "value": "Python & Data", "detail": "Backend, EDA & ML"}
    ]
}

SKILL_GROUPS = [
    {
        "category": "Programming Languages",
        "description": "Core languages for systems, algorithms, and application backends.",
        "icon": "code",
        "skills": ["Python", "Java", "C", "SQL", "JavaScript"]
    },
    {
        "category": "Web Development",
        "description": "Server-side architectures, templating, and modern responsive layouts.",
        "icon": "globe",
        "skills": ["HTML5", "CSS3", "Flask", "Jinja2", "REST APIs"]
    },
    {
        "category": "Data Analysis",
        "description": "Data wrangling, exploratory data analysis, and visual storytelling.",
        "icon": "bar-chart",
        "skills": ["Pandas", "NumPy", "Matplotlib", "Seaborn", "Excel", "Power BI"]
    },
    {
        "category": "Machine Learning",
        "description": "Supervised modeling, data preprocessing, and model inference pipelines.",
        "icon": "cpu",
        "skills": ["Scikit-learn", "Data Preprocessing", "Machine Learning Fundamentals"]
    },
    {
        "category": "Tools & Workflow",
        "description": "Development environments, version control, and collaborative tooling.",
        "icon": "tool",
        "skills": ["Git", "GitHub", "VS Code", "Jupyter Notebook", "Anaconda"]
    }
]

PROJECT_CATEGORIES = [
    {"id": "all", "name": "All Projects"},
    {"id": "web-ai", "name": "Web & AI"},
    {"id": "ml-data", "name": "Data Analytics & ML"},
    {"id": "utilities", "name": "Python Utilities"}
]

PROJECTS = [
    {
        "id": "glint",
        "title": "Glint: AI-Powered Placement Portal",
        "category": "web-ai",
        "category_label": "Web & AI",
        "featured": True,
        "priority": 1,
        "badge": "Tier-1 Flagship",
        "description": (
            "An AI-oriented placement platform designed to support student profiles, skill-gap identification, "
            "candidate matching, and placement workflows."
        ),
        "highlights": [
            "Comprehensive student profile management and resume indexing",
            "Skill-gap analysis engine for candidate job qualification",
            "Flask and SQLAlchemy architecture backed by PostgreSQL persistence"
        ],
        "tech_stack": ["Python", "Flask", "SQLAlchemy", "PostgreSQL"],
        "github_url": "https://github.com/bishalraj-gouda/Glint",
        "live_demo_url": "https://glint-placement-portal.onrender.com/",
        "icon": "briefcase"
    },
    {
        "id": "customer-churn",
        "title": "Customer Churn Prediction",
        "category": "ml-data",
        "category_label": "Machine Learning",
        "featured": True,
        "priority": 2,
        "badge": "Tier-1 ML Project",
        "description": (
            "A machine learning application that predicts customer churn using customer and subscription information, "
            "with preprocessing, model inference, and Flask backend functionality."
        ),
        "highlights": [
            "End-to-end data preprocessing and categorical feature encoding",
            "Supervised classification model trained with Scikit-learn",
            "Interactive Flask inference endpoint serving real-time prediction probabilities"
        ],
        "tech_stack": ["Python", "Flask", "Pandas", "Scikit-learn"],
        "github_url": "https://github.com/jayprakashbiswa49-pixel/Customer_Churn_Prediction",
        "live_demo_url": None,
        "icon": "users"
    },
    {
        "id": "sales-analysis",
        "title": "Sales Data Analysis",
        "category": "ml-data",
        "category_label": "Data Analytics",
        "featured": False,
        "priority": 3,
        "badge": "Analytics",
        "description": "Analyzed sales data to identify sales patterns, performance trends, and business insights.",
        "highlights": [
            "Revenue and profit distribution across product categories and regions",
            "Time-series trend analysis identifying seasonality and peaks",
            "Matplotlib visual storytelling for stakeholder decision-making"
        ],
        "tech_stack": ["Python", "Pandas", "Matplotlib"],
        "github_url": "https://github.com/jayprakashbiswa49-pixel/Sales-Data-Analysis",
        "live_demo_url": None,
        "icon": "trending-up"
    },
    {
        "id": "amazon-books",
        "title": "Amazon Books Analysis",
        "category": "ml-data",
        "category_label": "Data Analytics",
        "featured": False,
        "priority": 4,
        "badge": "Analytics",
        "description": "Explored Amazon bestseller data to compare ratings, genres, authors, and book performance.",
        "highlights": [
            "Exploration of multi-year bestseller pricing and review distributions",
            "Author popularity and genre correlation with user review volume",
            "Insightful charts illustrating commercial success vs user sentiment"
        ],
        "tech_stack": ["Python", "Pandas", "Data Visualization"],
        "github_url": "https://github.com/jayprakashbiswa49-pixel/Amazon_Books_Analysis",
        "live_demo_url": None,
        "icon": "book-open"
    },
    {
        "id": "ipl-analysis",
        "title": "IPL Data Analysis",
        "category": "ml-data",
        "category_label": "Sports Analytics",
        "featured": False,
        "priority": 5,
        "badge": "Sports Data",
        "description": "Analyzed IPL statistics and created visualizations to explore match data and performance patterns.",
        "highlights": [
            "Toss-decision impact on match win ratios across different venues",
            "Individual player batting strike rates and bowling economy rates",
            "Team head-to-head records synthesized into intuitive graphics"
        ],
        "tech_stack": ["Python", "Pandas", "Matplotlib"],
        "github_url": "https://github.com/jayprakashbiswa49-pixel/Ipl-Data-Analysis",
        "live_demo_url": None,
        "icon": "activity"
    },
    {
        "id": "modern-ui",
        "title": "Modern UI",
        "category": "web-ai",
        "category_label": "Frontend",
        "featured": False,
        "priority": 6,
        "badge": "Interface Design",
        "description": "Developed a responsive user interface focused on layout, visual hierarchy, and reusable styling.",
        "highlights": [
            "Mobile-first responsive architecture using modern CSS Grid and Flexbox",
            "Reusable design system tokens with clean visual hierarchy",
            "Zero heavy external dependencies for rapid page loads"
        ],
        "tech_stack": ["HTML5", "CSS3"],
        "github_url": "https://github.com/jayprakashbiswa49-pixel/Modern-UI",
        "live_demo_url": None,
        "icon": "layout"
    },
    {
        "id": "python-hands-on",
        "title": "Python Hands-on Projects",
        "category": "utilities",
        "category_label": "Python Utilities",
        "featured": False,
        "priority": 7,
        "badge": "Tool Suite",
        "description": (
            "Built practical Python utilities, including a calculator, quiz application, AI chatbot, "
            "news API application, water reminder, and PDF merger."
        ),
        "highlights": [
            "Interactive CLI and desktop utility implementations",
            "Third-party REST API integration for real-time news retrieval",
            "PDF file manipulation and automation using PyPDF2"
        ],
        "tech_stack": ["Python", "REST APIs", "PyPDF2"],
        "github_url": "https://github.com/jayprakashbiswa49-pixel/HANS-ON-PROJECT",
        "live_demo_url": None,
        "icon": "cpu"
    }
]

EDUCATION = {
    "degree": "BSc in Information Technology Management",
    "institution": "NIIS Group of Institutions",
    "location": "Bhubaneswar, Odisha, India",
    "year": "Third Year",
    "cgpa": "8.14",
    "highlights": [
        "Specialization in Information Technology Management and Software Systems",
        "Core coursework in Object-Oriented Programming, Database Management, and Data Structures",
        "Hands-on project work in Python backends, Web Technologies, and Business Data Analytics",
        "Maintained strong academic standing with consistent 8.14 CGPA"
    ]
}

CERTIFICATIONS = [
    {
        "title": "Job Ready Data Science",
        "issuer": "CodeWithHarry",
        "category": "Data Science",
        "focus": "Comprehensive data science lifecycle, statistics, and machine learning workflows"
    },
    {
        "title": "Python Bootcamp",
        "issuer": "CodeWithHarry",
        "category": "Programming",
        "focus": "Python core fundamentals, OOP, data structures, and automation scripting"
    },
    {
        "title": "AI Excel",
        "issuer": "SkillCourse",
        "category": "Analytics",
        "focus": "Advanced spreadsheet data modeling, business formulas, and AI-assisted workflows"
    },
    {
        "title": "Power BI",
        "issuer": "Great Learning / SkillCourse",
        "category": "Business Intelligence",
        "focus": "Interactive reporting dashboards, DAX queries, and visual business metrics"
    },
    {
        "title": "Web Development",
        "issuer": "Apna College",
        "category": "Web Development",
        "focus": "Semantic HTML5, CSS3 layouts, DOM scripting, and responsive principles"
    }
]
