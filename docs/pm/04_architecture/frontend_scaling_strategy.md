# 🚀 Frontend 확장성 전략 - 모노레포 vs 서브모듈

## 📋 현재 상태 분석

### 🏗️ 현재 아키텍처
Korea Public Data 프로젝트는 **Module Federation 기반 마이크로프론트엔드** 구조를 사용 중입니다.

```
fe/
├── shell/                 # Host 애플리케이션 (Orchestrator)
├── shared/               # 공통 라이브러리 & 컴포넌트
├── remote-auth/          # 인증 마이크로앱
├── remote-announcements/ # 공고 마이크로앱  
├── remote-businesses/    # 사업 마이크로앱
├── remote-contents/      # 콘텐츠 마이크로앱
└── remote-dashboard/     # 대시보드 마이크로앱
```

### ✅ 현재 장점
- **모듈러 구조**: 각 도메인별 독립적 개발 가능
- **런타임 통합**: Module Federation으로 동적 로딩
- **공통 라이브러리**: `@shared` 패키지로 코드 재사용
- **타입 안전성**: TypeScript 100% 적용

### 🔄 확장 시 예상 문제점
- **빌드 시간 증가**: 도메인 추가 시 전체 빌드 시간 증가
- **의존성 복잡성**: shared 라이브러리 변경 시 전체 영향
- **팀 간 결합도**: 하나의 레포지토리에 모든 코드 집중

## 🎯 확장 전략 로드맵

### 📊 단계별 확장 기준

| 단계 | 도메인 수 | 팀 구조 | 권장 전략 | 도구 |
|------|-----------|---------|-----------|------|
| **Phase 1** | 4-6개 | 통합 팀 | 모노레포 유지 | 현재 구조 |
| **Phase 2** | 7-12개 | 도메인별 팀 | 모노레포 + 도구 | Nx/Lerna |
| **Phase 3** | 13-20개 | 독립 팀 | 하이브리드 | 레포 분리 |
| **Phase 4** | 21+개 | 다중 조직 | 서브모듈 | 완전 분리 |

### 🚀 Phase 1: 현재 → 최적화 (4-6개 도메인)

#### 목표
현재 모노레포 구조를 유지하면서 확장성 개선

#### 실행 계획
```bash
# 1. Workspace 최적화
npm install -g pnpm
pnpm install  # 더 효율적인 패키지 관리

# 2. 빌드 최적화
npm install --save-dev @nx/core  # 빌드 캐싱
```

#### 예상 도메인 추가
- `remote-users/` - 사용자 관리
- `remote-notifications/` - 알림 시스템

### 🔧 Phase 2: 도구 도입 (7-12개 도메인)

#### Nx Workspace 도입

```bash
# Nx 설치 및 설정
npx nx@latest init

# nx.json 설정
{
  "extends": "nx/presets/npm.json",
  "targetDefaults": {
    "build": {
      "cache": true,
      "dependsOn": ["^build"]
    }
  }
}
```

#### 프로젝트 구조 개선
```
fe/
├── apps/
│   ├── shell/              # Host 앱
│   ├── auth/               # 인증 앱
│   ├── announcements/      # 공고 앱
│   └── businesses/         # 사업 앱
├── libs/
│   ├── shared-ui/          # UI 컴포넌트
│   ├── shared-utils/       # 유틸리티
│   └── shared-types/       # 타입 정의
└── tools/
    ├── webpack/            # Webpack 설정
    └── eslint/             # Lint 규칙
```

#### 장점
- **캐시된 빌드**: 변경된 부분만 재빌드
- **의존성 그래프**: 영향도 자동 분석
- **코드 생성**: 일관된 프로젝트 구조

### 🌐 Phase 3: 하이브리드 접근 (13-20개 도메인)

#### 전략
핵심 도메인 그룹별로 레포지토리 분리하되 Module Federation으로 통합

```
korea-public-data-core/        # 핵심 비즈니스 로직
├── announcements/
├── businesses/
└── contents/

korea-public-data-platform/    # 플랫폼 기능
├── auth/
├── users/
└── notifications/

korea-public-data-admin/       # 관리자 기능
├── admin-dashboard/
├── analytics/ 
└── system-management/
```

#### Module Federation 설정
```javascript
// webpack.config.js (각 레포지토리)
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'coreServices',
      exposes: {
        './Announcements': './src/components/Announcements',
        './Businesses': './src/components/Businesses'
      },
      shared: {
        react: { singleton: true },
        'react-dom': { singleton: true },
        '@shared/types': { singleton: true }
      }
    })
  ]
};
```

### 🏢 Phase 4: 완전 분리 (21+개 도메인)

#### 서브모듈 전략
```bash
# 메인 레포지토리
git submodule add https://github.com/team/fe-auth.git packages/auth
git submodule add https://github.com/team/fe-announcements.git packages/announcements

# 개발 환경 설정
git submodule update --init --recursive
```

#### 패키지 관리
```json
// package.json (각 서브모듈)
{
  "name": "@korea-public-data/auth",
  "version": "1.0.0",
  "peerDependencies": {
    "@korea-public-data/shared-types": "^1.0.0"
  }
}
```

## 🛠️ 기술적 구현 방안

### 1. 공통 라이브러리 관리

#### NPM Private Registry 구축
```bash
# Verdaccio 설치
npm install -g verdaccio
verdaccio

# 패키지 발행
npm publish --registry http://localhost:4873
```

#### 패키지 버전 관리
```json
// lerna.json
{
  "version": "independent",
  "npmClient": "pnpm",
  "command": {
    "publish": {
      "conventionalCommits": true,
      "message": "chore(release): publish"
    }
  }
}
```

### 2. Module Federation 최적화

#### 런타임 타입 안전성
```typescript
// types/module-federation.d.ts
declare module 'auth/AuthModule' {
  import { ComponentType } from 'react';
  const AuthModule: ComponentType;
  export default AuthModule;
}
```

#### 공유 의존성 최적화
```javascript
const shared = {
  react: { 
    singleton: true,
    requiredVersion: '^18.0.0'
  },
  '@shared/types': {
    singleton: true,
    strictVersion: true
  }
};
```

### 3. 빌드 최적화

#### Turborepo 설정
```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "build/**"]
    },
    "test": {
      "cache": false
    }
  }
}
```

#### 캐시 전략
```bash
# 로컬 캐시
turbo build --cache-dir=.turbo

# 원격 캐시 (Vercel)
turbo build --token=$TURBO_TOKEN
```

## 📊 확장성 메트릭

### 성능 지표
| 메트릭 | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|---------|---------|---------|---------|
| **빌드 시간** | ~5분 | ~3분 | ~2분 | ~1분 |
| **번들 크기** | 2MB | 1.5MB | 1MB | 800KB |
| **개발 서버 시작** | 30초 | 15초 | 10초 | 5초 |
| **타입 체크** | 2분 | 1분 | 30초 | 10초 |

### 개발 경험 지표
```bash
# 코드 변경 후 핫 리로드
Phase 1: ~3초
Phase 2: ~2초  
Phase 3: ~1초
Phase 4: ~500ms
```

## 🎨 도메인별 특화 전략

### 📢 Announcements Domain
```
high-traffic 도메인 → 독립적인 CDN 배포 권장
└── 별도 레포지토리 우선 고려
```

### 🏭 Businesses Domain  
```
복잡한 비즈니스 로직 → 모노레포에서 유지
└── 다른 도메인과의 강한 결합성
```

### 📄 Contents Domain
```
컨텐츠 관리 시스템 → CMS 팀 독립성 고려
└── Phase 3에서 분리 고려
```

### 👤 Users Domain (예정)
```
보안 민감 → 독립적인 레포지토리 권장
└── 별도 배포 파이프라인 구축
```

## 🚦 의사결정 가이드라인

### 모노레포 유지 기준
- [ ] 팀 크기 < 10명
- [ ] 도메인 간 강한 결합성
- [ ] 공통 릴리즈 사이클
- [ ] 빌드 시간 < 5분

### 서브모듈 분리 기준  
- [ ] 독립적인 팀 (3명 이상)
- [ ] 다른 릴리즈 사이클
- [ ] 특별한 보안 요구사항
- [ ] 다른 기술 스택 필요

## 🔄 마이그레이션 시나리오

### Scenario A: 점진적 분리
```bash
# 1단계: Nx 도입
npx nx@latest init

# 2단계: 라이브러리 분리  
nx generate @nx/react:library shared-ui

# 3단계: 앱 분리
nx generate @nx/react:application new-domain
```

### Scenario B: 긴급 분리
```bash
# 기존 코드 그대로 새 레포로 이동
git subtree push --prefix=fe/remote-auth origin auth-repo

# Module Federation 설정 업데이트
# 의존성 재구성
```

## 💡 권장사항

### 현재 시점 (2025년)
1. **Phase 1 유지**: 현재 구조가 적절함
2. **pnpm 도입**: 더 효율적인 패키지 관리
3. **Nx 준비**: 미래 확장성을 위한 기반 구축

### 6개월 후 재평가 기준
- 개발팀 규모 변화
- 도메인 추가 속도
- 빌드 시간 증가율
- 팀 간 충돌 빈도

### 1년 후 목표
- **빌드 시간**: 현재 대비 50% 단축
- **개발 생산성**: 20% 향상  
- **배포 독립성**: 도메인별 독립 배포 가능

---

**📅 작성일**: 2025-07-30  
**👤 작성자**: PM Team  
**🔄 검토 주기**: 분기별  
**📋 다음 검토**: 2025-10-30  
**🎯 적용 대상**: 전체 Frontend 아키텍처