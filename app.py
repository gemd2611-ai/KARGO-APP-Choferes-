import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime

# --- CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Trimotos Pro", layout="wide", page_icon="🚀")
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .stButton>button { border-radius: 15px; background-color: #00C853; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #00E676; }
    .trip-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; border-left: 5px solid #00C853;}
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS EN MEMORIA ---
if "tarifas" not in st.session_state:
    st.session_state.tarifas = {"base_A": 6.0, "km_extra_A": 0.80, "base_B": 9.0, "km_extra_B": 1.00, "comision_pct": 0.20}
if "viajes" not in st.session_state:
    st.session_state.viajes = []
if "choferes" not in st.session_state:
    st.session_state.choferes = ["Carlos Pérez", "José Rodríguez", "Luis Gómez"]

# --- MOTOR DE GEOLOCALIZACIÓN Y GEOMETRÍA DE RUTA (OSRM + GEOPY) ---
def obtener_datos_ruta(origen_str, destino_str):
    geolocator = Nominatim(user_agent="trimoto_caracas_mapper")
    try:
        # 1. Obtener Coordenadas de los puntos
        loc_orig = geolocator.geocode(origen_str + ", Caracas, Venezuela")
        loc_dest = geolocator.geocode(destino_str + ", Caracas, Venezuela")
        
        if loc_orig and loc_dest:
            lat1, lon1 = loc_orig.latitude, loc_orig.longitude
            lat2, lon2 = loc_dest.latitude, loc_dest.longitude
            
            # 2. Pedir geometría completa a OSRM (geometries=geojson)
            url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
            res = requests.get(url, timeout=6)
            data = res.json()
            
            if data.get("code") == "Ok":
                metros = data["routes"][0]["distance"]
                km = round(metros / 1000.0, 2)
                
                # Invertir coordenadas GeoJSON [lon, lat] a [lat, lon] para Folium
                geometria_raw = data["routes"][0]["geometry"]["coordinates"]
                puntos_ruta = [[p[1], p[0]] for p in geometria_raw]
                
                return {
                    "km": km,
                    "puntos": puntos_ruta,
                    "origen_coords": [lat1, lon1],
                    "destino_coords": [lat2, lon2]
                }
    except Exception as e:
        pass
    return None

def calcular_tarifa(distancia_km, categoria):
    if "Cat. A" in categoria:
        base, km_extra = st.session_state.tarifas["base_A"], st.session_state.tarifas["km_extra_A"]
    else:
        base, km_extra = st.session_state.tarifas["base_B"], st.session_state.tarifas["km_extra_B"]
    
    total = base if distancia_km <= 3 else base + ((distancia_km - 3) * km_extra)
    comision = total * st.session_state.tarifas["comision_pct"]
    return round(total, 2), round(comision, 2), round(total - comision, 2)

# --- NAVEGACIÓN ---
st.sidebar.title("🚚 Trimotos Pro")
menu = st.sidebar.radio("Menú", ["📍 Despacho Central", "📱 App Choferes", "📊 Historial y Fotos", "⚙️ Precios"])

# ==========================================
# 📍 MÓDULO 1: DESPACHO CENTRAL CON MAPA
# ==========================================
if menu == "📍 Despacho Central":
    st.title("📍 Despacho Central con Mapa de Ruta")
    
    col_input, col_cotiz = st.columns([1, 1])
    
    if "datos_ruta" not in st.session_state:
        st.session_state.datos_ruta = None

    with col_input:
        st.subheader("1. Parámetros de la Carrera")
        comercio = st.text_input("Cliente / Comercio", "Ferretería El Ancla")
        origen = st.text_input("Origen", "Quinta Crespo")
        destino = st.text_input("Destino", "Chacao")
        categoria = st.selectbox("Categoría de Carga", ["Cat. A (Hasta 150 kg)", "Cat. B (151 kg a 450 kg)"])
        
        if st.button("🗺️ Calcular y Trazar Ruta", use_container_width=True):
            with st.spinner("Trazando ruta por las calles de Caracas..."):
                info = obtener_datos_ruta(origen, destino)
                if info:
                    st.session_state.datos_ruta = info
                    st.success(f"¡Ruta generada con éxito! Distancia: {info['km']} km")
                else:
                    st.error("No se pudo ubicar la dirección. Intenta detallar más el sector.")

    with col_cotiz:
        st.subheader("2. Cotización y Despacho")
        if st.session_state.datos_ruta:
            dist_final = st.session_state.datos_ruta["km"]
            total, comision, pago_chofer = calcular_tarifa(dist_final, categoria)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Distancia", f"{dist_final} km")
            m2.metric("Cobro Total", f"${total}")
            m3.metric("Pago Chofer", f"${pago_chofer}")
            
            st.markdown("---")
            chofer_asig = st.selectbox("Asignar al Chofer:", st.session_state.choferes)
            
            if st.button("🚀 Confirmar y Enviar Carga", use_container_width=True):
                nuevo_viaje = {
                    "ID": len(st.session_state.viajes) + 1,
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Comercio": comercio,
                    "Origen": origen,
                    "Destino": destino,
                    "Total ($)": total,
                    "Chofer": chofer_asig,
                    "Estatus": "🟡 En Ruta",
                    "Foto": None
                }
                st.session_state.viajes.append(nuevo_viaje)
                st.success(f"¡Carrera enviada exitosamente a {chofer_asig}!")
                st.balloons()
        else:
            st.info("Ingresa los puntos de salida y llegada, luego presiona 'Calcular y Trazar Ruta'.")

    # --- SECCIÓN DEL MAPA (OCUPA EL ANCHO COMPLETO ABAJO) ---
    if st.session_state.datos_ruta:
        st.markdown("---")
        st.subheader("🗺️ Visualización de la Ruta por Calle")
        
        ruta_info = st.session_state.datos_ruta
        centro_mapa = ruta_info["origen_coords"]
        
        # Crear mapa centrado en la salida
        m = folium.Map(location=centro_mapa, zoom_start=13, tiles="OpenStreetMap")
        
        # Marcador Origen (Verde)
        folium.Marker(
            location=ruta_info["origen_coords"],
            popup=f"Origen: {origen}",
            tooltip="Punto de Salida",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(m)
        
        # Marcador Destino (Rojo)
        folium.Marker(
            location=ruta_info["destino_coords"],
            popup=f"Destino: {destino}",
            tooltip="Punto de Llegada",
            icon=folium.Icon(color="red", icon="stop")
        ).add_to(m)
        
        # Dibujar trazado de la ruta sobre las calles en color azul
        folium.PolyLine(
            locations=ruta_info["puntos"],
            color="#0066FF",
            weight=5,
            opacity=0.8
        ).add_to(m)
        
        # Renderizar en la app
        st_folium(m, width=1200, height=450)

# ==========================================
# 📱 MÓDULO 2: APP DE CHOFERES
# ==========================================
elif menu == "📱 App Choferes":
    st.title("📱 Mi Ruta (Panel de Chofer)")
    yo_soy = st.selectbox("¿Quién eres?", ["Selecciona tu nombre..."] + st.session_state.choferes)
    
    if yo_soy != "Selecciona tu nombre...":
        mis_viajes = [v for v in st.session_state.viajes if v["Chofer"] == yo_soy and v["Estatus"] == "🟡 En Ruta"]
        if not mis_viajes:
            st.info("No tienes carreras pendientes en este momento.")
        else:
            for viaje in mis_viajes:
                st.markdown(f"""
                <div class="trip-card">
                    <h4>📦 Cliente: {viaje['Comercio']}</h4>
                    <p><b>📍 Recoger en:</b> {viaje['Origen']}</p>
                    <p><b>🏁 Entregar en:</b> {viaje['Destino']}</p>
                    <p><b>💵 Cobrar:</b> ${viaje['Total ($)']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                foto = st.camera_input(f"📸 Foto de entrega (Carrera #{viaje['ID']})")
                if foto is not None:
                    if st.button(f"✅ Confirmar Entrega Exitosamente", key=f"btn_{viaje['ID']}"):
                        for v in st.session_state.viajes:
                            if v["ID"] == viaje["ID"]:
                                v["Estatus"] = "🟢 Entregado"
                                v["Foto"] = foto
                        st.success("¡Entrega guardada!")
                        st.rerun()

# ==========================================
# 📊 MÓDULO 3: HISTORIAL Y FOTOS
# ==========================================
elif menu == "📊 Historial y Fotos":
    st.title("📊 Control de Entregas")
    if not st.session_state.viajes:
        st.info("No hay historial registrado aún.")
    else:
        for v in reversed(st.session_state.viajes):
            with st.expander(f"{v['Estatus']} | {v['Comercio']} - Chofer: {v['Chofer']} | {v['Fecha']}"):
                st.write(f"**Ruta:** {v['Origen']} ➡️ {v['Destino']}")
                st.write(f"**Monto Total:** ${v['Total ($)']}")
                if v["Foto"] is not None:
                    st.image(v["Foto"], caption="Prueba de Entrega", width=300)

# ==========================================
# ⚙️ MÓDULO 4: PRECIOS
# ==========================================
elif menu == "⚙️ Precios":
    st.title("⚙️ Configuración de Tarifas")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.tarifas["base_A"] = st.number_input("Base Cat A", value=st.session_state.tarifas["base_A"])
        st.session_state.tarifas["km_extra_A"] = st.number_input("Km Extra Cat A", value=st.session_state.tarifas["km_extra_A"])
    with c2:
        st.session_state.tarifas["base_B"] = st.number_input("Base Cat B", value=st.session_state.tarifas["base_B"])
        st.session_state.tarifas["km_extra_B"] = st.number_input("Km Extra Cat B", value=st.session_state.tarifas["km_extra_B"])