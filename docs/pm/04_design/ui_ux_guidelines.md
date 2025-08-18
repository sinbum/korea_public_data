# 🎨 UI/UX 디자인 가이드라인

> Korea Public Data 프로젝트의 일관된 사용자 경험을 위한 디자인 원칙과 가이드라인

## 📋 목차
- [디자인 원칙](#디자인-원칙)
- [시각적 계층 구조](#시각적-계층-구조)
- [컬러 시스템](#컬러-시스템)
- [타이포그래피](#타이포그래피)
- [컴포넌트 디자인](#컴포넌트-디자인)
- [반응형 디자인](#반응형-디자인)
- [접근성](#접근성)
- [인터랙션 패턴](#인터랙션-패턴)

## 🎯 디자인 원칙

### 1. 명확성 (Clarity)
- **직관적인 네비게이션**: 사용자가 쉽게 원하는 정보를 찾을 수 있도록 구성
- **명확한 레이블링**: 모든 버튼, 링크, 입력 필드에 명확한 라벨 사용
- **일관된 용어**: 동일한 기능에는 동일한 용어 사용

### 2. 일관성 (Consistency)
- **디자인 시스템 준수**: Tailwind CSS 기반 일관된 스타일링
- **컴포넌트 재사용**: HeadlessUI 기반 표준 컴포넌트 활용
- **패턴 통일**: 유사한 기능은 동일한 인터랙션 패턴 적용

### 3. 효율성 (Efficiency)
- **최소 클릭**: 핵심 기능까지 3번 이내 클릭으로 접근
- **빠른 로딩**: 3초 이내 페이지 로드 (3G 기준)
- **스마트 기본값**: 자주 사용되는 옵션을 기본값으로 설정

### 4. 접근성 (Accessibility)
- **WCAG 2.1 AA 준수**: 모든 컴포넌트 접근성 표준 충족
- **키보드 네비게이션**: 마우스 없이 모든 기능 사용 가능
- **스크린 리더 지원**: 의미있는 ARIA 라벨 제공

## 🎨 시각적 계층 구조

### 페이지 레이아웃
```
┌─────────────────────────────────────┐
│         Navigation Bar              │
├─────────┬───────────────────────────┤
│ Sidebar │      Main Content         │
│  (240px)│                           │
│         │   ┌──────────────────┐    │
│         │   │   Page Header    │    │
│         │   ├──────────────────┤    │
│         │   │                  │    │
│         │   │   Content Area   │    │
│         │   │                  │    │
│         │   └──────────────────┘    │
└─────────┴───────────────────────────┘
```

### Z-Index 계층
- **9999**: 긴급 알림, 시스템 메시지
- **1000**: 모달, 다이얼로그
- **100**: 드롭다운, 툴팁
- **10**: 스티키 헤더
- **1**: 기본 콘텐츠

## 🎨 컬러 시스템

### 주요 색상
```css
/* Primary Colors */
--primary-50: #eff6ff;
--primary-500: #3b82f6;
--primary-900: #1e3a8a;

/* Semantic Colors */
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;

/* Neutral Colors */
--gray-50: #f9fafb;
--gray-500: #6b7280;
--gray-900: #111827;
```

### 색상 사용 규칙
- **Primary**: 주요 액션 버튼, 활성 상태
- **Secondary**: 보조 액션, 비활성 상태
- **Success**: 성공 메시지, 완료 상태
- **Warning**: 주의 필요, 경고 메시지
- **Error**: 오류 상태, 유효성 검사 실패

## 📝 타이포그래피

### 폰트 패밀리
```css
/* 한글 */
font-family: 'Noto Sans KR', 'Pretendard', sans-serif;

/* 영문/숫자 */
font-family: 'Inter', system-ui, sans-serif;
```

### 폰트 크기 체계
| 용도 | 크기 | 행간 | 사용처 |
|------|------|------|--------|
| Display | 48px | 1.2 | 랜딩 페이지 제목 |
| H1 | 36px | 1.3 | 페이지 제목 |
| H2 | 28px | 1.4 | 섹션 제목 |
| H3 | 24px | 1.4 | 서브섹션 제목 |
| Body | 16px | 1.6 | 본문 텍스트 |
| Small | 14px | 1.5 | 보조 텍스트 |
| Caption | 12px | 1.4 | 캡션, 라벨 |

## 🧩 컴포넌트 디자인

### 버튼 (Buttons)
```tsx
/* Primary Button */
<Button variant="primary" size="md">
  주요 액션
</Button>

/* Secondary Button */
<Button variant="secondary" size="md">
  보조 액션
</Button>

/* Ghost Button */
<Button variant="ghost" size="md">
  최소 강조
</Button>
```

### 입력 필드 (Input Fields)
- **최소 높이**: 44px (모바일 터치 타겟)
- **패딩**: 12px 16px
- **보더**: 1px solid #d1d5db
- **포커스**: 2px solid primary-500

### 카드 (Cards)
```css
.card {
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  background: white;
}
```

## 📱 반응형 디자인

### 브레이크포인트
```css
/* Mobile First Approach */
sm: 640px   /* 태블릿 세로 */
md: 768px   /* 태블릿 가로 */
lg: 1024px  /* 노트북 */
xl: 1280px  /* 데스크톱 */
2xl: 1536px /* 대형 모니터 */
```

### 반응형 그리드
```css
/* Mobile: 1 column */
grid-cols-1

/* Tablet: 2 columns */
sm:grid-cols-2

/* Desktop: 3-4 columns */
lg:grid-cols-3
xl:grid-cols-4
```

## ♿ 접근성

### 필수 체크리스트
- [ ] 모든 이미지에 alt 텍스트 제공
- [ ] 폼 요소에 label 연결
- [ ] 키보드로 모든 기능 접근 가능
- [ ] 포커스 인디케이터 명확히 표시
- [ ] 색상만으로 정보 전달 금지
- [ ] 최소 4.5:1 색상 대비율
- [ ] 에러 메시지 명확히 표시

### ARIA 사용 예시
```html
<button 
  aria-label="검색"
  aria-pressed="false"
  aria-describedby="search-help"
>
  <SearchIcon />
</button>
```

## 🎭 인터랙션 패턴

### 로딩 상태
- **스켈레톤 스크린**: 콘텐츠 로딩 시
- **스피너**: 액션 처리 중
- **프로그레스 바**: 장시간 작업

### 피드백 메시지
- **토스트**: 간단한 알림 (3초 후 자동 사라짐)
- **배너**: 중요 공지사항
- **모달**: 사용자 확인 필요

### 애니메이션
```css
/* Smooth transitions */
transition: all 0.2s ease-in-out;

/* Hover effects */
hover:scale-105
hover:shadow-lg

/* Focus effects */
focus:ring-2
focus:ring-primary-500
```

## 📊 성능 최적화

### 이미지 최적화
- **포맷**: WebP 우선, JPEG/PNG 폴백
- **레이지 로딩**: Intersection Observer 활용
- **반응형 이미지**: srcset 활용

### CSS 최적화
- **Tailwind Purge**: 사용하지 않는 스타일 제거
- **Critical CSS**: 초기 렌더링 필수 CSS 인라인
- **CSS-in-JS 최소화**: 런타임 오버헤드 감소

## 🔄 업데이트 이력

| 버전 | 날짜 | 변경사항 | 작성자 |
|------|------|----------|--------|
| 1.0.0 | 2025-08-14 | 초기 가이드라인 작성 | PM |

---

*본 가이드라인은 지속적으로 업데이트되며, 모든 팀원은 이를 준수하여 일관된 사용자 경험을 제공해야 합니다.*