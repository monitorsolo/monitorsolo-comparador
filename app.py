import streamlit as st
import spacy
import pandas as pd

# Cargar modelo clínico de SciSpacy (asegúrate de instalarlo antes)
# pip install scispacy
# pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_sm-0.5.1.tar.gz
nlp = spacy.load("en_core_sci_sm")

st.title("Comparador MonitorSolo - Extracción automática desde texto clínico")
st.markdown("Sube un archivo de texto clínico (.txt) y extrae automáticamente los datos clave para comparar con el CRF.")

# Subida del archivo
archivo_txt = st.file_uploader("📄 Subir texto clínico (.txt)", type="txt")

if archivo_txt:
    texto = archivo_txt.read().decode("utf-8")
    st.markdown("### Texto clínico cargado:")
    st.write(texto)

    # Procesar el texto
    doc = nlp(texto)
    entidades = doc.ents

    # Inicializar resultados
    valores_extraidos = {
        "HbA1c": "",
        "Glucosa": "",
        "Presión_Arterial": "",
        "Peso": "",
        "Creatinina": "",
        "eGFR": "",
        "Medicamento": []
    }

    # Extraer valores relevantes desde entidades detectadas
    for ent in entidades:
        txt = ent.text.lower()
        if "hba1c" in txt:
            valores_extraidos["HbA1c"] = txt
        elif "glucosa" in txt or "glucose" in txt:
            valores_extraidos["Glucosa"] = txt
        elif "presión" in txt or "blood pressure" in txt:
            valores_extraidos["Presión_Arterial"] = txt
        elif "peso" in txt or "weight" in txt:
            valores_extraidos["Peso"] = txt
        elif "creatinina" in txt:
            valores_extraidos["Creatinina"] = txt
        elif "egfr" in txt:
            valores_extraidos["eGFR"] = txt
        elif any(med in txt for med in ["metformina", "metformin", "enalapril", "canagliflozin", "sitagliptin"]):
            valores_extraidos["Medicamento"].append(txt)

    # Convertir medicamentos a cadena de texto
    valores_extraidos["Medicamento"] = ", ".join(valores_extraidos["Medicamento"])

    # Mostrar resultados
    df_ehr = pd.DataFrame([valores_extraidos])
    st.markdown("### Datos extraídos desde texto clínico:")
    st.dataframe(df_ehr)

    # Descargar CSV
    st.download_button("⬇️ Descargar CSV para comparar", df_ehr.to_csv(index=False), file_name="ehr_extraido_para_comparar.csv")