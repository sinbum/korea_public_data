# 🧪 테스트 전략 및 계획

> Korea Public Data 프로젝트의 품질 보증을 위한 종합 테스트 전략

## 📋 목차
- [테스트 원칙](#테스트-원칙)
- [테스트 피라미드](#테스트-피라미드)
- [테스트 유형별 전략](#테스트-유형별-전략)
- [Frontend 테스트](#frontend-테스트)
- [Backend 테스트](#backend-테스트)
- [테스트 자동화](#테스트-자동화)
- [테스트 커버리지 목표](#테스트-커버리지-목표)
- [테스트 환경](#테스트-환경)

## 🎯 테스트 원칙

### 핵심 원칙
1. **Shift Left Testing**: 개발 초기 단계부터 테스트 시작
2. **Test Early, Test Often**: 지속적이고 빈번한 테스트
3. **Automate Everything**: 반복 가능한 모든 테스트 자동화
4. **Risk-Based Testing**: 위험도가 높은 영역 우선 테스트
5. **Continuous Feedback**: 빠른 피드백 루프 구축

### 품질 목표
- **기능적 정확성**: 모든 요구사항 충족
- **신뢰성**: 99.9% 가동률 목표
- **성능**: 3초 이내 페이지 로드
- **보안**: OWASP Top 10 대응
- **접근성**: WCAG 2.1 AA 준수

## 📊 테스트 피라미드

```
         /\
        /  \  E2E Tests (10%)
       /    \ - Critical user journeys
      /      \ - Cross-browser testing
     /--------\
    /          \ Integration Tests (30%)
   /            \ - API integration
  /              \ - Component integration
 /                \ - Database queries
/------------------\
     Unit Tests (60%)
   - Business logic
   - Utility functions
   - Component rendering
```

## 🔍 테스트 유형별 전략

### 1. 단위 테스트 (Unit Testing)
**목적**: 개별 함수, 컴포넌트의 독립적 검증

**도구**:
- Frontend: Vitest, React Testing Library
- Backend: pytest, unittest

**대상**:
- 비즈니스 로직 함수
- 유틸리티 함수
- React 컴포넌트
- API 엔드포인트 핸들러

### 2. 통합 테스트 (Integration Testing)
**목적**: 모듈 간 상호작용 검증

**도구**:
- Frontend: Vitest + MSW (Mock Service Worker)
- Backend: pytest-asyncio, TestClient

**대상**:
- API 통합
- 데이터베이스 연동
- 외부 서비스 연동
- 컴포넌트 간 상호작용

### 3. E2E 테스트 (End-to-End Testing)
**목적**: 실제 사용자 시나리오 검증

**도구**:
- Playwright (크로스 브라우저)
- @axe-core/playwright (접근성)

**대상**:
- 핵심 사용자 플로우
- 회원가입/로그인
- 공고 검색 및 조회
- 알림 설정

### 4. 성능 테스트 (Performance Testing)
**목적**: 응답 시간, 처리량, 자원 사용량 검증

**도구**:
- Frontend: Lighthouse CI, Web Vitals
- Backend: locust, pytest-benchmark

**메트릭**:
- LCP < 2.5s
- FID < 100ms
- CLS < 0.1
- API 응답 < 200ms

### 5. 보안 테스트 (Security Testing)
**목적**: 보안 취약점 식별 및 해결

**도구**:
- OWASP ZAP
- Snyk
- npm audit

**체크리스트**:
- SQL Injection
- XSS
- CSRF
- 인증/인가
- 민감 데이터 노출

## 🎨 Frontend 테스트

### 컴포넌트 테스트
```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button Component', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Hook 테스트
```tsx
// useDebounce.test.ts
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  it('debounces value changes', async () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 500 } }
    );
    
    expect(result.current).toBe('initial');
    
    rerender({ value: 'updated', delay: 500 });
    expect(result.current).toBe('initial');
    
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 600));
    });
    
    expect(result.current).toBe('updated');
  });
});
```

### E2E 테스트
```typescript
// announcements.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Announcements Page', () => {
  test('displays announcement list', async ({ page }) => {
    await page.goto('/announcements');
    
    // 페이지 로드 확인
    await expect(page.getByRole('heading', { name: '공고 목록' }))
      .toBeVisible();
    
    // 테이블 렌더링 확인
    const table = page.getByRole('table');
    await expect(table).toBeVisible();
    
    // 데이터 로드 확인
    const rows = table.locator('tbody tr');
    await expect(rows).toHaveCount(20); // 페이지당 20개
  });

  test('filters announcements', async ({ page }) => {
    await page.goto('/announcements');
    
    // 필터 적용
    await page.getByLabel('기관명').fill('서울');
    await page.getByRole('button', { name: '검색' }).click();
    
    // 결과 확인
    await expect(page.getByText('검색 결과')).toBeVisible();
  });
});
```

## ⚙️ Backend 테스트

### API 엔드포인트 테스트
```python
# test_announcements_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_announcements():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/announcements")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) <= 20  # 페이지네이션

@pytest.mark.asyncio
async def test_create_announcement_unauthorized():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/announcements",
            json={"title": "Test"}
        )
        
        assert response.status_code == 401  # Unauthorized
```

### 서비스 레이어 테스트
```python
# test_announcement_service.py
import pytest
from unittest.mock import AsyncMock, patch
from app.domains.announcements.service import AnnouncementService

@pytest.mark.asyncio
async def test_get_announcements_with_cache():
    service = AnnouncementService()
    
    with patch.object(service.cache, 'get', new=AsyncMock(return_value=None)):
        with patch.object(service.repository, 'find_all', 
                         new=AsyncMock(return_value=[])):
            result = await service.get_announcements(page=1, limit=20)
            
            assert result is not None
            assert isinstance(result, list)
```

### 데이터베이스 테스트
```python
# test_repository.py
import pytest
from app.domains.announcements.repository import AnnouncementRepository

@pytest.mark.asyncio
async def test_repository_create(test_db):
    repo = AnnouncementRepository(test_db)
    
    announcement = await repo.create({
        "title": "Test Announcement",
        "organization": "Test Org",
        "deadline": "2025-12-31"
    })
    
    assert announcement.id is not None
    assert announcement.title == "Test Announcement"
```

## 🤖 테스트 자동화

### CI/CD 파이프라인
```yaml
# .github/workflows/test.yml
name: Test Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: cd fe && npm ci
      
      - name: Run unit tests
        run: cd fe && npm run test
      
      - name: Run E2E tests
        run: cd fe && npm run test:e2e

  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: cd be && pip install -r requirements.txt
      
      - name: Run tests
        run: cd be && pytest --cov=app tests/
```

## 📈 테스트 커버리지 목표

### 전체 목표
- **단위 테스트**: 80% 이상
- **통합 테스트**: 70% 이상
- **E2E 테스트**: 핵심 플로우 100%

### Frontend 커버리지
| 영역 | 목표 | 현재 | 상태 |
|------|------|------|------|
| Components | 85% | - | 🟡 진행중 |
| Hooks | 90% | - | 🟡 진행중 |
| Utils | 95% | - | 🟡 진행중 |
| Services | 80% | - | 🟡 진행중 |

### Backend 커버리지
| 영역 | 목표 | 현재 | 상태 |
|------|------|------|------|
| API Routes | 90% | - | 🟡 진행중 |
| Services | 85% | - | 🟡 진행중 |
| Repositories | 80% | - | 🟡 진행중 |
| Utils | 95% | - | 🟡 진행중 |

## 🌍 테스트 환경

### 환경 구성
| 환경 | 용도 | 데이터 | 접근 |
|------|------|--------|------|
| Local | 개발자 테스트 | Mock 데이터 | 로컬 |
| Dev | 통합 테스트 | 테스트 데이터 | VPN |
| Staging | UAT, 성능 테스트 | 준운영 데이터 | 제한적 |
| Production | 모니터링만 | 실제 데이터 | 운영팀 |

### 테스트 데이터 관리
```python
# fixtures/test_data.py
TEST_ANNOUNCEMENT = {
    "id": "test-001",
    "title": "테스트 공고",
    "organization": "테스트 기관",
    "deadline": "2025-12-31",
    "status": "active"
}

TEST_USER = {
    "id": "user-001",
    "email": "test@example.com",
    "name": "테스트 사용자",
    "role": "user"
}
```

## 📝 테스트 케이스 관리

### 테스트 케이스 템플릿
```markdown
## TC-001: 사용자 로그인

**목적**: 사용자가 이메일과 비밀번호로 로그인할 수 있는지 확인

**사전 조건**:
- 등록된 사용자 계정 존재
- 로그인 페이지 접근 가능

**테스트 단계**:
1. 로그인 페이지 접속
2. 이메일 입력: test@example.com
3. 비밀번호 입력: ********
4. 로그인 버튼 클릭

**예상 결과**:
- 대시보드로 리다이렉트
- 사용자 정보 표시
- 인증 토큰 저장

**실제 결과**: [테스트 후 기록]

**상태**: ✅ Pass / ❌ Fail
```

## 🚨 버그 리포팅

### 버그 리포트 템플릿
```markdown
## 버그 제목

**심각도**: Critical / High / Medium / Low
**발견 일자**: 2025-08-14
**발견자**: Tester Name

**재현 단계**:
1. [단계 1]
2. [단계 2]
3. [단계 3]

**예상 동작**:
[예상되는 정상 동작]

**실제 동작**:
[발생한 문제]

**스크린샷/로그**:
[첨부]

**환경**:
- Browser: Chrome 120
- OS: macOS 14
- Environment: Dev
```

## 🔄 업데이트 이력

| 버전 | 날짜 | 변경사항 | 작성자 |
|------|------|----------|--------|
| 1.0.0 | 2025-08-14 | 초기 테스트 전략 수립 | PM |

---

*본 테스트 전략은 프로젝트 진행에 따라 지속적으로 업데이트되며, 모든 팀원은 품질 목표 달성을 위해 테스트 우선 개발을 실천해야 합니다.*