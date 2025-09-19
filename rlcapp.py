import streamlit as st
import random
import math
import cmath

# ---------- Funciones ----------
def calcular_solucion(R, L, C, f, Vp, phi, modo_circuito):
    w = 2 * math.pi * f
    # Fuente RMS fasorial
    V = cmath.rect(Vp / math.sqrt(2), math.radians(phi))

    if modo_circuito == "serie":
        Z = complex(R, w * L - 1/(w*C))
    else:  # paralelo
        Y = complex(1/R, w*C - 1/(w*L))
        Z = 1 / Y

    I = V / Z
    return Z, I

# ---------- App ----------
st.set_page_config(page_title="Juego RLC", layout="centered")

st.title("⚡ Juego RLC — Corriente Fasorial")
st.write("Practicá con circuitos RLC en **serie o paralelo**.")

# --- Generar un ejercicio nuevo ---
if "ejercicio" not in st.session_state:
    st.session_state.ejercicio = None
    st.session_state.modo = None
    st.session_state.puntaje = 0

if st.button("🎲 Nuevo ejercicio"):
    R = random.randint(10, 220)        # Ω
    L_mH = random.randint(5, 220)      # mH
    C_uF = random.randint(1, 220)      # µF
    f = random.choice([50, 60, 100, 400])
    Vp = random.randint(10, 120)       # V pico
    phi = random.randint(-80, 80)      # grados

    st.session_state.ejercicio = {
        "R": float(R),
        "L": L_mH * 1e-3,
        "C": C_uF * 1e-6,
        "f": float(f),
        "Vp": float(Vp),
        "phi": float(phi),
        "R_disp": R,
        "L_disp": L_mH,
        "C_disp": C_uF
    }
    st.session_state.modo = random.choice(["serie", "paralelo"])

# --- Mostrar ejercicio ---
if st.session_state.ejercicio:
    datos = st.session_state.ejercicio
    st.subheader(f"Circuito: {st.session_state.modo.upper()}")
    st.markdown(f"""
    - R = {datos['R_disp']} Ω  
    - L = {datos['L_disp']} mH  
    - C = {datos['C_disp']} µF  
    - f = {datos['f']} Hz  
    - Fuente: {datos['Vp']}·sen(ωt + {datos['phi']}°) (se usará RMS)
    """)

    st.write("👉 Ingresá tu respuesta (corriente fasorial):")
    usu_mag = st.number_input("Módulo [A]", min_value=0.0, step=0.01, format="%.3f")
    usu_ang = st.number_input("Ángulo [°]", min_value=-180.0, max_value=180.0, step=0.5, format="%.2f")

    if st.button("✅ Verificar"):
        Z, I = calcular_solucion(datos["R"], datos["L"], datos["C"], datos["f"], datos["Vp"], datos["phi"], st.session_state.modo)
        I_mag, I_ang = cmath.polar(I)
        I_ang_deg = math.degrees(I_ang)

        tol_mag = 0.05   # ±5 %
        tol_ang = 5      # ±5°

        ok_mag = abs(usu_mag - I_mag) <= I_mag * tol_mag
        ok_ang = abs(((usu_ang - I_ang_deg + 180) % 360) - 180) <= tol_ang

        if ok_mag and ok_ang:
            st.session_state.puntaje += 10
            st.success(f"✔ Correcto! +10 puntos.\n\nCorriente: {I_mag:.3f} ∠ {I_ang_deg:.2f}° A")
        else:
            st.session_state.puntaje -= 5
            st.error(f"❌ Incorrecto. -5 puntos.\n\nSolución: {I_mag:.3f} ∠ {I_ang_deg:.2f}° A\n\nTu respuesta: {usu_mag:.3f} ∠ {usu_ang:.2f}°")

    st.info(f"🏆 Puntaje actual: {st.session_state.puntaje}")
else:
    st.warning("Presioná **Nuevo ejercicio** para comenzar.")
