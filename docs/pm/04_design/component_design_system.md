# 🧩 컴포넌트 디자인 시스템

> Korea Public Data 프로젝트의 재사용 가능한 UI 컴포넌트 라이브러리 정의

## 📋 목차
- [개요](#개요)
- [기술 스택](#기술-스택)
- [컴포넌트 카테고리](#컴포넌트-카테고리)
- [Core Components](#core-components)
- [Domain Components](#domain-components)
- [컴포넌트 개발 가이드](#컴포넌트-개발-가이드)
- [테스팅](#테스팅)

## 📖 개요

본 디자인 시스템은 Korea Public Data 프로젝트의 일관된 UI/UX를 보장하기 위한 컴포넌트 라이브러리입니다.

### 핵심 원칙
- **재사용성**: 한 번 만들어 여러 곳에서 활용
- **일관성**: 동일한 패턴과 스타일 적용
- **접근성**: WCAG 2.1 AA 표준 준수
- **성능**: 최적화된 렌더링과 번들 크기

## 🛠 기술 스택

```json
{
  "ui-framework": "React 18",
  "component-library": "@headlessui/react",
  "icons": "@heroicons/react",
  "styling": "Tailwind CSS 4",
  "animation": "framer-motion (optional)",
  "build": "Next.js 14.2.3"
}
```

## 📦 컴포넌트 카테고리

### 1. Layout Components
페이지 구조와 레이아웃을 담당하는 컴포넌트

### 2. Navigation Components
사용자 네비게이션을 위한 컴포넌트

### 3. Data Display Components
데이터를 표시하는 컴포넌트

### 4. Input Components
사용자 입력을 받는 컴포넌트

### 5. Feedback Components
사용자 피드백을 제공하는 컴포넌트

## 🎨 Core Components

### Button
```tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}

// 사용 예시
<Button 
  variant="primary" 
  size="md"
  icon={<PlusIcon />}
  onClick={handleSubmit}
>
  새 공고 추가
</Button>
```

### Input
```tsx
interface InputProps {
  type: 'text' | 'email' | 'password' | 'number' | 'search';
  label: string;
  placeholder?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  value: string;
  onChange: (value: string) => void;
}

// 사용 예시
<Input
  type="email"
  label="이메일"
  placeholder="user@example.com"
  error={errors.email}
  required
  value={email}
  onChange={setEmail}
/>
```

### Table
```tsx
interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  pagination?: PaginationProps;
  onSort?: (column: string) => void;
  onRowClick?: (row: T) => void;
}

// 사용 예시
<Table
  columns={announcementColumns}
  data={announcements}
  loading={isLoading}
  pagination={{
    current: 1,
    total: 100,
    pageSize: 20
  }}
/>
```

### Dialog (Modal)
```tsx
interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  actions?: DialogAction[];
}

// 사용 예시
<Dialog
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  title="공고 상세"
  actions={[
    { label: '취소', onClick: handleCancel },
    { label: '저장', onClick: handleSave, variant: 'primary' }
  ]}
>
  <AnnouncementDetail />
</Dialog>
```

### Badge
```tsx
interface BadgeProps {
  variant: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  size: 'sm' | 'md';
  children: React.ReactNode;
}

// 사용 예시
<Badge variant="success" size="sm">
  진행중
</Badge>
```

## 🏢 Domain Components

### AnnouncementCard
공고 정보를 표시하는 카드 컴포넌트
```tsx
interface AnnouncementCardProps {
  announcement: Announcement;
  onBookmark?: (id: string) => void;
  onShare?: (id: string) => void;
  compact?: boolean;
}

// Features
- 제목, 기관, 마감일 표시
- 북마크/공유 기능
- 반응형 디자인
- 스켈레톤 로딩
```

### BusinessInfoPanel
기업 정보 표시 패널
```tsx
interface BusinessInfoPanelProps {
  business: Business;
  showDetails?: boolean;
  actions?: BusinessAction[];
}

// Features
- 기업 기본 정보
- 통계 데이터 시각화
- 연락처 정보
- 액션 버튼
```

### StatisticsChart
통계 데이터 차트 컴포넌트
```tsx
interface StatisticsChartProps {
  type: 'line' | 'bar' | 'pie' | 'area';
  data: ChartData;
  options?: ChartOptions;
  loading?: boolean;
}

// Features
- 다양한 차트 타입
- 반응형 크기 조절
- 툴팁/레전드
- 데이터 export
```

### NotificationItem
알림 항목 컴포넌트
```tsx
interface NotificationItemProps {
  notification: Notification;
  onRead?: (id: string) => void;
  onAction?: (action: string) => void;
}

// Features
- 읽음/안읽음 상태
- 타임스탬프
- 액션 버튼
- 알림 타입별 아이콘
```

## 📝 컴포넌트 개발 가이드

### 1. 파일 구조
```
src/components/
├── core/           # 재사용 가능한 기본 컴포넌트
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── Button.stories.tsx
│   └── ...
├── domain/         # 도메인 특화 컴포넌트
│   ├── announcements/
│   ├── businesses/
│   └── ...
└── index.ts       # 컴포넌트 export
```

### 2. 컴포넌트 템플릿
```tsx
// Button.tsx
import { forwardRef } from 'react';
import { clsx } from 'clsx';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', loading, className, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={clsx(
          'inline-flex items-center justify-center font-medium transition-colors',
          // variant styles
          {
            'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
            'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary',
          },
          // size styles
          {
            'px-3 py-1.5 text-sm': size === 'sm',
            'px-4 py-2 text-base': size === 'md',
            'px-6 py-3 text-lg': size === 'lg',
          },
          className
        )}
        disabled={loading || props.disabled}
        {...props}
      >
        {loading && <Spinner className="mr-2" />}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

### 3. Props 규칙
- TypeScript 인터페이스 필수
- 기본값 제공
- JSDoc 주석 추가
- forwardRef 사용 (DOM 요소)

### 4. 스타일링 규칙
- Tailwind CSS 클래스 사용
- clsx로 조건부 스타일링
- 커스텀 CSS 최소화
- 다크모드 지원

### 5. 접근성 체크리스트
- [ ] 키보드 네비게이션
- [ ] ARIA 속성
- [ ] 포커스 관리
- [ ] 스크린 리더 지원
- [ ] 색상 대비

## 🧪 테스팅

### 단위 테스트
```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### 시각적 테스트
```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Core/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
};
```

## 📊 컴포넌트 사용 현황

| 컴포넌트 | 사용 빈도 | 마지막 업데이트 | 담당자 |
|---------|-----------|----------------|--------|
| Button | 높음 (50+) | 2025-08-14 | FE Team |
| Table | 높음 (30+) | 2025-08-14 | FE Team |
| Input | 높음 (40+) | 2025-08-14 | FE Team |
| Dialog | 중간 (15+) | 2025-08-14 | FE Team |
| Badge | 중간 (20+) | 2025-08-14 | FE Team |

## 🔄 버전 관리

| 버전 | 날짜 | 변경사항 | 작성자 |
|------|------|----------|--------|
| 1.0.0 | 2025-08-14 | 초기 디자인 시스템 구축 | PM |

## 📚 참고 자료

- [Headless UI Documentation](https://headlessui.dev/)
- [Heroicons](https://heroicons.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)

---

*본 디자인 시스템은 지속적으로 발전하며, 모든 개발자는 일관된 컴포넌트 사용을 통해 통일된 사용자 경험을 제공해야 합니다.*