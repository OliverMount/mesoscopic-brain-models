import streamlit as st
import numpy as np
from utils.JansenRit import JansenRit
import matplotlib.pyplot as plt

def run_tab():
  if st.button("Run Simulation"):

    with st.spinner("Running simulation..."):
      
        params =st.session_state.params 
        model = JansenRit(p=params)
       
        # For progress bar (begin) 
        progress = st.progress(0, text="Starting...")
        model.solve(progress_bar=progress)
        progress.progress(100, text="Done!!!")

        st.session_state.model = model

    st.success("Simulation finished.")
 
  if "model" in st.session_state:

    model = st.session_state.model
    
    t,eeg_out = model.return_t_eeg()
    simu_time=model.params['simu_time']
    tick_array=np.arange(0,simu_time+0.2,0.25)  # in 500 msec increment
    tick_values= np.arange(0,int(simu_time*1000)+1,250)

    f,ax = plt.subplots(1,figsize=(15,3))
    ax.plot(t, eeg_out)
    ax.set_xlabel('Time (sec)',fontsize=14) 
    ax.set_ylabel('EEG amplitude',fontsize=14)
    ax.set_xticks(tick_array)
    ax.set_xticklabels(tick_values,fontsize=14)
    ax.set_yticklabels(ax.get_yticks(), fontsize=14)   
    ax.spines[["right","top"]].set_visible(False)  
    st.pyplot(f)          
