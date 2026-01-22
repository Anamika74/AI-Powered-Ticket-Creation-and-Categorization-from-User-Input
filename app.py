import time
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import database as db  
from engine_wrapper import ProfessionalTicketEngine

# 1. Initialize Database and AI Engine

db.init_db()
db.init_feedback_table()
db.init_comments_table()
db.init_preferences_table()
db.init_model_feedback_table() 
@st.cache_resource
def load_engine():
    return ProfessionalTicketEngine(
        bert_path="Kaggle Dataset/models/final_bert_model",
        svm_path="Kaggle Dataset/models/svm_model.pkl",
        tfidf_path="Kaggle Dataset/models/tfidf_vectorizer.pkl"
    )
engine = load_engine()

# 2. Page Configuration & Styling
# 2. Page Configuration & Styling
st.set_page_config(page_title="AI Service Desk", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #05070A; color: #F8FAFC; }
    
    /* Analytics Cards */
    .stMetric { 
        background-color: #111827; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #1E293B; 
    }
    
    /* Highlighting Priority and SLA alerts */
    .priority-high { 
        color: #FF4B4B; 
        font-weight: bold; 
        text-shadow: 0 0 10px rgba(255,75,75,0.3); 
    }
    
    .sla-breached { 
        color: #FF0000; 
        font-weight: bold; 
        border: 1px solid #FF0000; 
        padding: 2px 5px; 
        border-radius: 5px; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Role-Based Session State
if 'role' not in st.session_state:
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.user_name = None

# 4. Global Analytics Header (Requirement 9 & 11)
# app.py

def show_top_metrics():
    try:
        # Auto-close tickets resolved for 24+ hours
        try:
            db.auto_close_resolved()
        except Exception as auto_close_err:
            pass  # Non-critical, continue anyway
        
        all_data = db.get_tickets()
        # If no tickets exist, don't try to create a DataFrame
        if not all_data:
            st.info("System Initialized: No tickets recorded yet.")
            return

        # Correct column mapping: id[0], ticket_id[1], user_id[2], user_name[3], title[4], desc[5], cat[6], priority[7], status[8], created_at[9]
        df = pd.DataFrame(all_data, columns=['id', 'ticket_id', 'user_id', 'user_name', 'title', 'description', 'category', 'priority', 'status', 'created_at'])
        
        # Display Metrics
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Tickets", len(df))
        c2.metric("Open Tickets", len(df[df['status'] == 'Open']))
        c3.metric("In Progress", len(df[df['status'] == 'In Progress']))
        c4.metric("Resolved", len(df[df['status'] == 'Resolved']))
        c5.metric("Closed", len(df[df['status'] == 'Closed']))
        st.divider()
    except Exception as e:
        # Debug the error
        st.error(f"Error loading metrics: {str(e)}")
        st.warning("Please refresh the page to retry.")

# --- LOGIN SCREEN REFINED ---
if not st.session_state.role:
    st.markdown("<h1 style='text-align:center;'>🛡️ AI Service Desk Login</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Using a form to prevent auto-login on text-entry
        with st.form("login_form"):
            role = st.selectbox("Select Your Role", ["General User", "Support Staff", "Administrator"])
            name = st.text_input("Full Name")
            emp_id = st.text_input("Employee/User ID")
            submit_login = st.form_submit_button("Access Dashboard") # Only runs on click

            if submit_login:
                if name and emp_id:
                    st.session_state.role = role
                    st.session_state.user_name = name
                    st.session_state.user_id = emp_id
                    st.rerun() # Successful login
                else:
                    st.error("Please provide all credentials.")

# --- AUTHORIZED DASHBOARDS ---
else:
    show_top_metrics()
    
    # SIDEBAR: User Info, Help & Support, Logout
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.write(f"**Role:** {st.session_state.role}")
        st.write(f"**ID:** {st.session_state.user_id}")
        
        st.divider()
        
        # Help & Support Link
        st.subheader("📚 Help & Support")
        if st.button("📖 Open Help & Support Page", use_container_width=True):
            st.switch_page("pages/help_support.py")
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.role = None
            st.rerun()

    # VIEW 1: General User (Requirement 1 & 3)
    if st.session_state.role == "General User":
        st.header("🆕 Raise a New IT Incident")
        
        # === KNOWLEDGE BASE ===
        with st.expander("📚 Knowledge Base - Common Solutions", expanded=False):
            kb = {
                "Access": "If you can't access a system or application: Check your credentials, reset password, or contact IT support.",
                "Hardware": "Hardware issues? Restart the device, check power/connections, or submit a ticket for repair.",
                "Storage": "Running out of storage? Clear temp files, archive old data, or request additional storage.",
                "Purchase": "To purchase IT equipment: Fill out purchase request form and send to procurement team.",
                "Administrative rights": "Need admin rights? Submit a request through IT Security portal with business justification.",
                "HR Support": "HR-related issues? Contact Human Resources directly or create a ticket for escalation.",
                "Internal Project": "Project management queries? Contact your project manager or tech lead.",
                "Miscellaneous": "For other issues: Describe your problem in detail so we can assist properly."
            }
            for category, solution in kb.items():
                st.markdown(f"**{category}:** {solution}")
        
        # Ticket Title
        t_title = st.text_input("📝 Ticket Title", placeholder="Brief summary of the issue (e.g., Cannot access email)")
        
        # Ticket Description
        t_desc = st.text_area("📋 Describe the technical issue...", height=150, placeholder="E.g., I cannot access the finance reports, my laptop won't connect to WiFi, etc.")
        
        if st.button("Execute AI Triage", use_container_width=True):
            if t_title and t_desc:
                with st.spinner("🤖 AI Analyzing..."):
                    result = engine.process_ticket(t_desc)
                    
                    # Check for validation errors
                    if result.get('error'):
                        st.error(f"❌ {result['error']}")
                    else:
                        # SAVE TO DB - only if not in "Requires Manual Review" status with very low confidence
                        if result['confidence'] >= 20:  # Only save if somewhat relevant
                            db.add_ticket(st.session_state.user_id, st.session_state.user_name, t_title, t_desc, result['category'], result['urgency'])
                            
                            # Show categorization details
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Category", result['category'])
                            col2.metric("Confidence", f"{result['confidence']:.1f}%")
                            col3.metric("Urgency", result['urgency'])
                            
                            # Show suggested solution from KB
                            if result['category'] in kb:
                                st.info(f"💡 **Suggested Solution:** {kb[result['category']]}")
                            
                            st.success("✅ Ticket logged successfully!")
                        else:
                            st.error("❌ Ticket rejected: Too low confidence. Please provide more details about your IT issue.")
            elif not t_title:
                st.warning("⚠️ Please provide a ticket title.")
            else:
                st.warning("⚠️ Please describe your technical issue.")
        
        # Show User's Personal History
        st.divider()
        st.subheader("📋 My Raised Tickets")
        user_tickets = db.get_tickets(st.session_state.user_id)
        if user_tickets:
            for t in user_tickets:
                # Mapping: id[0], ticket_id[1], user_id[2], user_name[3], title[4], desc[5], cat[6], priority[7], status[8], created_at[9]
                try:
                    ticket_id = t[1] if len(t) > 1 else "UNKNOWN"
                    title = t[4] if len(t) > 4 else "Untitled"
                    status = t[8] if len(t) > 8 else "Unknown"
                    description = t[5] if len(t) > 5 else ""
                    category = t[6] if len(t) > 6 else "Unknown"
                    priority = t[7] if len(t) > 7 else "Standard"
                    
                    with st.expander(f"🎫 {ticket_id} | {title} | Status: {status}"):
                        st.write(f"**Description:** {description}")
                        st.write(f"**Category:** {category} | **Priority:** {priority}")
                except Exception as e:
                    st.error(f"Error displaying ticket: {str(e)}")
        else:
            st.write("You haven't raised any tickets yet.")

    # VIEW 2: Support Staff / Admin (Requirement 2 & 10)
    else:
        st.header("🎧 Support Management Console")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎫 Support Management",
            "🔍 Search & Filter", 
            "📊 Feedback Analytics",
            "💬 Ticket Comments",
            "📈 Advanced Analytics"
        ])
        
        # ============= TAB 1: SUPPORT MANAGEMENT CONSOLE =============
        with tab1:
            st.subheader("🎫 Support Management Console")
            
            # Filter options for Support/Admin
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.multiselect("Filter by Status", ["Open", "In Progress", "Resolved", "Closed"], default=["Open", "In Progress"], key="tab1_status")
            with col2:
                filter_category = st.multiselect("Filter by Category", ["Access", "Administrative rights", "Hardware", "HR Support", "Internal Project", "Miscellaneous", "Purchase", "Storage"], key="tab1_category")
            with col3:
                show_archived = st.checkbox("Show Closed/Archived", value=False, key="tab1_archived")
        
            # Fetch all tickets from the database
            all_tickets = db.get_tickets()
            
            if not all_tickets:
                st.info("No tickets currently in the system.")
            else:
                # Apply filters
                filtered_tickets = []
                for t in all_tickets:
                    # Mapping: id[0], ticket_id[1], user_id[2], user_name[3], title[4], desc[5], cat[6], priority[7], status[8], created_at[9]
                    t_status = t[8]  # status is at index 8
                    t_category = t[6]  # category is at index 6
                    
                    # Apply status filter
                    if t_status not in filter_status and not (t_status == "Closed" and show_archived):
                        continue
                    
                    # Apply category filter - if no category filter selected, show all
                    if filter_category and t_category not in filter_category:
                        continue
                    
                    filtered_tickets.append(t)
                
                if not filtered_tickets:
                    st.info("No tickets match the current filters.")
                else:
                    st.write(f"**Showing {len(filtered_tickets)} of {len(all_tickets)} tickets**")
                    
                    # Create table header
                    cols = st.columns([0.8, 2, 2, 1, 1.2, 1.2, 1, 0.8])
                    cols[0].write("**ID**")
                    cols[1].write("**Title**")
                    cols[2].write("**Description**")
                    cols[3].write("**Category**")
                    cols[4].write("**SLA Status**")
                    cols[5].write("**Hours Open**")
                    cols[6].write("**Status**")
                    cols[7].write("**Action**")
                    st.divider()
                    
                    for t in filtered_tickets:
                        # TICKET DATA MAPPING: id[0], ticket_id[1], user_id[2], user_name[3], title[4], desc[5], cat[6], priority[7], status[8], created_at[9]
                        try:
                            t_id = t[0] if len(t) > 0 else 0
                            t_ticket_id = t[1] if len(t) > 1 else "UNKNOWN"
                            t_user_id = t[2] if len(t) > 2 else ""
                            t_user_name = t[3] if len(t) > 3 else ""
                            t_title = t[4] if len(t) > 4 else "Untitled"
                            t_desc = t[5] if len(t) > 5 else ""
                            t_cat = t[6] if len(t) > 6 else "Unknown"
                            t_prio = t[7] if len(t) > 7 else "Standard"
                            t_status = t[8] if len(t) > 8 else "Unknown"
                            t_time = t[9] if len(t) > 9 else ""
                        except Exception as e:
                            st.error(f"Error parsing ticket data: {str(e)}")
                            continue
                    
                        # --- SLA TIMER LOGIC ---
                        try:
                            created_time = datetime.strptime(str(t_time), '%Y-%m-%d %H:%M:%S.%f')
                        except:
                            created_time = datetime.strptime(str(t_time), '%Y-%m-%d %H:%M:%S')
                        
                        time_diff = datetime.now() - created_time
                        hours_open = time_diff.total_seconds() / 3600
                    
                        # Color code based on time
                        if hours_open < 2:
                            sla_icon, sla_label = "🟢", "On Track"
                            sla_color = "#00AA00"
                        elif hours_open < 6:
                            sla_icon, sla_label = "🟡", "Warning"
                            sla_color = "#FFAA00"
                        else:
                            sla_icon, sla_label = "🔴", "Breached"
                            sla_color = "#FF0000"
                    
                        # --- RENDER ROW ---
                        r = st.columns([0.8, 2, 2, 1, 1.2, 1.2, 1, 0.8])
                        r[0].write(f"🎫 {t_ticket_id}")
                        
                        # Safely handle None values
                        title_display = (t_title or "Untitled")[:30]
                        title_display += ("..." if len(t_title or "") > 30 else "")
                        r[1].write(title_display)
                        
                        desc_display = (t_desc or "No description")[:40]
                        desc_display += ("..." if len(t_desc or "") > 40 else "")
                        r[2].write(desc_display)
                        
                        r[3].write(t_cat or "Unknown")
                        
                        # Apply SLA color coding
                        r[4].markdown(f'<span style="color: {sla_color}; font-weight: bold;">{sla_icon} {sla_label}</span>', unsafe_allow_html=True)
                        r[5].write(f"{hours_open:.1f}h")
                    
                        # --- STATUS DROPDOWN ---
                        status_options = ["Open", "In Progress", "Resolved", "Closed"]
                        current_idx = status_options.index(t_status) if t_status in status_options else 0
                    
                        updated_status = r[6].selectbox("status", status_options, index=current_idx, 
                                                        key=f"status_{t_id}", label_visibility="collapsed")
                    
                        # --- UPDATE & DELETE BUTTONS ---
                        action_col = r[7]
                        col_update, col_delete = action_col.columns(2)
                        
                        if col_update.button("✓", key=f"update_{t_id}", help="Update status"):
                            db.update_status(t_id, updated_status)
                            st.success(f"Ticket #{t_id} updated to {updated_status}!")
                            time.sleep(0.5)
                            st.rerun()
                        
                        if col_delete.button("🗑️", key=f"delete_{t_id}", help="Delete ticket (Admin/Support only)"):
                            db.delete_ticket(t_id)
                            st.warning(f"Ticket #{t_id} has been deleted.")
                            time.sleep(0.5)
                            st.rerun()
                        
                        # === MODEL FEEDBACK TRACKING ===
                        with st.expander(f"🤖 Report AI Category Issue - {t_ticket_id}", expanded=False):
                            st.write(f"**Predicted:** {t_cat} | **User:** {t_user_name}")
                            correct_cat = st.selectbox("What should the category be?", 
                                                     ['Access', 'Administrative rights', 'Hardware', 
                                                      'HR Support', 'Internal Project', 'Miscellaneous', 
                                                      'Purchase', 'Storage'], key=f"feedback_{t_id}")
                            feedback_type = st.radio("Feedback Type", 
                                                   ["Wrong Category", "Misclassification", "Incorrect Priority"],
                                                   key=f"type_{t_id}")
                            
                            if st.button("📝 Submit Feedback", key=f"submit_feedback_{t_id}"):
                                db.add_model_feedback(t_id, t_cat, correct_cat, 0.5, feedback_type)
                                st.success("Thank you! Feedback recorded for model retraining.")
                        
                        # === PRIORITY OVERRIDE ===
                        with st.expander(f"⚡ Priority Override - {t_ticket_id}", expanded=False):
                            st.write(f"**Current Priority:** {t_prio}")
                            new_priority = st.selectbox("Set new priority", 
                                                       ["Low", "Standard", "High", "Critical"],
                                                       key=f"priority_{t_id}")
                            if st.button("✅ Override Priority", key=f"override_priority_{t_id}"):
                                db.update_priority(t_id, new_priority)
                                st.success(f"Priority changed to {new_priority}")
                                time.sleep(0.5)
                                st.rerun()
                        
                        st.divider()
            
            # Additional Admin Features
            st.subheader("📊 Advanced Management")
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("💡 **Auto-Close**: Resolved tickets automatically close after 24 hours.")
            
            with col2:
                if st.button("🔄 Refresh & Auto-Close Now"):
                    db.auto_close_resolved()
                    st.success("Auto-close process completed!")
                    time.sleep(0.5)
                    st.rerun()
        
        # ============= TAB 2: SEARCH & FILTERING =============
        with tab2:
            st.subheader("🔍 Search & Advanced Filtering")
            
            search_col1, search_col2 = st.columns(2)
            with search_col1:
                search_query = st.text_input("Search by title or description", key="admin_search_tab2")
            
            with search_col2:
                filter_status = st.multiselect("Filter by Status", 
                                              ["All", "Open", "In Progress", "Resolved", "Closed"], 
                                              default=["All"], key="admin_filter_status_tab2")
            
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                filter_category = st.multiselect("Filter by Category",
                                               ["All"] + ['Access', 'Administrative rights', 'Hardware', 
                                                        'HR Support', 'Internal Project', 'Miscellaneous', 
                                                        'Purchase', 'Storage'],
                                               default=["All"], key="admin_filter_cat_tab2")
            
            with filter_col2:
                date_from = st.date_input("From Date", key="admin_date_from_tab2")
                date_to = st.date_input("To Date", key="admin_date_to_tab2")
            
            # Build filter dict
            search_filters = {}
            if filter_status != ["All"]:
                search_filters["status"] = filter_status
            if filter_category != ["All"]:
                search_filters["category"] = filter_category
            if date_from and date_to:
                search_filters["date_from"] = date_from
                search_filters["date_to"] = date_to
            
            # Perform search
            if search_query or search_filters:
                try:
                    search_results = db.search_tickets(search_query if search_query else "", search_filters)
                    st.success(f"Found {len(search_results)} tickets")
                    
                    if search_results:
                        st.dataframe(pd.DataFrame(search_results, columns=['ID', 'Ticket ID', 'User', 'Title', 
                                                                           'Description', 'Category', 'Priority', 
                                                                           'Status', 'Created']), use_container_width=True)
                except Exception as e:
                    st.error(f"Search error: {str(e)}")
            
            # === BULK OPERATIONS ===
            st.divider()
            st.subheader("📋 Bulk Operations")
            
            bulk_col1, bulk_col2 = st.columns(2)
            with bulk_col1:
                bulk_ids = st.text_input("Enter Ticket IDs (comma-separated)", key="bulk_ids_tab2")
                bulk_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"], key="bulk_status_tab2")
            
            with bulk_col2:
                if st.button("✅ Bulk Update Status", key="bulk_update_tab2"):
                    if bulk_ids:
                        id_list = [int(x.strip()) for x in bulk_ids.split(",") if x.strip().isdigit()]
                        try:
                            db.bulk_update_status(id_list, bulk_status)
                            st.success(f"Updated {len(id_list)} tickets to '{bulk_status}'")
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                if st.button("🗑️ Bulk Delete", key="bulk_delete_tab2"):
                    if bulk_ids and st.checkbox("Confirm deletion", key="confirm_delete_tab2"):
                        id_list = [int(x.strip()) for x in bulk_ids.split(",") if x.strip().isdigit()]
                        try:
                            db.bulk_delete(id_list)
                            st.success(f"Deleted {len(id_list)} tickets")
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            # === EXPORT FUNCTIONALITY ===
            st.divider()
            st.subheader("📥 Export Data")
            
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("📊 Export All Tickets to CSV", key="export_tickets_tab2"):
                    try:
                        all_tickets = db.get_tickets()
                        df = pd.DataFrame(all_tickets, columns=['ID', 'Ticket ID', 'User ID', 'User Name', 
                                                               'Title', 'Description', 'Category', 'Priority', 
                                                               'Status', 'Created At'])
                        csv = df.to_csv(index=False)
                        st.download_button("Download Tickets CSV", csv, "tickets_export.csv", "text/csv", key="download_tickets_tab2")
                    except Exception as e:
                        st.error(f"Export error: {str(e)}")
            
            with export_col2:
                if st.button("📊 Export All Feedback to CSV", key="export_feedback_tab2"):
                    try:
                        all_feedback = db.get_all_feedback()
                        df = pd.DataFrame(all_feedback, columns=['ID', 'User ID', 'User Name', 'Email', 
                                                                'Type', 'Message', 'Rating', 'Created At'])
                        csv = df.to_csv(index=False)
                        st.download_button("Download Feedback CSV", csv, "feedback_export.csv", "text/csv", key="download_feedback_tab2")
                    except Exception as e:
                        st.error(f"Export error: {str(e)}")
        
        # ============= TAB 3: FEEDBACK ANALYTICS =============
        with tab3:
            st.subheader("📊 Feedback Analytics")
            
            try:
                all_feedback = db.get_all_feedback()
                if all_feedback:
                    df_feedback = pd.DataFrame(all_feedback, columns=['ID', 'User ID', 'User Name', 'Email', 
                                                                     'Type', 'Message', 'Rating', 'Created At'])
                    
                    # Metrics
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Total Feedback", len(df_feedback))
                    with metric_col2:
                        avg_rating = df_feedback['Rating'].mean() if 'Rating' in df_feedback.columns else 0
                        st.metric("Average Rating", f"{avg_rating:.1f}/5")
                    with metric_col3:
                        st.metric("Feedback Types", df_feedback['Type'].nunique())
                    
                    # Feedback by type
                    if 'Type' in df_feedback.columns:
                        feedback_by_type = df_feedback['Type'].value_counts()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.bar_chart(feedback_by_type)
                        with col2:
                            st.write("**Feedback Distribution:**")
                            for ftype, count in feedback_by_type.items():
                                st.write(f"- {ftype}: {count}")
                    
                    # Detailed feedback table
                    st.write("**Recent Feedback:**")
                    st.dataframe(df_feedback.sort_values('Created At', ascending=False).head(20), 
                               use_container_width=True)
                else:
                    st.info("No feedback yet")
            except Exception as e:
                st.error(f"Feedback dashboard error: {str(e)}")
        
        # ============= TAB 4: TICKET COMMENTS =============
        with tab4:
            st.subheader("💬 Ticket Comments Management")
            
            comment_col1, comment_col2 = st.columns(2)
            with comment_col1:
                comment_ticket_id = st.text_input("Enter Ticket ID (e.g., TK000001 or ticket number)", key="comment_ticket_id_tab4", placeholder="Search by ticket ID...")
            
            with comment_col2:
                if st.button("🔍 Search Ticket", key="search_ticket_tab4"):
                    if comment_ticket_id:
                        all_tickets = db.get_tickets()
                        found_ticket = None
                        for t in all_tickets:
                            # t[1] is ticket_id
                            if str(t[1]).lower() == str(comment_ticket_id).lower() or str(t[0]) == str(comment_ticket_id):
                                found_ticket = t
                                break
                        
                        if found_ticket:
                            st.session_state.selected_comment_ticket = found_ticket
                            st.success(f"✅ Found Ticket: {found_ticket[1]}")
                        else:
                            st.error(f"❌ Ticket not found: {comment_ticket_id}")
            
            # Display selected ticket info
            if hasattr(st.session_state, 'selected_comment_ticket'):
                ticket = st.session_state.selected_comment_ticket
                st.info(f"**Selected Ticket:** {ticket[1]} | **Title:** {ticket[4]} | **Status:** {ticket[8]}")
                
                is_internal = st.checkbox("Internal Note (visible to support staff only)", key="is_internal_comment_tab4")
                
                comment_text = st.text_area("Add Comment", key="comment_text_tab4")
                
                if st.button("➕ Add Comment", key="add_comment_tab4"):
                    if comment_text:
                        try:
                            db.add_comment(ticket[0], st.session_state.user_id, 
                                         st.session_state.user_name, comment_text, int(is_internal))
                            st.success("Comment added!")
                            del st.session_state.selected_comment_ticket
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error adding comment: {str(e)}")
            else:
                st.info("👉 Enter a Ticket ID and click 'Search Ticket' to get started")
        
        # ============= TAB 5: ADVANCED ANALYTICS =============
        with tab5:
            st.subheader("📈 Advanced Analytics")
            
            try:
                all_tickets = db.get_tickets()
                if all_tickets:
                    df_all = pd.DataFrame(all_tickets, columns=['ID', 'Ticket ID', 'User ID', 'User Name', 
                                                               'Title', 'Description', 'Category', 'Priority', 
                                                               'Status', 'Created At'])
                    
                    analytics_col1, analytics_col2 = st.columns(2)
                    
                    with analytics_col1:
                        st.write("**Tickets by Category:**")
                        cat_counts = df_all['Category'].value_counts()
                        st.bar_chart(cat_counts)
                    
                    with analytics_col2:
                        st.write("**Tickets by Status:**")
                        status_counts = df_all['Status'].value_counts()
                        st.bar_chart(status_counts)
                    
                    # Priority distribution
                    st.write("**Tickets by Priority:**")
                    priority_counts = df_all['Priority'].value_counts()
                    st.bar_chart(priority_counts)
                    
                    # Time-based analysis
                    st.write("**Tickets Created Over Time:**")
                    if df_all['Created At'].dtype == 'object':
                        df_all['Created At'] = pd.to_datetime(df_all['Created At'], errors='coerce')
                    df_all['Date'] = df_all['Created At'].dt.date
                    time_series = df_all.groupby('Date').size()
                    st.line_chart(time_series)
                    
            except Exception as e:
                st.error(f"Analytics error: {str(e)}")



# Requirement 9: Refresh the app every 30 seconds to update SLA timers and metrics
st.empty() 
time.sleep(0.1) # Prevents excessive CPU usage
# Optional: Use a fragment or specific timer for auto-refresh if desired.