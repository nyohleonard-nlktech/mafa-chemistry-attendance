import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. GLOBAL CONFIGURATION ---
# Adhering to the requested title format and professional engineering standards
APP_TITLE = "MAFA 🧪 Chemistry Studio: Attendance Lab 06/04/2026"

# --- 2. DATASET REPOSITORY ---
# Full attendance data integrated into the source for portability
RAW_DATA = """
AMAZING GRACE HIGH SCHOOL
- Bridget Nyuyfoni

BGS MOLYKO
- Tendoh Kathlyn
- Takang Lauretta

AMBEANDE ENUAKWE
- Tebi Joseph
- Nankam Mambou Reghis Ismaël

COSBA / COSBA FOUMBOT
- Njoya Hermione
- Njinguh Ivana
- Asaah Arrey
- Etta-Nyor Singo Charles
- Miyanwi Peace
- Ndami Farida

CSAO
- Kuetegue franck

DAAS COLLEGE
- Chi Atanga Sonibelle
- Mungu Tabot Alicia

DU VAAL INTERNATIONAL SCHOOL
- Fotio Wetchoua
- Tagne Ephrem

GBHS BERTOUA
- Billal Oumar

GBHS BEKOKO
- Unabit lorinita
- Kioloh Francis
- Lima Gamaliel (Lycée Bekoko)

GBHS BRAZZAVILLE
- fopossi alex

GBHS ETOUG EBE
- Clemson Tanze

GBHS FOUMBOT
- Ndan Susan
- NkEming Asibecheh Joyce
- Asongmoh Dorita

GBHS GÉNIE MILITAIRE
- Zangue Nawa Arol
- Brayane Delange
- Yomb Tchoffo Yuan Ulysse

GBHS MBALNGONG
- Mbuh darine zoh
- Fuli Demia

GBHS MENDONG
- Yvanna Theresa
- Victory woteh
- Tchapmo ina
- Maffo Aude

GBHS MIMBOMAN
- Gamgou Blessing

GBHS NGAOUNDÉRÉ
- Tanwarong Faith
- Tandap Grace

GBHS NGODI BAKOKO
- Tchafack Mahel
- Fankam Tchawa

GBHS NYALLA DEFFO
- Fotso Raphaël

GBHS PENKA-MICHEL
- Tchinda Tiayo Glorinda

GBHS TIKO
- Fon Michelline

GHS BATOKE
- Agwa Kelvin
- Mary promise

INSET COLLEGE
- Njeyo Hustine Kehdinga

INSTITUT SAINT LOUIS
- Okolong Kad

NDAP COLLEGE
- Meyeh Daniella
- Asheri

LADYBIRD ENGLISH SECONDARY SCHOOL
- Ngeupnang Loïsha
- Tchamtcheu Ngadeu Nathan Vianney
- Kong de Mankong Yvan
- Le messie Boning
- Toko Daniel
- Nyabang Cécilia Charlène
- Jiomo Stephan Levy
- Nguemjop Nathael

LYBINYA
- Tchameni Kehou Maryan Karel

NABESK COMPREHENSIVE COLLEGE
- Agbor Neri

PCSS AZIRE
- Tem joy

PETIT ROUSSEAU BILINGUAL COLLEGE
- Matip claire
- Agendia Tim
- Awatcha

RABISCO
- Heubissi Flora

SAINT BENEDICT MVOLYE
- Siango Yan

SAINT CLARET RELIEF ACADEMY
- Mokom Marie-Noel
- Ngwi Ngonjang Faith
- lalong Njeck Larisa acha
- Mbuh Jude Amah
- Mbognou Lionel
- Ntehmo
- Precious Gift

SAINT STEPHEN'S INTERNATIONAL COLLEGE
- Tracy Daisy
- M.B Onyx-Louange
- Wakuna mandé

SAJOCCO
- Tangeh Muhammad kabiru

STARS OF ANGELS COLLEGE
- Nguessong belva

STEP BY STEP HIGH SCHOOL
- Nange Therese

SURE VISION COLLEGE
- Kengne fosso Yvan Cabrel
- Menguute Ketu Treasure junior

TOMIFIDELE MOAMOS
- Yemdo Marie Evane
"""

# --- 3. ETL ENGINE (Extract, Transform, Load) ---
@st.cache_data
def load_and_normalize_data(text: str) -> pd.DataFrame:
    """
    Parses unstructured strings into a tabular DataFrame format.
    Ensures data integrity through string sanitization.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    records = []
    current_institution = "Unknown"
    
    for line in lines:
        # Detect Institution (Non-bulleted lines)
        if not line.startswith('-'):
            current_institution = line
        else:
            # Detect Student (Bulleted lines)
            student_name = line.lstrip('- ').strip()
            records.append({
                "Institution": current_institution, 
                "Student": student_name
            })
    
    return pd.DataFrame(records)

# --- 4. DATA VISUALIZATION & INTERFACE ---
def run_app():
    # Page Setup
    st.set_page_config(page_title="MAFA Attendance Analytics", layout="wide")
    st.title(APP_TITLE)
    st.caption("Engineering Data Analysis | Module: Attendance Visualization")
    
    # Load Data
    df = load_and_normalize_data(RAW_DATA)
    
    # 4.1 Executive Summary Metrics
    col1, col2, col3 = st.columns(3)
    
    # Metric Calculations
    total_count = len(df)
    unique_schools = df['Institution'].nunique()
    top_performer = df['Institution'].value_counts().idxmax()
    
    col1.metric("Total Attendance", f"{total_count} Students")
    col2.metric("Active Institutions", f"{unique_schools} Schools")
    col3.metric("Lead Institution", top_performer)
    
    st.divider()

    # 4.2 Analytical Visualization
    left_viz, right_viz = st.columns([3, 2])
    
    with left_viz:
        st.subheader("Institution Hierarchy Treemap")
        # Visualizing the weight of each school within the total cohort
        fig = px.treemap(
            df, 
            path=[px.Constant("Chemistry Studio"), 'Institution', 'Student'], 
            color='Institution',
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with right_viz:
        st.subheader("Institution Density Leaderboard")
        
        # Prepare Leaderboard Data
        leaderboard = df['Institution'].value_counts().reset_index()
        leaderboard.columns = ['Institution', 'Count']
        
        # Enhanced Table with Progress Indicators
        st.dataframe(
            leaderboard,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Institution": st.column_config.TextColumn("School Name"),
                "Count": st.column_config.ProgressColumn(
                    "Student Density",
                    help="Relative frequency of students per school",
                    format="%d 👤",
                    min_value=0,
                    max_value=int(leaderboard['Count'].max()),
                    color="#008080"  # Hex code for Teal (Standardized)
                )
            }
        )

    # 4.3 Technical Audit Expanders
    with st.expander("🔬 View Processed Data Schema"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    run_app()