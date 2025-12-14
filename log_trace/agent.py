# log_trace_test/agent.py

from google import genai
from google.adk.agents.llm_agent import Agent # ADK Agent 클래스 다시 사용
from .tools import read_build_log, find_last_modifier, send_email_to_developer

# (GenAI Client 초기화 코드는 그대로 둡니다.)
try:
    client = genai.Client()
    print(">>> GenAI Client 초기화 성공 <<<")
except Exception as e:
    print(f"FATAL: GenAI Client 초기화 실패: {e}") 
    import sys
    sys.exit(1)

# 1. 도구 목록 정의 (ADK Agent에 전달할 함수 목록)
tools_list = [read_build_log, find_last_modifier, send_email_to_developer]

# 2. ADK Agent 초기화 (이전의 error_analysis_agent를 다시 만듭니다.)
# 이 객체가 Web UI가 찾는 'root_agent'가 됩니다.
root_agent = Agent(
    model='gemini-2.5-flash',
    name='ErrorAnalysisAgent',
    description='빌드 로그를 분석하고 에러 원인 파일을 찾아 수정 담당자에게 이메일을 보냅니다.',
    instruction='당신은 빌드 에러 전문가입니다. 제공된 로그 소스를 분석하여 적절한 도구를 순서대로 호출하고 최종 분석 결과를 사용자에게 제공해야 합니다.',
    tools=tools_list,
    # client=client # Pydantic 오류 방지를 위해 client는 전달하지 않고 환경 변수에 의존
)

# 3. run_build_error_agent 함수 수정
# 이 함수는 이제 Agent의 실행 로직을 감싸는 wrapper 역할을 합니다.
def run_build_error_agent(log_source: str) -> str:
    print(f">>> run_build_error_agent (Wrapper) 함수 호출됨: {log_source} <<<")
    prompt = f"다음 빌드 로그 소스를 분석하여 에러 대응을 시작하세요: {log_source}"

    print("--- Error Analysis Agent 실행 시작 (ADK) ---")
    
    # root_agent 객체의 메서드를 호출합니다. (가장 가능성 높은 .start()로 재시도)
    try:
        response = root_agent.start(prompt=prompt)
    except AttributeError:
        # start도 안 되면, .run()을 시도합니다. (가장 일반적인 이름)
        response = root_agent.run(prompt=prompt)
    
    print("--- Error Analysis Agent 실행 완료 (ADK) ---")
    
    return str(response) # ADK 응답 객체를 문자열로 변환하여 반환