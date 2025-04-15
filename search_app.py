
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# تحميل البيانات وتنظيف الأعمدة
df = pd.read_excel("assets_data.xlsx")
df.columns = [col.strip() for col in df.columns]
df["Asset Description"] = df["Asset Description"].astype(str).str.strip()

st.set_page_config(page_title="نظام البحث الذكي عن الأصول", layout="wide")
st.title("🔍 نظام البحث الذكي عن الأصول")

# اختيار نوع البحث
search_mode = st.radio("اختر طريقة البحث:", ["🔤 وصف الأصل", "🔢 Tag Number"])
result = pd.DataFrame()

if search_mode == "🔤 وصف الأصل":
    search_input = st.text_input("🔍 اكتب وصف الأصل (مثال: حاسب، طابعة، جهاز)")
    if search_input:
        # استخدام n-gram character-based TF-IDF
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
        tfidf_matrix = vectorizer.fit_transform(df["Asset Description"])
        query_vec = vectorizer.transform([search_input])
        similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

        df["تشابه"] = similarity_scores
        filtered = df[df["تشابه"] > 0.05].sort_values(by="تشابه", ascending=False).head(10)

        if not filtered.empty:
            st.success(f"تم العثور على {len(filtered)} نتيجة قريبة 👇")
            st.table(filtered[["Asset Description", "تشابه"]])
            selected_desc = st.selectbox("اختر وصف الأصل لعرض التفاصيل:", filtered["Asset Description"].values)
            result = df[df["Asset Description"] == selected_desc]
        else:
            st.warning("لم يتم العثور على أوصاف مشابهة.")

elif search_mode == "🔢 Tag Number":
    tag_number_input = st.text_input("أدخل رقم الأصل:")
    if tag_number_input:
        tag_column = [col for col in df.columns if "Tag number" in col]
        if tag_column:
            result = df[df[tag_column[0]].astype(str).str.strip() == tag_number_input]
        else:
            st.error("⚠️ لم يتم العثور على عمود رقم الأصل (Tag Number) في الملف.")

# اختيار البيانات التي يرغب المستخدم بعرضها
st.markdown("## حدد البيانات التي ترغب في عرضها")
options = st.multiselect(
    "اختر من التالي:",
    ["بيانات تعريف الأصل الأساسية", "تصنيف الأصل المحاسبي", "التفاصيل الفنية والمالية والموقع"],
    default=["بيانات تعريف الأصل الأساسية", "تصنيف الأصل المحاسبي", "التفاصيل الفنية والمالية والموقع"]
)

if not result.empty:
    if "بيانات تعريف الأصل الأساسية" in options:
        st.subheader("📘 بيانات تعريف الأصل الأساسية")
        cols = [
            "Unique Factory ID (Asset Serial Number)", 
            "Old Tag number", 
            "Custodian"
        ]
        existing_cols = [col for col in cols if col in df.columns]
        st.table(result[existing_cols])

    if "تصنيف الأصل المحاسبي" in options:
        st.subheader("📗 التصنيف المحاسبي")
        cols = [
            "Level 1 FA Module - Arabic Description", "Level 1 FA Module - English Description", "Level 1 FA Module Code",
            "Level 2 FA Module - Arabic Description", "Level 2 FA Module - English Description", "Level 2 FA Module Code",
            "Level 3 FA Module - Arabic Description", "Level 3 FA Module - English Description", "Level 3 FA Module Code",
            "accounting group Arabic Description", "accounting group English Description", "accounting group Code",
            "Asset Code For Accounting Purpose"
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
    st.info("⬅️ ابدأ بالبحث عن الأصل عن طريق الوصف أو رقم الأصل.")
