# 🚀 CuraGenie Deployment Guide

This guide provides multiple deployment options for your **CuraGenie Healthcare Platform**.

## 📋 Pre-Deployment Checklist

### 1. Environment Variables Setup
Create production environment files:

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
NEXT_PUBLIC_APP_URL=https://your-frontend-domain.com
NODE_ENV=production
```

#### Backend (.env)
```bash
DATABASE_URL=sqlite:///./curagenie.db
SECRET_KEY=your-super-secret-key-here-32-chars-minimum
CORS_ORIGINS=https://your-frontend-domain.com
DEBUG=false
OPENAI_API_KEY=your-openai-api-key-here
REDIS_URL=redis://localhost:6379
```

## 🎯 Deployment Options

---

## Option 1: 🌐 Vercel + Railway (Recommended for MVP)

### **Frontend on Vercel** (Free tier available)

1. **Push to GitHub first:**
```bash
git remote add origin https://github.com/your-username/curagenie.git
git push -u origin master
```

2. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Connect your GitHub account
   - Import your repository
   - Set environment variables in Vercel dashboard:
     - `NEXT_PUBLIC_API_URL`: Your backend URL
   - Deploy automatically

### **Backend on Railway** ($5/month)

1. **Go to [railway.app](https://railway.app)**
2. **Deploy from GitHub:**
   - Connect GitHub repository
   - Select `curagenie-backend` folder
   - Railway will auto-detect Python and use Dockerfile

3. **Set environment variables in Railway:**
```bash
DATABASE_URL=sqlite:///./curagenie.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://your-vercel-app.vercel.app
PORT=8000
```

4. **Add Redis service:** Click "Add Service" → Redis

---

## Option 2: 🐳 Docker + DigitalOcean (Production Ready)

### **Deploy Full Stack with Docker**

1. **Create a DigitalOcean Droplet:**
   - Choose Ubuntu 22.04
   - At least 2GB RAM recommended
   - Install Docker and Docker Compose

2. **Clone your repository on the server:**
```bash
git clone https://github.com/your-username/curagenie.git
cd curagenie
```

3. **Set up environment variables:**
```bash
# Create .env file
cp .env.example .env
# Edit with your production values
nano .env
```

4. **Deploy with Docker Compose:**
```bash
# Build and start all services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

5. **Set up SSL with Let's Encrypt:**
```bash
# Install certbot
sudo apt install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Update nginx.conf with SSL paths
```

---

## Option 3: ☁️ AWS (Enterprise Scale)

### **Frontend on AWS S3 + CloudFront**

1. **Build the frontend:**
```bash
npm run build
npm run export  # If using static export
```

2. **Upload to S3 bucket**
3. **Configure CloudFront distribution**
4. **Set up custom domain with Route 53**

### **Backend on AWS ECS/Fargate**

1. **Push Docker image to ECR**
2. **Create ECS cluster and task definition**
3. **Set up Application Load Balancer**
4. **Configure RDS for database (optional)**

---

## Option 4: 🔥 Firebase + Google Cloud Run

### **Frontend on Firebase Hosting**
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
npm run build
firebase deploy
```

### **Backend on Google Cloud Run**
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/curagenie-backend ./curagenie-backend

# Deploy to Cloud Run
gcloud run deploy curagenie-backend --image gcr.io/YOUR_PROJECT_ID/curagenie-backend --platform managed
```

---

## Option 5: 📱 Heroku (Simple but Paid)

### **Backend on Heroku**
```bash
# Install Heroku CLI
# Login and create app
heroku login
heroku create curagenie-backend

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DATABASE_URL=sqlite:///./curagenie.db

# Deploy
git subtree push --prefix curagenie-backend heroku master
```

### **Frontend on Heroku**
```bash
heroku create curagenie-frontend
heroku config:set NEXT_PUBLIC_API_URL=https://curagenie-backend.herokuapp.com
git push heroku master
```

---

## 🛠️ Production Optimizations

### 1. **Database Migration (SQLite → PostgreSQL)**
For production, consider upgrading to PostgreSQL:

```bash
# Install PostgreSQL dependencies
pip install psycopg2-binary

# Update DATABASE_URL
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### 2. **File Storage (Local → S3/CloudFlare R2)**
For file uploads, use cloud storage:

```python
# Add to backend requirements.txt
boto3==1.26.137

# Configure S3 in backend
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_BUCKET_NAME=curagenie-uploads
```

### 3. **Caching & CDN**
- Use Redis for session management
- CloudFlare for CDN and DDoS protection
- Implement API response caching

### 4. **Monitoring & Logging**
```bash
# Add monitoring services
SENTRY_DSN=your-sentry-dsn-here
NEW_RELIC_LICENSE_KEY=your-new-relic-key
```

---

## 🔐 Security Checklist

- [ ] **HTTPS enabled** (SSL certificates)
- [ ] **Environment variables secured**
- [ ] **API rate limiting implemented**
- [ ] **CORS properly configured**
- [ ] **Database backups scheduled**
- [ ] **File upload validation**
- [ ] **Authentication tokens secured**
- [ ] **Dependency vulnerabilities checked**

---

## 📊 Cost Estimates

### **MVP Deployment (Vercel + Railway):**
- Frontend: **Free** (Vercel Hobby)
- Backend: **$5/month** (Railway)
- Domain: **$10/year**
- **Total: ~$65/year**

### **Production Deployment (DigitalOcean):**
- Droplet (4GB): **$24/month**
- Load Balancer: **$12/month**
- Database: **$15/month**
- **Total: ~$610/year**

### **Enterprise Deployment (AWS):**
- **$100-500/month** depending on traffic

---

## 🚀 Quick Start - Deploy in 5 Minutes

**For fastest deployment (MVP):**

1. **Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/curagenie.git
git push -u origin master
```

2. **Deploy Frontend to Vercel:**
   - Visit [vercel.com](https://vercel.com) → Import Project
   - Connect GitHub → Select repository
   - Set `NEXT_PUBLIC_API_URL` environment variable

3. **Deploy Backend to Railway:**
   - Visit [railway.app](https://railway.app) → New Project
   - Deploy from GitHub → Select `curagenie-backend`
   - Add environment variables
   - Add Redis service

**🎉 Your CuraGenie platform will be live in minutes!**

---

## 📞 Support & Troubleshooting

### Common Issues:
- **Build failures**: Check Node.js version compatibility
- **Database errors**: Verify connection strings
- **CORS issues**: Update CORS_ORIGINS with your frontend URL
- **File upload issues**: Check file permissions and storage configuration

### Getting Help:
- Check deployment logs for specific error messages
- Verify all environment variables are set correctly
- Test API endpoints individually
- Check database connectivity

---

## 🎯 Next Steps After Deployment

1. **Set up monitoring** (Sentry, New Relic)
2. **Configure automated backups**
3. **Set up CI/CD pipelines**
4. **Add performance monitoring**
5. **Implement user analytics**
6. **Set up email notifications**
7. **Add API documentation** (Swagger/OpenAPI)

---

**💡 Need help with deployment? Each option has detailed step-by-step instructions available!**
