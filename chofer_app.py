import streamlit as st
import base64
from supabase import create_client

st.set_page_config(page_title="Trimotos Delivery", layout="centered", page_icon="🛵")

# Estilos CSS tipo Yummy App
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F8; }
    .yummy-card {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        color: white; padding: 20px; border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .badge { background-color: #00C853; color: white; padding: 4px 10px; border-radius: 10px; font-weight: bold; font-size: 12px; }
    .trip-box { background-color: white; border-radius: 15px; padding: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; border-left: 6px solid #00C853; }
    .trip-box-done { background-color: white; border-radius: 15px; padding: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; border-left: 6px solid #9CA3AF; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN NUBE ---
SUPABASE_URL = "https://jlurdtdidymjzctryilh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpsdXJkdGRpZHltanpjdHJ5aWxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NTA5MjUsImV4cCI6MjEwMzMyNjkyNX0.ZaA_AwdoyAU-bt_rmby98ORfAkpvkLhX7XHdrK9D_zE"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if "chofer_login" not in st.session_state:
    st.session_state.chofer_login = None

# ==========================================
# PANTALLA DE LOGIN
# ==========================================
if not st.session_state.chofer_login:
    st.title("🛵 Trimotos Delivery")
    st.subheader("Iniciar Sesión")
    
    ci = st.text_input("Cédula de Identidad").strip()
    passw = st.text_input("Contraseña", type="password").strip()
    
    if st.button("Ingresar a mi Panel", use_container_width=True):
        if not ci or not passw:
            st.warning("Por favor completa la cédula y la contraseña.")
        else:
            res = supabase.table("choferes").select("*").eq("cedula", ci).eq("clave", passw).execute()
            if res.data:
                st.session_state.chofer_login = res.data[0]
                st.rerun()
            else:
                st.error("Cédula o contraseña incorrectos.")

# ==========================================
# PANTALLA PRINCIPAL TIPO YUMMY
# ==========================================
else:
    c = st.session_state.chofer_login
    
    # Header Perfil Chofer
    moto_marca = c.get('moto_marca', 'Trimoto')
    moto_modelo = c.get('moto_modelo', 'Carga')
    placa = c.get('placa', 'Sin Placa')
    capacidad = c.get('capacidad_kg', '300')

    st.markdown(f"""
    <div class="yummy-card">
        <span class="badge">CHOFER ACTIVO</span>
        <h2 style="margin-top:10px; margin-bottom:2px; color:white;">{c.get('nombre', 'Conductor')}</h2>
        <p style="color:#9CA3AF; margin-bottom:12px;">🪪 CI: {c.get('cedula', '')}</p>
        <hr style="border-color:#374151;">
        <div style="display:flex; justify-content:space-between;">
            <div><b>🛵 Vehículo:</b> {moto_marca} {moto_modelo}</div>
            <div><b>🏷️ Placa:</b> {placa}</div>
        </div>
        <div style="margin-top:5px;"><b>📦 Capacidad Máx:</b> {capacidad} kg</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.chofer_login = None
        st.rerun()

    # PESTAÑAS: Carreras Activas vs Histórico
    tab1, tab2 = st.tabs(["📦 Carreras Pendientes", "📜 Histórico de Viajes"])

    # ------------------------------------------
    # TAB 1: CARRERAS PENDIENTES
    # ------------------------------------------
    with tab1:
        res_v = supabase.table("viajes").select("*").eq("chofer_cedula", c['cedula']).eq("estatus", "🟡 En Ruta").execute()
        viajes = res_v.data
        
        if not viajes:
            st.info("No tienes despachos pendientes en este momento. ☕")
        else:
            for v in viajes:
                st.markdown(f"""
                <div class="trip-box">
                    <h4 style="margin:0; color:#111827;">🏢 Cliente: {v.get('comercio', 'Particular')}</h4>
                    <p style="margin:5px 0;"><b>📍 Salida:</b> {v.get('origen', 'N/A')}</p>
                    <p style="margin:5px 0;"><b>🏁 Entrega:</b> {v.get('destino', 'N/A')}</p>
                    <h3 style="color:#00C853; margin:5px 0;">Cobrar: ${v.get('total', 0)}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                foto = st.camera_input("📸 Tomar foto de entrega", key=f"cam_{v['id']}")
                
                if foto:
                    if st.button("✅ Confirmar y Enviar Foto", key=f"btn_{v['id']}", use_container_width=True):
                        b64_foto = "data:image/png;base64," + base64.b64encode(foto.getvalue()).decode()
                        
                        supabase.table("viajes").update({
                            "estatus": "🟢 Entregado", 
                            "foto_base64": b64_foto
                        }).eq("id", v['id']).execute()
                        
                        st.success("¡Entrega guardada con éxito!")
                        st.rerun()

   # ------------------------------------------
    # TAB 2: HISTÓRICO DE VIAJES
    # ------------------------------------------
    with tab2:
        # Traer viajes con estatus "🟢 Entregado" ordenados de más reciente a más viejo
        res_h = supabase.table("viajes").select("*").eq("chofer_cedula", c['cedula']).eq("estatus", "🟢 Entregado").order("id", desc=True).execute()
        historico = res_h.data

        if not historico:
            st.info("Aún no has completado ninguna carrera. ¡A rodar!")
        else:
            # Métrica express: Total cobrado acumulado
            total_generado = sum([v.get('total', 0) for v in historico])
            st.metric(label="💰 Total Producido en Entregas", value=f"${total_generado:.2f}")
            st.divider()

            for h in historico:
                st.markdown(f"""
                <div class="trip-box-done">
                    <span style="color:#00C853; font-weight:bold; font-size:12px;">✅ ENTREGADO</span>
                    <h4 style="margin:5px 0 0 0; color:#111827;">🏢 Cliente: {h.get('comercio', 'Particular')}</h4>
                    <p style="margin:3px 0;"><b>📍 Salida:</b> {h.get('origen', 'N/A')}</p>
                    <p style="margin:3px 0;"><b>🏁 Entrega:</b> {h.get('destino', 'N/A')}</p>
                    <h4 style="color:#111827; margin:5px 0;">Monto: ${h.get('total', 0)}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Desplegable para ver la foto de la entrega en Base64 con el parámetro corregido
                if h.get('foto_base64'):
                    with st.expander(f"🖼️ Ver Comprobante de Foto (Viaje #{h['id']})"):
                        st.image(h['foto_base64'], caption="Comprobante de Entrega", use_container_width=True)