import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="منصة رصد اتجاهات التقنية وسوق العمل",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 منصة رصد اتجاهات التقنية وتنبؤ المهارات المطلوبة")
st.markdown("""
منصة تحليلات ذكية ترصد الطلب على التقنيات والمهارات الحالية (مثل الذكاء الاصطناعي، تحليلات البيانات، ونظم المعلومات)، وتتنبأ بالاتجاهات المستقبلية في سوق العمل.
""")
st.divider()

@st.cache_data
def load_market_data():
    return pd.read_csv("data/job_market_data.csv")

try:
    df = load_market_data()
except Exception:
    data = {
        'Skill': ['Python', 'Python', 'Python', 'SQL', 'SQL', 'SQL', 'Power BI', 'Power BI', 'Power BI', 'PyTorch/AI', 'PyTorch/AI', 'PyTorch/AI'],
        'Year': [2022, 2023, 2024, 2022, 2023, 2024, 2022, 2023, 2024, 2022, 2023, 2024],
        'Job_Postings_Demand': [1200, 1600, 2100, 1500, 1800, 2200, 800, 1100, 1500, 400, 950, 1700],
        'Domain': ['Data & AI', 'Data & AI', 'Data & AI', 'Data & Systems', 'Data & Systems', 'Data & Systems', 'Business Intelligence', 'Business Intelligence', 'Business Intelligence', 'Artificial Intelligence', 'Artificial Intelligence', 'Artificial Intelligence']
    }
    df = pd.DataFrame(data)

st.sidebar.header("🎯 خيارات التصفية")
selected_domain = st.sidebar.multiselect(
    "اختر المجال التقني:",
    options=df['Domain'].unique(),
    default=df['Domain'].unique()
)

filtered_df = df[df['Domain'].isin(selected_domain)]

col1, col2, col3 = st.columns(3)
col1.metric("عدد المهارات المرصودة", len(filtered_df['Skill'].unique()))
col2.metric("إجمالي الطلب الوظيفي (2024)", f"{filtered_df[filtered_df['Year'] == 2024]['Job_Postings_Demand'].sum():,} إعلان")
col3.metric("المهارة الأكثر نمواً", "PyTorch / AI (+78%)")

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 مسار نمو الطلب على المهارات (2022 - 2024)")
    fig_line = px.line(
        filtered_df, 
        x='Year', 
        y='Job_Postings_Demand', 
        color='Skill', 
        markers=True,
        labels={'Job_Postings_Demand': 'عدد الإعلانات الوظيفية', 'Year': 'السنة', 'Skill': 'المهارة'}
    )
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.subheader("📊 توزيع الطلب حسب المهارة لعام 2024")
    df_2024 = filtered_df[filtered_df['Year'] == 2024]
    fig_bar = px.bar(
        df_2024, 
        x='Skill', 
        y='Job_Postings_Demand', 
        color='Skill', 
        text_auto=True,
        labels={'Job_Postings_Demand': 'عدد الإعلانات', 'Skill': 'المهارة'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.subheader("🔮 التنبؤ بالطلب المستقبلي على المهارة (2026/2027)")

skill_to_predict = st.selectbox("اختر المهارة للتنبؤ بمستقبلها:", df['Skill'].unique())

skill_data = df[df['Skill'] == skill_to_predict]
X = skill_data[['Year']].values
y = skill_data['Job_Postings_Demand'].values

model = LinearRegression()
model.fit(X, y)

pred_2026 = model.predict(np.array([[2026]]))[0]

st.success(f"الطلب الوظيفي المتوقع على مهارة **{skill_to_predict}** في عام 2026 هو حوالي: **{int(pred_2026):,} إعلان وظيفي**")
