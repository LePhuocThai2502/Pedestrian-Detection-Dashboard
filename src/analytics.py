import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from src.config import HISTORY_PATH

def get_stats(tab="image"):
    folder = os.path.join(HISTORY_PATH, tab)
    log_path = os.path.join(folder, "log.csv")
    import pandas as pd
    if not os.path.exists(log_path):
        return pd.DataFrame()
    df = pd.read_csv(log_path)
    # Đảm bảo cột num_person là số
    df["num_person"] = pd.to_numeric(df["num_person"], errors="coerce").fillna(0).astype(int)
    return df


def plot_stats(stats_df):
    if stats_df.empty:
        return None
    fig, ax = plt.subplots()
    stats_df["num_person"].plot(kind="bar", ax=ax)
    plt.title("Số người phát hiện trên từng ảnh")
    plt.xlabel("Ảnh")
    plt.ylabel("Số người")
    return fig
