# 가상 환경 생성
python -m venv venv 

# 가상 환경 활성화 (Mac/Linux 기준)
source venv/bin/activate
# (만약 Windows를 사용하신다면: venv\Scripts\activate)

pip install -r requirements.txt

# OpenAI API 키 설정
# 아래 명령어에 자신의 API 키를 넣어주세요
export OPENAI_API_KEY="your-api-key-here"

python data_processor.py
