import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import pydeck as pdk
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Flight Status Prediction", layout="wide")

# --- CARGA DE DATOS Y MODELO ---
@st.cache_resource
def load_model():
    model = xgb.XGBClassifier()
    # Asegúrate de que la ruta sea correcta según tu estructura de carpetas
    model.load_model("models/xgb_model.json") 
    return model

@st.cache_data
def load_airports_data():
    # Asegúrate de que airports.csv tenga: iata_code, latitude_deg, longitude_deg
    df_airports = pd.read_csv('../data/airports.csv')
    return df_airports

# IMPORTANTE: Debes copiar aquí TODAS las columnas resultantes del OneHotEncoder de tu notebook
# para que el modelo no de error de dimensiones.
EXPECTED_COLUMNS = [
    'year', 'month', 'day_of_month', 'day_of_week', 'op_carrier_fl_num'
    # Agrega aquí el resto de columnas: 'op_unique_carrier_AA', 'origin_JFK', etc.
]

# --- INTERFAZ DE USUARIO ---
st.title("✈️ Flight Status Predictor")
st.markdown("We predict whether your flight will arrive on time or delayed using Artificial Intelligence (XGBoost).")

with st.container():
    st.subheader("Enter your flight details")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        airline = st.selectbox("Airline (Carrier)", ['9E','AA','AS','B6','DL','F9','G4','HA','MQ','NK','OH','OO','UA','WN','YX'])
        flight_num = st.text_input("Flight Number", value="")
    
    with col2:
        origin = st.text_input("Origin Airport (IATA)", value="").upper()
        dest = st.text_input("Destination Airport (IATA)", value="").upper()
        
    with col3:
        flight_date = st.date_input("Flight Date", datetime.now())
        year, month, day = flight_date.year, flight_date.month, flight_date.day
        day_of_week = flight_date.weekday() + 1

# --- LÓGICA DE PREDICCIÓN ---
if st.button("Predict Flight Status"):
    # 1. Preparar datos para el modelo
    input_data = {col: 0 for col in EXPECTED_COLUMNS}
    input_data.update({
        'year': year, 'month': month, 'day_of_month': day,
        'day_of_week': day_of_week, 'op_carrier_fl_num': int(flight_num) if flight_num.isdigit() else 0
    })
    
    if f'op_unique_carrier_{airline}' in input_data: input_data[f'op_unique_carrier_{airline}'] = 1
    if f'origin_{origin}' in input_data: input_data[f'origin_{origin}'] = 1
    
    # Simulación de predicción (Descomenta las líneas de abajo para usar tu modelo real)
    # model = load_model()
    # prediction = model.predict(pd.DataFrame([input_data]))[0]
    prediction = np.random.choice([0, 1]) 

    # 2. Visualización del Mapa
    st.subheader("Flight Route")
    df_airports = load_airports_data()
    
    # Extraer coordenadas
    orig_row = df_airports[df_airports['iata_code'] == origin]
    dest_row = df_airports[df_airports['iata_code'] == dest]
    
    if not orig_row.empty and not dest_row.empty:
        # Coordenadas numéricas puras
        start_lat, start_lon = float(orig_row.iloc[0]['latitude_deg']), float(orig_row.iloc[0]['longitude_deg'])
        end_lat, end_lon = float(dest_row.iloc[0]['latitude_deg']), float(dest_row.iloc[0]['longitude_deg'])
        
        # Datos para las capas
        arc_data = [{"source": [start_lon, start_lat], "target": [end_lon, end_lat]}]
        
        # El avión lo posicionamos en el punto medio del arco
        airplane_data = [{"coord": [(start_lon + end_lon) / 2, (start_lat + end_lat) / 2], "icon": "✈️"}]

        # Capa del Arco
        arc_layer = pdk.Layer(
            "ArcLayer",
            arc_data,
            get_source_position="source",
            get_target_position="target",
            get_source_color=[0, 255, 128, 200], # Verde neón
            get_target_color=[255, 100, 0, 200], # Naranja neón
            get_width=6,
        )

        # Capa del Avión (TextLayer con Emoji)
        airplane_layer = pdk.Layer(
            "TextLayer",
            airplane_data,
            get_position="coord",
            get_text="icon",
            get_size=35,
            get_color=[255, 255, 255],
            get_angle=0, # Podrías calcular el ángulo entre puntos para rotarlo
        )

        # Configurar la vista centrada en USA
        view_state = pdk.ViewState(
            latitude=(start_lat + end_lat) / 2,
            longitude=(start_lon + end_lon) / 2,
            zoom=3.5,
            pitch=50, # Inclinación para ver el efecto 3D del arco
            bearing=0
        )

        st.pydeck_chart(pdk.Deck(
            layers=[arc_layer, airplane_layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/dark-v10" # El estilo oscuro hace que el arco brille
        ))
    else:
        st.warning("Could not find coordinates for the entered IATA codes.")

    # 3. Resultado de Predicción
    st.markdown("---")
    if prediction == 0:
        st.success("### ✅ Status: ON TIME\nYour flight is predicted to be on schedule. Have a nice trip!")
    else:
        st.error("### ⚠️ Status: DELAYED\nThere is a high probability of delay for this flight.")