import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("DC Motor Simulation")

st.sidebar.header("Input Parameters")

La = st.sidebar.slider("Armature inductance (H)", min_value=0.01, max_value=0.1, value=0.04, step=0.01, key='La')
Ra = st.sidebar.slider("Armature resistance (Ohms)", min_value=1.0, max_value=100.0, value=20.0, step=1.0, key='Ra')
KE = st.sidebar.slider("Back emf constant (V/(rad/sec))", min_value=0.1, max_value=1.0, value=0.5, step=0.1, key='KE')
KT = st.sidebar.slider("Torque constant (Nm/A)", min_value=0.1, max_value=1.0, value=0.5, step=0.1, key='KT')
J = st.sidebar.slider("Moment of Inertia (kg.m^2)", min_value=0.0001, max_value=0.01, value=0.001, step=0.0001, key='J')
D = st.sidebar.slider("Frictional coefficient (Nm/(rad/sec))", min_value=0.1, max_value=1.0, value=0.2, step=0.1, key='D')
dt = st.sidebar.slider("Time step (s)", min_value=0.0001, max_value=0.01, value=0.0001, step=0.0001, key='dt')
Wref = st.sidebar.slider("Reference speed (rad/sec)", min_value=0.1, max_value=10.0, value=2.0, step=0.1, key='Wref')
TL = st.sidebar.slider("Load torque (Nm)", min_value=0.01, max_value=1.0, value=0.05, step=0.01, key='TL')
N = st.sidebar.slider("Number of iterations", min_value=100, max_value=1000, value=500, step=1, key='N')

def run_simulation(La, Ra, KE, KT, J, D, dt, Wref, TL, N):
    A = np.array([[1, 0, dt, 0],
                  [0, 1, 0, dt],
                  [-Ra/La, -KE/La, 0, 0],
                  [KT/J, -D/J, 0, 0]])
    
    B = np.array([0, 0, 1/La, 0])
    C = np.array([0, 0, 0, -1/J])
    X = np.array([0, 0, 0, 0])
    V = ((Ra * D / KT) + KE) * Wref + (Ra / KT) * TL
    
    w = np.zeros(N)
    I = np.zeros(N)

    for n in range(N):
        w[n] = X[1]
        I[n] = X[0]
        X = np.dot(A, X) + B * V + C * TL

    return w, I

w, I = run_simulation(La, Ra, KE, KT, J, D, dt, Wref, TL, N)

st.line_chart(w, width=700, height=300)
st.line_chart(I, width=700, height=300)
