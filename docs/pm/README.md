# 🎯 Korea Public Data - Project Management Documentation

> **애자일 방법론 기반 풀스택 프로젝트 관리 시스템**

## 📋 개요

본 문서는 Korea Public Data 프로젝트의 **Product Manager (PM)** 역할을 수행하며, **Backend (FastAPI + MongoDB)** 와 **Frontend (React + Module Federation)** 를 통괄 관리하는 종합 문서 시스템입니다.

## 🗂️ 문서 구조

### 📁 01_planning - 기획 문서
프로젝트 비전, 목표, 로드맵 및 전략적 계획 수립
- 프로젝트 비전 및 목표
- 로드맵 및 마일스톤
- 스테이크홀더 매핑
- 리스크 관리 계획

### 📁 02_requirements - 요구사항 분석
기능/비기능 요구사항 및 사용자 스토리 관리
- 기능 요구사항 (Functional Requirements)
- 비기능 요구사항 (Non-Functional Requirements)
- 사용자 스토리 및 수용 기준
- 우선순위 매트릭스

### 📁 03_specifications - 기술 스펙
시스템 아키텍처 및 기술적 명세서
- 시스템 아키텍처
- API 스펙 통합 문서
- 데이터베이스 설계
- 보안 요구사항

### 📁 04_design - 설계 문서
UI/UX 및 시스템 설계 관련 문서
- UI/UX 가이드라인
- 컴포넌트 설계
- 상태 관리 설계
- 에러 핸들링 전략

### 📁 05_development - 개발 관리
스프린트 계획 및 개발 프로세스 관리
- 스프린트 계획
- BE/FE 태스크 할당 매트릭스
- 코드 리뷰 가이드라인
- 브랜치 전략

### 📁 06_testing - 테스트 관리
품질 보증 및 테스트 전략
- 테스트 전략 및 계획
- 테스트 케이스 매트릭스
- 품질 체크리스트
- 성능 테스트 계획

### 📁 07_deployment - 배포 관리
배포 파이프라인 및 환경 관리
- 배포 파이프라인
- 환경별 설정 관리
- 롤백 전략
- 모니터링 설정

### 📁 08_operations - 운영 관리
서비스 운영 및 장애 대응
- 장애 대응 매뉴얼
- 성능 모니터링
- 백업 전략
- 보안 체크리스트

### 📁 09_retrospectives - 회고 및 개선
지속적 개선 및 팀 성과 관리
- 스프린트 회고
- 개선 사항 추적
- 메트릭 분석
- 팀 성과 평가

### 📁 10_templates - 템플릿 모음
표준화된 문서 템플릿
- 이슈 템플릿
- PR 템플릿
- 회의록 템플릿
- 보고서 템플릿

## 🔄 애자일 프로세스

### Scrum Framework
- **Daily Standup**: 매일 진행 상황 공유
- **Sprint Planning**: 2주 단위 스프린트 계획
- **Sprint Review**: 스프린트 결과물 검토
- **Sprint Retrospective**: 프로세스 개선 논의

### Kanban Board
```
📋 Product Backlog → 🚀 Sprint Backlog → 👨‍💻 In Progress → 🔍 Code Review → ✅ Done
```

## 🎯 역할 및 책임

### PM (Product Manager) 역할
- **전략 수립**: 제품 비전 및 로드맵 관리
- **요구사항 관리**: 스테이크홀더 요구사항 수집 및 정리
- **우선순위 결정**: 기능 개발 우선순위 설정
- **진행상황 관리**: 스프린트 진행 및 블로커 해결
- **품질 관리**: 코드 리뷰 및 품질 기준 준수
- **커뮤니케이션**: 팀 간 협업 촉진 및 의사소통

### Backend Team 관리
- **FastAPI + MongoDB** 아키텍처 관리
- **K-Startup API** 통합 관리
- **데이터 모델링** 및 **API 설계**
- **성능 최적화** 및 **보안 관리**

### Frontend Team 관리
- **React + Module Federation** 아키텍처 관리
- **컴포넌트 라이브러리** 관리
- **상태 관리** 및 **타입 안전성**
- **사용자 경험 최적화**

## 📊 메트릭 및 KPI

### 개발 메트릭
- **Velocity**: 스프린트별 완료 스토리 포인트
- **Burndown Chart**: 스프린트 진행률
- **Code Coverage**: 테스트 커버리지
- **Lead Time**: 기능 개발 소요 시간

### 품질 메트릭
- **Bug Rate**: 버그 발생률
- **Technical Debt**: 기술 부채 관리
- **Performance**: 응답 시간 및 처리량
- **Security**: 보안 취약점 관리

## 🚀 시작하기

1. **현재 스프린트 확인**: `05_development/sprint_current.md`
2. **백로그 확인**: `02_requirements/product_backlog.md`
3. **일일 스탠드업**: `05_development/daily_standup/`
4. **이슈 보고**: `10_templates/issue_template.md` 활용

## 📞 연락처 및 지원

- **PM**: Claude (AI Project Manager)
- **Repository**: `/Users/macmini/dev/korea_public_data`
- **Documentation**: `/docs/pm/`
- **Issue Tracking**: GitHub Issues (연동 예정)

---

> **"모든 성공적인 프로젝트는 명확한 계획과 지속적인 소통에서 시작됩니다."**

**Last Updated**: `2025-07-30`  
**Version**: `1.0.0`