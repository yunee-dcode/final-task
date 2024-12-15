import streamlit as st
import pandas as pd
from io import BytesIO

st.sidebar.title("1. 친구의 장점 찾아주기")
st.sidebar.title("2. 장점 표 확인하기")
st.sidebar.title("3. 장점 그래프 완성하기")
st.sidebar.write("친구들이 생각하는 나의 장점은 무엇인가요?")

st.markdown(
    """
    <div style="text-align: center;">
        <h1><span style="color: white; background-color: black;">우리 반 </span> <span style="color: yellow; background-color: black;">시상식</span> 🎓</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 간결한 코드로 제목 표시
st.write('### 1. 모든 친구들에게 나의 장점을 물어보세요. 친구가 알려 준 나의 장점 두 가지에 표시해 보세요.')

# 열을 분리하고 사이에 빈 열 삽입
col1, spacer, col2 = st.columns([1, 1, 1])  # 비율 조정: 0.5로 간격 조정

#단 나누기
col1, col2 = st.columns(2)

with col2:
    st.write('<div style="font-size:18px; color:#0000FF; font-weight:bold;">※잠깐! 나의 장점을 알려준 고마운 친구의 이름에 먼저 표시해 봅시다.</div>', unsafe_allow_html=True)
    # 이름 리스트
    names = [
        "1. 재운", "2. 재준", "3. 태은", "4. 난먙",
        "5. 선홍", "6. 은수", "7. 인성", "8. 준현",
        "9. 시온", "10. 우재", "11. 주연", "12. 이한",
        "13. 애린", "14. 설하", "15. 성호", "16. 도연"
    ]
    # 4x4 레이아웃
    cols_per_row = 4  # 한 줄에 4개
    for i in range(0, len(names), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(names):
                col.checkbox(names[i + j])

with col1:
    data = pd.DataFrame({
        "번호": [1, 2, 3, 4, 5,6,7,8],
        "장점": ["청소를 잘 해요", "책을 많이 읽어요", "친절해요", "잘 웃어줘요", "그림을 잘 그려요", "규칙을 잘 지켜요", "골고루 잘 먹어요", "양보를 잘 해요"],
        "횟수": [0,0,0,0,0,0,0,0]
    })

    # 세션 상태에 데이터 저장
    if "data" not in st.session_state:
        st.session_state["data"] = data

    # 데이터프레임에 합계 추가
    data_with_total = st.session_state["data"].copy()
    # 합계 행을 DataFrame 형태로 생성
    total_row = pd.DataFrame({
        "번호": [None],
        "장점": ["합계"],
        "횟수": [data_with_total["횟수"].sum()]
    })
    data_with_total = pd.concat([data_with_total, total_row], ignore_index=True)

    # 제목 설정
    if "table_title" not in st.session_state:
        st.session_state["table_title"] = "친구들이 생각하는 나의 (  )별 투표 (  )"

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
        
        #cols[0].write(row["번호"])
        #cols[1].write(row["장점"])

        # 횟수를 즉각 반영
        count_placeholder = cols[2].empty()
        count_placeholder.markdown(
            f"""
            <div style="font-size: 18px;  font-weight: bold; text-align: center; 
                color: white; background-color: #A0A0FF; padding: 10px; 
                border-radius: 5px;  display: inline-block; height: 40px; width: 40px;">
                {row["횟수"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if cols[3].button("➕", key=f"btn_{index}"):
            st.session_state["data"].at[index, "횟수"] += 1
            # 업데이트된 횟수 즉시 반영
            count_placeholder.markdown(
                f"""
                <div style="
                    font-size: 20px; font-weight: bold; 
                    text-align: center;  color: yellow;  background-color: #5A5AFF; 
                    padding: 10px;   border-radius: 5px; 
                    display: inline-block;  height: 40px;   width: 40px;">
                    {st.session_state["data"].at[index, "횟수"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if cols[4].button("➖", key=f"btn_minus_{index}"):
            if st.session_state["data"].at[index, "횟수"] > 0:  # 0 이하로 내려가지 않도록 제한
                st.session_state["data"].at[index, "횟수"] -= 1
                # 업데이트된 횟수 즉시 반영
                count_placeholder.markdown(
                    f"""
                    <div style="
                        font-size: 20px; font-weight: bold; 
                        text-align: center;  color: yellow;   background-color: #FF5A5A; 
                        padding: 10px;   border-radius: 5px; 
                        display: inline-block;  height: 40px;  width: 40px;">
                        {st.session_state["data"].at[index, "횟수"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )     
    # 각 행에 버튼 추가
    for index, row in st.session_state["data"].iterrows():
        create_button_row(row, index)

st.write("")
st.write("")
st.write("")

# 최종 데이터 출력
st.write("### 2. 친구들이 알려려 준 나의 장점을 표로 확인해 봅시다.")
title_input = st.text_input("표의 제목은 어떻게 지으면 좋을까요? 제목을 짓고 제출버튼을 눌러 표를 확인하세요.", value=st.session_state["table_title"])
if st.button("제출"):
    st.session_state["table_title"] = title_input
    st.success("정답: 친구들이 생각하는 나의 장점별 투표 횟수")
st.write(f"##### {st.session_state['table_title']}")

st.write(data_with_total)

if st.button("표 저장하기"):
    buffer = BytesIO()
    data_with_total.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)  # 버퍼의 시작 위치로 이동

    # 사용자에게 다운로드 링크 제공
    st.download_button(
        label="엑셀 파일 다운로드",
        data=buffer,
        file_name="mytable.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
  
st.write("")
st.write("")

# 간결한 코드로 제목 표시
st.write("### 3. 위의 표를 참고하여 그래프를 완성해 봅시다. 빈칸을 누르면 ❤️가 나타납니다.")
st.write(
    '<div style="font-size:15px; font-weight:bold; color:#EB0000; text-align:right; padding:8px;">'
    '잘못 누른 경우 하트를 다시 한 번 누르세요. 하트가 사라집니다. <br>아래의 "그래프 완성"버튼을 눌러야 그래프가 완성됩니다.'
    '</div>',
    unsafe_allow_html=True
)

# 엑셀 파일 불러오기
uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])
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
                    
    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")
else:
    st.info("엑셀 파일을 업로드하세요.")
