import streamlit as st
import base64
import textwrap
from supabase import create_client

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Trimotos Delivery | Chofer",
    page_icon="🛵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# ESTILOS — APP CHOFER
# =========================================================
def render_html(content, unsafe_allow_html=True):
    """
    Render HTML directamente con el motor nativo de Streamlit.
    Se conserva unsafe_allow_html por compatibilidad con el código existente.
    """
    st.html(textwrap.dedent(content).strip())


render_html(
    """
    <style>
    /* ---------- BASE ---------- */
    .stApp {
        background: #F7F8FA;
    }

    [data-testid="stHeader"] {
        background: rgba(247,248,250,0.95);
    }

    .block-container {
        max-width: 760px;
        padding-top: 1.2rem;
        padding-bottom: 5.5rem;
    }

    /* ---------- OCULTAR NAVEGACIÓN NATIVA ---------- */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ---------- HEADER ---------- */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .brand-small {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-small-icon {
        width: 43px;
        height: 43px;
        border-radius: 14px;
        background: #35D0B1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }

    .brand-small-name {
        color: #111827;
        font-size: 15px;
        font-weight: 800;
        line-height: 1.1;
    }

    .brand-small-sub {
        color: #9CA3AF;
        font-size: 10px;
        margin-top: 2px;
    }

    .notification {
        width: 43px;
        height: 43px;
        border-radius: 14px;
        background: white;
        border: 1px solid #E5E7EB;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 19px;
        box-shadow: 0 4px 14px rgba(17,24,39,.04);
    }

    /* ---------- TITLES ---------- */
    .greeting {
        color: #111827;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.15;
        margin-top: 8px;
    }

    .subtitle {
        color: #6B7280;
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    .section-title {
        color: #111827;
        font-size: 19px;
        font-weight: 800;
        margin-top: 22px;
        margin-bottom: 12px;
    }

    /* ---------- DRIVER CARD ---------- */
    .profile-card {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        color: white;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 12px 26px rgba(17,24,39,.16);
    }

    .active-badge {
        display: inline-block;
        background: #35D0B1;
        color: #10201D;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: .5px;
    }

    .driver-name {
        color: white;
        font-size: 23px;
        font-weight: 800;
        margin-top: 12px;
    }

    .driver-ci {
        color: #9CA3AF;
        font-size: 12px;
        margin-top: 3px;
    }

    .vehicle-row {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        border-top: 1px solid #374151;
        margin-top: 15px;
        padding-top: 14px;
    }

    .vehicle-item {
        color: #E5E7EB;
        font-size: 12px;
    }

    .vehicle-value {
        color: white;
        font-weight: 800;
        font-size: 13px;
        margin-top: 3px;
    }

    /* ---------- SERVICE CARD ---------- */
    .service-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 23px;
        padding: 19px;
        margin-bottom: 14px;
        box-shadow: 0 7px 20px rgba(17,24,39,.05);
    }

    .service-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 10px;
    }

    .service-client {
        color: #111827;
        font-size: 16px;
        font-weight: 800;
    }

    .service-date {
        color: #9CA3AF;
        font-size: 11px;
        margin-top: 4px;
    }

    .service-price {
        color: #0B9E84;
        font-size: 22px;
        font-weight: 900;
        white-space: nowrap;
    }

    .pending-pill {
        display: inline-block;
        background: #FFF6D8;
        color: #8A6700;
        border-radius: 999px;
        padding: 5px 9px;
        font-size: 10px;
        font-weight: 800;
        margin-top: 13px;
    }

    .accepted-pill {
        background: #EAF2FF;
        color: #285EA8;
    }

    .route-container {
        background: #F7F8FA;
        border-radius: 17px;
        padding: 13px;
        margin-top: 13px;
    }

    .route-item {
        display: flex;
        gap: 10px;
        align-items: flex-start;
        color: #374151;
        font-size: 13px;
        line-height: 1.35;
    }

    .route-item + .route-item {
        margin-top: 10px;
    }

    .route-icon {
        width: 27px;
        height: 27px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 13px;
    }

    .origin-icon {
        background: #E8FBF7;
    }

    .destination-icon {
        background: #FFF0F0;
    }

    .route-label {
        color: #9CA3AF;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .route-value {
        color: #111827;
        font-weight: 700;
        margin-top: 2px;
    }

    /* ---------- EARNINGS ---------- */
    .earnings-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 17px;
        box-shadow: 0 6px 18px rgba(17,24,39,.04);
    }

    .earnings-label {
        color: #6B7280;
        font-size: 12px;
    }

    .earnings-value {
        color: #111827;
        font-size: 25px;
        font-weight: 900;
        margin-top: 3px;
    }

    /* ---------- HISTORY ---------- */
    .history-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .history-title {
        color: #111827;
        font-size: 14px;
        font-weight: 800;
    }

    .history-route {
        color: #6B7280;
        font-size: 12px;
        margin-top: 6px;
    }

    .history-price {
        color: #0B9E84;
        font-size: 17px;
        font-weight: 900;
    }

    /* ---------- EMPTY STATE ---------- */
    .empty-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 23px;
        padding: 35px 20px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(17,24,39,.04);
    }

    .empty-icon {
        font-size: 40px;
        margin-bottom: 8px;
    }

    .empty-title {
        color: #111827;
        font-size: 17px;
        font-weight: 800;
    }

    .empty-text {
        color: #9CA3AF;
        font-size: 12px;
        margin-top: 5px;
    }

    /* ---------- BOTTOM NAV ---------- */
    .bottom-space {
        height: 55px;
    }

    /* ---------- STREAMLIT BUTTONS ---------- */
    .stButton > button {
        min-height: 43px;
        border-radius: 13px;
        font-weight: 750;
        border: 1px solid #E5E7EB;
    }

    .stButton > button[kind="primary"] {
        background: #35D0B1;
        border-color: #35D0B1;
        color: #10201D;
    }

    /* ---------- LOGIN ---------- */
    .login-logo {
        width: 76px;
        height: 76px;
        border-radius: 24px;
        background: #35D0B1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 38px;
        margin: 30px auto 18px;
    }

    .login-title {
        color: #111827;
        text-align: center;
        font-size: 29px;
        font-weight: 900;
    }

    .login-subtitle {
        color: #6B7280;
        text-align: center;
        font-size: 13px;
        margin-bottom: 25px;
    }

    .login-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(17,24,39,.05);
    }

    @media (max-width: 500px) {
        .block-container {
            padding-left: .85rem;
            padding-right: .85rem;
        }

        .greeting {
            font-size: 25px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SUPABASE
# =========================================================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    SUPABASE_URL = "https://jlurdtdidymjzctryilh.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpsdXJkdGRpZHltanpjdHJ5aWxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc3NTA5MjUsImV4cCI6MjEwMzMyNjkyNX0.ZaA_AwdoyAU-bt_rmby98ORfAkpvkLhX7XHdrK9D_zE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ESTADO_NUEVA = "🟡 Nueva"
ESTADO_ACEPTADA = "🔵 Aceptada"
ESTADO_EN_CAMINO = "🟠 En camino"
ESTADO_EN_ENTREGA = "🟣 En entrega"
ESTADO_RECHAZADA = "🔴 Rechazada"
ESTADO_ENTREGADA = "🟢 Entregado"
ESTADO_LEGACY = "🟡 En Ruta"

ESTADOS_PENDIENTES_CHOFER = {ESTADO_NUEVA, ESTADO_ACEPTADA, ESTADO_EN_CAMINO, ESTADO_EN_ENTREGA, ESTADO_LEGACY}


def actualizar_estatus_viaje(viaje_id, nuevo_estatus):
    try:
        (
            supabase.table("viajes")
            .update({"estatus": nuevo_estatus})
            .eq("id", viaje_id)
            .execute()
        )
        return True, None
    except Exception as e:
        return False, e



# =========================================================
# SESIÓN
# =========================================================
if "chofer_login" not in st.session_state:
    st.session_state.chofer_login = None

if "chofer_tab" not in st.session_state:
    st.session_state.chofer_tab = "🏠 Inicio"


# =========================================================
# LOGIN
# =========================================================
if not st.session_state.chofer_login:
    render_html('<div class="login-logo">🛵</div>', unsafe_allow_html=True)
    render_html(
        '<div class="login-title">Trimotos Delivery</div>',
        unsafe_allow_html=True,
    )
    render_html(
        '<div class="login-subtitle">Panel del conductor</div>',
        unsafe_allow_html=True,
    )

    render_html('<div class="login-card">', unsafe_allow_html=True)

    ci = st.text_input(
        "Cédula de identidad",
        placeholder="Ej. V-20123456",
    ).strip()

    passw = st.text_input(
        "Contraseña",
        type="password",
        placeholder="Ingresa tu contraseña",
    ).strip()

    if st.button(
        "Ingresar a mi panel",
        use_container_width=True,
        type="primary",
    ):
        if not ci or not passw:
            st.warning("Completa la cédula y la contraseña.")
        else:
            try:
                res = (
                    supabase.table("choferes")
                    .select("*")
                    .eq("cedula", ci)
                    .eq("clave", passw)
                    .execute()
                )

                if res.data:
                    st.session_state.chofer_login = res.data[0]
                    st.session_state.chofer_tab = "🏠 Inicio"
                    st.rerun()
                else:
                    st.error("Cédula o contraseña incorrectos.")
            except Exception as e:
                st.error(f"No fue posible iniciar sesión: {e}")

    render_html("</div>", unsafe_allow_html=True)

    render_html(
        """
        <div style="
            text-align:center;
            color:#9CA3AF;
            font-size:11px;
            margin-top:20px;
        ">
            Trimotos Delivery · Panel de Chofer
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# PANEL PRINCIPAL
# =========================================================
else:
    c = st.session_state.chofer_login

    nombre = c.get("nombre", "Conductor")
    cedula = c.get("cedula", "")
    moto_marca = c.get("moto_marca", "Trimoto")
    moto_modelo = c.get("moto_modelo", "Carga")
    placa = c.get("placa", "Sin placa")
    capacidad = c.get("capacidad_kg", 300)

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------
    render_html(
        f"""
        <div class="app-header">
            <div class="brand-small">
                <div class="brand-small-icon">🛵</div>
                <div>
                    <div class="brand-small-name">TRIMOTOS DELIVERY</div>
                    <div class="brand-small-sub">Panel de conductor</div>
                </div>
            </div>
            <div class="notification">🔔</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # NAVEGACIÓN
    # -----------------------------------------------------
    nav_cols = st.columns(4)

    nav_items = [
        ("🏠 Inicio", "🏠 Inicio"),
        ("📦 Viajes", "📦 Viajes"),
        ("💰 Ganancias", "💰 Ganancias"),
        ("👤 Perfil", "👤 Perfil"),
    ]

    for col, (label, value) in zip(nav_cols, nav_items):
        with col:
            if st.button(
                label,
                key=f"nav_{value}",
                use_container_width=True,
            ):
                st.session_state.chofer_tab = value
                st.rerun()

    active_tab = st.session_state.chofer_tab

    # -----------------------------------------------------
    # DATOS DE VIAJES
    # -----------------------------------------------------
    try:
        res_v = (
            supabase.table("viajes")
            .select("*")
            .eq("chofer_cedula", cedula)
            .execute()
        )
        viajes = res_v.data or []
    except Exception as e:
        st.error(f"No fue posible cargar tus viajes: {e}")
        viajes = []

    pendientes = [
        v for v in viajes
        if v.get("estatus") in ESTADOS_PENDIENTES_CHOFER
    ]

    entregados = [
        v for v in viajes
        if v.get("estatus") == "🟢 Entregado"
    ]

    total_generado = sum(
        float(v.get("total", 0) or 0)
        for v in entregados
    )

    # =====================================================
    # 🏠 INICIO
    # =====================================================
    if active_tab == "🏠 Inicio":
        render_html(
            f'<div class="greeting">Hola, {nombre.split()[0]} 👋</div>',
            unsafe_allow_html=True,
        )
        render_html(
            '<div class="subtitle">¿Listo para rodar?</div>',
            unsafe_allow_html=True,
        )

        render_html(
            f"""
            <div class="profile-card">
                <span class="active-badge">● CHOFER ACTIVO</span>

                <div class="driver-name">{nombre}</div>
                <div class="driver-ci">🪪 CI: {cedula}</div>

                <div class="vehicle-row">
                    <div class="vehicle-item">
                        🛵 Vehículo
                        <div class="vehicle-value">
                            {moto_marca} {moto_modelo}
                        </div>
                    </div>

                    <div class="vehicle-item">
                        🏷️ Placa
                        <div class="vehicle-value">{placa}</div>
                    </div>

                    <div class="vehicle-item">
                        📦 Capacidad
                        <div class="vehicle-value">{capacidad} kg</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_html(
            '<div class="section-title">📦 Servicio activo</div>',
            unsafe_allow_html=True,
        )

        if not pendientes:
            render_html(
                """
                <div class="empty-card">
                    <div class="empty-icon">☕</div>
                    <div class="empty-title">
                        No tienes servicios pendientes
                    </div>
                    <div class="empty-text">
                        Cuando la Central te asigne una carrera aparecerá aquí.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for v in sorted(
                pendientes,
                key=lambda x: str(x.get("fecha", "")),
                reverse=True,
            ):
                render_html(
                    f"""
                    <div class="service-card">
                        <div class="service-top">
                            <div>
                                <div class="service-client">
                                    🏢 {v.get("comercio", "Particular")}
                                </div>
                                <div class="service-date">
                                    {v.get("fecha", "")}
                                </div>
                            </div>

                            <div class="service-price">
                                ${float(v.get("total", 0) or 0):.2f}
                            </div>
                        </div>

                        <span class="pending-pill">{v.get("estatus", "Sin estado")}</span>

                        <div class="route-container">
                            <div class="route-item">
                                <div class="route-icon origin-icon">📍</div>
                                <div>
                                    <div class="route-label">Origen</div>
                                    <div class="route-value">
                                        {v.get("origen", "N/A")}
                                    </div>
                                </div>
                            </div>

                            <div class="route-item">
                                <div class="route-icon destination-icon">🏁</div>
                                <div>
                                    <div class="route-label">Destino</div>
                                    <div class="route-value">
                                        {v.get("destino", "N/A")}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                estatus_viaje = v.get("estatus")

                if estatus_viaje == ESTADO_NUEVA:
                    st.warning("🟡 Nueva carrera · Esperando tu respuesta")
                    b_accept, b_reject = st.columns(2)

                    with b_accept:
                        if st.button(
                            "✅ Aceptar carrera",
                            key=f"accept_home_{v['id']}",
                            use_container_width=True,
                            type="primary",
                        ):
                            ok, error = actualizar_estatus_viaje(
                                v["id"], ESTADO_ACEPTADA
                            )
                            if ok:
                                st.success("¡Carrera aceptada!")
                                st.rerun()
                            else:
                                st.error(f"No fue posible aceptar la carrera: {error}")

                    with b_reject:
                        if st.button(
                            "❌ Rechazar",
                            key=f"reject_home_{v['id']}",
                            use_container_width=True,
                        ):
                            ok, error = actualizar_estatus_viaje(
                                v["id"], ESTADO_RECHAZADA
                            )
                            if ok:
                                st.warning("Carrera rechazada.")
                                st.rerun()
                            else:
                                st.error(f"No fue posible rechazar la carrera: {error}")

                else:
                    if estatus_viaje == ESTADO_ACEPTADA:
                        st.success("🔵 Carrera aceptada · Confirma cuando salgas hacia el origen.")
                        if st.button(
                            "🛵 Iniciar camino al origen",
                            key=f"start_{v['id']}",
                            use_container_width=True,
                            type="primary",
                        ):
                            ok, error = actualizar_estatus_viaje(v["id"], ESTADO_EN_CAMINO)
                            if ok:
                                st.rerun()
                            else:
                                st.error(f"No fue posible iniciar el viaje: {error}")

                    elif estatus_viaje == ESTADO_EN_CAMINO:
                        st.warning("🟠 En camino al origen")
                        st.caption("Cuando llegues al punto de recogida, inicia la entrega.")
                        if st.button(
                            "📦 Llegué al origen · Iniciar entrega",
                            key=f"pickup_{v['id']}",
                            use_container_width=True,
                            type="primary",
                        ):
                            ok, error = actualizar_estatus_viaje(v["id"], ESTADO_EN_ENTREGA)
                            if ok:
                                st.rerun()
                            else:
                                st.error(f"No fue posible iniciar la entrega: {error}")

                    elif estatus_viaje == ESTADO_EN_ENTREGA:
                        st.info("🟣 En entrega · Toma la foto al completar el servicio.")
                        foto = st.camera_input(
                            "📸 Tomar foto de entrega",
                            key=f"cam_home_{v['id']}",
                        )

                        if foto:
                            if st.button(
                                "✅ Confirmar entrega y enviar foto",
                                key=f"btn_home_{v['id']}",
                                use_container_width=True,
                                type="primary",
                            ):
                                b64_foto = (
                                    "data:image/png;base64,"
                                    + base64.b64encode(foto.getvalue()).decode()
                                )

                                try:
                                    (
                                        supabase.table("viajes")
                                        .update({
                                            "estatus": ESTADO_ENTREGADA,
                                            "foto_base64": b64_foto,
                                        })
                                        .eq("id", v["id"])
                                        .execute()
                                    )
                                    st.success("¡Entrega guardada correctamente!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"No fue posible guardar la entrega: {e}")

                    elif estatus_viaje == ESTADO_LEGACY:
                        st.info("🛵 Carrera activa de un despacho anterior.")
                        foto = st.camera_input(
                            "📸 Tomar foto de entrega",
                            key=f"cam_home_{v['id']}",
                        )
                        if foto and st.button(
                            "✅ Confirmar entrega y enviar foto",
                            key=f"btn_home_{v['id']}",
                            use_container_width=True,
                            type="primary",
                        ):
                            b64_foto = "data:image/png;base64," + base64.b64encode(foto.getvalue()).decode()
                            try:
                                supabase.table("viajes").update({
                                    "estatus": ESTADO_ENTREGADA,
                                    "foto_base64": b64_foto,
                                }).eq("id", v["id"]).execute()
                                st.success("¡Entrega guardada correctamente!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"No fue posible guardar la entrega: {e}")

        render_html(
            '<div class="section-title">💰 Resumen</div>',
            unsafe_allow_html=True,
        )

        e1, e2 = st.columns(2)

        with e1:
            render_html(
                f"""
                <div class="earnings-card">
                    <div class="earnings-label">Entregas completadas</div>
                    <div class="earnings-value">{len(entregados)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with e2:
            render_html(
                f"""
                <div class="earnings-card">
                    <div class="earnings-label">Total generado</div>
                    <div class="earnings-value">${total_generado:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # =====================================================
    # 📦 VIAJES
    # =====================================================
    elif active_tab == "📦 Viajes":
        render_html(
            '<div class="greeting">Mis viajes 📦</div>',
            unsafe_allow_html=True,
        )
        render_html(
            '<div class="subtitle">Servicios pendientes y completados.</div>',
            unsafe_allow_html=True,
        )

        tab_pending, tab_done = st.tabs(
            ["📥 Nuevas / Activas", "🟢 Completados"]
        )

        with tab_pending:
            if not pendientes:
                render_html(
                    """
                    <div class="empty-card">
                        <div class="empty-icon">☕</div>
                        <div class="empty-title">Todo al día</div>
                        <div class="empty-text">
                            No tienes servicios pendientes.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                for v in sorted(
                    pendientes,
                    key=lambda x: str(x.get("fecha", "")),
                    reverse=True,
                ):
                    render_html(
                        f"""
                        <div class="service-card">
                            <div class="service-top">
                                <div>
                                    <div class="service-client">
                                        🏢 {v.get("comercio", "Particular")}
                                    </div>
                                    <div class="service-date">
                                        {v.get("fecha", "")}
                                    </div>
                                </div>
                                <div class="service-price">
                                    ${float(v.get("total", 0) or 0):.2f}
                                </div>
                            </div>

                            <div class="route-container">
                                <div class="route-item">
                                    <div class="route-icon origin-icon">📍</div>
                                    <div>
                                        <div class="route-label">Origen</div>
                                        <div class="route-value">
                                            {v.get("origen", "N/A")}
                                        </div>
                                    </div>
                                </div>

                                <div class="route-item">
                                    <div class="route-icon destination-icon">🏁</div>
                                    <div>
                                        <div class="route-label">Destino</div>
                                        <div class="route-value">
                                            {v.get("destino", "N/A")}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if v.get("estatus") == ESTADO_NUEVA:
                        st.caption("🟡 Nueva carrera · Esperando tu respuesta")
                        b_accept, b_reject = st.columns(2)
                        with b_accept:
                            if st.button(
                                "✅ Aceptar",
                                key=f"accept_list_{v['id']}",
                                use_container_width=True,
                                type="primary",
                            ):
                                ok, error = actualizar_estatus_viaje(v["id"], ESTADO_ACEPTADA)
                                if ok:
                                    st.rerun()
                                else:
                                    st.error(f"No fue posible aceptar: {error}")
                        with b_reject:
                            if st.button(
                                "❌ Rechazar",
                                key=f"reject_list_{v['id']}",
                                use_container_width=True,
                            ):
                                ok, error = actualizar_estatus_viaje(v["id"], ESTADO_RECHAZADA)
                                if ok:
                                    st.rerun()
                                else:
                                    st.error(f"No fue posible rechazar: {error}")
                    elif v.get("estatus") == ESTADO_ACEPTADA:
                        st.success("🔵 Carrera aceptada")
                        if st.button("🛵 Iniciar camino al origen", key=f"start_list_{v['id']}", use_container_width=True, type="primary"):
                            ok, error = actualizar_estatus_viaje(v["id"], ESTADO_EN_CAMINO)
                            if ok:
                                st.rerun()
                            else:
                                st.error(f"No fue posible iniciar el viaje: {error}")
                    elif v.get("estatus") == ESTADO_EN_CAMINO:
                        st.warning("🟠 En camino al origen")
                        if st.button("📦 Llegué al origen · Iniciar entrega", key=f"pickup_list_{v['id']}", use_container_width=True, type="primary"):
                            ok, error = actualizar_estatus_viaje(v["id"], ESTADO_EN_ENTREGA)
                            if ok:
                                st.rerun()
                            else:
                                st.error(f"No fue posible iniciar la entrega: {error}")
                    elif v.get("estatus") == ESTADO_EN_ENTREGA:
                        st.info("🟣 En entrega")
                        foto = st.camera_input("📸 Tomar foto de entrega", key=f"cam_list_{v['id']}")
                        if foto and st.button("✅ Confirmar entrega y enviar foto", key=f"btn_list_{v['id']}", use_container_width=True, type="primary"):
                            b64_foto = "data:image/png;base64," + base64.b64encode(foto.getvalue()).decode()
                            try:
                                supabase.table("viajes").update({"estatus": ESTADO_ENTREGADA, "foto_base64": b64_foto}).eq("id", v["id"]).execute()
                                st.success("¡Entrega guardada correctamente!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"No fue posible guardar la entrega: {e}")
                    elif v.get("estatus") == ESTADO_LEGACY:
                        st.info("🛵 Carrera activa de un despacho anterior")

        with tab_done:
            if not entregados:
                st.info("Aún no tienes entregas completadas.")
            else:
                for v in sorted(
                    entregados,
                    key=lambda x: str(x.get("fecha", "")),
                    reverse=True,
                ):
                    render_html(
                        f"""
                        <div class="history-card">
                            <div style="
                                display:flex;
                                justify-content:space-between;
                                gap:10px;
                            ">
                                <div>
                                    <div class="history-title">
                                        🟢 {v.get("comercio", "Particular")}
                                    </div>
                                    <div class="history-route">
                                        📍 {v.get("origen", "N/A")}
                                        → 🏁 {v.get("destino", "N/A")}
                                    </div>
                                    <div class="history-route">
                                        {v.get("fecha", "")}
                                    </div>
                                </div>
                                <div class="history-price">
                                    ${float(v.get("total", 0) or 0):.2f}
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if v.get("foto_base64"):
                        with st.expander(
                            f"🖼️ Ver comprobante · Viaje #{v.get('id', '')}"
                        ):
                            st.image(
                                v["foto_base64"],
                                caption="Comprobante de entrega",
                                use_container_width=True,
                            )

    # =====================================================
    # 💰 GANANCIAS
    # =====================================================
    elif active_tab == "💰 Ganancias":
        render_html(
            '<div class="greeting">Mis ganancias 💰</div>',
            unsafe_allow_html=True,
        )
        render_html(
            '<div class="subtitle">Resumen de tus entregas completadas.</div>',
            unsafe_allow_html=True,
        )

        g1, g2 = st.columns(2)

        with g1:
            render_html(
                f"""
                <div class="earnings-card">
                    <div class="earnings-label">Total generado</div>
                    <div class="earnings-value">${total_generado:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with g2:
            render_html(
                f"""
                <div class="earnings-card">
                    <div class="earnings-label">Entregas</div>
                    <div class="earnings-value">{len(entregados)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        render_html(
            '<div class="section-title">Últimas entregas</div>',
            unsafe_allow_html=True,
        )

        if not entregados:
            st.info("Todavía no tienes ganancias registradas.")
        else:
            for v in sorted(
                entregados,
                key=lambda x: str(x.get("fecha", "")),
                reverse=True,
            )[:10]:
                render_html(
                    f"""
                    <div class="history-card">
                        <div style="
                            display:flex;
                            justify-content:space-between;
                            gap:10px;
                        ">
                            <div>
                                <div class="history-title">
                                    🏢 {v.get("comercio", "Particular")}
                                </div>
                                <div class="history-route">
                                    {v.get("fecha", "")}
                                </div>
                            </div>
                            <div class="history-price">
                                +${float(v.get("total", 0) or 0):.2f}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # =====================================================
    # 👤 PERFIL
    # =====================================================
    elif active_tab == "👤 Perfil":
        render_html(
            '<div class="greeting">Mi perfil 👤</div>',
            unsafe_allow_html=True,
        )
        render_html(
            '<div class="subtitle">Información de tu cuenta y vehículo.</div>',
            unsafe_allow_html=True,
        )

        render_html(
            f"""
            <div class="profile-card">
                <span class="active-badge">● CUENTA ACTIVA</span>
                <div class="driver-name">{nombre}</div>
                <div class="driver-ci">🪪 CI: {cedula}</div>

                <div class="vehicle-row">
                    <div class="vehicle-item">
                        🛵 Vehículo
                        <div class="vehicle-value">
                            {moto_marca} {moto_modelo}
                        </div>
                    </div>

                    <div class="vehicle-item">
                        🏷️ Placa
                        <div class="vehicle-value">{placa}</div>
                    </div>
                </div>

                <div style="
                    margin-top:14px;
                    color:#E5E7EB;
                    font-size:12px;
                ">
                    📦 Capacidad máxima:
                    <b style="color:white;">{capacidad} kg</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_html(
            '<div class="section-title">Cuenta</div>',
            unsafe_allow_html=True,
        )

        st.info(
            "La edición del perfil se habilitará en una siguiente etapa."
        )

        if st.button(
            "🚪 Cerrar sesión",
            use_container_width=True,
        ):
            st.session_state.chofer_login = None
            st.rerun()

    render_html('<div class="bottom-space"></div>', unsafe_allow_html=True)
