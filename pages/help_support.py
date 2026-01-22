import streamlit as st
import time
import database as db

# Page configuration
st.set_page_config(page_title="Help & Support", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05070A; color: #F8FAFC; }
    .stMetric { 
        background-color: #111827; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #1E293B; 
    }
    </style>
    """, unsafe_allow_html=True)

# Back button in sidebar
if st.sidebar.button("← Back to Main App"):
    st.switch_page("app.py")

# Tab-based navigation
tab1, tab2, tab3 = st.tabs(["❓ FAQ", "📞 Contact Support", "💬 Send Feedback"])

# Tab 1: FAQ
with tab1:
    st.header("❓ Frequently Asked Questions")
    
    faqs = {
        "What is AI Service Desk?": 
            "AI Service Desk is an intelligent ticket management system that uses artificial intelligence (BERT + SVM ensemble) to automatically categorize IT support tickets into 8 categories: Access, Administrative Rights, Hardware, HR Support, Internal Project, Miscellaneous, Purchase, and Storage.",
        
        "How does the AI categorization work?": 
            "The system uses a hybrid ensemble approach combining:\n- **BERT**: Advanced language model (60% weight) for deep semantic understanding\n- **SVM**: Support Vector Machine with TF-IDF (40% weight) for statistical pattern matching\n- **Weighted Soft Voting**: Combines both models with 60/40 weighting for accurate predictions",
        
        "What are the ticket statuses?": 
            "Tickets flow through these statuses:\n- **Open**: Initial state when created\n- **In Progress**: Support team is working on it\n- **Resolved**: Issue has been fixed\n- **Closed**: Resolved tickets auto-close after 24 hours",
        
        "What is SLA Status?": 
            "SLA (Service Level Agreement) Status shows response time:\n- 🟢 **On Track**: < 2 hours (within SLA)\n- 🟡 **Warning**: 2-6 hours (approaching SLA breach)\n- 🔴 **Breached**: > 6 hours (SLA violated)",
        
        "Who can see my tickets?": 
            "General Users can only see their own tickets. Support Staff and Administrators can see all tickets in the system with filtering options.",
        
        "Can I delete my tickets?": 
            "No, General Users cannot delete tickets. Only Support Staff and Administrators can delete tickets for cleanup.",
        
        "How is urgency determined?": 
            "Urgency is automatically detected based on keywords in your description:\n- **High**: Contains keywords like 'urgent', 'broken', 'emergency', 'critical', 'down', 'outage', 'crash', 'severe'\n- **Standard**: Regular tickets without urgent indicators",
        
        "What languages are supported?": 
            "Currently, only English is supported. Tickets in other languages will be rejected.",
        
        "How long does AI categorization take?": 
            "Usually less than 1-2 seconds. The AI analyzes your text and immediately assigns a category and confidence score.",
        
        "What if the AI confidence is low?": 
            "If confidence is below 45%, the ticket is marked for 'Requires Manual Review'. Support staff will review and manually assign the correct category.",
    }
    
    for question, answer in faqs.items():
        with st.expander(f"❓ {question}"):
            st.write(answer)

# Tab 2: Contact Support
with tab2:
    st.header("📞 Contact Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📧 Email Support")
        st.write("**Primary Contact:** support@servicedesk.com")
        st.write("**Response Time:** Within 24 hours")
        st.write("**Hours:** Monday - Friday, 9 AM - 6 PM")
    
    with col2:
        st.subheader("📱 Live Chat")
        st.write("**Available:** Monday - Friday, 10 AM - 5 PM")
        st.write("**Average Wait:** 5-10 minutes")
        st.write("⚠️ *Feature coming soon*")
    
    st.divider()
    
    st.subheader("🔧 Troubleshooting")
    troubleshooting = {
        "Ticket not appearing in dashboard": "Try refreshing the page (F5). If still not visible, contact support with your Ticket ID.",
        "AI categorized my ticket incorrectly": "The support team will manually review and recategorize. You can also provide feedback below.",
        "Cannot login": "Verify your Employee/User ID and Full Name match your records. Contact IT if the issue persists.",
        "Urgent issue needs immediate attention": "Mark your ticket with 'urgent' in the description for High priority flagging.",
    }
    
    for issue, solution in troubleshooting.items():
        with st.expander(f"🔧 {issue}"):
            st.write(solution)

# Tab 3: Send Feedback
with tab3:
    st.header("💬 Send Us Your Feedback")
    st.write("Your feedback helps us improve the AI Service Desk system. All feedback is saved and reviewed by our team.")
    
    # Initialize feedback table
    db.init_feedback_table()
    
    # Get user info from session state
    user_id = st.session_state.get('user_id', 'Anonymous')
    user_name = st.session_state.get('user_name', 'Unknown')
    
    with st.form("feedback_form"):
        st.subheader("Feedback Details")
        
        feedback_type = st.selectbox(
            "Feedback Type",
            ["Bug Report", "Feature Request", "General Feedback", "AI Categorization Issue", "Other"]
        )
        
        message = st.text_area(
            "Your Message",
            placeholder="Please describe your feedback in detail...",
            height=150
        )
        
        rating = st.slider(
            "Rate Your Experience",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Poor, 5 = Excellent"
        )
        
        email = st.text_input(
            "Email Address (optional)",
            value=user_id if user_id != 'Anonymous' else "",
            placeholder="your.email@company.com"
        )
        
        submit_feedback = st.form_submit_button("Submit Feedback", use_container_width=True)
        
        if submit_feedback:
            if message.strip():
                try:
                    db.add_feedback(
                        user_id=user_id,
                        user_name=user_name,
                        email=email,
                        feedback_type=feedback_type,
                        message=message,
                        rating=rating
                    )
                    st.success("✅ Thank you! Your feedback has been saved and will be reviewed by our team.")
                    st.info("📧 Our team will analyze your feedback and use it to improve the system.")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving feedback: {str(e)}")
            else:
                st.warning("⚠️ Please enter your feedback message.")
    
    st.divider()
    st.subheader("💡 Why Your Feedback Matters")
    st.markdown("""
    - ✅ **Improves AI Accuracy**: Your categorization feedback helps retrain models
    - ✅ **Feature Development**: Popular requests are prioritized for development
    - ✅ **Bug Fixes**: Bug reports help us identify and fix issues faster
    - ✅ **User Experience**: Your suggestions make the system more user-friendly
    """)
