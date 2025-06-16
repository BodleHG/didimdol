# ---------- Stage 1: Build Environment ----------
FROM python:3.11-slim as builder

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 의존성 설치용 디렉토리 생성
WORKDIR /install

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install/packages -r requirements.txt

# ---------- Stage 2: Final Lightweight Container ----------
FROM python:3.11-slim

# 런타임 디렉토리 설정
WORKDIR /app

# builder 단계에서 설치한 패키지 복사
COPY --from=builder /install/packages /usr/local

# 로컬 파이썬 파일들 복사 (파일 이름은 예시)
COPY simulation_engine.py model_select.py model_create.py mode_select.py ./

WORKDIR /app/scenarios
COPY scenarios/smart_farm.py ./


WORKDIR /app
# 메인 실행 파일 설정
ENTRYPOINT ["python", "-u", "simulation_engine.py"]
