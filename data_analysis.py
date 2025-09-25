import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

print("="*60)
print("CORD-19 METADATA ANALYSIS")
print("="*60)

# --- Part 1: Load and Explore ---
try:
    df = pd.read_csv("metadata.csv")  # or use metadata_sample.csv
    print("✅ Dataset loaded successfully!")
except FileNotFoundError:
    print("❌ metadata.csv not found. Please upload the file.")
    exit()

print("\nFirst 5 rows:")
print(df.head())

print("\nShape:", df.shape)
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())

print("\nBasic statistics:")
print(df.describe())

# --- Part 2: Cleaning ---
# Drop columns with too many missing values
missing_ratio = df.isnull().mean()
to_drop = missing_ratio[missing_ratio > 0.5].index
df_clean = df.drop(columns=to_drop)

# Fill missing abstracts with empty string
df_clean["abstract"] = df_clean["abstract"].fillna("")

# Convert publish_time to datetime
df_clean["publish_time"] = pd.to_datetime(df_clean["publish_time"], errors="coerce")
df_clean["year"] = df_clean["publish_time"].dt.year

# Add abstract word count
df_clean["abstract_word_count"] = df_clean["abstract"].apply(lambda x: len(str(x).split()))

print("\n✅ Data cleaned successfully")

# --- Part 3: Analysis ---
# Count by year
papers_per_year = df_clean["year"].value_counts().sort_index()
print("\nPapers by year:\n", papers_per_year)

# Top journals
top_journals = df_clean["journal"].value_counts().head(10)
print("\nTop journals:\n", top_journals)

# Frequent words in titles
all_titles = " ".join(df_clean["title"].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_titles)

# --- Visualizations ---
# 1. Publications over time
plt.figure(figsize=(10,6))
papers_per_year.plot(kind="line", marker="o")
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.grid(True)
plt.show()

# 2. Top publishing journals
plt.figure(figsize=(10,6))
top_journals.plot(kind="bar")
plt.title("Top Publishing Journals")
plt.xlabel("Journal")
plt.ylabel("Number of Papers")
plt.xticks(rotation=45)
plt.show()

# 3. Word cloud of titles
plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Frequent Words in Paper Titles")
plt.show()

# 4. Distribution by source
plt.figure(figsize=(10,6))
df_clean["source_x"].value_counts().head(10).plot(kind="bar")
plt.title("Top Sources of Papers")
plt.xlabel("Source")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()
