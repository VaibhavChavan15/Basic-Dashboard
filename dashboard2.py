import streamlit as st
import pandas as pd
import plotly.express as px

# Complete demographic questions with proper scoring based on research
demographic_questions = {
    "Q1. What is your age (in years)?": {
        "options": ["15-25", "25-35", "35-45", "45-55", "55-65"],
        "scores": [85, 100, 95, 70, 50],
        "weight": 0.8
    },
    "Q2. What is your educational qualification?": {
        "options": [
            "Illiterate", "Basic education/primary", "8th", "10th", "12th",
            "Graduation (BBA, B. Com, BSc., BTech, etc.)", 
            "Post Graduation (MBA, M. Com, MSc., MTech, etc.)",
            "Professional (CS, CA, ICWA, etc.)", "Other"
        ],
        "scores": [50, 55, 60, 65, 70, 85, 100, 95, 60],
        "weight": 1.2
    },
    "Q3. Religion": {
        "options": ["Hindu", "Muslim", "Sikh", "Christian", "Buddhist", "Jain", "Other"],
        "scores": [80, 75, 80, 80, 80, 80, 75],
        "weight": 0.6
    },
    "Q4. Caste": {
        "options": ["General", "EWS", "OBC", "SC", "ST"],
        "scores": [85, 75, 90, 60, 65],
        "weight": 0.7
    },
    "Q5. Do you watch T.V.?": {
        "options": ["Yes", "No"],
        "scores": [70, 60],
        "weight": 0.4
    },
    "Q6. Do you have a mobile phone?": {
        "options": ["Yes", "No"],
        "scores": [100, 20],
        "weight": 1.5
    },
    "Q7. Do you/does your family have internet access?": {
        "options": ["Yes", "No"],
        "scores": [100, 30],
        "weight": 1.4
    },
    "Q8. Do you have a social media account?": {
        "options": ["Yes", "No"],
        "scores": [95, 40],
        "weight": 1.1
    },
    "Q9. What business do you use to serve your customers?": {
        "options": ["Offline", "Online", "Both"],
        "scores": [60, 85, 100],
        "weight": 1.0
    },
    "Q10. Business Nature": {
        "options": [
            "Artificial jewelry making", "Clothing Designer/stitching", 
            "Hair Salon/Beauty Care", "Buying and Selling Clothes", 
            "Jute making", "Leather bag/other leather material"
        ],
        "scores": [75, 85, 80, 70, 65, 75],
        "weight": 0.9
    },
    "Q11. Initial Motivation to Start a Business": {
        "options": [
            "Was not initially interested but was supported by government/NGO", 
            "Family support", "Wants to become self-reliant", "Other"
        ],
        "scores": [70, 85, 100, 60],
        "weight": 1.3
    },
    "Q12. Age of your business (in years)": {
        "options": ["Less than 1 year", "1-5 years", "5-10 years", "More than 10 years"],
        "scores": [60, 85, 95, 100],
        "weight": 1.1
    },
    "Q13. What encouraged you to pursue training?": {
        "options": [
            "To enhance skills", "Networking with other women", 
            "To increase self-confidence", "Other"
        ],
        "scores": [100, 85, 90, 70],
        "weight": 1.0
    },
    "Q14. Monthly income before joining the training": {
        "options": ["Not earning money", "Less than 10 thousand", "10-20 thousand", "More than 20 thousand"],
        "scores": [30, 60, 80, 90],
        "weight": 1.2
    },
    "Q15. Monthly income after the training/present income": {
        "options": ["Not earning money", "Less than 10 thousand", "10-20 thousand", "More than 20 thousand"],
        "scores": [20, 60, 80, 100],
        "weight": 1.6
    }
}

# Calculate maximum possible weighted score for normalization
TOTAL_MAX_WEIGHTED_SCORE = sum(max(details["scores"]) * details["weight"] 
                              for details in demographic_questions.values())

# Define Likert scale questions
likert_questions = {
    "Entrepreneurial Intention": [
        "I am ready to do anything to be an entrepreneur.",
        "My professional goal is to be an entrepreneur.",
        "I will make every effort to start and run my own business.",
        "I am determined to create a business venture in the future.",
        "I have very seriously thought of starting a firm.",
        "I have the strong intention to start a firm someday."
    ],
    "Mentorship Support and Motivation": [
        "The mentor praises me for my good performance.",
        "The mentors at JSS were supportive and approachable throughout the program.",
        "I felt comfortable discussing my challenges and ideas with my mentor.",
        "My mentor was available when I needed guidance or advice.",
        "The mentor encourages me to put effort into business execution.",
        "The mentor encourages me to develop professional skills."
    ],
    "Networking": [
        "JSS provided me networking opportunities with other women.",
        "JSS provided us opportunity to connect us with different businesses.",
        "JSS organised seminars and workshops to help me in networking.",
        "I think JSS provided enough opportunity to build my entrepreneurial network.",
        "The people I meet through JSS networking events are relevant to my business interests.",
        "JSS actively provides networking opportunities to grow professional networks."
    ],
    "Training": [
        "The policy taught us how to start a business.",
        "The policy taught us practical knowledge in training related to our domain.",
        "The training provided in the program was relevant to my entrepreneurial goals.",
        "I feel confident in applying what I learned during the training to real-world situations.",
        "The training provided practical tools and techniques that I can apply in my entrepreneurial activities.",
        "The training equipped me with actionable insights that are useful in my business ventures.",
        "The practical knowledge provided in the training is of good quality.",
        "The practical knowledge provided by the JSS is useful in real-life scenarios."
    ],
    "Entrepreneurial Education": [
        "The entrepreneurial education I received was thorough and covered essential aspects of entrepreneurship.",
        "Entrepreneurship course offered gives me better understanding of the qualities that must be possessed to become an entrepreneur.",
        "Entrepreneurial education provided by JSS was practical, and I am using it in my business.",
        "JSS provides the necessary knowledge about entrepreneurship.",
        "JSS develops my entrepreneurial skills and abilities.",
        "JSS teaches students about entrepreneurship and starting a business."
    ],
    "Entrepreneurial Attitude": [
        "I think being an entrepreneur is a good idea.",
        "I think entrepreneurship is a respectful profession.",
        "I believe that starting a business is a desirable career option.",
        "Being an entrepreneur would allow me to achieve my personal goals.",
        "Starting my own business would give me great satisfaction."
    ],
    "Economic Empowerment": [
        "I have control over how to use my personal or family income.",
        "I have access to financial services (e.g., bank accounts, loans, savings).",
        "I am involved in income-generating activities (e.g., employment, business).",
        "I am not depending on others for my long-term financial decisions.",
        "I have control over my savings.",
        "I actively participate in decisions regarding household financial matters.",
        "I independently manage my financial resources via budgeting."
    ],
    "Social Empowerment": [
        "Important decisions in the family are taken mutually by me and my husband.",
        "I can move out of home freely without any restrictions for work.",
        "Working freely has improved my social status.",
        "I know most of the women living in my locality.",
        "I feel confident participating in community activities or social gatherings.",
        "I am involved in important decisions (related to health, education, child-rearing) made within my household."
    ]
}

# Streamlit app setup
st.set_page_config(page_title="Women Entrepreneurship Evaluation", layout="wide")
st.title("🚀 Women Entrepreneurship Evaluation Dashboard")
st.markdown("*Comprehensive assessment based on demographic factors and entrepreneurial indicators*")

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Demographic Information")
    
    # Collect demographic responses
    demographic_responses = {}
    for question, details in demographic_questions.items():
        demographic_responses[question] = st.selectbox(
            question, 
            details["options"],
            key=f"demo_{question}"
        )

with col2:
    st.header("📈 Evaluation Questions")
    
    # Collect Likert scale responses
    likert_responses = {}
    for category, questions in likert_questions.items():
        with st.expander(f"**{category}**", expanded=False):
            likert_responses[category] = []
            for i, question in enumerate(questions):
                response = st.slider(
                    question, 
                    min_value=1, 
                    max_value=5, 
                    value=3,
                    key=f"{category}_{i}"
                )
                likert_responses[category].append(response)

# Calculate and display results
if st.button("🔍 Calculate Evaluation Score", type="primary"):
    
    # Calculate demographic score with proper weighting
    total_weighted_score = 0
    demographic_breakdown = {}
    
    for question, response in demographic_responses.items():
        details = demographic_questions[question]
        option_index = details["options"].index(response)
        raw_score = details["scores"][option_index]
        weight = details["weight"]
        weighted_score = raw_score * weight
        total_weighted_score += weighted_score
        
        demographic_breakdown[question] = {
            "response": response,
            "raw_score": raw_score,
            "weight": weight,
            "weighted_score": weighted_score
        }
    
    # Normalize demographic score to 0-100 scale
    normalized_demographic_score = (total_weighted_score / TOTAL_MAX_WEIGHTED_SCORE) * 100
    
    # Calculate Likert domain scores
    likert_scores = {}
    for category, responses_list in likert_responses.items():
        max_score = len(responses_list) * 5
        total_score = sum(responses_list)
        likert_scores[f'{category}'] = (total_score / max_score) * 100
    
    # Combine all scores for overall evaluation
    all_scores = list(likert_scores.values()) + [normalized_demographic_score]
    overall_score = sum(all_scores) / len(all_scores)
    
    # Display results
    st.markdown("---")
    st.header("🎯 Evaluation Results")
    
    # Overall score with color coding
    if overall_score >= 80:
        color = "🟢"
        level = "Excellent"
    elif overall_score >= 70:
        color = "🟡"
        level = "Good"
    elif overall_score >= 60:
        color = "🟠"
        level = "Average"
    else:
        color = "🔴"
        level = "Needs Improvement"
    
    st.markdown(f"### {color} Overall Evaluation Score: **{overall_score:.1f}%** ({level})")
    
    # Score breakdown in columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Domain Scores")
        st.markdown(f"**Demographic Score:** {normalized_demographic_score:.1f}%")
        for category, score in likert_scores.items():
            st.markdown(f"**{category}:** {score:.1f}%")
    
    with col2:
        st.subheader("🔍 Demographic Breakdown")
        for question, data in demographic_breakdown.items():
            st.markdown(f"**{question.split('.')[0]}:** {data['response']} ({data['raw_score']} pts × {data['weight']} weight = {data['weighted_score']:.1f})")
    
    # Visualization
    st.subheader("📈 Score Visualization")
    
    # Prepare data for visualization
    chart_data = pd.DataFrame({
        "Domain": ["Demographics"] + list(likert_scores.keys()),
        "Score (%)": [normalized_demographic_score] + list(likert_scores.values())
    })
    
    # Create bar chart
    fig = px.bar(
        chart_data, 
        x="Domain", 
        y="Score (%)", 
        color="Score (%)",
        color_continuous_scale="RdYlGn",
        title="Entrepreneurial Evaluation Scores by Domain"
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=False
    )
    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations based on scores
    st.subheader("💡 Recommendations")
    
    low_scores = [(domain, score) for domain, score in 
                  list(likert_scores.items()) + [("Demographics", normalized_demographic_score)] 
                  if score < 70]
    
    if low_scores:
        st.warning("**Areas for Improvement:**")
        for domain, score in low_scores:
            if domain == "Demographics":
                st.markdown(f"- **{domain}** ({score:.1f}%): Consider improving technology access and business setup")
            else:
                st.markdown(f"- **{domain}** ({score:.1f}%): Focus on developing skills in this area")
    else:
        st.success("**Excellent performance across all domains!** Continue building on your strengths.")
    
    # Export option
    if st.button("📥 Export Results"):
        results_df = pd.DataFrame({
            "Domain": ["Demographics"] + list(likert_scores.keys()) + ["Overall"],
            "Score (%)": [normalized_demographic_score] + list(likert_scores.values()) + [overall_score]
        })
        st.download_button(
            label="Download Results as CSV",
            data=results_df.to_csv(index=False),
            file_name="entrepreneurship_evaluation_results.csv",
            mime="text/csv"
        )

# Information sidebar
with st.sidebar:
    st.header("ℹ️ About This Evaluation")
    st.markdown("""
    This comprehensive evaluation assesses women's entrepreneurial potential based on:
    
    **Demographic Factors (Weighted):**
    - Technology access (High importance)
    - Education level (High importance)  
    - Business motivation (High importance)
    - Income progression (Highest importance)
    - Age and experience (Moderate importance)
    
    **Entrepreneurial Indicators:**
    - Intention and attitude
    - Training and education received
    - Mentorship and networking
    - Economic and social empowerment
    
    **Scoring System:**
    - 90-100: Exceptional potential
    - 80-89: High potential
    - 70-79: Good potential
    - 60-69: Moderate potential
    - Below 60: Needs development
    """) 