import streamlit as st
import pandas as pd

st.title("Stakeholder Engagement & Participation Plan")

# Initialize session state for tracking
if 'step' not in st.session_state: st.session_state.step = 1
if 'plan' not in st.session_state: st.session_state.plan = []
if 'temp_data' not in st.session_state: st.session_state.temp_data = {}

# --- EXACT CHARACTERIZATION LOGIC (STEP 2A) ---
def determine_stakeholder_type(affected, affects, wants, can):
    if affected == 'Yes' and affects == 'Yes' and wants == 'Yes' and can == 'Yes':
        return "Standard Stakeholder"
    elif affected == 'Yes' and affects == 'No' and wants == 'Yes' and can == 'No':
        return "Silent stakeholder"
    elif affected == 'Yes' and affects == 'Yes' and wants == 'Yes' and can == 'No':
        return "Standard Stakeholder (unable to participate)"
    elif affected == 'Yes' and affects == 'No' and wants == 'Yes' and can == 'Yes':
        return "Interested Stakeholder"
    elif affected == 'Yes' and affects == 'Yes' and wants == 'No' and can == 'No':
        return "Unwilling Stakeholder with influence (unable to participate) or Fiduciary's client"
    elif affected == 'Yes' and affects == 'No' and wants == 'No' and can == 'Yes':
        return "Unwilling Stakeholder without influence"
    elif affected == 'Yes' and affects == 'Yes' and wants == 'No' and can == 'Yes':
        return "Unwilling Stakeholder with influence or Fiduciary's client"
    elif affected == 'Yes' and affects == 'No' and wants == 'No' and can == 'No':
        return "Unwilling Stakeholder without influence (unable to participate)"
    elif affected == 'No' and affects == 'Yes' and wants == 'Yes' and can == 'No':
        return "Fiduciary Stakeholder (unable to participate)"
    elif affected == 'No' and affects == 'Yes' and wants == 'No' and can == 'Yes':
        return "Unwilling fiduciary stakeholder"
    elif affected == 'No' and affects == 'Yes' and wants == 'Yes' and can == 'Yes':
        return "Fiduciary Stakeholder"
    elif affected == 'No' and affects == 'Yes' and wants == 'No' and can == 'No':
        return "Unwilling fiduciary stakeholder (unable to participate)"
    elif affected == 'No' and affects == 'No':
        return "Not a stakeholder"
    else:
        return "Other Stakeholder"

# --- COMPREHENSIVE PARTICIPATION LEVEL & TECHNIQUE LOGIC (MATCHING THE AUTOMATED MATRIX) ---
def get_participation_plan(st_type, alliance, expertise, power, other, time):
    # Standard Stakeholder Rules
    if "Standard Stakeholder" in st_type:
        if alliance == "Ally":
            if expertise == "Yes":
                if power == "Yes":
                    if other == "Yes" and time == "Yes":
                        return "Co-decision", "Workshops / Deliberative forums / Joint committees"
                    elif other == "Yes" and time == "No":
                        return "Collaboration", "Working groups with flexible timelines"
                    elif other == "No" and time == "Yes":
                        return "Co-decision", "Joint steering committees"
                    else:
                        return "Collaboration", "Joint working groups"
                else: # Power == "No"
                    return "Collaboration", "Consultation workshops / Focus groups"
            else: # Expertise == "No"
                return "Consultation", "Public consultations / Surveys"
        elif alliance == "Potential ally":
            return "Collaboration", "Bilateral meetings / Constructive dialogues"
        else: # Blind resources / Unwilling / Other
            return "Consultation / Information", "Targeted briefings / Impact mitigation reviews"

    # Interested Stakeholder Rules
    elif "Interested Stakeholder" in st_type:
        if alliance == "Ally":
            if expertise == "Yes":
                return "Collaboration", "Expert panels / Stakeholder advisory committees"
            else:
                return "Consultation", "Public surveys / Information sessions"
        else:
            return "Consultation", "Open forums / Information feedback channels"

    # Fiduciary Stakeholder Rules
    elif "Fiduciary Stakeholder" in st_type:
        if alliance == "Ally":
            return "Co-decision / Consultation", "Formal institutional coordination meetings"
        else:
            return "Consultation", "Official hearings / Compliance reporting"

    # Unwilling Stakeholder Rules
    elif "Unwilling Stakeholder" in st_type or "Unwilling fiduciary" in st_type:
        return "Information / Impact Management", "Targeted transparency reporting / Conflict mitigation framework"

    # Silent Stakeholder Rules
    elif "Silent stakeholder" in st_type:
        return "Consultation", "Proactive outreach / Targeted interviews / Surveys"

    # Default fallback mapping
    else:
        if power == "Yes":
            return "Collaboration", "Bilateral discussions / Negotiation sessions"
        else:
            return "Information", "Public newsletters / Informational reports / Website updates"

# --- SIDEBAR DISPLAY FOR CURRENT PLAN ---
if len(st.session_state.plan) > 0:
    st.sidebar.subheader("📋 Current plan")
    sidebar_df = pd.DataFrame(st.session_state.plan)
    sidebar_df.index = range(1, len(sidebar_df) + 1)
    st.sidebar.dataframe(sidebar_df[['Name', 'Type of Stakeholder', 'Level of Participation']])
    
    if st.sidebar.button("🔄 Back to full plan / Export"):
        st.session_state.step = 4
        st.rerun()
    if st.sidebar.button("➕ Add another stakeholder"):
        st.session_state.temp_data = {}  # Reset temp data for a clean form
        st.session_state.step = 1
        st.rerun()
    st.sidebar.divider()

# --- STEP 1: CHARACTERIZATION (QUESTIONS) ---
if st.session_state.step == 1:
    st.header("Step 1: Characterize Stakeholder")
    
    # Retrieve pre-filled values if returning from step 1.5
    saved_name = st.session_state.temp_data.get('Name', '')
    saved_affected = st.session_state.temp_data.get('Affected', 'Yes')
    saved_affects = st.session_state.temp_data.get('Affects', 'Yes')
    saved_wants = st.session_state.temp_data.get('Wants', 'Yes')
    saved_can = st.session_state.temp_data.get('Can', 'Yes')

    affected_options = ["Yes", "No"]
    affects_options = ["Yes", "No"]
    wants_options = ["Yes", "No"]
    can_options = ["Yes", "No"]

    with st.form("stage1"):
        name = st.text_input("Name of the Stakeholder", value=saved_name)
        affected = st.selectbox("Is this stakeholder affected by the issue or project?", affected_options, index=affected_options.index(saved_affected) if saved_affected in affected_options else 0)
        affects = st.selectbox("Does this stakeholder affect the issue or project?", affects_options, index=affects_options.index(saved_affects) if saved_affects in affects_options else 0)
        wants = st.selectbox("Does this stakeholder want to participate in the decision process?", wants_options, index=wants_options.index(saved_wants) if saved_wants in wants_options else 0)
        can = st.selectbox("Can this stakeholder participate in the decision process?", can_options, index=can_options.index(saved_can) if saved_can in can_options else 0)
        
        if st.form_submit_button("Determine Stakeholder Type"):
            if name.strip() == "":
                st.warning("Please enter a stakeholder name.")
            else:
                st_type = determine_stakeholder_type(affected, affects, wants, can)
                st.session_state.temp_data = {
                    'Name': name, 
                    'Affected': affected, 
                    'Affects': affects, 
                    'Wants': wants, 
                    'Can': can,
                    'Type of Stakeholder': st_type
                }
                st.session_state.step = 1.5
                st.rerun()

# --- STEP 1.5: DISPLAY STAKEHOLDER TYPE BEFORE STEP 2 ---
elif st.session_state.step == 1.5:
    st.header("Step 1 Result: Stakeholder Classification")
    st.info(f"The stakeholder **{st.session_state.temp_data['Name']}** is characterized as:")
    
    st.markdown(f"### 🎯 Type : `{st.session_state.temp_data['Type of Stakeholder']}`")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➡️ Continue to step 2 (Resources & Alliance)"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("⬅️ Modify the answers from step 1"):
            st.session_state.step = 1
            st.rerun()

# --- STEP 2: RESOURCES & PLAN ---
elif st.session_state.step == 2:
    st.header(f"Step 2: Refine for {st.session_state.temp_data['Name']}")
    st.write(f"Current Type: **{st.session_state.temp_data['Type of Stakeholder']}**")
    
    with st.form("stage2"):
        alliance = st.selectbox("Potential for alliance", ["Ally", "Potential ally", "Blind resources"])
        expertise = st.selectbox("Useful expertise?", ["Yes", "No"])
        power = st.selectbox("Power to influence the project (positively or negatively)?", ["Yes", "No"])
        other = st.selectbox("Other important aspect?", ["Yes", "No"])
        time = st.selectbox("Time available?", ["Yes", "No"])
        
        col1, col2 = st.columns(2)
        submit_btn = col1.form_submit_button("Generate Recommendation")
        back_btn = col2.form_submit_button("⬅️ Back to type")

        if back_btn:
            st.session_state.step = 1.5
            st.rerun()
            
        if submit_btn:
            st_type = st.session_state.temp_data['Type of Stakeholder']
            level, technique = get_participation_plan(st_type, alliance, expertise, power, other, time)
            
            final_entry = {
                **st.session_state.temp_data, 
                'Alliance': alliance, 
                'Useful Expertise': expertise,
                'Power': power,
                'Other Aspect': other, 
                'Time Available': time, 
                'Level of Participation': level, 
                'Participatory Technique': technique
            }
            
            st.session_state.plan.append(final_entry)
            st.session_state.temp_data = {}  # Reset temporary inputs
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: ADD ANOTHER? ---
elif st.session_state.step == 3:
    st.success("Stakeholder added successfully!")
    
    st.subheader("Last stakeholder added:")
    latest_df = pd.DataFrame([st.session_state.plan[-1]])
    latest_df.index = [len(st.session_state.plan)]
    st.dataframe(latest_df)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add another stakeholder"):
            st.session_state.temp_data = {}
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("🏁 Finish and View Full Plan"):
            st.session_state.step = 4
            st.rerun()

# --- FINAL DISPLAY ---
elif st.session_state.step == 4:
    st.subheader("Final Participation Plan")
    df = pd.DataFrame(st.session_state.plan)
    df.index = range(1, len(df) + 1)
    st.dataframe(df)
    
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=True).encode('utf-8')
        st.download_button("📥 Download Plan as CSV", csv, "participation_plan.csv", "text/csv")
    with col2:
        if st.button("➕ Add another stakeholder (back)"):
            st.session_state.temp_data = {}
            st.session_state.step = 1
            st.rerun()