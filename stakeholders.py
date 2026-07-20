import streamlit as st
import pandas as pd

st.title("Stakeholder Engagement & Participation Plan")

# Initialize session state for tracking
if 'step' not in st.session_state: st.session_state.step = 1
if 'plan' not in st.session_state: st.session_state.plan = []

# --- LOGIC FUNCTION ---
def get_participation_plan(data):
    # This logic maps your characterization to the Engagement/Participation framework
    if data['Affected'] == 'Yes' and data['Affects'] == 'Yes' and data['Expertise'] == 'Yes':
        return "Co-decision", "Workshops / Deliberative forums"
    elif data['Affected'] == 'Yes' and data['Affects'] == 'No':
        return "Collaboration", "Consultation meetings / Surveys"
    else:
        return "Information", "Newsletters / Website / Reports"

# --- STEP 1: CHARACTERIZATION ---
if st.session_state.step == 1:
    st.header("Step 1: Characterize Stakeholder")
    with st.form("stage1"):
        name = st.text_input("Name of the Stakeholder")
        affected = st.selectbox("Is this stakeholder affected?", ["Yes", "No"])
        affects = st.selectbox("Does this stakeholder affect the project?", ["Yes", "No"])
        wants = st.selectbox("Wants to participate?", ["Yes", "No"])
        can = st.selectbox("Can this stakeholder participate?", ["Yes", "No"])
        
        if st.form_submit_button("Next: Define Resources"):
            st.session_state.temp_data = {'Name': name, 'Affected': affected, 'Affects': affects, 'Wants': wants, 'Can': can}
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: RESOURCES & PLAN ---
elif st.session_state.step == 2:
    st.header(f"Step 2: Refine for {st.session_state.temp_data['Name']}")
    with st.form("stage2"):
        alliance = st.selectbox("Potential for alliance", ["Ally", "Potential ally", "Blind resources"])
        expertise = st.selectbox("Useful expertise?", ["Yes", "No"])
        power = st.selectbox("Power to influence?", ["Yes", "No"])
        other = st.selectbox("Other important aspect?", ["Yes", "No"])
        time = st.selectbox("Time available?", ["Yes", "No"])
        
        if st.form_submit_button("Generate Recommendation"):
            data = {**st.session_state.temp_data, 'Expertise': expertise, 'Power': power}
            level, technique = get_participation_plan(data)
            
            final_entry = {**data, 'Alliance': alliance, 'Other': other, 'Time': time, 
                           'Level of Participation': level, 'Participatory Technique': technique}
            
            st.session_state.plan.append(final_entry)
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: ADD ANOTHER? ---
elif st.session_state.step == 3:
    st.success("Stakeholder added to the plan!")
    if st.button("Add another stakeholder"):
        st.session_state.step = 1
        st.rerun()
    if st.button("Finish and View Plan"):
        st.session_state.step = 4
        st.rerun()

# --- FINAL DISPLAY ---
if st.session_state.step == 4:
    st.subheader("Final Participation Plan")
    df = pd.DataFrame(st.session_state.plan)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Plan as CSV", csv, "participation_plan.csv", "text/csv")