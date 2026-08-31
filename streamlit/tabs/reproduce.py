import streamlit as st
import numpy as np
from utils.JansenRit import JansenRit
import matplotlib.pyplot as plt


def run_reproduce():
    if st.button("Reproduce Fig. 3 of [1]."):
        with st.spinner("Running simulation..."):
          # As per Fig. 3 of [1]
          C_list = np.array([68, 128, 135, 270, 675, 1350])
          y = np.zeros((len(C_list)))
          res = {} # For storing the reproducibility results 
        
          # 1. Create a single placeholder container before the loop starts
          status_placeholder = st.empty()
        
          for idx, C in enumerate(C_list):  
              print("**************************************")
              print("For the value of C", C)
              print("**************************************")
              model = JansenRit(C=C)
            
              # Placeholder for starting message
              status_placeholder.success(f"Begin solving for {C}")
              model.solve()
           
              if 't' not in res: 
                 res['t'],res[f'y_{idx}']  = model.return_t_eeg()
              else:
                 _,res[f'y_{idx}']  = model.return_t_eeg()
    
              # 3. Overwrite placeholder with the current completion message
              status_placeholder.success(f"Done for {C}")
              st.session_state.Fig3 = res
            
          # 4. Clear the placeholder text completely after the loop finishes
          status_placeholder.empty()
        st.success("Simulation finished.")
        
    #print(st.session_state.Fig3)

    #print(st.session_state['Fig3'])
    #print("Fig3" in st.session_state)
    
    
    col1, col2 = st.columns(2)
    with col1:
      st.subheader("Reproduced")
      if "Fig3" in st.session_state:
       
         num_of_figs= sum(k.startswith('y') for k in list(st.session_state['Fig3'].keys()))
         
         f,ax=plt.subplots(num_of_figs,figsize=(10,10))
         (t_begin,t_end) = (st.session_state.Fig3['t'][0],st.session_state.Fig3['t'][-1]) 
         tick_array=np.arange(t_begin,t_end+0.1,0.5)  # in 500 msec increment
         tick_values= np.arange(0,2001,500)  # It is hardcoed as it is for reproduciblity
       
         for idx, aa in enumerate(ax):
             aa.plot(st.session_state.Fig3['t'], st.session_state.Fig3[f'y_{idx}'])
             aa.set_xlabel('Time (msec)') 
             aa.spines[["right","top"]].set_visible(False) 
             #print(np.arange(t_begin,t_end+0.1,0.5))
             aa.set_xticks(tick_array)
             aa.set_xticklabels(tick_values)
             #ax.set_ylabel('EEG amplitude')
         st.pyplot(f)          
       
    with col2:
      st.subheader('Original from Fig. 3, [1]')
      st.image(
          "images/JR_original.png",
          use_container_width=True
      )
