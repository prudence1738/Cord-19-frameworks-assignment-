print("Python is working!")
print("Testing basic imports...")

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import streamlit as st
    from wordcloud import WordCloud
    print("✅ All imports successful!")
    print(f"Pandas version: {pd.__version__}")
except ImportError as e:
    print(f"❌ Import error: {e}")
