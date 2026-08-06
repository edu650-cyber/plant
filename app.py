# ==============================================================================
# 프로젝트명: 제주 바이오 활성 예측 시스템 (Streamlit Web App)
# 설명: 제주 자생식물의 항산화 성분 및 표적 단백질 억제 활성을 예측하는 웹 애플리케이션 기본 골격
# 작성 언어: Python (Streamlit)
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import time

# ------------------------------------------------------------------------------
# 1. 페이지 기본 설정 (페이지 제목, 레이아웃, 아이콘)
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="제주 바이오 활성 예측 시스템",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# 2. Custom CSS 스타일링 (깔끔한 Green & Orange 포인트 바이오테크 스타일)
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    /* 메인 배경 및 본문 폰트 설정 */
    .main {
        background-color: #f9fbf8;
    }
    
    /* 상단 메인 헤더 스타일링 */
    .header-container {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        padding: 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .header-subtitle {
        font-size: 1.1rem;
        color: #e8f5e9;
        line-height: 1.6;
    }
    
    /* 사이드바 스타일링 */
    section[data-testid="stSidebar"] {
        background-color: #f1f8e9;
        border-right: 1px solid #c8e6c9;
    }
    
    /* 강조 주황색 서브 포인트 */
    .orange-highlight {
        color: #e65100;
        font-weight: bold;
    }
    
    /* 정보 카어드 박스 디자인 */
    .info-card {
        background-color: #ffffff;
        border-left: 5px solid #2e7d32;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* 주황색 아웃라인 포인트 카드 */
    .highlight-card {
        background-color: #fff8e1;
        border-left: 5px solid #ff9800;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_gradient=True, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. 사이드바 (Sidebar) 메뉴 구성
# ------------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/000000/sprout.png", width=70)
st.sidebar.title("🔬 예측 시뮬레이션 설정")
st.sidebar.markdown("---")

# [1] 제주 자생식물 선택
st.sidebar.subheader("🌱 [1] 제주 자생식물 선택")
plant_list = [
    "황칠나무 (Dendropanax morbiferus)",
    "동백나무 (Camellia japonica)",
    "제주진달래 (Rhododendron mucronulatum)",
    "황근 (Hibiscus hamabo)",
    "순비기나무 (Vitex rotundifolia)",
    "초피나무 (Zanthoxylum piperitum)"
]
selected_plant = st.sidebar.selectbox(
    "분석할 자생식물을 선택하세요:",
    options=plant_list,
    index=0,
    help="제주지역에서 자생하는 주요 바이오 소재 식물 목록입니다."
)

# 선택한 식물의 주요 성분 정보 미리보기
st.sidebar.caption(f"💡 **선택된 소재:** <span class='orange-highlight'>{selected_plant.split(' (')[0]}</span>", unsafe_allow_html=True)

st.sidebar.markdown("---")

# [2] 표적 단백질 선택
st.sidebar.subheader("🧬 [2] 표적 단백질 선택")
protein_list = [
    "COX-2 (염증 반응 표적 단백질)",
    "Tyrosinase (미백/멜라닌 합성 표적)",
    "MMP-1 (주름 개선/콜라겐 분해 효소)",
    "Alpha-Glucosidase (항당뇨 관련 표적)",
    "Keap1 (Nrf2 항산화 경로 표적 단백질)"
]
selected_protein = st.sidebar.selectbox(
    "억제 예측 대상 표적 단백질을 선택하세요:",
    options=protein_list,
    index=0,
    help="항산화 및 생리활성 예측 시 타겟으로 설정할 단백질/효소입니다."
)

st.sidebar.markdown("---")

# [3] 시뮬레이션 조건 설정
st.sidebar.subheader("⚙️ [3] 시뮬레이션 조건 설정")

# 조건 - 추출 용매
solvent = st.sidebar.select_slider(
    "추출 용매 (에탄올 농도 %):",
    options=[0, 30, 50, 70, 100],
    value=70,
    help="식물 유효성분 추출 시 사용되는 에탄올 농도 조건입니다."
)

# 조건 - 추출 온도
temperature = st.sidebar.slider(
    "추출 온도 (°C):",
    min_value=20,
    max_value=100,
    value=60,
    step=5,
    help="추출 과정의 설정 온도입니다."
)

# 조건 - 시뮬레이션 실행 버튼
st.sidebar.markdown("---")
run_button = st.sidebar.button("🚀 예측 시뮬레이션 실행", use_container_width=True, type="primary")


# ------------------------------------------------------------------------------
# 4. 메인 화면 헤더 및 프로젝트 소개
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="header-container">
        <div class="header-title">🌿 제주 바이오 활성 예측 시스템</div>
        <div class="header-subtitle">
            Jeju Native Plant Antioxidant & Target Protein Inhibition Prediction System
            <br><br>
            본 시스템은 <b>제주 자생식물 유래 천연물</b>의 항산화 활성 및 주요 질환 관련 <b>표적 단백질 억제 효능</b>을 AI 기반 AI-In-Silico 기술로 예측하는 바이오테크 플랫폼입니다.
        </div>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. 메인 화면 컨텐츠 영역 (대시보드 레이아웃)
# ------------------------------------------------------------------------------

# 대시보드 2열 컬럼 구성
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
        <div class="info-card">
            <h4 style="color: #1b5e20; margin-top:0;">📌 선택된 분석 조건 개요</h4>
            <ul>
                <li><b>자생식물:</b> <span class="orange-highlight">{}</span></li>
                <li><b>표적 단백질:</b> <b>{}</b></li>
                <li><b>추출 조건:</b> 에탄올 {}% / {}°C</li>
            </ul>
        </div>
    """.format(selected_plant, selected_protein, solvent, temperature), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="highlight-card">
            <h4 style="color: #e65100; margin-top:0;">💡 시스템 활용 안내</h4>
            <p style="font-size: 0.95rem; color: #424242;">
                좌측 사이드바에서 자생식물 및 단백질 타겟을 지정한 뒤 <b>[예측 시뮬레이션 실행]</b> 버튼을 누르면,
                딥러닝/분자 도킹 모델 기반 항산화 IC50 수치 및 억제율 예측 결과를 확인할 수 있습니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("### 📊 자생식물 성분 및 활성 예측 미리보기")

# 예측 실행 시 시뮬레이션 결과 출력 (버튼 클릭 전/후 동적 변화)
if run_button:
    with st.spinner("딥러닝 모델 기반 인실리코(In-silico) 활성 예측 분석 중..."):
        time.sleep(1.2) # 시뮬레이션 연산 대기 시간 연출
    
    st.success(f"✅ '{selected_plant.split(' (')[0]}' 소재의 '{selected_protein.split(' (')[0]}' 표적 억제 예측이 완료되었습니다!")
    
    # 결과 지표 3개 메트릭 표시
    m1, m2, m3 = st.columns(3)
    m1.metric(label="예측 항산화 활성 (DPPH IC50)", value="12.4 μg/mL", delta="-2.1 μg/mL (우수)")
    m2.metric(label="표적 단백질 억제율 (Inhibition)", value="84.2 %", delta="+12.5%")
    m3.metric(label="결합 친화도 (Binding Affinity)", value="-8.7 kcal/mol", delta="강한 결합")
    
    # 예시 예측 결과 그래프
    st.subheader("📈 추출 온도별 예상 표적 억제 활성 변이")
    chart_data = pd.DataFrame({
        "온도 (°C)": [20, 40, 60, 80, 100],
        "예측 억제율 (%)": [45, 62, 84, 78, 51]
    })
    st.line_chart(chart_data, x="온도 (°C)", y="예측 억제율 (%)")

else:
    # 기본 대기 상태 표시
    st.info("👈 좌측 사이드바에서 원하는 조건을 설정하고 [예측 시뮬레이션 실행] 버튼을 클릭하세요.")
    
    # 기본 더미 샘플 데이터 테이블
    sample_df = pd.DataFrame({
        "주요 주요 지표": ["DPPH 라디칼 소거능", "ABTS 소거능", "표적 단백질 결합 에너지"],
        "기존 실험 평균값": ["18.5 μg/mL", "24.1 μg/mL", "-7.2 kcal/mol"],
        "AI 예측 기대치": ["12.4 μg/mL", "16.8 μg/mL", "-8.7 kcal/mol"],
        "상태": ["High", "Medium-High", "Optimal"]
    })
    st.dataframe(sample_df, use_container_width=True)

# ------------------------------------------------------------------------------
# 6. 하단 푸터 (Footer)
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #757575; font-size: 0.85rem;">
        © 2026 Jeju Bio-Resource AI Research Center | Jeju Native Plant Bioactivity Prediction Web Framework
    </div>
    """,
    unsafe_allow_html=True
)
