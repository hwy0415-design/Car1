import streamlit as st

# 1. 리스트(list): 냉각수 선택지와 서킷 구간 데이터 정의
coolant_list = ["물-에틸렌글리콜", "절연 냉각유", "액체 질소 냉매"]
track_sectors = ["섹터 1 (직선 가속)", "섹터 2 (고속 코너)", "섹터 3 (최종 질주)"]


# 2. 함수(def): 냉각수, 유량, 배터리 출력을 입력받아 온도와 랩타임을 계산하는 함수
def simulate_race(coolant_type, flow_rate, power_mode):
    # 조건문(if-elif-else) 1: 선택한 냉각수 종류에 따라 열 흡수 효율(비열 특성) 설정
    if coolant_type == "물-에틸렌글리콜":
        cooling_efficiency = 4.0
    elif coolant_type == "절연 냉각유":
        cooling_efficiency = 5.5
    else:
        cooling_efficiency = 7.5

    # 배터리 온도 계산식: 기본 40도 + 발열량(출력 비례) - 냉각량(유량 × 냉각 효율)
    battery_temp = 40.0 + (power_mode * 0.8) - (flow_rate * cooling_efficiency)

    # 기본 랩타임 계산: 출력이 높을수록 기본 주행 시간이 단축됨
    base_time = 95.0 - (power_mode * 0.2)

    # 조건문(if-elif-else) 2: 계산된 배터리 온도에 따라 과열 여부와 최종 기록 판정
    if battery_temp > 80.0:
        status_type = "error"
        status_msg = "🔥 경고! 배터리 과열(열폭주 위험)로 출력이 강제 제한되었습니다!"
        lap_time = base_time + 12.0
        grade = "C등급 (과열 페널티)"
    elif battery_temp >= 40.0 and power_mode >= 85:
        status_type = "success"
        status_msg = "🏆 완벽한 제어! 최적 열교환과 풀파워 주행으로 신기록을 달성했습니다!"
        lap_time = base_time - (flow_rate * 0.3)
        grade = "S등급 (트랙 신기록)"
    elif battery_temp >= 40.0:
        status_type = "success"
        status_msg = "✅ 완주 성공! 배터리 온도가 안정 범위에서 유지되었습니다."
        lap_time = base_time - (flow_rate * 0.2)
        grade = "A등급 (안정 완주)"
    else:
        status_type = "warning"
        status_msg = "❄️ 주의! 과도한 냉각 펌프 가동으로 배터리 전력이 낭비되었습니다."
        lap_time = base_time + 5.0
        grade = "B등급 (에너지 손실)"

    # 반복문(for): 서킷 구간 리스트를 순회하며 표(테이블)에 들어갈 구간별 로그 생성
    sector_logs = []
    for sector in track_sectors:
        if battery_temp > 80.0:
            judgment = "위험"
            analysis = "열폭주 임박, 출력 강제 제한"
        elif battery_temp >= 40.0:
            judgment = "통과"
            analysis = "냉각수 열교환 효율 최적 유지"
        else:
            judgment = "주의"
            analysis = "과냉각으로 펌프 전력 손실 발생"

        sector_logs.append({
            "서킷 구간": sector,
            "판정": judgment,
            "열관리 상태 분석": analysis
        })

    return battery_temp, lap_time, grade, status_type, status_msg, sector_logs


# 3. Streamlit 웹 화면(UI) 구성
st.set_page_config(page_title="F1 배터리 냉각 레이싱", page_icon="🏎️")

st.title("🏎️ F1 하이퍼카 배터리 냉각 레이싱")
st.write("화학공학의 **열전달 및 열폭주 방지 원리**를 활용해 냉각 시스템을 튜닝하고 최고 랩타임에 도전하세요!")

st.divider()

# 사용자 입력 영역
selected_coolant = st.selectbox("(1) 냉각수 종류 선택", coolant_list)
selected_flow = st.slider("(2) 냉각수 유량 설정 (L/min)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
selected_power = st.slider("(3) 배터리 출력 모드 (%)", min_value=50, max_value=100, value=80, step=5)

# 버튼 클릭 시 시뮬레이션 함수 실행 및 결과 출력
if st.button("🏁 서킷 주행 시작!", use_container_width=True):
    final_temp, final_time, final_grade, msg_type, message, race_logs = simulate_race(
        selected_coolant, selected_flow, selected_power
    )

    st.divider()
    st.subheader("📊 레이싱 시뮬레이션 결과")

    # (1) 상태 메시지 출력
    if msg_type == "success":
        st.success(message)
    elif msg_type == "warning":
        st.warning(message)
    else:
        st.error(message)

    # (2) 강조 수치(Metric) 출력
    st.metric(
        label="최종 랩타임 & 레이싱 등급",
        value=f"{final_time:.1f}초 ({final_grade})",
        delta=f"최고 배터리 온도: {final_temp:.1f} °C"
    )

    # (3) 테이블(표) 출력
    st.write("**서킷 구간별 배터리 온도 및 냉각 로그**")
    st.dataframe(race_logs, hide_index=True, use_container_width=True)
