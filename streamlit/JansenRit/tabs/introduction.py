import streamlit as st

def introduction_tab():

    st.header("Classical Jansen-Rit Neural Mass Model")
  
    st.markdown("""
    
        The **Jansen–Rit** model is a mathematical model of a cortical column [1] used to simulate cortical population activity.

        **Goal**: This simulator provides an interactive environment for studying how model parameters influence corical column output.
        
        For this purpose, we provide: 
          
        - **⚙️ Parameters tab** - to set the model parameters (assumed a knowledge of model parameters). 
        - **▶️ Run tab** - to simulate and to view  single cortical column output (for the parameters recently set)
        - **🔬 Reproducibility tab** - to reproduce published result from [1]. 
        """)
     
    st.divider()
      
    st.caption("[1] Jansen, B. H., & Rit, V. G. (1995). Electroencephalogram and visual evoked potential generation in a mathematical model of coupled cortical columns. Biological Cybernetics, 73(4), 357–366.")
    st.caption("[2] brain2 reproducible codes are here ->  https://brian2.readthedocs.io/en/2.7.0/examples/frompapers.Jansen_Rit_1995_single_column.html")
