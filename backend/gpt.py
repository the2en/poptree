import sys
import os

# 스크립트의 현재 디렉토리 (__file__은 gpt.py의 경로)
script_dir = os.path.dirname(os.path.abspath(__file__))
# 부모 디렉토리 (프로젝트 루트)
project_root = os.path.dirname(script_dir)
# 프로젝트 루트를 sys.path에 추가하여 모듈을 찾을 수 있도록 함
sys.path.append(project_root)

from openai import OpenAI
import numpy as np
import faiss
import sqlite3
import json
from django.conf import settings
import django
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Django 설정을 로드합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

from investments.models import EtfDetail # EtfDetail 모델 import

# 환경 변수에서 OpenAI API 키 불러오기 (또는 직접 입력)
#api_key = os.getenv("OPENAI_API_KEY")
api_key = "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"
# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

# 사용자 질문 정제
def clarify_question(question):
    prompt = f"다음 사용자의 질문을 명확하고 구체적인 형태로 정제해줘:\n\n'{question}'"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# 텍스트 임베딩 생성
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# FAISS 유사도 검색
def find_similar_top_k(query_embedding, db_embeddings, k=3):
    dim = len(query_embedding)
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(db_embeddings).astype('float32'))
    D, I = index.search(np.array([query_embedding]).astype('float32'), k)
    return I[0]  # 인덱스 반환

# GPT 추천 생성
def answer_with_context(question, context_texts):
    context = "\n".join(context_texts)
    prompt = f"""사용자 질문: "{question}"

아래는 사용자 프로필, 소비 패턴 요약 및 유사도가 높은 금융 상품 (ETF, 예금/적금 등) 정보입니다:
{context}

- 제공된 사용자 프로필, 소비 패턴 및 금융 상품 정보를 종합적으로 고려하여 사용자에게 가장 적합한 금융 상품을 우선순위대로 최대 3개 추천하고 그 이유를 간단히 설명해주세요.
### 금융 상품 추천 요청 사항:
1. 제공된 '소비 패턴 요약' 정보를 바탕으로 사용자의 전반적인 성향 (예: 절약형, 소비 지향형, 안정 추구형 등)을 간략하게 분석합니다.
2. 분석된 소비 성향과 제공된 사용자 프로필 정보(투자 성향, 관심 분야 등)를 종합하여 사용자의 잠재적인 투자 성향을 유추합니다.
3. 유추된 투자 성향 및 제공된 금융 상품 정보를 바탕으로, 사용자에게 가장 적합한 금융 상품을 우선순위대로 최대 3개 추천합니다.
4. 각 추천 상품에 대해 왜 사용자에게 적합한지 그 이유를 간단히 설명합니다.

"""
    response = client.chat.completions.create(
        model="gpt-4o-mini", # 필요시 다른 모델 사용 가능
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# 예금/적금 데이터 가져오기 함수 (db.sqlite3 구조에 따라 수정 필요)
def get_deposit_savings_data(db_path="db.sqlite3"):
    conn = None
    data = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # InvestmentProduct 모델 구조에 맞춰 쿼리 수정
        # fin_prdt_nm, kor_co_nm, interest_detail, spcl_cnd, etc_note 등 활용
        cursor.execute("SELECT fin_prdt_nm, kor_co_nm, interest_detail, spcl_cnd, etc_note, type FROM investments_investmentproduct WHERE type IN ('예금', '적금')")
        rows = cursor.fetchall()

        for row in rows:
            fin_prdt_nm, kor_co_nm, interest_detail_json, spcl_cnd, etc_note, prod_type = row

            # interest_detail (JSON string) 파싱
            interest_info = ""
            if interest_detail_json:
                try:
                    detail = json.loads(interest_detail_json)
                    if detail and isinstance(detail, list):
                        # 예시: 가장 높은 금리 정보 포함
                        highest_rate_option = max(detail, key=lambda x: float(x.get('intr_rate', 0)) if x.get('intr_rate') not in [None, ''] else -1)
                        highest_rate = highest_rate_option.get('intr_rate', '정보 없음')
                        save_trm = highest_rate_option.get('save_trm', '정보 없음')
                        intr_rate_type_nm = highest_rate_option.get('intr_rate_type_nm', '정보 없음')
                        interest_info = f", 최고금리: {highest_rate}% ({save_trm}개월, {intr_rate_type_nm})"
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"❌ interest_detail 파싱 오류: {e}")

            # 임베딩을 위해 텍스트 형식으로 변환
            product_text = f"{prod_type}: {fin_prdt_nm} ({kor_co_nm}){interest_info}"
            if spcl_cnd:
                product_text += f", 우대조건: {spcl_cnd}"
            if etc_note:
                product_text += f", 기타: {etc_note}"
            data.append(product_text.strip())

    except sqlite3.Error as e:
        print(f"❌ 데이터베이스 오류 발생: {e}")
    finally:
        if conn:
            conn.close()
        return data

# 사용자 프로필 데이터 가져오기 함수 (db.sqlite3 구조에 따라 수정 필요)
def get_user_profile_from_db(user_id, db_path="db.sqlite3"):
    conn = None
    profile_data = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # accounts_user 테이블에 있는 'id' 컬럼으로 조회
        cursor.execute("SELECT name FROM accounts_user WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if row:
            # 'name'만 가져오고 나머지 프로필 정보는 기본값으로 설정
            profile_data = {
                "이름": row[0], # name 컬럼 값
                "투자성향": "정보 없음", # DB에서 직접 가져오지 않음
                "관심분야": "정보 없음", # DB에서 직접 가져오지 않음
                "보유 ETF": [], # DB에서 직접 가져오지 않음
                "소비 패턴": "정보 없음" # DB에서 직접 가져오지 않음
            }

            # Spending 모델에서 소비 데이터 가져와 요약 (최근 3개월 예시)
            from datetime import datetime, timedelta
            today = datetime.now()
            three_months_ago = today - timedelta(days=90)

            # user_id로 바로 사용
            if user_id:
                # 해당 사용자의 최근 3개월 총 소비 금액 조회
                cursor.execute("SELECT SUM(amount) FROM spending_spending WHERE user_id = ? AND date >= ?", (user_id, three_months_ago.strftime('%Y-%m-%d %H:%M:%S')))
                total_spending_row = cursor.fetchone()
                total_spending = total_spending_row[0] if total_spending_row and total_spending_row[0] is not None else 0

                spending_summary_text = ""
                if total_spending > 0:
                    # spending_spending 테이블에서 해당 사용자의 최근 3개월 소비 데이터 (카테고리별 합계) 조회
                    cursor.execute("SELECT category, SUM(amount) FROM spending_spending WHERE user_id = ? AND date >= ? GROUP BY category ORDER BY SUM(amount) DESC LIMIT 5", (user_id, three_months_ago.strftime('%Y-%m-%d %H:%M:%S')))
                    spending_summary_rows = cursor.fetchall()

                    if spending_summary_rows:
                        spending_summary_text += "\n최근 3개월 주요 소비 카테고리 (%): "
                        for category, total_amount in spending_summary_rows:
                            # 백분율 계산
                            percentage = (total_amount / total_spending) * 100
                            spending_summary_text += f"{category} ({percentage:.1f}%), " # 소수점 첫째 자리까지 표시
                        spending_summary_text = spending_summary_text.rstrip(', ') # 마지막 쉼표 제거

                # 기존 '소비 패턴' 정보를 가져오지 않으므로, '소비 요약' 정보로 대체
                profile_data["소비 패턴"] = spending_summary_text.strip() if spending_summary_text else "소비 데이터 없음"

    except sqlite3.Error as e:
        print(f"❌ 데이터베이스 오류 발생: {e}")
    except Exception as e:
        print(f"❌ 사용자 프로필 처리 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()
        return profile_data

def get_etf_data_from_db():
    """데이터베이스에서 ETF 상세 정보를 읽어와 텍스트 목록으로 반환"""
    etf_texts = []
    try:
        # 모든 EtfDetail 객체를 가져옴
        etfs = EtfDetail.objects.all()

        for etf in etfs:
            # 각 ETF 객체에서 필요한 정보 추출 및 텍스트 형식으로 가공
            # holdings와 dividends는 JSON 문자열이므로 json.loads로 파싱
            holdings = json.loads(etf.holdings) if etf.holdings else []
            dividends = json.loads(etf.dividends) if etf.dividends else []

            holdings_str = ", ".join([f"{h.get('name', '')} ({h.get('weight', '')})" for h in holdings])
            dividends_str = ", ".join([f"배당일: {d.get('pay', '')}, 금액: {d.get('amt', '')}" for d in dividends])

            etf_text = (
                f"코드: {etf.code}\n"  # ETF 코드
                f"이름: {etf.name}\n"  # ETF 이름
                f"티커: {etf.ticker}\n" # 티커 심볼
                f"요약: {etf.summary if etf.summary else '정보 없음'}\n" # 요약 설명
                f"운용사: {etf.manager if etf.manager else '정보 없음'}\n" # 운용사
                f"시가총액: {etf.marketcap if etf.marketcap else '정보 없음'}\n" # 시가총액
                f"운용자산(AUM): {etf.asset if etf.asset else '정보 없음'}\n" # 운용자산
                f"상장일: {etf.list_date if etf.list_date else '정보 없음'}\n" # 상장일
                f"NAV: {etf.nav if etf.nav else '정보 없음'}\n" # 순자산가치
                f"운용보수: {etf.fee if etf.fee else '정보 없음'}\n" # 운용보수
                f"괴리율: {etf.gap if etf.gap else '정보 없음'}\n" # 괴리율
                f"주요 보유 종목: {holdings_str if holdings_str else '정보 없음'}\n" # 주요 보유 종목
                f"배당금 지급 내역: {dividends_str if dividends_str else '정보 없음'}" # 배당금 내역
            )
            etf_texts.append(etf_text)

    except Exception as e:
        print(f"ETF 데이터를 불러오는 중 오류 발생: {e}")
        # 오류 발생 시 빈 목록 반환 또는 오류 처리
        pass

    return etf_texts

# 전체 실행 흐름
def run_etf_recommender(user_question, user_profile_dict, etf_db_texts):
    clarified_question = clarify_question(user_question)
    
    # 사용자 마이데이터 (프로필 + 소비) + 질문 임베딩
    profile_text = "\n".join([f"{k}: {v}" for k, v in user_profile_dict.items()])
    query_text = clarified_question + "\n" + profile_text
    query_embedding = get_embedding(query_text)
    
    # 금융 상품 DB (ETF + 예금/적금) 임베딩
    deposit_savings_texts = get_deposit_savings_data() # 예금/적금 데이터 가져오기
    # ETF 텍스트 형식도 임베딩에 맞게 조정 (예: "ETF: QQQ, 설명:...")
    etf_texts_formatted = [f"ETF: {etf}" if not etf.startswith("ETF:") else etf for etf in etf_db_texts]
    financial_products_texts = etf_texts_formatted + deposit_savings_texts # ETF와 합치기
    
    db_embeddings = [get_embedding(doc) for doc in financial_products_texts]

    # 유사도 기반 top-k 금융 상품 선택
    top_k_indices = find_similar_top_k(query_embedding, db_embeddings, k=3)
    # 선택된 상품 텍스트 가져오기 (원본 리스트에서 인덱스 사용)
    top_k_texts = [financial_products_texts[i] for i in top_k_indices]
    
    # GPT로 최종 추천 생성
    final_answer = answer_with_context(clarified_question, top_k_texts)
    return final_answer

@api_view(['POST'])
def gpt_answer(request):
    user_id = request.data.get('user_id')
    user_name = request.data.get('user_name')
    question = request.data.get('question')
    if not user_id or not question:
        return Response({'error': 'user_id, question 필수'}, status=status.HTTP_400_BAD_REQUEST)
    user_profile = get_user_profile_from_db(user_id)
    if not user_profile:
        return Response({'error': '해당 유저 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    etf_db = get_etf_data_from_db()
    try:
        answer = run_etf_recommender(question, user_profile, etf_db)
        return Response({'user_name': user_name or user_profile.get('이름', ''), 'answer': answer})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 샘플 실행 예시
if __name__ == "__main__":
    # 사용자 질문
    user_question = "내 투자 성향에 맞는 금융 상품을 추천해줘"

    # DB에서 사용자 프로필 정보 가져오기
    user_id_to_load = 1  # 예시: 1번 유저
    user_profile = get_user_profile_from_db(user_id_to_load)

    if not user_profile:
        print(f"❌ 사용자 프로필 정보를 DB에서 찾을 수 없습니다: {user_id_to_load}")
        # DB에서 찾지 못했을 경우 기본 프로필 사용 또는 종료
        user_profile = {
            "이름": str(user_id_to_load),
            "투자성향": "정보 없음",
            "관심분야": "정보 없음",
            "보유 ETF": [],
            "소비 패턴": "정보 없음"
        }
        print("기본 프로필 정보로 실행합니다.")

    # ETF 정보 데이터베이스 (간단 예시 - 실제는 get_etf.py에서 가져올 수 있음)
    etf_db = get_etf_data_from_db()

    # 사용자 이름과 소비 패턴 정보 출력
    print("\n--- 사용자 정보 ---")
    print(f"이름: {user_profile.get('이름', '정보 없음')}")
    print(f"소비 패턴 요약: {user_profile.get('소비 패턴', '정보 없음')}")
    print("------------------")

    # 실행
    answer = run_etf_recommender(user_question, user_profile, etf_db)
    print("\n✅ GPT 추천 결과:\n")
    print(answer)