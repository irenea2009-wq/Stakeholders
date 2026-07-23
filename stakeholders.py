import streamlit as st
import pandas as pd

st.title("Stakeholder Engagement & Participation Plan")

# Initialize session state for tracking
if 'step' not in st.session_state: st.session_state.step = 1
if 'plan' not in st.session_state: st.session_state.plan = []

# --- EXACT CHARACTERIZATION LOGIC BASED ON YOUR TABLE ---
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

# --- RECOMMENDATION / PARTICIPATION PLAN LOGIC ---
def get_participation_plan(st_type, alliance, expertise, power, other, time):
    if "Standard Stakeholder" in st_type:
        if expertise == 'Yes' and power == 'Yes':
            return "Co-decision", "Workshops / Deliberative forums / Joint committees"
        else:
            return "Collaboration", "Working groups / Joint project design"
    elif "Interested Stakeholder" in st_type:
        return "Collaboration", "Consultation meetings / Focus groups / Surveys"
    elif "Fiduciary Stakeholder" in st_type:
        return "Consultation", "Public hearings / Formal feedback sessions"
    elif "Unwilling Stakeholder" in st_type:
        return "Information / Impact Management", "Targeted communication / Mitigation reporting"
    elif "Silent stakeholder" in st_type:
        return "Consultation", "Proactive outreach / Surveys / Informational interviews"
    else:
        return "Information", "Newsletters / Website / Public updates"

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
        st.session_state.step = 1
        st.rerun()
    st.sidebar.divider()

# --- STEP 1: CHARACTERIZATION (QUESTIONS) ---
if st.session_state.step == 1:
    st.header("Step 1: Characterize Stakeholder")
    with st.form("stage1"):
        name = st.text_input("Name of the Stakeholder")
        affected = st.selectbox("Is this stakeholder affected by the issue or project?", ["Yes", "No"])
        affects = st.selectbox("Does this stakeholder affect the issue or project?", ["Yes", "No"])
        wants = st.selectbox("Does this stakeholder want to participate in the decision process?", ["Yes", "No"])
        can = st.selectbox("Can this stakeholder participate in the decision process?", ["Yes", "No"])
        
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
                # On passe à une nouvelle étape intermédiaire (Étape 1B) pour afficher le type
                st.session_state.step = 1.5
                st.rerun()

# --- STEP 1.5: DISPLAY STAKEHOLDER TYPE BEFORE STEP 2 ---
elif st.session_state.step == 1.5:
    st.header("Step 1 Result: Stakeholder Classification")
    st.info(f"Le stakeholder **{st.session_state.temp_data['Name']}** is characterized as :")
    
    st.markdown(f"### 🎯 Type : `{st.session_state.temp_data['Type of Stakeholder']}`")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➡️ Continue to step 2 (Ressources & Alliance)"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("⬅️ Modify answers from step 1"):
            st.session_state.step = 1
            st.rerun()

# --- STEP 2: RESOURCES & PLAN ---
elif st.session_state.step == 2:
    st.header(f"Step 2: Refine for {st.session_state.temp_data['Name']}")
    st.write(f"Type actuel : **{st.session_state.temp_data['Type of Stakeholder']}**")
    
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
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: ADD ANOTHER? ---
elif st.session_state.step == 3:
    st.success("Stakeholder added successfully!")
    
    st.subheader("Last stakeholder added :")
    latest_df = pd.DataFrame([st.session_state.plan[-1]])
    latest_df.index = [len(st.session_state.plan)]
    st.dataframe(latest_df)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add another stakeholder"):
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
            st.session_state.step = 1
            st.rerun()