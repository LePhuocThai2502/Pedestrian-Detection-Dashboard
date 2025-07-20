import streamlit as st
from src.detector import PedestrianDetector
from src.utils import draw_boxes, save_temp_image, save_history, clear_temp_files
from src.analytics import get_stats, plot_stats
from src.config import APP_INFO, LOGO_PATH
import os
import time

# ====== SETUP APP & CUSTOM CSS ======
st.set_page_config(page_title=APP_INFO["title"], layout="wide", page_icon="🚶")
st.markdown("""
<style>
body, .main, .stApp {
    background: #181a20 !important;
    color: #e4e6eb !important;
}
h1 {
    font-size: 2.6rem;
    font-weight: 900;
    color: #2d5be3 !important;
    letter-spacing: 1px;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid #2d5be3;
}
.stTabs [data-baseweb="tab"] {
    font-size: 1.12rem;
    color: #aaa;
    padding: 0.7rem 1.3rem 0.5rem 1.3rem;
}
.stTabs [aria-selected="true"] {
    color: #fff !important;
    font-weight: 800;
    border-bottom: 4px solid #2d5be3 !important;
    background: #23272f !important;
}
.stSidebar {
    background: #15161c !important;
}
.sidebar-content {
    padding: 2rem 1.2rem 1rem 1.2rem;
}
.stSlider > div[data-testid="stSlider"] {
    color: #2d5be3 !important;
}
.stButton button {
    border-radius: 1.2rem !important;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.55rem 1.6rem;
    background: linear-gradient(90deg, #2d5be3 0%, #4ecdc4 100%) !important;
    border: none;
}
.stProgress > div > div {
    background-image: linear-gradient(90deg,#2d5be3 20%,#4ecdc4 100%);
}
.uploadedFileName {
    font-size: 1rem;
    color: #2d5be3;
    font-weight: bold;
}
hr {
    border: 0;
    border-top: 2px solid #2d5be3;
}
.stAlert {
    border-radius: 1.3rem;
    font-size: 1.02rem;
    padding: 1rem;
}
/* Hide deprecation warning */
[data-testid="stNotificationContentWarning"] {display: none;}
/* Rounded image */
img {
    border-radius: 16px !important;
    box-shadow: 0 4px 28px 0 rgba(0,0,0,0.23);
}
</style>
""", unsafe_allow_html=True)

# ====== SIDEBAR ======
with st.sidebar:
    st.image(LOGO_PATH, width=120)
    st.markdown(APP_INFO["guide"])

# ====== MAIN HEADER ======
st.markdown(
    "<h1 style='font-size:2.6rem;font-weight:900;color:#2d5be3;margin-bottom:0.25em'>Pedestrian Detection Dashboard 🚶‍♂️</h1>"
    "<div style='font-size:1.3rem;font-weight:500;color:#53d0c5;margin-bottom:1.5em;'>Nhanh – Chính xác – Giao diện hiện đại</div>",
    unsafe_allow_html=True
)
st.markdown(f"<span>{APP_INFO['desc']}</span>", unsafe_allow_html=True)

tabs = st.tabs(["Ảnh", "Video/Webcam", "Analytics/History"])

# ====== TAB 1: IMAGE DETECTION ======
with tabs[0]:
    st.subheader("Nhận diện người đi bộ trên ảnh")
    threshold = st.slider("Threshold phát hiện", min_value=0.1, max_value=0.9, value=0.3, step=0.05)
    files = st.file_uploader(
        "Chọn ảnh (có thể chọn nhiều)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    detector = PedestrianDetector()
    if files:
        # Hiển thị mini preview các ảnh đã chọn
        cols = st.columns(len(files)) if len(files) < 5 else st.columns(5)
        for idx, f in enumerate(files):
            with cols[idx % 5]:
                st.image(f, width=100, caption=f.name, use_container_width=False)

    if st.button("Detect ảnh", type="primary"):
        if files:
            clear_temp_files()
            results = []
            if len(files) > 1:
                progress = st.progress(0)
            for idx, f in enumerate(files):
                tmp_path = save_temp_image(f)
                result = detector.detect(tmp_path, conf=threshold)
                out_img = draw_boxes(result)
                st.image(
                    out_img,
                    caption=f"{f.name} - Số người: {len(result.boxes)}",
                    use_container_width=True,
                    output_format="JPEG"
                )
                save_history(out_img, f.name, len(result.boxes), tab="image")
                results.append({
                    "filename": f.name,
                    "count": len(result.boxes),
                })
                if len(files) > 1:
                    progress.progress((idx+1)/len(files))
            st.success(f"✅ Đã detect {len(results)} ảnh thành công!", icon="✅")

# ====== TAB 2: VIDEO/WEBCAM (Demo, sẽ nâng cấp nếu cần) ======
with tabs[1]:
    st.subheader("Nhận diện trên Video/Webcam")
    st.info("🎥 Chức năng này sẽ được nâng cấp ở phiên bản tiếp theo hoặc theo yêu cầu.")

# ====== TAB 3: ANALYTICS/HISTORY ======
with tabs[2]:
    st.subheader("Analytics & Lịch sử")
    stats_df = get_stats()
    if not stats_df.empty:
        fig = plot_stats(stats_df)
        if fig:
            st.pyplot(fig)
        st.dataframe(stats_df)
    else:
        st.info("Chưa có dữ liệu lịch sử!")


