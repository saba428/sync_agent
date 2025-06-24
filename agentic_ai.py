import streamlit as st

class RoutineAgent:
    # Global Routine (Sabke liye same)
    global_routine = {
        "lunch_time": "1:00 PM",
        "meeting_time": "11:00 AM"
    }
    
    def __init__(self, name, mode="agent"):
        self.name = name
        self.mode = mode
        if 'personal_routine' not in st.session_state:
            st.session_state.personal_routine = {}
    
    def add_task(self, task, time):
        st.session_state.personal_routine[task] = time
        return f"✅ {task} added at {time}"
    
    def check_schedule(self, task):
        if self.mode == "agent":
            return self._check_agent(task)
        elif self.mode == "global":
            return self._check_global(task)
        else: # hybrid
            return self._check_hybrid(task)
    
    def _check_agent(self, task):
        if task in st.session_state.personal_routine:
            return f"{self.name} ka {task}: {st.session_state.personal_routine[task]}"
        return f"{self.name} ke paas yeh task nahi hai"
    
    def _check_global(self, task):
        if task in self.global_routine:
            return f"Company ka {task}: {self.global_routine[task]}"
        return "Yeh company rule nahi hai"
    
    def _check_hybrid(self, task):
        agent_result = self._check_agent(task)
        global_result = self._check_global(task)
        return f"PERSONAL: {agent_result}\nGLOBAL: {global_result}"

# Streamlit UI
st.title("🚀 3-Tarike ka Agent")

# 1. Agent Creation
col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox(
        "Agent Type",
        ["agent", "global", "hybrid"],
        help="Agent: Personal, Global: Company, Hybrid: Dono"
    )
with col2:
    name = st.text_input("Agent Name")

if st.button("Create Agent"):
    st.session_state.agent = RoutineAgent(name, mode)
    st.success(f"{name} ({mode}) agent created!")

# 2. Task Management
if 'agent' in st.session_state:
    st.subheader("Add Task" if mode == "agent" else "Add Data")
    task = st.text_input("Task/Rule Name")
    time = st.text_input("Time")
    
    if st.button("Save"):
        result = st.session_state.agent.add_task(task, time)
        st.success(result)
    
    # 3. Schedule Check
    st.subheader("Check Schedule")
    check_task = st.text_input("What to check?")
    
    if st.button("Check"):
        result = st.session_state.agent.check_schedule(check_task)
        st.info(result)

    # Current Data Display
    with st.expander("Show Current Data"):
        st.write("Personal Tasks:", st.session_state.personal_routine)
        st.write("Global Rules:", RoutineAgent.global_routine) 


