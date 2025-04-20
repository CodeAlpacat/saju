.PHONY: venv setup start clean dev

# 가상환경 생성
venv:
	python3.11 -m venv venv

# 필요한 패키지 설치
setup:
	venv/bin/pip install -r requirements.txt

# 애플리케이션 실행
start:
	streamlit run streamlit.py

# 개발 모드 실행 (가상환경 활성화 후 사용)
dev:
	streamlit run streamlit.py --server.runOnSave=true

# 가상환경 및 캐시 제거
clean:
	rm -rf venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
