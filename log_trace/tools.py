import os
import re
from typing import List, Optional
# 실제 환경에서는 'requests', 'gitpython', 'smtplib' 등의 라이브러리가 필요합니다.

# --- 도구 1: 로그 파일 읽기 ---
def read_build_log(source: str) -> str:
    """
    파일 경로 또는 URL에서 빌드 로그 내용을 읽어옵니다.
    
    Args:
        source: 빌드 로그 파일 경로 (로컬) 또는 URL (Jenkins 등).
        
    Returns:
        로그 파일 전체 내용 (문자열) 또는 오류 메시지.
    """
    if source.lower().startswith('http'):
        # 실제 구현: requests 라이브러리를 사용하여 URL에서 로그를 다운로드
        # 예시: response = requests.get(source); return response.text
        return f"가상의 Jenkins 로그 내용 (URL: {source}):\n...\nERROR: CXX compile failed in file_A.cc:200\nERROR: Undefined reference to 'function_X' in file_B.cpp\n...\n"
    elif os.path.exists(source):
        try:
            with open(source, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"로그 파일 읽기 오류: {e}"
    else:
        return f"오류: 지정된 빌드 로그 소스 ({source})를 찾을 수 없습니다."

# --- 도구 2: Git History 검색 및 수정자 도출 ---
def find_last_modifier(file_path: str) -> Optional[str]:
    """
    주어진 파일 경로의 가장 최근 수정자(이메일 주소)를 Git History에서 검색합니다.
    
    Args:
        file_path: 컴파일 에러를 일으킨 파일 경로.
        
    Returns:
        가장 최근 수정자의 이메일 주소 (문자열) 또는 None.
    """
    # 실제 구현: GitPython 라이브러리 사용
    # 예시: repo = git.Repo('.'); last_commit = repo.log('--max-count=1', file_path)
    # last_modifier_email = last_commit.author.email
    
    # 레퍼런스 확보 문제: 이 기능은 'gitpython' 라이브러리와 실제 'git' 환경 설정에 크게 의존합니다.
    # 해당 코드가 실행되는 환경에 git 저장소가 있어야 하며, 라이브러리 설치가 필요합니다.
    
    # 가상 구현 (파일 경로에 따라 가상의 이메일 반환):
    if "file_A.cc" in file_path:
        return "developer_A@company.com"
    elif "file_B.cpp" in file_path:
        return "developer_B@company.com"
    else:
        return None

# --- 도구 3: 이메일 발송 ---
def send_email_to_developer(recipient_email: str, subject: str, body: str) -> str:
    """
    지정된 개발자에게 분석 결과를 이메일로 보냅니다.
    
    Args:
        recipient_email: 수신자 이메일 주소.
        subject: 이메일 제목.
        body: 이메일 내용.
        
    Returns:
        발송 성공/실패 메시지.
    """
    # 실제 구현: smtplib 라이브러리를 사용하여 SMTP 서버를 통해 이메일을 발송합니다.
    # 이메일 서버, 포트, 인증 정보 (비밀번호) 설정이 필요합니다. (보안 문제로 여기에 포함하기 어려움)
    
    # 레퍼런스 확보 문제: SMTP 서버 설정, 인증 정보(암호) 보안 처리가 필요합니다.
    
    # 가상 구현:
    print(f"\n--- 이메일 발송 시뮬레이션 ---")
    print(f"수신: {recipient_email}")
    print(f"제목: {subject}")
    print(f"본문:\n{body}")
    print(f"---------------------------\n")
    return f"이메일이 {recipient_email}에게 성공적으로 발송되었습니다."

# --- 도구 4: 에러 분석 (LLM이 담당) ---
# 이 단계는 LLM의 추론 능력(reasoning)을 사용하여 로그 분석 및 파일 도출을 수행합니다.
# 따라서 별도의 Python 함수(Tool)가 필요하지 않습니다.