# Korean Public Data Platform

통합된 한국 공공데이터 플랫폼의 전체 배포를 위한 Docker Compose 구성입니다.

## 🏗️ 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (MongoDB)     │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 27017   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐             │
         │              │     Redis       │             │
         └──────────────►│   (Cache)       │◄────────────┘
                        │   Port: 6379    │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │   Celery        │
                        │   (Workers)     │
                        └─────────────────┘
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd korea_public_data

# 환경 변수 파일 복사 및 수정
cp .env.example .env
# .env 파일을 편집하여 실제 값으로 변경
```

### 2. 프로덕션 배포

```bash
# 자동 배포 스크립트 실행
./deploy.sh

# 또는 수동 실행
docker-compose up -d --build
```

### 3. 개발 환경 실행

```bash
# 개발 모드로 실행 (핫 리로드 지원)
docker-compose -f docker-compose.dev.yml up -d --build
```

## 📋 서비스 구성

### 🌐 웹 서비스
- **Frontend**: Next.js 애플리케이션 (http://localhost:3000)
- **Backend**: FastAPI 서버 (http://localhost:8000)

### 💾 데이터베이스
- **MongoDB**: 메인 데이터베이스 (mongodb://localhost:27017)
- **Redis**: 캐시 및 세션 스토어 (redis://localhost:6379)

### ⚙️ 백그라운드 서비스
- **Celery Worker**: 비동기 작업 처리
- **Celery Beat**: 스케줄된 작업 실행

### 📊 모니터링
- **Grafana**: 모니터링 대시보드 (http://localhost:3001)
- **Prometheus**: 메트릭 수집 (http://localhost:9090)

### 🔗 리버스 프록시
- **Nginx**: 웹 서버 및 로드 밸런서 (http://localhost)

## 🔧 환경 변수

주요 환경 변수들을 `.env` 파일에서 설정해야 합니다:

```bash
# 데이터베이스
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=your_secure_password
DATABASE_NAME=korea_public_api

# API 키
PUBLIC_DATA_API_KEY=your_public_data_api_key
PUBLIC_DATA_API_KEY_DECODE=your_decoded_api_key

# NextAuth
NEXTAUTH_SECRET=your_nextauth_secret
NEXTAUTH_URL=http://localhost:3000

# 모니터링
GRAFANA_PASSWORD=your_grafana_password
```

## 🛠️ 유용한 명령어

### 서비스 관리
```bash
# 모든 서비스 시작
docker-compose up -d

# 특정 서비스 재시작
docker-compose restart frontend

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f backend

# 모든 서비스 중지
docker-compose down

# 볼륨까지 완전 삭제
docker-compose down -v --remove-orphans
```

### 개발 모드
```bash
# 개발 모드 시작
docker-compose -f docker-compose.dev.yml up -d

# 개발 모드 로그 확인
docker-compose -f docker-compose.dev.yml logs -f

# 개발 모드 중지
docker-compose -f docker-compose.dev.yml down
```

### 데이터베이스 작업
```bash
# MongoDB 접속
docker exec -it korea_mongodb_prod mongosh

# Redis 접속
docker exec -it korea_redis_prod redis-cli

# 데이터 백업
./be/scripts/backup.sh

# 데이터 복원
./be/scripts/restore.sh
```

## 📁 볼륨 구조

백엔드의 기존 볼륨 구조를 그대로 사용합니다:

```
be/volumes/
├── mongodb/
│   ├── data/           # MongoDB 데이터
│   └── configdb/       # MongoDB 설정
├── redis/
│   └── data/           # Redis 데이터
├── logs/               # 애플리케이션 로그
├── uploads/            # 업로드된 파일
├── tmp/                # 임시 파일
├── prometheus/         # Prometheus 데이터
└── grafana/           # Grafana 데이터
```

## 🔍 헬스체크

모든 서비스에 헬스체크가 구성되어 있습니다:

```bash
# 헬스체크 상태 확인
docker-compose ps

# 개별 서비스 헬스체크
curl http://localhost:3000/api/health  # Frontend
curl http://localhost:8000/health      # Backend
```

## 🚨 트러블슈팅

### 일반적인 문제들

1. **포트 충돌**
   ```bash
   # 사용 중인 포트 확인
   lsof -i :3000
   lsof -i :8000
   ```

2. **권한 문제**
   ```bash
   # 볼륨 권한 수정
   sudo chmod -R 755 be/volumes/
   ```

3. **서비스 시작 실패**
   ```bash
   # 개별 서비스 로그 확인
   docker-compose logs service_name
   
   # 컨테이너 재빌드
   docker-compose build --no-cache service_name
   ```

4. **데이터베이스 연결 실패**
   ```bash
   # MongoDB 연결 테스트
   docker exec korea_mongodb_prod mongosh --eval "db.adminCommand('ping')"
   
   # Redis 연결 테스트
   docker exec korea_redis_prod redis-cli ping
   ```

## 📈 모니터링

### Grafana 대시보드
- URL: http://localhost:3001
- 기본 로그인: admin / admin123 (변경 권장)

### Prometheus
- URL: http://localhost:9090
- 메트릭 수집 및 쿼리

### 로그 모니터링
```bash
# 실시간 로그 모니터링
docker-compose logs -f --tail=100

# 특정 서비스 로그
docker-compose logs -f frontend backend
```

## 🔄 업데이트

```bash
# 이미지 업데이트
docker-compose pull

# 서비스 재시작
docker-compose up -d

# 전체 재빌드
docker-compose build --no-cache
docker-compose up -d
```

## 🛡️ 보안 고려사항

1. `.env` 파일의 패스워드를 강력하게 설정
2. 프로덕션에서는 기본 포트 변경 고려
3. SSL/TLS 인증서 설정 (Nginx 설정 참조)
4. 방화벽 규칙 적용
5. 정기적인 보안 업데이트

## 📞 지원

문제가 발생하거나 도움이 필요한 경우:

1. 먼저 로그를 확인하세요: `docker-compose logs -f`
2. 헬스체크 상태를 확인하세요: `docker-compose ps`
3. 이슈 트래커에 보고해주세요

---

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.