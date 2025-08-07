# CuraGenie Quick Deployment Script for Windows PowerShell
# Run this script to deploy your CuraGenie platform

Write-Host "🚀 CuraGenie Deployment Script" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green

# Check if Git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "❌ Git repository not found. Initializing..." -ForegroundColor Red
    git init
    git add .
    git commit -m "🚀 Initial commit: CuraGenie Healthcare Platform"
}

Write-Host "`n📋 Deployment Options:" -ForegroundColor Yellow
Write-Host "1. 🌐 Quick Deploy (Vercel + Railway) - FREE/5$ per month" -ForegroundColor Cyan
Write-Host "2. 🐳 Docker Deploy (DigitalOcean) - $24 per month" -ForegroundColor Cyan
Write-Host "3. 📱 Local Deploy (Test before production)" -ForegroundColor Cyan
Write-Host "4. 📖 View deployment guide" -ForegroundColor Cyan

$choice = Read-Host "`nSelect an option (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`n🌐 Quick Deploy Setup:" -ForegroundColor Green
        Write-Host "1. Create GitHub repository at: https://github.com/new" -ForegroundColor Yellow
        Write-Host "2. Copy this command and run it:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "git remote add origin https://github.com/YOUR_USERNAME/curagenie.git" -ForegroundColor White -BackgroundColor Black
        Write-Host "git branch -M main" -ForegroundColor White -BackgroundColor Black
        Write-Host "git push -u origin main" -ForegroundColor White -BackgroundColor Black
        Write-Host ""
        Write-Host "3. Frontend (FREE): Go to https://vercel.com" -ForegroundColor Yellow
        Write-Host "   - Import your GitHub repository" -ForegroundColor Gray
        Write-Host "   - Set environment variable: NEXT_PUBLIC_API_URL" -ForegroundColor Gray
        Write-Host ""
        Write-Host "4. Backend (`$5/month): Go to https://railway.app" -ForegroundColor Yellow
        Write-Host "   - Deploy from GitHub" -ForegroundColor Gray
        Write-Host "   - Select curagenie-backend folder" -ForegroundColor Gray
        Write-Host "   - Add environment variables (see .env.example)" -ForegroundColor Gray
        Write-Host "   - Add Redis service" -ForegroundColor Gray
        Write-Host ""
        Write-Host "⚡ Total cost: ~`$5/month (Frontend FREE + Backend `$5)" -ForegroundColor Green
    }
    
    "2" {
        Write-Host "`n🐳 Docker Deploy Instructions:" -ForegroundColor Green
        Write-Host "1. Create DigitalOcean Droplet (Ubuntu 22.04, 2GB RAM)" -ForegroundColor Yellow
        Write-Host "2. SSH into your server and run:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "git clone https://github.com/YOUR_USERNAME/curagenie.git" -ForegroundColor White -BackgroundColor Black
        Write-Host "cd curagenie" -ForegroundColor White -BackgroundColor Black
        Write-Host "cp .env.example .env" -ForegroundColor White -BackgroundColor Black
        Write-Host "# Edit .env with production values" -ForegroundColor White -BackgroundColor Black
        Write-Host "docker-compose up -d --build" -ForegroundColor White -BackgroundColor Black
        Write-Host ""
        Write-Host "⚡ Total cost: ~`$24/month" -ForegroundColor Green
    }
    
    "3" {
        Write-Host "`n📱 Testing Local Deployment..." -ForegroundColor Green
        
        # Start backend
        Write-Host "Starting backend server..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-Command", "cd curagenie-backend; python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload" -WindowStyle Minimized
        
        # Wait a moment
        Start-Sleep -Seconds 3
        
        # Start frontend
        Write-Host "Starting frontend server..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-Command", "npm run dev" -WindowStyle Minimized
        
        Write-Host "✅ Local deployment started!" -ForegroundColor Green
        Write-Host "🌐 Frontend: http://localhost:3002" -ForegroundColor Cyan
        Write-Host "⚡ Backend: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
        
        # Open browser
        Start-Process "http://localhost:3002"
    }
    
    "4" {
        Write-Host "`n📖 Opening deployment guide..." -ForegroundColor Green
        Start-Process "DEPLOYMENT_GUIDE.md"
    }
    
    default {
        Write-Host "❌ Invalid option selected." -ForegroundColor Red
    }
}

Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "• Set up custom domain name" -ForegroundColor Gray
Write-Host "• Configure SSL certificates" -ForegroundColor Gray
Write-Host "• Set up monitoring and backups" -ForegroundColor Gray
Write-Host "• Add your LinkedIn profile: linkedin.com/in/harsh-gupta-kiet" -ForegroundColor Gray

Write-Host "`n💡 Need help? Check DEPLOYMENT_GUIDE.md for detailed instructions!" -ForegroundColor Cyan
