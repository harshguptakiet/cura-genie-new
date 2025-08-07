# 🧠 CuraGenie - AI-Powered Healthcare Platform

<div align="center">

**Transform your healthcare experience with intelligent medical insights**

[![Next.js](https://img.shields.io/badge/Next.js-15.4.5-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue?style=for-the-badge&logo=typescript)](https://typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0+-cyan?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)

[Demo](http://localhost:3002) • [API Docs](http://localhost:8000/docs) • [LinkedIn](https://linkedin.com/in/harsh-gupta-kiet/)

</div>

## 🌟 Features

### 🔬 **Medical AI Analysis**
- **Brain Tumor Detection** - Advanced CNN-based MRI scan analysis
- **Real-time Processing** - Instant medical image classification  
- **Multiple Tumor Types** - Detects Glioma, Meningioma, and other abnormalities
- **Confidence Scoring** - Provides accuracy metrics for each prediction

### 🧬 **Genomic Analysis**
- **VCF File Processing** - Comprehensive genetic variant analysis
- **PRS Calculations** - Polygenic Risk Score computation
- **Disease Prediction** - AI-powered health risk assessment
- **Personalized Reports** - Detailed genomic insights

### 💬 **AI Healthcare Chatbot**
- **Medical Queries** - Intelligent health-related Q&A
- **Symptom Analysis** - Preliminary health assessment
- **Treatment Suggestions** - Evidence-based recommendations
- **24/7 Availability** - Round-the-clock healthcare support

### 📊 **Health Dashboard**
- **Real-time Monitoring** - Live health metrics tracking
- **Interactive Visualizations** - Dynamic charts and graphs
- **Progress Tracking** - Historical health data analysis
- **Predictive Analytics** - Future health trend forecasting

## 🚀 Tech Stack

### Frontend
- **Framework**: Next.js 15.4.5 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Custom animations
- **Components**: Custom UI components with Lucide icons
- **State Management**: Zustand for global state
- **HTTP Client**: Native fetch API
- **Authentication**: JWT tokens

### Backend  
- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.9+
- **Database**: SQLite with SQLAlchemy ORM
- **AI/ML**: TensorFlow, OpenCV, scikit-learn
- **File Processing**: Pillow, BioPython
- **Real-time**: WebSockets
- **Authentication**: JWT with bcrypt hashing

## 📋 Features Implemented

### Phase 1: Core User Dashboard
- ✅ **Project Setup**: Next.js 14+ with TypeScript and Tailwind CSS
- ✅ **Root Layout**: TanStack Query Provider and Toaster integration
- ✅ **Dashboard Layout**: Persistent sidebar navigation
- ✅ **File Upload Component**: VCF/FASTQ genomic data upload with progress tracking
- ✅ **PRS Score Display**: Interactive polygenic risk score visualization
- ✅ **Recommendations Display**: Personalized health recommendations with priority levels

### Phase 2: Visualization & Advanced UI
- ✅ **PRS Chart**: Interactive bar chart comparing user scores to population averages
- ✅ **Results Timeline**: Chronological visualization of analysis events
- ✅ **Genome Browser**: D3.js-based conceptual chromosome visualization

### Phase 3: Portals, Settings, and Final Components
- ✅ **Doctor Portal**: Separate interface for healthcare professionals
- ✅ **Patient List**: Searchable table with risk assessment and status tracking
- ✅ **Consent Management**: Toggle switches for data sharing preferences
- ✅ **AI Chatbot**: Interactive genomics assistant with contextual responses

## 🎯 Key Components

### File Upload (`FileUpload`)
- Drag & drop interface for genomic files
- File validation (VCF, FASTQ formats)
- Upload progress tracking with TanStack Query mutations
- Success/error handling with toast notifications

### PRS Score Display (`PrsScoreDisplay`)
- Grid layout showing risk scores for multiple conditions
- Color-coded risk levels (low, moderate, high)
- Progress bars and percentile rankings
- Loading and error states

### Interactive Charts (`PrsChart`)
- Recharts bar chart comparing user scores to population averages
- Custom tooltips with detailed information
- Responsive design with proper legends
- Color coding based on risk levels

### AI Chatbot (`Chatbot`)
- Real-time chat interface with message history
- Context-aware responses based on genomic data
- Loading states and error handling
- Scrollable message area with timestamps

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Modern web browser

### Installation
```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Visit `http://localhost:3000` to view the application.

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## 🎨 Pages and Navigation

### Main Dashboard (`/dashboard`)
- Overview with file upload, PRS scores, and recommendations
- Quick access to all major features

### Visualizations (`/dashboard/visualizations`)
- PRS comparison charts
- Results timeline
- Genome browser visualization

### AI Assistant (`/dashboard/chatbot`)
- Interactive chatbot for genomic insights
- Context-aware responses about user's data

### Doctor Portal (`/doctor/dashboard`)
- Patient management interface
- Risk assessment overview
- Analysis status tracking

### Settings (`/dashboard/settings/consent`)
- Privacy and consent management
- Data sharing preferences

## 🔧 API Integration

All components use TanStack Query for data fetching. Replace mock functions with actual API calls:

```typescript
// Example: Replace mock function in prs-score-display.tsx
const fetchPrsScores = async (userId: string): Promise<PrsScore[]> => {
  const response = await fetch(`/api/prs/scores/user/${userId}`);
  return response.json();
};
```

## 🔮 Future Enhancements

- **Real-time Updates**: WebSocket integration for live data updates
- **Advanced Filtering**: Enhanced search and filter capabilities
- **Export Features**: PDF report generation and data export
- **Multi-language Support**: i18n implementation
- **Offline Mode**: Service worker for offline functionality

## 📚 Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [TanStack Query Guide](https://tanstack.com/query/latest)
- [shadcn/ui Components](https://ui.shadcn.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Recharts Documentation](https://recharts.org/en-US/)
- [D3.js Documentation](https://d3js.org/)

---

Built with ❤️ for advancing personalized healthcare through genomics.
