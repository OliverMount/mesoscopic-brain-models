import streamlit as st
import numpy as np

def parameters_tab():

    st.session_state.params = {}
    c1,c2,c3 = st.columns([1,2,1])
          
    with c1:
        st.subheader("Connectivity")
        with st.container(border=True):
            mode = st.radio("**Mode**",("**Use common C**","**Specify C1-C4**")).replace("**","")
            if mode=="Use common C":
                C = st.number_input("**C**",value=128.0)
                st.session_state.params['C']=C   # This is enough
                
            else:
                col1,col2 = st.columns(2)
                
                with col1:
                    C1 = st.number_input("**C1**",value=128.0)
                    C2 = st.number_input("**C2**",value=102.4)
                
                with col2:
                    C3 = st.number_input("**C3**",value=32.0)
                    C4 = st.number_input("**C4**",value=32.0)  
                    
                    st.session_state.params['C1']=C1   
                    st.session_state.params['C2']=C2   
                    st.session_state.params['C3']=C3  
                    st.session_state.params['C4']=C4  
    with c2:
        st.subheader("Post-Synaptic Potential")
        col1, col2= st.columns(2)
                
        with col1:
            with st.container(border=True):
                st.markdown("**Excitatory**")
                A = st.number_input("**A (mV)**", value=3.25)
                a = st.number_input("**a (Hz)**", value=100.0)
                
        with col2:
            with st.container(border=True):
                st.markdown("**Inhibitory**")
                B = st.number_input("**B (mV)**", value=22.0)
                b = st.number_input("**b (Hz)**", value=50.0)
                st.session_state.params['A']=A
                st.session_state.params['B']=B
                st.session_state.params['a']=a
                st.session_state.params['b']=b
                
    with c3:
        st.subheader("Sigmoidal Parameters")
        with st.container(border=True):
            # Sigmodial parameters
            eo =st.number_input("**Max. firing rate: eo(Hz)**",2.5)
            vo =st.number_input("**Mean firing rate threshold: vo (mV)**",6)
            r =st.number_input("**Slope: r (Hz)**",0.56)
            st.session_state.params['eo']=eo
            st.session_state.params['vo']=vo
            st.session_state.params['r']=r
    
    # Second row beginning
    st.divider()
    c1,c2,c3,c4 = st.columns(4)

    # Noise input      
    with c1:
        st.subheader("Cortical noise parameters")
        with st.container(border=True):
            col1,col2 = st.columns(2)
            with col1:
                noise_type = st.radio("**Type**",("**Uniform**","**Gaussian**")).replace("**","")
                st.session_state.params['noise_type']=noise_type
            with col2:    
                if noise_type =="Uniform":
                    Ul=st.number_input("**Minimum (Hz)**",120)
                    Uh=st.number_input("**Maximum (Hz)**",320)
                    st.session_state.params['Uh']=Uh
                    st.session_state.params['Ul']=Ul
                elif noise_type =="Gaussian":
                    me=st.number_input("**Mean (Hz)**",220)
                    st.session_state.params['me']=me
                    sd=st.number_input("**Std. dev. (Hz)**",22)
                    st.session_state.params['sd']=sd
    with c2:
        st.subheader("Simulation timings")
        with st.container(border=True):
            simu_time = st.number_input("**Total simulation time (sec)**",value=2,min_value=1,max_value=60)
            offset_time = st.number_input("**Offset time (in msec)**",value=200,min_value=0,max_value=1000)
            dt = st.number_input("**dt (sec)**",value=0.001,max_value=0.01,min_value=0.0001)
    with c3:
        st.subheader("Solver Type")
        with st.container(border=True):
            solver_type = st.radio("**Solver Type**",("**Euler**","**RK4**")).replace("**","")
            st.session_state.params['simu_time']=simu_time
            st.session_state.params['offset_time']=offset_time
            st.session_state.params['dt']=dt
            st.session_state.params['solver_type']=solver_type
    with c4:
        st.subheader("Initial Conditions")
        with st.container(border=True):
            col1, col2  = st.columns(2)
            with col1:
                y0 = st.number_input("**y[0]**", value=0.0)
                y1 = st.number_input("**y[1]**", value=0.0)
                y2 = st.number_input("**y[2]**", value=0.0)
            with col2:
                z0 = st.number_input("**z[0]**",value=st.session_state.params['A']*st.session_state.params['a'])
                z1 = st.number_input("**z[1]**",value=st.session_state.params['A']*st.session_state.params['a'])
                z2 = st.number_input("**z[2]**",value=st.session_state.params['B']*st.session_state.params['b'])
        
            st.session_state.params['y0']=np.array([y0,y1,y2])
            st.session_state.params['z0']=np.array([z0,z1,z2])

    #print(st.session_state.params)
