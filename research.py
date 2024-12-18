import streamlit as st
import pandas as pd
from io import BytesIO

# 반응형 디자인을 위한 CSS 추가
st.markdown(
    """
    <style>
    @media (max-width: 768px) {
        .block-container { padding: 1rem; }
        h1 { font-size: 24px !important; }
        p { font-size: 16px !important; }
        .stButton button { font-size: 14px !important; }
    }
    @media (min-width: 769px) {
        .block-container { padding: 2rem; }
        h1 { font-size: 32px !important; }
        p { font-size: 18px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: left;">
        <h1>🎓<span style="color: white; background-color: black;">우리 반 </span> <span style="color: yellow; background-color: black;">시상식</span> 🎓</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<p style="font-size: 25px;font-weight:bold;"> 1️⃣ 모든 친구들에게 나의 장점을 물어보세요. 친구가 알려 준 나의 장점 두 가지에 표시해 보세요.</p>', unsafe_allow_html=True)

st.write('<div style="font-size:18px; color:#0000FF;">※잠깐! 나의 장점을 알려준 고마운 친구의 이름에 먼저 표시해 봅시다.</div>', unsafe_allow_html=True)

# 이름 리스트
names = [
    "1. 재운", "2. 재준", "3. 태은", "4. 난먙", "5. 선홍", "6. 은수", "7. 인성", "8. 준현",
    "9. 시온", "10. 우재", "11. 주연", "12. 이한", "13. 애린", "14. 설하", "15. 성호", "16. 도연"
]

# 8*2 레이아웃
cols_per_row = 2
for i in range(0, len(names), cols_per_row * 8):
    rows = st.columns(8)
    for row_idx, row in enumerate(rows):
        for j in range(cols_per_row):
            name_idx = i + row_idx * cols_per_row + j
            if name_idx < len(names):
               row.checkbox(names[name_idx])
                
# 장점 데이터 생성
data = pd.DataFrame({
    "번호": [1, 2, 3, 4, 5, 6, 7, 8],
    "장점": [
        "청소를 잘 해요", "책을 많이 읽어요", "친절해요", "잘 웃어줘요",
        "그림을 잘 그려요", "규칙을 잘 지켜요", "골고루 잘 먹어요", "양보를 잘 해요"
    ],
    "횟수": [0, 0, 0, 0, 0, 0, 0, 0]
})

# 세션 상태 초기화
if "data" not in st.session_state:
    st.session_state["data"] = data

# 데이터프레임에 합계 추가
data_with_total = st.session_state["data"].copy()
total_row = pd.DataFrame({
    "번호": [None],
    "장점": ["합계"],
    "횟수": [data_with_total["횟수"].sum()]
})
data_with_total = pd.concat([data_with_total, total_row], ignore_index=True)



st.write(
    '<div style="font-size:15px; color:#333; text-align:right; padding:10px;">'
    '친구가 알려준 나의 장점 ➕ 누르기 <br> 잘못 입력한 경우 ➖ 누르기'
    '</div>',
    unsafe_allow_html=True
)

def create_button_row(row, index):
    cols = st.columns([0.5, 3, 1, 1, 1])
    cols[0].write(f"<div style='font-size:18px; text-align:center;'>{row['번호']}</div>", unsafe_allow_html=True)
    cols[1].write(f"<div style='font-size:18px;'>{row['장점']}</div>", unsafe_allow_html=True)

    # 횟수를 즉각 반영
    count_placeholder = cols[2].empty()
    count_placeholder.markdown(
        f"""
        <div style="font-size: 18px; font-weight: bold; text-align: center; 
            color: white; background-color: #A0A0FF; padding: 10px; 
            border-radius: 5px; display: inline-block; height: 40px; width: 40px;">
            {row['횟수']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if cols[3].button("➕", key=f"btn_{index}"):
        st.session_state["data"].at[index, "횟수"] += 1

    if cols[4].button("➖", key=f"btn_minus_{index}"):
        if st.session_state["data"].at[index, "횟수"] > 0:
            st.session_state["data"].at[index, "횟수"] -= 1

# 각 행에 버튼 추가
for index, row in st.session_state["data"].iterrows():
    create_button_row(row, index)

st.write("")
st.write("")
st.markdown('<p style="font-size: 25px;font-weight:bold;"> 2️⃣ 친구들이 알려려 준 나의 장점을 표로 확인해 봅시다.</p>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    def clear_default_text():
        if "default_text_cleared" not in st.session_state:
            st.session_state["default_text_cleared"] = False

        if not st.session_state["default_text_cleared"]:
            st.session_state["table_title"] = ""
            st.session_state["default_text_cleared"] = True
    title_input = st.text_input(
        "표의 제목: 친구들이 생각하는 나의 ⬜️⬜️별 투표 ⬜️⬜️",
        value=st.session_state.get("table_title", ""),
        key="title_input",
        placeholder="빈 칸에 들어갈 말을 써 봅시다.",
        on_change=clear_default_text
    )
   
with col2:
    if st.button("정답 확인", key="custom_button"):
        st.session_state["table_title"] = "친구들이 생각하는 나의 장점별 투표 횟수"
        st.success("장점, 횟수")

# 데이터프레임 표시
st.dataframe(data_with_total)

# 표 저장 버튼과 안내 텍스트
col1, col2 = st.columns([1, 3])

with col1:
    buffer = BytesIO()
    data_with_total.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)  # 버퍼의 시작 위치로 이동

    # 바로 다운로드
    st.download_button(
        label="표 저장하기",
        data=buffer,
        file_name="mytable.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col2:
    st.markdown('<p style="font-size:20px;"> 🔔왼쪽 버튼을 눌러 표를 저장하세요.</p>', unsafe_allow_html=True)

# 간결한 코드로 제목 표시
st.markdown('<p style="font-size: 25px;font-weight:bold;"> 3️⃣ 저장한 표를 불러오세요. 빈칸을 눌러 ❤️를 채워 그래프를 완성해 보세요.</p>', unsafe_allow_html=True)
st.markdown(
    '<div style="font-size:15px; font-weight:bold; color:#EB0000; text-align:right; padding:8px;">'
    '잘못 누른 경우 ❤️를 다시 한 번 누르세요. ❤️가 사라집니다. <br>아래의 "그래프 완성"버튼을 눌러야 그래프가 완성됩니다. '
    '</div>',
    unsafe_allow_html=True
)

# 엑셀 파일 불러오기
uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])
st.markdown(
    "<span class='file-uploader-note'>위에서 저장한 '표'를 불러오세요.</span>",
    unsafe_allow_html=True
)
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file).iloc[:-1]
    
# 데이터프레임 처리
    max_count = int(data["횟수"].max())  # 횟수의 최댓값
    columns = [str(i+1) for i in range(max_count)]  # 열 이름 생성

# 데이터프레임 확장
    data_extended = data.drop(columns=["횟수"], errors="ignore").copy()  # '횟수' 열 제거
    for col in columns:
        data_extended[col] = " "  # 빈 열 추가

# 표 시각적 효과를 위한 상태 관리
    if "cells" not in st.session_state:
        st.session_state["cells"] = {
        f"cell_{i}_{j}": " " for i in range(len(data_extended)) for j in range(len(columns))
        }

    def render_interactive_table():
        if len(columns) == 0:
            st.warning("표시할 열이 없습니다. 데이터가 제대로 준비되었는지 확인하세요.")
            return
        
        for i, row in data_extended.iterrows():
            st.write(f"**{row['장점']}**")
            cols = st.columns(len(columns))
            for j, col in enumerate(columns):
                key = f"cell_{i}_{j}"
                cell_value = st.session_state["cells"].get(key, " ")
                if cols[j].button(cell_value, key=key):
                # 상태 업데이트
                    st.session_state["cells"][key] = "❤️" if cell_value == " " else " "

# 확장된 데이터프레임 표시
    render_interactive_table()

# 확장된 데이터 저장
    if st.button("그래프 완성"):
            # 셀 상태를 데이터프레임에 반영
            for i in range(len(data_extended)):
                for j, col in enumerate(columns):
                    key = f"cell_{i}_{j}"
                    data_extended.at[i, col] = st.session_state["cells"].get(key, " ")
                    

else:
    st.info("입력된 자료가 없습니다.")
