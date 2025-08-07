# 🚀 CuraGenie Deployment Guide

This guide covers multiple deployment options for the CuraGenie healthcare platform.

## 📋 Prerequisites

- Git installed
- Node.js 18+ and npm
- Python 3.9+
- Docker (optional)
- Vercel CLI (for Vercel deployment)
- Heroku CLI (for Heroku deployment)

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Frontend      │────│   Backend       │────│   Database      │
│   (Next.js)     │    │   (FastAPI)     │    │   (SQLite)      │
│   Port: 3000    │    │   Port: 8000    │    │                 │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🌐 Deployment Options

### 1. Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/curagenie-frontend.git
cd curagenie-frontend

# Frontend setup
npm install
npm run dev

# Backend setup (new terminal)
cd curagenie-backend
pip install -r requirements.txt
python init_db.py
python main.py
```

**URLs:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 2. Vercel (Frontend) + Heroku (Backend)

#### Deploy Frontend to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod

# Set environment variables in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend.herokuapp.com
```

#### Deploy Backend to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create curagenie-backend

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set CORS_ORIGINS=https://your-frontend.vercel.app
heroku config:set DATABASE_URL=sqlite:///./curagenie.db

# Deploy backend
git subtree push --prefix=curagenie-backend heroku main

# Run database migrations
heroku run python init_db.py
```

### 3. Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build individual containers
docker build -t curagenie-frontend .
docker build -t curagenie-backend ./curagenie-backend

# Run containers
docker run -p 3000:3000 curagenie-frontend
docker run -p 8000:8000 curagenie-backend
```

### 4. AWS ECS/Fargate

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

docker build -t curagenie-frontend .
docker tag curagenie-frontend:latest your-account.dkr.ecr.us-east-1.amazonaws.com/curagenie-frontend:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/curagenie-frontend:latest

docker build -t curagenie-backend ./curagenie-backend
docker tag curagenie-backend:latest your-account.dkr.ecr.us-east-1.amazonaws.com/curagenie-backend:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/curagenie-backend:latest
```

### 5. Railway Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and initialize
railway login
railway init

# Deploy backend
cd curagenie-backend
railway up

# Deploy frontend
cd ..
railway up
```

## 🔧 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=CuraGenie
NEXT_PUBLIC_ENVIRONMENT=development
```

### Backend (.env)
```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///./curagenie.db
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
DEBUG=false
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

## 🏥 Healthcare Compliance

### HIPAA Considerations
- Enable HTTPS in production
- Use encrypted database connections
- Implement proper access controls
- Regular security audits
- Data encryption at rest and in transit

### Security Checklist
- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] Database encrypted
- [ ] API rate limiting enabled
- [ ] Input validation implemented
- [ ] Authentication required
- [ ] Audit logging enabled

## 📊 Monitoring & Logging

### Frontend Monitoring
```bash
# Add to package.json
npm install @vercel/analytics @vercel/speed-insights
```

### Backend Monitoring
```python
# Add to requirements.txt
sentry-sdk[fastapi]
prometheus-fastapi-instrumentator
```

## 🔄 CI/CD Pipeline

### GitHub Actions (.github/workflows/deploy.yml)
```yaml
name: Deploy CuraGenie

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "curagenie-backend"
          heroku_email: "your-email@example.com"
          appdir: "curagenie-backend"
```

## 🧪 Testing Deployment

### Health Checks
```bash
# Frontend
curl https://your-frontend.vercel.app

# Backend
curl https://your-backend.herokuapp.com/health

# API Documentation
curl https://your-backend.herokuapp.com/docs
```

### Load Testing
```bash
# Install artillery
npm install -g artillery

# Create load test config
artillery quick --count 10 --num 100 https://your-backend.herokuapp.com/health
```

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS_ORIGINS in backend environment
   - Ensure frontend URL is whitelisted

2. **Database Connection Issues**
   - Verify DATABASE_URL format
   - Check database permissions
   - Run migrations: `python init_db.py`

3. **Build Failures**
   - Check Node.js version compatibility
   - Verify all dependencies are installed
   - Clear build cache: `npm run clean`

4. **API Timeouts**
   - Increase timeout limits
   - Check server resources
   - Optimize database queries

### Logs Access
```bash
# Vercel logs
vercel logs

# Heroku logs
heroku logs --tail -a curagenie-backend

# Docker logs
docker logs container-name
```

## 📞 Support

For deployment issues:
- 📧 Email: guptasecularharsh@gmail.com
- 💼 LinkedIn: [harsh-gupta-kiet](https://linkedin.com/in/harsh-gupta-kiet/)
- 🐛 Issues: GitHub Issues page

## 🔐 Security Best Practices

1. **Never commit secrets** to version control
2. **Use environment variables** for configuration
3. **Enable HTTPS** in production
4. **Regular security updates** for dependencies
5. **Implement rate limiting** on APIs
6. **Use secure headers** in responses
7. **Regular backups** of data
8. **Monitor access logs** for suspicious activity

---

Built with ❤️ for secure, scalable healthcare technology.
