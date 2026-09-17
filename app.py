import streamlit as st
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from resume_parser import (
    read_resume,
    parse_resume,
    parse_job_description,
    final_score
)


st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

with st.sidebar:
    st.markdown("---")
    st.subheader("👨‍💻 Developed by-")

    st.write("**Aniket Kumar**")
    st.write("AI & ML Student | Aspiring AI Engineer")

    st.markdown(
    "📧 [Email Me](https://mail.google.com/mail/?view=cm&fs=1&to=aniketkr2207@gmail.com)"
    )
    st.markdown(
        "🔗 [LinkedIn](https://www.linkedin.com/feed/foryou/)"
    )

    st.markdown(
        "💻 [GitHub](https://github.com/Aniket-Kumar-22)"
    )


st.title("📄 AI-powered Resume Screening and Candidate Ranking System")
st.write("Upload a job description and multiple resumes to rank candidates.")


st.subheader("Job Description")

job_description = st.text_area(
    "Paste the job description here:",
    height=250
)


st.subheader("Upload Resumes")

uploaded_resumes = st.file_uploader(
    "Upload PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


if uploaded_resumes:
    st.write(f"**{len(uploaded_resumes)} resume(s) uploaded**")

    for file in uploaded_resumes:
        st.write("📄", file.name)


# ========================================
# CLEAR & EXIT BUTTONS
# ========================================

col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    clear_button = st.button("🗑️ Clear Resumes")

with col2:
    exit_button = st.button("🚪 Exit")


# ========================================
# CLEAR RESUMES
# ========================================

if clear_button:
    st.session_state.clear()
    st.rerun()


# ========================================
# EXIT APPLICATION
# ========================================

if exit_button:
    st.session_state["exit_app"] = True
    st.rerun()


# ========================================
# EXIT SCREEN
# ========================================

if st.session_state.get("exit_app", False):

    st.title("👋 Application Closed")
    st.success("You have exited the Resume Screening System.")

    st.stop()

# ========================================
# PROCESS RESUME
# ========================================

def process_resume(uploaded_file, job):

    start = time.time()

    file_path = Path(uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:

        # ========================================
        # READ RESUME
        # ========================================

        resume_text = read_resume(file_path)

        print(
            f"{uploaded_file.name} - "
            f"PDF/DOCX extraction: "
            f"{time.time() - start:.2f}s"
        )

        if not resume_text or not resume_text.strip():
            return None, f"⚠️ {uploaded_file.name} is empty."


        # ========================================
        # PARSE RESUME
        # ========================================

        llm_start = time.time()

        parsed_resume = parse_resume(resume_text)

        print(
            f"{uploaded_file.name} - "
            f"Resume parsing: "
            f"{time.time() - llm_start:.2f}s"
        )


        # ========================================
        # FINAL SCORE
        # ========================================

        score_start = time.time()

        result = final_score(
            job,
            parsed_resume
        )

        print(
            f"{uploaded_file.name} - "
            f"Final scoring: "
            f"{time.time() - score_start:.2f}s"
        )


        # ========================================
        # RETURN RESULT
        # ========================================

        return {
            "name": parsed_resume.name,
            "email": parsed_resume.email,
            "phone": parsed_resume.phone,
            "total_experience_years": parsed_resume.total_experience_years,
            "skills": parsed_resume.skills,
            "experience": parsed_resume.experience,
            "education": parsed_resume.education,
            "projects": parsed_resume.projects,
            "certifications": parsed_resume.certifications,
            "score": result.score,
            "details": result.details
        }, None


    except Exception as e:

        return None, (
            f"⚠️ Could not process "
            f"{uploaded_file.name}: {e}"
        )


    finally:

        if file_path.exists():
            file_path.unlink()


# ========================================
# SCREEN RESUMES
# ========================================

if st.button("🚀 Screen Resumes"):

    start_time = time.time()


    # ========================================
    # VALIDATION
    # ========================================

    if not job_description.strip():

        st.warning(
            "Please enter a job description."
        )


    elif not uploaded_resumes:

        st.warning(
            "Please upload at least one resume."
        )


    else:

        with st.spinner(
            "AI is screening the resumes..."
        ):


            # ========================================
            # PARSE JOB DESCRIPTION
            # ========================================

            job_start = time.time()

            job = parse_job_description(
                job_description
            )

            print(
                f"Job description parsing: "
                f"{time.time() - job_start:.2f}s"
            )


            # ========================================
            # PROCESS RESUMES IN PARALLEL
            # ========================================

            results = []

            with ThreadPoolExecutor(
                max_workers=2
            ) as executor:

                futures = [
                    executor.submit(
                        process_resume,
                        uploaded_file,
                        job
                    )
                    for uploaded_file in uploaded_resumes
                ]


                for uploaded_file, future in zip(
                    uploaded_resumes,
                    futures
                ):

                    result, error = future.result()


                    if error:

                        st.warning(
                            f"{uploaded_file.name}: "
                            f"{error}"
                        )

                        continue


                    results.append(result)


            # ========================================
            # SORT CANDIDATES
            # ========================================

            results.sort(
                key=lambda candidate: candidate["score"],
                reverse=True
            )


        # ========================================
        # TOTAL TIME
        # ========================================

        elapsed_time = time.time() - start_time

        st.info(
            f"⏱️ Screening completed in "
            f"{elapsed_time:.2f} seconds"
        )

        st.success(
            "Screening completed! 🎉"
        )


        # ========================================
        # CANDIDATE RANKING
        # ========================================

        st.subheader(
            "🏆 Candidate Ranking"
        )


        for rank, candidate in enumerate(
            results,
            start=1
        ):

            st.markdown(
                f"## {rank}. "
                f"{candidate['name']}"
            )


            st.metric(
                "Match Score",
                f"{candidate['score']}%"
            )


            details = candidate["details"]


            st.write(
                "### Candidate Details"
            )


            # ========================================
            # MATCHING SKILLS
            # ========================================

            if "matching_skills" in details:

                st.write(
                    "**✅ Matching Skills:**"
                )

                matching_skills = details[
                    "matching_skills"
                ]

                if matching_skills:

                    st.write(
                        ", ".join(
                            matching_skills
                        )
                    )

                else:

                    st.write(
                        "None"
                    )


            # ========================================
            # MISSING SKILLS
            # ========================================

            if "missing_important_skills" in details:

                st.write(
                    "**❌ Missing Important Skills:**"
                )

                missing_skills = details[
                    "missing_important_skills"
                ]

                if missing_skills:

                    st.write(
                        ", ".join(
                            missing_skills
                        )
                    )

                else:

                    st.write(
                        "None"
                    )


            # ========================================
            # EXPERIENCE
            # ========================================

            if "experience_requirement_met" in details:

                st.write(
                    "**💼 Experience Requirement:**"
                )

                st.write(
                    details[
                        "experience_requirement_met"
                    ]
                )


            # ========================================
            # FINAL VERDICT
            # ========================================

            if "final_verdict" in details:

                st.write(
                    "**📌 Final Verdict:**"
                )

                st.write(
                    details[
                        "final_verdict"
                    ]
                )


            st.divider()




            # uv run streamlit run app.py