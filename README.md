# AI Resume Screening System

An AI-powered resume screening system that parses resume data and analyzes candidates against a given job description using Python and a large language model.

## 🚀 Features

* 📄 Resume parsing from PDF files
* 🤖 AI-powered resume analysis
* 🎯 Job description-based candidate analysis
* 🧩 Structured extraction of resume information
* 🔐 Secure API-key management using environment variables
* 🐍 Built with Python

## 🛠️ Tech Stack

* **Python**
* **Groq API**
* **Llama 3.3 70B Versatile**
* **Pydantic**
* **python-dotenv**
* PDF processing libraries

## 📂 Project Structure

```text
AI-Resume-Screening-System/
│
├── main.py
├── resume_parser.py
├── pyproject.toml
├── .python-version
├── README.md
├── .gitignore
└── resumes/              # Local resume files, ignored by Git
```

## ⚙️ How It Works

```text
Resume PDF
    ↓
Extract Resume Content
    ↓
AI Resume Parser
    ↓
Structured Resume Information
    ↓
Compare / Analyze with Job Description
    ↓
Candidate Screening Result
```

## 🔑 Environment Variables

Create a `.env` file in the project directory:

```env
Groq_Api_Key=your_groq_api_key
```

Never commit your `.env` file or expose your API key publicly.

## ▶️ Run Locally

Clone the repository:

```bash
git clone https://github.com/Aniket-Kumar-22/AI-Resume-Screening-System.git
cd AI-Resume-Screening-System
```

Install the project dependencies according to the project's `pyproject.toml`.

Create your `.env` file and add your Groq API key.

Then run:

```bash
python main.py
```

## 🔮 Future Improvements

* Candidate match score
* Skill matching and gap analysis
* Multiple resume screening
* Ranking candidates based on job requirements
* Web-based user interface
* Cloud deployment

## 👨‍💻 Author

**Aniket Kumar**

GitHub: [Aniket-Kumar-22](https://github.com/Aniket-Kumar-22)
