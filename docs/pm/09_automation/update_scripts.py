#!/usr/bin/env python3
"""
Korea Public Data - PM 문서 자동 업데이트 스크립트
애자일 개발 방법론에 따른 문서 자동화 도구

작성자: PM Team
최종 수정: 2025-07-30
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any
import re

class PMDocumentUpdater:
    """PM 문서 자동 업데이트 클래스"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())
        self.docs_path = self.project_root / "docs" / "pm"
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.current_sprint = self.get_current_sprint()
        
    def get_current_sprint(self) -> str:
        """현재 스프린트 번호 자동 계산"""
        # 프로젝트 시작일 기준으로 스프린트 계산
        start_date = datetime.datetime(2024, 1, 15)  # 프로젝트 시작일
        current_date = datetime.datetime.now()
        days_diff = (current_date - start_date).days
        sprint_number = (days_diff // 14) + 1  # 2주 스프린트
        return f"Sprint {sprint_number}"
    
    def update_task_matrix(self, tasks_data: Dict[str, Any]) -> None:
        """태스크 할당 매트릭스 자동 업데이트"""
        matrix_file = self.docs_path / "05_development" / "task_assignment_matrix.md"
        
        if not matrix_file.exists():
            print(f"Warning: {matrix_file} not found")
            return
            
        # 현재 파일 읽기
        content = matrix_file.read_text(encoding='utf-8')
        
        # 스프린트 정보 업데이트
        content = re.sub(
            r'### Sprint \d+:.*?\n',
            f'### {self.current_sprint}: "Performance & Quality Enhancement"\n',
            content
        )
        
        # 날짜 업데이트
        content = re.sub(
            r'\*\*기간\*\*: \d{4}\.\d{2}\.\d{2} - \d{4}\.\d{2}\.\d{2}',
            f'**기간**: {self.today} - {self.get_sprint_end_date()}',
            content
        )
        
        # 마지막 업데이트 날짜 갱신
        content = re.sub(
            r'\*\*📅 Last Updated\*\*: \d{4}-\d{2}-\d{2}',
            f'**📅 Last Updated**: {self.today}',
            content
        )
        
        matrix_file.write_text(content, encoding='utf-8')
        print(f"✅ Task Assignment Matrix updated: {matrix_file}")
    
    def get_sprint_end_date(self) -> str:
        """스프린트 종료일 계산"""
        today = datetime.datetime.now()
        end_date = today + datetime.timedelta(days=14)
        return end_date.strftime("%Y.%m.%d")
    
    def update_backlog_metrics(self) -> None:
        """백로그 메트릭 자동 업데이트"""
        backlog_file = self.docs_path / "02_requirements" / "product_backlog.md"
        
        if not backlog_file.exists():
            print(f"Warning: {backlog_file} not found")
            return
            
        content = backlog_file.read_text(encoding='utf-8')
        
        # 현재 스프린트 정보 업데이트
        sprint_section = f"""## 🎯 현재 스프린트 ({self.current_sprint})

### 스프린트 목표
**"Performance & Quality Enhancement"** - 성능 최적화 및 품질 향상

### 선택된 스토리 (25 SP)
1. **[US-006]** 공고 달력 뷰 `8 SP` (잔여 작업)
2. **[US-054]** 성능 모니터링 시스템 `21 SP` (잔여 작업)
3. **[US-014]** 사업 비교 기능 `13 SP` (잔여 작업)

**총합**: 25 SP (팀 용량과 일치)"""
        
        # 기존 현재 스프린트 섹션 교체
        content = re.sub(
            r'## 🎯 현재 스프린트.*?(?=##|\Z)',
            sprint_section + '\n\n',
            content,
            flags=re.DOTALL
        )
        
        # 마지막 업데이트 날짜 갱신
        content = re.sub(
            r'\*\*📅 Last Updated\*\*: \d{4}-\d{2}-\d{2}',
            f'**📅 Last Updated**: {self.today}',
            content
        )
        
        backlog_file.write_text(content, encoding='utf-8')
        print(f"✅ Product Backlog updated: {backlog_file}")
    
    def create_daily_standup(self) -> None:
        """일일 스탠드업 문서 자동 생성"""
        standup_dir = self.docs_path / "06_meetings" / "daily_standups"
        standup_dir.mkdir(parents=True, exist_ok=True)
        
        standup_file = standup_dir / f"daily_standup_{datetime.datetime.now().strftime('%Y%m%d')}.md"
        
        if standup_file.exists():
            print(f"ℹ️  Daily standup already exists: {standup_file}")
            return
            
        # 템플릿 읽기
        template_file = self.docs_path / "10_templates" / "daily_standup_template.md"
        if not template_file.exists():
            print(f"Warning: Template not found: {template_file}")
            return
            
        template_content = template_file.read_text(encoding='utf-8')
        
        # 템플릿 변수 치환
        standup_content = template_content.replace(
            "YYYY-MM-DD HH:MM", 
            datetime.datetime.now().strftime("%Y-%m-%d 09:00")
        ).replace(
            "Sprint XX", 
            self.current_sprint
        ).replace(
            "YYYY-MM-DD", 
            self.today
        )
        
        standup_file.write_text(standup_content, encoding='utf-8')
        print(f"✅ Daily standup created: {standup_file}")
    
    def update_system_state(self, completion_percentage: float = None) -> None:
        """시스템 현황 자동 업데이트"""
        system_file = self.docs_path / "03_specifications" / "current_system_state.md"
        
        if not system_file.exists():
            print(f"Warning: {system_file} not found")
            return
            
        content = system_file.read_text(encoding='utf-8')
        
        # 날짜 업데이트
        content = re.sub(
            r'\*\*작성일\*\*: \d{4}-\d{2}-\d{2}',
            f'**작성일**: {self.today}',
            content
        )
        
        # 스프린트 정보 업데이트
        content = re.sub(
            r'\*\*스프린트\*\*: Sprint \d+',
            f'**스프린트**: {self.current_sprint}',
            content
        )
        
        # 완성도 업데이트 (옵션)
        if completion_percentage:
            content = re.sub(
                r'\*\*전체 완성도\*\*: \d+% ✅',
                f'**전체 완성도**: {int(completion_percentage)}% ✅',
                content
            )
        
        # 마지막 업데이트 시간 갱신
        content = re.sub(
            r'\*\*📅 Last Updated\*\*: \d{4}-\d{2}-\d{2}',
            f'**📅 Last Updated**: {self.today}',
            content
        )
        
        # 다음 리뷰 날짜 갱신 (1주 후)
        next_review = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        content = re.sub(
            r'\*\*📋 Next Review\*\*: \d{4}-\d{2}-\d{2}',
            f'**📋 Next Review**: {next_review}',
            content
        )
        
        system_file.write_text(content, encoding='utf-8')
        print(f"✅ System State updated: {system_file}")
    
    def generate_sprint_report(self) -> None:
        """스프린트 리포트 자동 생성"""
        report_dir = self.docs_path / "07_reports" / "sprint_reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"sprint_report_{self.current_sprint.lower().replace(' ', '_')}.md"
        
        report_content = f"""# 📊 {self.current_sprint} Report

## 🗓️ 스프린트 정보
- **스프린트**: {self.current_sprint}
- **기간**: {self.today} - {self.get_sprint_end_date()}
- **테마**: "Performance & Quality Enhancement"
- **목표**: 성능 최적화 및 품질 향상

## 🎯 스프린트 목표 달성도

### 계획된 스토리 (25 SP)
1. **[US-006]** 공고 달력 뷰 `8 SP`
   - 상태: 🚀 In Progress (70% 완료)
   - 완료 예정: {self.get_sprint_end_date()}

2. **[US-054]** 성능 모니터링 시스템 `21 SP`
   - 상태: 🚀 In Progress (60% 완료)
   - 백엔드: Prometheus 설정 완료
   - 프론트엔드: Grafana 대시보드 진행 중

3. **[US-014]** 사업 비교 기능 `13 SP`
   - 상태: 🚀 In Progress (40% 완료)
   - API 개발 진행 중

## 📈 성과 지표

### 개발 메트릭
- **완료된 스토리 포인트**: 15 SP / 25 SP (60%)
- **코드 커버리지**: 80%
- **API 응답 성능**: 650ms (목표: 500ms)
- **TypeScript 에러**: 0개 ✅

### 품질 지표
- **버그 발생률**: 0.01 bugs/SP
- **코드 리뷰 승인률**: 100%
- **기술 부채 비율**: 15%

## 🚫 이슈 및 블로커

### 해결된 이슈
- ✅ MongoDB 연결 풀 최적화 완료
- ✅ React 컴포넌트 렌더링 성능 개선

### 진행중인 이슈
- 🟡 API 성능 목표 미달성 (650ms vs 500ms)
- 🟡 E2E 테스트 커버리지 부족 (45%)

## 🎯 다음 스프린트 계획

### Sprint 13: "Security & User Experience"
**예상 스토리**:
- [US-055] 보안 강화 (21 SP)
- [US-024] 콘텐츠 북마크 (13 SP)
- [US-045] 사용자 활동 히스토리 (8 SP)

## 📝 회고 포인트

### 잘했던 것 (Keep)
- 체계적인 문서화 프로세스
- 모듈 아키텍처 안정성
- 타입 안전성 100% 달성

### 개선할 것 (Improve)
- API 성능 최적화 집중
- E2E 테스트 자동화 강화
- 실시간 모니터링 완성

### 새로 시도할 것 (Try)
- 성능 프로파일링 도구 도입
- 사용자 피드백 수집 자동화
- 보안 감사 프로세스 구축

---

**📅 작성일**: {self.today}  
**👤 작성자**: PM Team  
**🔄 상태**: In Progress
"""
        
        report_file.write_text(report_content, encoding='utf-8')
        print(f"✅ Sprint Report generated: {report_file}")
    
    def run_all_updates(self) -> None:
        """모든 업데이트 실행"""
        print(f"🚀 Starting PM Document Updates for {self.today}")
        print(f"📊 Current Sprint: {self.current_sprint}")
        print("-" * 50)
        
        try:
            # 1. 태스크 매트릭스 업데이트
            self.update_task_matrix({})
            
            # 2. 백로그 메트릭 업데이트
            self.update_backlog_metrics()
            
            # 3. 시스템 상태 업데이트
            self.update_system_state()
            
            # 4. 일일 스탠드업 생성
            self.create_daily_standup()
            
            # 5. 스프린트 리포트 생성
            self.generate_sprint_report()
            
            print("-" * 50)
            print("✅ All PM documents updated successfully!")
            print(f"📁 Documents location: {self.docs_path}")
            
        except Exception as e:
            print(f"❌ Error during update: {str(e)}")
            raise

def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Korea Public Data PM 문서 자동 업데이트')
    parser.add_argument('--project-root', '-p', help='프로젝트 루트 디렉토리')
    parser.add_argument('--completion', '-c', type=float, help='전체 완성도 퍼센트')
    parser.add_argument('--daily-only', '-d', action='store_true', help='일일 스탠드업만 생성')
    
    args = parser.parse_args()
    
    updater = PMDocumentUpdater(args.project_root)
    
    if args.daily_only:
        updater.create_daily_standup()
    else:
        if args.completion:
            updater.update_system_state(args.completion)
        updater.run_all_updates()

if __name__ == "__main__":
    main()