# streamlit_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

st.set_page_config(page_title="Simulador Goldman", layout="wide")

st.image("PsicowLab_logo-dscr_preto.png", width=200)  # coloque o nome exato da sua imagem
st.markdown("### Prof. Dr. Eduardo Luiz Gasnhar Moreira  \nUniversidade Federal de Santa Catarina")
st.title("🧠 Calculadora Visual de Potencial de Repouso - Equação de Goldman")

st.markdown("""
Este simulador interativo calcula o **potencial de membrana (Vm)** com base na **Equação de Goldman**, considerando os principais íons:
- Potássio (K⁺)
- Sódio (Na⁺)
- Cloreto (Cl⁻)
- Cálcio (Ca²⁺)

Você pode modificar as **concentrações intra e extracelulares** e as **permeabilidades relativas (P)** para ver como isso afeta o potencial de repouso do neurônio.
""")

# Fator da equação de Goldman (37ºC, log10)
FACTOR = 61.54

def calcular_vm(K_in, K_out, Na_in, Na_out, Cl_in, Cl_out, Ca_in, Ca_out, P_K, P_Na, P_Cl, P_Ca):
    num = (P_K * K_out + P_Na * Na_out + P_Cl * Cl_in + P_Ca * Ca_out)
    den = (P_K * K_in + P_Na * Na_in + P_Cl * Cl_out + P_Ca * Ca_in)
    Vm = FACTOR * np.log10(num / den)
    return Vm

# Layout de duas colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Concentrações (mM)")
    K_out = st.slider("K⁺ extracelular", 1, 200, 5)
    K_in = st.slider("K⁺ intracelular", 1, 200, 100)

    Na_out = st.slider("Na⁺ extracelular", 1, 200, 150)
    Na_in = st.slider("Na⁺ intracelular", 1, 150, 15)

    Cl_out = st.slider("Cl⁻ extracelular", 1, 200, 150)
    Cl_in = st.slider("Cl⁻ intracelular", 1, 200, 13)

    Ca_out = st.slider("Ca²⁺ extracelular", 1.0, 5.0, 2.0)
    Ca_in = st.number_input("Ca²⁺ intracelular (em mM)", value=0.0002, format="%f")

with col2:
    st.subheader("Permeabilidades Relativas (P)")
    P_K = st.slider("P_K (K⁺)", 0.0, 2.0, 1.0, step=0.001)
    P_Na = st.slider("P_Na (Na⁺)", 0.0, 1.0, 0.04, step=0.001)
    P_Cl = st.slider("P_Cl (Cl⁻)", 0.0, 1.0, 0.45, step=0.001)
    P_Ca = st.slider("P_Ca (Ca²⁺)", 0.0, 1.0, 0.001, step=0.001)

# Calcular Vm
Vm = calcular_vm(K_in, K_out, Na_in, Na_out, Cl_in, Cl_out, Ca_in, Ca_out, P_K, P_Na, P_Cl, P_Ca)

st.markdown("---")
st.subheader("Resultado")
st.metric("Potencial de Membrana (Vm)", f"{Vm:.2f} mV")

# Desenho do neurônio com voltímetro
fig, ax = plt.subplots(figsize=(10, 5))

# Corpo celular (soma)
soma = Ellipse((3, 3), width=2, height=2.5, color='#A9CCE3', ec='black')
ax.add_patch(soma)
ax.text(3, 3, 'NEURÔNIO', fontsize=10, ha='center', va='center', weight='bold')

# Axônio
ax.plot([4, 9], [3, 3], color='gray', linewidth=4)

# Voltímetro
volt = plt.Rectangle((9.5, 2.5), 2.0, 1.0, fc='#FADBD8', ec='black')
ax.add_patch(volt)
ax.text(10.5, 3.0, f"Vm = {Vm:.1f} mV", ha='center', va='center', fontsize=14, weight='bold')

# Canais iônicos (Na⁺ e K⁺)
canal_y = [2.0, 2.5, 3.0, 3.5, 4.0]
for y in canal_y:
    ax.plot([2.0, 2.3], [y, y], color='orange', lw=2)
    ax.text(1.9, y, 'K⁺', fontsize=8, ha='right')
    ax.plot([3.7, 4.0], [y, y], color='red', lw=2)
    ax.text(4.1, y, 'Na⁺', fontsize=8, ha='left')

# Bomba Na/K
ax.text(3, 0.8, "Na⁺/K⁺ ATPase", fontsize=9, ha='center')
ax.arrow(2.6, 1.1, 0.3, 0.6, head_width=0.1, color='blue')
ax.arrow(3.4, 1.7, -0.3, -0.6, head_width=0.1, color='orange')

ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis('off')
ax.set_title("Visualização do neurônio em repouso", fontsize=12)

st.pyplot(fig)

st.markdown("""
---
📘 **Equação de Goldman utilizada:**

\[ V_m = 61{,}54 \cdot \log_{10}\left( \frac{P_K[K^+]_o + P_{Na}[Na^+]_o + P_{Cl}[Cl^-]_i + P_{Ca}[Ca^{2+}]_o}{P_K[K^+]_i + P_{Na}[Na^+]_i + P_{Cl}[Cl^-]_o + P_{Ca}[Ca^{2+}]_i} \right) \]

🧪 Modifique os valores e observe como o Vm responde às alterações!
""")
