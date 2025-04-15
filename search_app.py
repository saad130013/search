
import streamlit as st
import pandas as pd
from fpdf import FPDF

# Load and clean the data
df = pd.read_excel("assets_data.xlsx")
df.columns = [col.strip() for col in df.columns]  # إزالة الفراغات من أسماء الأعمدة

st.set_page_config(page_title="Asset Lookup App", layout="wide")
st.title("🔍 نظام البحث عن الأصول")

# البحث إما بوصف الأصل أو رقم الأصل
search_mode = st.radio("اختر طريقة البحث:", ["🔤 وصف الأصل", "🔢 Tag Number"])

if search_mode == "🔤 وصف الأصل":
    asset_descriptions = df["Asset Description"].dropna().unique()
    search_input = st.text_input("اكتب جزء من وصف الأصل:")
    suggestions = [desc for desc in asset_descriptions if search_input in str(desc)]
    if suggestions:
        selected_desc = st.selectbox("اختر وصف الأصل:", suggestions)
        result = df[df["Asset Description"] == selected_desc]
    else:
        result = pd.DataFrame()

elif search_mode == "🔢 Tag Number":
    tag_number_input = st.text_input("أدخل رقم الأصل:")
    result = df[df["Tag number"] == tag_number_input] if tag_number_input else pd.DataFrame()

# اختيار نوع البيانات المراد عرضها
st.markdown("## حدد البيانات التي ترغب في عرضها")
options = st.multiselect(
    "اختر من التالي:",
    ["بيانات تعريف الأصل الأساسية", "تصنيف الأصل المحاسبي", "التفاصيل الفنية والمالية والموقع"],
    default=["بيانات تعريف الأصل الأساسية", "تصنيف الأصل المحاسبي", "التفاصيل الفنية والمالية والموقع"]
)

if not result.empty:
    if "بيانات تعريف الأصل الأساسية" in options:
        st.subheader("📘 بيانات تعريف الأصل الأساسية")
        st.table(result[["Unique Factory ID (Asset Serial Number)", "Old Tag number", "Custodian"]])

    if "تصنيف الأصل المحاسبي" in options:
        st.subheader("📗 التصنيف المحاسبي")
        cols = [
            "Level 1 FA Module - Arabic Description", "Level 1 FA Module - English Description", "Level 1 FA Module Code",
            "Level 2 FA Module - Arabic Description", "Level 2 FA Module - English Description", "Level 2 FA Module Code",
            "Level 3 FA Module - Arabic Description", "Level 3 FA Module - English Description", "Level 3 FA Module Code",
            "accounting group Arabic Description", "accounting group English Description", "accounting group Code",
            "Asset Code For Accounting Purpose "
        ]
        cols = [col.strip() for col in cols if col.strip() in df.columns]
        st.table(result[cols])

    if "التفاصيل الفنية والمالية والموقع" in options:
        st.subheader("📙 التفاصيل الفنية والمالية والموقع")
        cols = [
            "Building Number", "Geographical Coordinates", "Acquisition Method", "Date Placed in Service",
            "Acquisition Date", "Acquisition Cost", "Supportive Documents For Acquisition Cost",
            "Archive Document Number", "Manufacturer", "Model", "Capacity factor unit of measure",
            "Capacity measurement factor", "Capacity factor value", "Asset Utilization", "Replacement Value",
            "Insurance Policy Number", "Asset Condition", "Inspection Date", "Valuation Method",
            "Valuation Report Date", "Opening Balance Date", "Asset Opening Value", "Valuation Report Reference",
            "Base Unit of Measure", "Quantity", "Floors Number", "Room/office Number"
        ]
        cols = [col.strip() for col in cols if col.strip() in df.columns]
        st.table(result[cols])
else:
    st.warning("الرجاء إدخال وصف أو رقم أصل صالح للبحث.")
