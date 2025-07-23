# Paper Summary Agent

> AI-powered academic paper management system with multi-user support and intelligent summarization

## 🚀 Overview

Paper Summary Agent is a comprehensive platform that automates the process of discovering, summarizing, and managing academic papers. Built with modern technologies and powered by Gemini Flash 2.0, it helps researchers stay up-to-date with the latest developments in their fields of interest.

## ✨ Features

### 🤖 AI-Powered Summarization
- **Gemini Flash 2.0 Integration**: High-quality, fast summarization of academic papers
- **Structured Summaries**: Extracts key information including research questions, methods, innovations, and conclusions
- **Multi-language Support**: Automatic translation to Chinese for better accessibility

### 📧 Automated Paper Discovery
- **Email Integration**: Supports Gmail, QQ Mail, Outlook, and other IMAP providers
- **Google Scholar Alerts**: Automatically processes Google Scholar alert emails
- **Smart Parsing**: Extracts paper URLs and metadata from subscription emails

### 👥 Multi-User Management
- **Individual Accounts**: Each user has their own isolated workspace
- **Custom Keywords**: Define personal research interests and topics
- **Category Management**: Organize keywords into hierarchical categories

### 🔍 Advanced Search & Organization
- **Full-Text Search**: PostgreSQL-powered search across all paper content
- **Filtering Options**: Filter by date, category, read status, and custom tags
- **Annotation System**: Add personal notes, highlights, and bookmarks
- **Smart Recommendations**: AI-powered suggestions based on reading history

### 📱 Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Theme**: Comfortable reading in any lighting condition
- **shadcn/ui Components**: Beautiful, accessible, and consistent UI
- **Real-time Updates**: Live notifications for new papers and system updates

## 🛠 Technology Stack

### Backend
- **Framework**: FastAPI with Python 3.11
- **Database**: PostgreSQL 15 with full-text search
- **Cache & Queue**: Redis for caching and Celery for background tasks
- **AI Integration**: OpenRouter API with Gemini Flash 2.0
- **Authentication**: JWT tokens with refresh mechanism

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript for type safety
- **UI Library**: shadcn/ui with Tailwind CSS
- **State Management**: Zustand for client state
- **Data Fetching**: TanStack Query for server state

### Infrastructure
- **Containerization**: Docker and Docker Compose
- **Web Server**: Nginx reverse proxy
- **Monitoring**: Prometheus and Grafana
- **Package Management**: UV for Python dependencies

## 🚀 Quick Start

### Prerequisites
- **UV Package Manager**: For Python dependency management
- **Docker & Docker Compose**: For running services
- **Node.js 18+**: For frontend development

### Installation

1. **Install UV Package Manager**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.cargo/env
   ```

2. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd paper-agent
   ```

3. **Set Up Python Environment**
   ```bash
   uv venv --python 3.11
   source .venv/bin/activate
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start Services**
   ```bash
   docker-compose up -d
   ```

6. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📚 Documentation

- **[Implementation Plan](docs/Implementation-Plan.md)**: Detailed development roadmap
- **[API Documentation](http://localhost:8000/docs)**: Interactive API reference
- **[User Guide](docs/user-guide.md)**: Complete user manual
- **[Development Guide](docs/development.md)**: Setup and contribution guide

## 🔧 Development

### Backend Development

1. **Navigate to Backend Directory**
   ```bash
   cd backend
   ```

2. **Install Dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Run Database Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start Development Server**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Development

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

### Running Tests

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# E2E tests
npx playwright test
```

## 🗂 Project Structure

```
paper-agent/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Core functionality
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   └── tasks/             # Background tasks
│   ├── tests/                 # Backend tests
│   └── requirements.txt       # Python dependencies
├── frontend/                  # Next.js frontend application
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── lib/                   # Utilities and API client
│   └── package.json           # Node.js dependencies
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── legacy/                    # Original project files
└── docker-compose.yml         # Docker services
```

## 🌟 Key Features in Detail

### Smart Paper Processing Pipeline

1. **Email Monitoring**: Continuous monitoring of configured email accounts
2. **Link Extraction**: Intelligent parsing of academic paper URLs
3. **Content Scraping**: Full-text extraction using Firecrawl service
4. **AI Summarization**: Structured summarization using Gemini Flash 2.0
5. **Database Storage**: Efficient storage with search optimization
6. **User Notification**: Real-time updates on new papers

### Personalization Engine

- **Keyword Matching**: Papers are automatically categorized based on user-defined keywords
- **Reading History**: AI learns from user reading patterns
- **Smart Recommendations**: Personalized paper suggestions
- **Custom Categories**: Hierarchical organization system

### Advanced Search Capabilities

- **Full-Text Search**: Search across titles, abstracts, and summaries
- **Faceted Search**: Filter by multiple criteria simultaneously
- **Saved Searches**: Store and reuse complex search queries
- **Export Options**: Export search results in various formats

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Protection against abuse and DoS attacks
- **Data Encryption**: Sensitive data encrypted at rest
- **CORS Protection**: Secure cross-origin resource sharing
- **Input Validation**: Comprehensive input sanitization

## 📊 Monitoring & Analytics

- **System Metrics**: Comprehensive monitoring with Prometheus
- **User Analytics**: Reading patterns and usage statistics
- **Performance Tracking**: API response times and error rates
- **Cost Monitoring**: AI API usage and cost tracking

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Standards
- **Code Style**: Follow Black and ESLint configurations
- **Testing**: Maintain >80% test coverage
- **Documentation**: Update docs for new features
- **Type Safety**: Use TypeScript and Python type hints

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter**: For providing excellent AI model access
- **Firecrawl**: For reliable web scraping capabilities
- **shadcn/ui**: For beautiful and accessible UI components
- **FastAPI**: For the excellent Python web framework
- **Next.js**: For the powerful React framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/paper-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/paper-agent/discussions)
- **Email**: support@paper-agent.com

## 🚀 Roadmap

### Phase 1 (Current)
- [x] Core paper processing pipeline
- [x] Multi-user authentication system
- [x] Basic web interface
- [ ] Mobile responsive design

### Phase 2 (Next)
- [ ] Mobile applications (iOS/Android)
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard
- [ ] Integration with reference managers

### Phase 3 (Future)
- [ ] Multi-language support
- [ ] Advanced AI features
- [ ] API for third-party integrations
- [ ] Enterprise features

---

<div align="center">
  <p>Built with ❤️ using modern technologies</p>
  <p>
    <a href="#-overview">Overview</a> •
    <a href="#-features">Features</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-documentation">Documentation</a> •
    <a href="#-contributing">Contributing</a>
  </p>
</div>