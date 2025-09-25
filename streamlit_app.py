import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("metadata.csv")  # or metadata_sample.csv

df = load_data()
df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
df["year"] = df["publish_time"].dt.year

# Show sample
st.subheader("Sample Data")
st.write(df.head())

# Filter by year
years = df["year"].dropna().unique()
min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.slider("Select year range", min_year, max_year, (2020, 2021))
filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

st.subheader("Publications by Year")
papers_per_year = filtered["year"].value_counts().sort_index()
st.bar_chart(papers_per_year)

# Word cloud of titles
all_titles = " ".join(filtered["title"].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_titles)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)
