# 🌟 AstraCalc Agent Server

AI-powered astrology assistant backend using Pydantic AI + FastAPI.

## 📊 Current Status: **Level 0** ✅

**Level 0: Hello World Agent**
- ✅ FastAPI server running
- ✅ Pydantic AI agent working
- ✅ Claude Sonnet 4 integration
- ✅ Basic chat endpoint
- ❌ Tools (coming in Level 1)
- ❌ Memory (coming in Level 3)
- ❌ WebSocket (coming in Level 4)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Anthropic API key

### Local Development

1. **Clone and setup:**
```bash
git clone https://github.com/yourusername/agent-server.git
cd agent-server
```

2. **Create .env file:**
```bash
cp .env.example .env
# Edit .env with your keys
```

3. **Run with Docker Compose:**
```bash
docker-compose up --build
```

4. **Test the API:**
```bash
# Health check
curl http://localhost:8585/health

# Chat
curl -X POST http://localhost:8585/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Merhaba!"}'
```

## 🏗️ Architecture

```
┌─────────────────────────┐
│   FastAPI Server        │
│   (main.py)             │
├─────────────────────────┤
│   Pydantic AI Agent     │
│   (agent.py)            │
├─────────────────────────┤
│   Claude Sonnet 4       │
│   (Anthropic API)       │
└─────────────────────────┘
```

## 📁 Project Structure

```
agent-server/
├── main.py              # FastAPI application
├── agent.py             # Pydantic AI agent
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Multi-container setup
├── .env                 # Environment variables (not in git)
└── README.md            # This file
```

## 🔧 Configuration

Key environment variables (see `.env.example`):

```env
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxx
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Optional
ENVIRONMENT=production
PORT=8585
LOG_LEVEL=INFO
```

## 📡 API Endpoints

### GET /
Root endpoint, returns service info.

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "production"
}
```

### POST /chat
Chat with the AI agent.

**Request:**
```json
{
  "message": "Bugün nasıl bir gün?",
  "user_id": "optional-user-id"
}
```

**Response:**
```json
{
  "response": "Bugün Ay Balık burcunda...",
  "model": "claude-sonnet-4-20250514"
}
```

## 🐳 Deployment (Dokploy)

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Level 0: Hello World Agent"
git push origin main
```

### Step 2: Dokploy Setup

1. **Create Application:**
   - Go to Dokploy Dashboard
   - Applications → New Application
   - Name: `astrocalc-agent-server`

2. **Connect GitHub:**
   - Source: GitHub
   - Repository: `agent-server`
   - Branch: `main`

3. **Build Configuration:**
   - Build Type: Dockerfile
   - Dockerfile Path: `./Dockerfile`
   - Build Context: `.`

4. **Environment Variables:**
   ```
   ANTHROPIC_API_KEY=your-key
   ANTHROPIC_MODEL=claude-sonnet-4-20250514
   ENVIRONMENT=production
   PORT=8585
   LOG_LEVEL=INFO
   REDIS_URL=redis://:password@astrocalc-redis:6379/0
   ```

5. **Port Mapping:**
   - Container Port: `8585`
   - Public Port: `8585` (or auto)

6. **Domain (Optional):**
   - Custom domain: `agent.yourdomain.com`
   - SSL: Auto (Let's Encrypt)

7. **Health Check:**
   - Endpoint: `/health`
   - Interval: `30s`

8. **Resources:**
   - CPU: `0.5` core
   - Memory: `512` MB

9. **Deploy!**

### Step 3: Verify Deployment

```bash
# Health check
curl https://agent.yourdomain.com/health

# Chat test
curl -X POST https://agent.yourdomain.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Merhaba!"}'
```

## 🧪 Testing

### Manual Testing
```bash
# Test locally
python agent.py

# Test API
curl -X POST http://localhost:8585/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Güneşim hangi burçta?"}'
```

### Expected Response
```json
{
  "response": "Merhaba! Ben AstraCalc AI. Size astroloji konularında yardımcı olabilirim. Güneşinizin hangi burçta olduğunu öğrenmek için doğum tarihinizi söyler misiniz?",
  "model": "claude-sonnet-4-20250514"
}
```

## 📈 Next Levels

### Level 1: First Tool ⏳
- Add `get_current_date()` tool
- Tool calling implementation
- Response contextualization

### Level 2: Calculation Engine ⏳
- Connect to Calculation Engine API
- Real astrology data
- Natal chart calculations

### Level 3: Zep Memory ⏳
- Conversation history
- User context
- Fact extraction

### Level 4: WebSocket (AG-UI) ⏳
- Real-time communication
- Streaming responses
- Mobile app integration

### Level 5: Redis Cache ⏳
- Response caching
- Performance optimization

### Level 6: Intent Classification ⏳
- User intent detection
- Smart routing

## 🐛 Troubleshooting

### Issue: "ANTHROPIC_API_KEY not configured"
**Solution:** Make sure `.env` file has valid API key.

### Issue: Docker build fails
**Solution:** Check Docker daemon is running and requirements.txt is correct.

### Issue: Agent returns empty response
**Solution:** Check logs: `docker-compose logs agent-server`

### Issue: Health check fails
**Solution:** Verify port 8585 is not in use: `lsof -i :8585`

## 📝 Logs

View logs in real-time:
```bash
# Docker Compose
docker-compose logs -f agent-server

# Dokploy
# Dashboard → Application → Logs tab
```

## 🔒 Security

- ✅ API keys in environment variables
- ✅ CORS configured
- ✅ No sensitive data in git
- ✅ HTTPS in production (via Dokploy)
- ⏳ Rate limiting (coming soon)
- ⏳ Authentication (coming soon)

## 📚 Resources

- [Pydantic AI Docs](https://ai.pydantic.dev/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Dokploy Docs](https://dokploy.com/docs)

## 📄 License

Private project - All rights reserved.

## 🤝 Contributing

This is a private project. For questions, contact the team.

---

**Current Version:** 0.1.0 (Level 0)  
**Last Updated:** 2025-01-09
