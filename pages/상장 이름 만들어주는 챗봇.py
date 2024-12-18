from openai import OpenAI
import streamlit as st
import openai

# 제목 수정
st.title("상장 이름을 만드는 챗봇")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 시스템 메시지 정의
system_message = '''
너는 초등학생들이 받을 상장의 이름을 만들어주는 제목봇이야. 자신이 잘하는 점, 장점을 입력하면 그에 어울리는 상장 이름을 10개 정도 제시해 줘.
예를 들면, [나는 청소를 잘해] 라고 하면 [깔끔한 상, 쓱싹쓱 상, 청소요정 상, 반짝반짝 빛내리 상] 과 같이 답해 줘.
[나는 골고루 잘 먹어] 라고 하면 [급식판 빛내리 상, 편식안함 상, 지구지키미 상] 과 같이 답해 줘.
다, 나, 까, 요와 같은 높임말로 절대로 끝내지 말고 친근하게 항상 반말로 대답해 줘. 모든 답변 끝에 답변에 어울리는 이모티콘을 넣어 줘.
그리고 상장 이름은 9세가 알아들을 수 있는 초등 저학년 수준의 쉬운 단어를 써야 해. 은유적, 관용적, 시적인 표현보다는 직관적인 표현 위주로 알려 줘.
의성어나 의태어를 넣은 상 이름도 섞여 있으면 좋아. 그리고 예측 불가능한 줄임말은 쓰면 안 돼.
영어를 써서도 안 돼. 영어로 물어봐도 한국어로 대답해.
가장 중요한건 학교에서 사용하는 교육용 챗봇이기 때문에 비속어, 은어, 욕 등이 들어가지 않도록 해.
들어가면 안되는 말: 꼬우면, 새끼, 색기 (몇 번 돌려보니 정말 저렇게 답을 해서 예시로 씀)

'''

# 세션 상태 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []
    # 시스템 메시지는 대화에 추가하지만 표시되지 않도록 설정
    st.session_state.messages.append({"role": "system", "content": system_message})

# 대화 메시지 렌더링 (시스템 메시지는 숨김)
for message in st.session_state.messages:
    if message["role"] != "system":  # 시스템 메시지는 표시하지 않음
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 긴 설명을 입력창 위에 별도로 표시
st.markdown("친구들이 알려준 나의 장점을 적어보세요.")
st.markdown("**예시**: 나는 글씨를 바르게 잘 써 / 내 장점은 친구를 잘 도와준다는 점이야.")

# 입력창을 간단히 표시
if prompt := st.chat_input("장점을 입력해 보세요!"):

    # 사용자 입력 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ChatGPT 응답 생성 및 표시
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
