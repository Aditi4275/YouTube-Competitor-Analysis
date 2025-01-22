import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_chart(channels, chart_type):
    if not channels:
        raise ValueError("No channel data provided.")
    
    df = pd.DataFrame(channels)
    
    for col in ["subscribers", "video_count", "total_likes", "view_count"]:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)
    
    plt.figure(figsize=(10,6))
    
    if chart_type == "subscribers":
        df_sorted = df.sort_values(by='subscribers', ascending=False)
        sns.barplot(x="title", y="subscribers", data=df_sorted)
    elif chart_type == "video_count":
        df_sorted = df.sort_values(by="video_count", ascending=False)
        sns.barplot(x="title", y="video_count", data=df_sorted)
    elif chart_type == "total_likes":
        df_sorted = df.sort_values(by='total_likes', ascending=False)
        sns.barplot(x='title', y='total_likes', data=df_sorted)
    elif chart_type == "view_count":
        df_sorted = df.sort_values(by='view_count', ascending=False)
        sns.barplot(x='title', y='view_count', data=df_sorted)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    chart_file = f"static/{chart_type}_chart.png"
    plt.savefig(chart_file)
    plt.close()
    return f"{chart_type}_chart.png"