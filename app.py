
import streamlit as st
import requests
import datetime

SUPABASE_URL = "https://hmdazhipjqqstdykdzyp.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhtZGF6aGlwanFxc3RkeWtkenlwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkyMDYxNjAsImV4cCI6MjA2NDc4MjE2MH0.mHUz2csaKDb8epR3NZGyxk6NCpNhQPCi44y7B_HQS0I"
headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(layout="wide")
st.title("✅ 원용이 체크리스트 (110점 만점 / Supabase 연동)")

selected_date = st.date_input("날짜 선택", datetime.date.today())
items = ['거짓말하지 않기 / 부모님 속이지 않기', '욕설 사용 금지', '형제에게 신체적 폭력 금지', '학원 출석', '학원/과외 숙제 완수', '타 스마트폰 몰래 사용', 'PC방 무단 출입 없음', '방과 후 무단 체류 없음', '식사 1인분 혼자 힘으로', '남의 물건 훔치기', '스마트폰 시간 달라고 조르지 않기']
checks = [st.checkbox(item) for item in items]
full_score = 110
score = full_score - sum(checks) * 10
st.markdown(f"### 🔻 오늘 점수: {score} / {full_score}")

if st.button("💾 저장하기"):
    payload = {
        "date": str(selected_date),
        "score": score
    }
    res = requests.post(f"{SUPABASE_URL}/rest/v1/wonyong_checklist", headers=headers, json=payload)
    if res.status_code == 201:
        st.success("저장 완료!")
    else:
        st.error(f"저장 실패: {res.status_code} - {res.text}")

# 이전 기록 보기
st.divider()
st.subheader("📖 이전 기록 보기")
res = requests.get(f"{SUPABASE_URL}/rest/v1/wonyong_checklist?select=*&order=date.desc", headers=headers)
if res.status_code == 200:
    data = res.json()
    if data:
        for r in data:
            st.write(f"📅 {r['date']} — 점수: {r['score']}")
    else:
        st.info("저장된 기록이 없습니다.")
else:
    st.error(f"기록 불러오기 실패: {res.status_code}")

# 삭제 기능
st.divider()
st.subheader("🗑️ 저장된 기록 삭제")
if res.status_code == 200 and data:
    records = {f"{r['date']} - 점수: {r['score']}": r["id"] for r in data if 'id' in r}
    selected = st.selectbox("삭제할 기록을 선택하세요", list(records.keys()))
    if st.button("❌ 선택한 기록 삭제"):
        record_id = records[selected]
        del_res = requests.delete(f"{SUPABASE_URL}/rest/v1/wonyong_checklist?id=eq.{record_id}", headers=headers)
        if del_res.status_code == 204:
            st.success("삭제 완료! 새로고침 해주세요.")
        else:
            st.error(f"삭제 실패: {del_res.status_code} - {del_res.text}")
