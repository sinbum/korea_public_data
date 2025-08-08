# 🤖 PM 문서 자동화 시스템

## 📋 개요

Korea Public Data 프로젝트의 **PM 문서 자동화 시스템**입니다. 애자일 개발 방법론에 따른 문서 관리를 자동화하여 일관성과 효율성을 보장합니다.

## 🛠️ 도구 목록

### 1. `update_scripts.py` - 메인 자동화 스크립트
프로젝트 문서들을 자동으로 업데이트하는 핵심 스크립ت

#### 주요 기능
- 📊 태스크 할당 매트릭스 자동 업데이트
- 📋 백로그 메트릭 갱신
- 📈 시스템 현황 문서 업데이트
- 📅 일일 스탠드업 문서 자동 생성
- 📊 스프린트 리포트 생성

#### 사용법
```bash
# 모든 문서 업데이트
python docs/pm/09_automation/update_scripts.py

# 특정 프로젝트 루트 지정
python docs/pm/09_automation/update_scripts.py -p /path/to/project

# 완성도 지정하여 업데이트
python docs/pm/09_automation/update_scripts.py -c 85

# 일일 스탠드업만 생성
python docs/pm/09_automation/update_scripts.py -d
```

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
# Python 3.8+ 필요
pip install pathlib
```

### 2. 기본 실행
```bash
cd /Users/macmini/dev/korea_public_data
python docs/pm/09_automation/update_scripts.py
```

### 3. 실행 결과 확인
```
🚀 Starting PM Document Updates for 2025-07-30
📊 Current Sprint: Sprint 12
--------------------------------------------------
✅ Task Assignment Matrix updated
✅ Product Backlog updated
✅ System State updated
✅ Daily standup created
✅ Sprint Report generated
--------------------------------------------------
✅ All PM documents updated successfully!
```

## 📁 영향받는 문서들

### 자동 업데이트 대상
| 문서 | 경로 | 업데이트 내용 |
|------|------|---------------|
| **태스크 매트릭스** | `05_development/task_assignment_matrix.md` | 스프린트 정보, 날짜, 진행률 |
| **백로그** | `02_requirements/product_backlog.md` | 현재 스프린트, 메트릭 |
| **시스템 현황** | `03_specifications/current_system_state.md` | 날짜, 완성도, 스프린트 |

### 자동 생성 대상
| 문서 | 경로 | 생성 조건 |
|------|------|-----------|
| **일일 스탠드업** | `06_meetings/daily_standups/daily_standup_YYYYMMDD.md` | 매일 새로 생성 |
| **스프린트 리포트** | `07_reports/sprint_reports/sprint_report_sprint_XX.md` | 스프린트별 생성 |

## ⚙️ 설정 및 커스터마이징

### 스프린트 설정
스크립트는 다음 기준으로 현재 스프린트를 자동 계산합니다:
- **프로젝트 시작일**: 2024-01-15
- **스프린트 길이**: 2주 (14일)
- **자동 계산**: `(현재날짜 - 시작일) / 14 + 1`

### 커스터마이징 포인트
```python
# 프로젝트 시작일 변경
start_date = datetime.datetime(2024, 1, 15)

# 스프린트 길이 변경 (일)
sprint_length = 14

# 기본 스토리 포인트 용량
default_capacity = 25
```

## 📅 권장 사용 패턴

### 1. 일일 루틴 (매일 아침)
```bash
python docs/pm/09_automation/update_scripts.py -d
```
- 오늘의 스탠드업 문서 생성

### 2. 주간 루틴 (매주 금요일)
```bash
python docs/pm/09_automation/update_scripts.py
```
- 모든 문서 동기화 및 업데이트

### 3. 스프린트 시작/종료 시
```bash
python docs/pm/09_automation/update_scripts.py -c 82
```
- 완성도 업데이트와 함께 전체 문서 갱신

## 🔄 GitHub Actions 연동

### `.github/workflows/pm-docs-update.yml`
```yaml
name: PM 문서 자동 업데이트

on:
  schedule:
    - cron: '0 9 * * 1-5'  # 평일 오전 9시
  workflow_dispatch:

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Update PM Documents
        run: |
          python docs/pm/09_automation/update_scripts.py
      
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/pm/
          git commit -m "🤖 Auto-update PM documents [skip ci]" || exit 0
          git push
```

## 📊 모니터링 및 로그

### 로그 출력 예시
```
🚀 Starting PM Document Updates for 2025-07-30
📊 Current Sprint: Sprint 12
--------------------------------------------------
✅ Task Assignment Matrix updated: /docs/pm/05_development/task_assignment_matrix.md
✅ Product Backlog updated: /docs/pm/02_requirements/product_backlog.md
✅ System State updated: /docs/pm/03_specifications/current_system_state.md
✅ Daily standup created: /docs/pm/06_meetings/daily_standups/daily_standup_20250730.md
✅ Sprint Report generated: /docs/pm/07_reports/sprint_reports/sprint_report_sprint_12.md
--------------------------------------------------
✅ All PM documents updated successfully!
📁 Documents location: /docs/pm
```

### 에러 처리
스크립트는 다음과 같은 상황을 자동으로 처리합니다:
- 누락된 템플릿 파일 경고
- 이미 존재하는 일일 스탠드업 스킵
- 파일 권한 오류 보고
- 날짜 형식 검증

## 🔧 확장 가능성

### 추가 가능한 기능들
1. **Slack/Discord 알림 연동**
   ```python
   def send_notification(message):
       # Slack WebHook 연동
       pass
   ```

2. **Jira/Trello 동기화**
   ```python
   def sync_with_jira():
       # Jira API 연동
       pass
   ```

3. **Git 커밋 메트릭 분석**
   ```python
   def analyze_git_commits():
       # Git log 분석
       pass
   ```

4. **성능 메트릭 자동 수집**
   ```python
   def collect_performance_metrics():
       # API 성능 측정
       pass
   ```

## 🛡️ 보안 고려사항

### 안전한 사용을 위한 권장사항
- 스크립트 실행 권한 최소화
- 중요한 설정값 환경변수 사용
- 백업 파일 자동 생성
- 변경사항 Git 추적

### 백업 전략
```python
def create_backup():
    """문서 변경 전 백업 생성"""
    backup_dir = Path("backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
    # 백업 로직 구현
```

---

**📅 작성일**: 2025-07-30  
**👤 작성자**: PM Team  
**🔄 업데이트 주기**: 매주  
**📋 상태**: Active