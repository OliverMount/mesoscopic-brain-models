import numpy as np
import matplotlib.pyplot as plt
import time


class JansenRit:
   
    def __init__(self,p=None,C=None): # p is an optional dictionary
       
        if p is None:
          self.get_default_parameters()  # This will set self.params
        else:
          self.params=p
       
        if C is not None:  # for reproducibility plot
          self.params['C']=C
          
        
        if 'C' in self.params:
            # Default connectivity values
            self.params['C1']=self.params['C']
            self.params['C2']=0.8*self.params['C1']
            self.params['C3']=0.25*self.params['C1']
            self.params['C4']=0.25*self.params['C1']
        
        # Default solving method
        # Simulation time
        self.offset_in_sec=(self.params['offset_time']*0.001) # offset time in sec
        self.params['total_time']=self.params['simu_time']+ self.offset_in_sec
        self.t=np.arange(0,self.params['total_time']-self.params['dt'],self.params['dt'])
        self.params['nt']= len(self.t) 
        self.offset_samples= int(self.offset_in_sec/self.params['dt'])
        
        ## Default noise parameters (for uniform distribution)
        if self.params['noise_type'] == "Uniform":
          self.pn=np.random.uniform(self.params['Ul'],self.params['Uh'],self.params['nt'])
        elif self.params['noise_type'] == "Gaussian":
          self.pn = (self.params['sd']*np.random.randn(self.params['nt'])) + self.params['me'] 
        else:
          pass
      
        #print("From JR class __init__() method")
        #print(self.params)
        
    def S(self,v): 
        return (2*self.params['eo'])/(1+np.exp(self.params['r']*(self.params['vo']-v)))  
        
    def f(self,z):
        return z

    def g_e(self,y,z,x): 
        return self.params['A']*self.params['a']*x - 2*self.params['a']*z - pow(self.params['a'],2)*y
    
    def g_i(self,y,z,x): 
        return self.params['B']*self.params['b']*x - 2*self.params['b']*z - pow(self.params['b'],2)*y 
    
    def g(self,y,z,lt):
        gval= np.array(
                 [self.g_e(y[0],z[0],self.S(y[1]-y[2])), 
                  self.g_e(y[1],z[1],self.pn[lt] + self.params['C2']*self.S(self.params['C1']*y[0])),  
                  self.g_i(y[2],z[2],self.params['C4']*self.S(self.params['C3']*y[0])) 
                 ]
               )
        return gval
    
    def advance(self):
        lt=self.k  # local time point for computation
        dy   =  self.f(self.z[lt-1])  
        dz   =  self.g(self.y[lt-1],self.z[lt-1],lt-1)
        
        Euler_slope_y, Euler_slope_z=  self.params['dt']*dy, self.params['dt']*dz  
        
        if self.params['solver_type']=="Euler":
            self.y[lt] =  self.y[lt-1] +  Euler_slope_y        
            self.z[lt] =  self.z[lt-1] +  Euler_slope_z  
        elif self.params['solver_type']=="RK4":
            k1= Euler_slope_y     # RK starts with the Euler slope
            l1= Euler_slope_z 
            
            k2 = self.params['dt'] * self.f(self.z[lt-1]+(l1/2))  
            l2 = self.params['dt'] * self.g(self.y[lt-1]+(k1/2),self.z[lt-1]+(l1/2),lt-1)
            
            k3 = self.params['dt'] * self.f(self.z[lt-1]+(l2/2))  
            l3 = self.params['dt'] * self.g(self.y[lt-1]+(k2/2),self.z[lt-1]+(l2/2),lt-1)
            
            k4 = self.params['dt'] * self.f(self.z[lt-1]+l3)  
            l4 = self.params['dt'] * self.g(self.y[lt-1]+k3,self.z[lt-1]+l3,lt-1)
            
            Increment_y = (1/6) * (k1 + 2*k2 + 2*k3 + k4) 
            Increment_z = (1/6) * (l1 + 2*l2 + 2*l3 + l4) 
 
            self.y[lt] =  self.y[lt-1] + Increment_y    
            self.z[lt] =  self.z[lt-1] + Increment_z 
            
        else:
            print("No such solver available in this version")


    def solve(self,progress_bar=None):
        self.y = np.zeros((self.params['nt'],3))   # JR State variables (3 for three cells)
        self.z = np.zeros((self.params['nt'],3))   # JR auxillary variables 
        
        # Initial conditions
        self.y[0] = self.params['y0']
        self.z[0] = self.params['z0']
        
        # Time loop for solving JR differential equations
        for k in range(1,self.params['nt']):
            self.k = k
            self.advance()
            if progress_bar is not None and k % 10 == 0:
                progress_bar.progress((k - 1)/ self.params['nt'],text=f"Running simulation... {(k - 1)*self.params['dt']} sec")
                time.sleep(0.0000001) 
                
    def return_t_eeg(self):
        eeg_signal= self.y[:,1]-self.y[:,2]
        eeg_out= eeg_signal[self.offset_samples:]
        t_out = np.arange(0,len(eeg_out)*self.params['dt'],self.params['dt'])
        return (t_out,eeg_out) 
      
    def get_default_parameters(self):
      self.params={'C' : 128,
              # Default post-synaptic potential values
              'A' : 3.25,  # mV
              'a' : 100,   # Hz
              'B' : 22,    # mV
              'b' : 50,    # Hz
              # Default (sigmoidal) activation function values 
              'vo' : 6,          #mV  Threshold
              'eo' : 2.5,        #Hz   twice the maximum firing rate
              'r' : 0.56,
              ## Default noise parameters (for uniform distribution)
              # Uniform noise
              'noise_type' : "Uniform", # for reproducible plots
              'Ul': 120,
              'Uh': 320, 
              'solver_type' : "RK4",
              'simu_time' : 2,  #sec
              'offset_time' : 250, # in msec
              'dt' : 0.001,
              'y0' : np.zeros(3)    # Initial conditions for y0
              }
              
       # Derived initial values for z0 are  here
      self.params["z0"] = np.array([
      self.params["A"] * self.params["a"],
      self.params["A"] * self.params["a"],
      self.params["B"] * self.params["b"],
      ])
