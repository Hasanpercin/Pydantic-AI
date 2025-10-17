# 🌟 AstraCalc Agent Server

AI-powered astrology assistant backend using Pydantic AI + FastAPI + Calculation Engine.

## 📊 Current Status: **Level 2** ✅

**Level 2: Calculation Engine + N8N Integration**
- ✅ FastAPI server running
- ✅ Pydantic AI agent with async support
- ✅ Claude Sonnet 4.5 integration
- ✅ Basic chat endpoint
- ✅ **Tools: 3 active tools** (get_current_date, get_sun_sign, generate_chart_report)
- ✅ **Calculation Engine integration** (Sun sign calculations)
- ✅ **N8N Webhook** (Full chart reports)
- ⏳ Memory (coming in Level 3)
- ⏳ Redis Cache (coming in Level 5)
- ⏳ WebSocket (coming in Level 4)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Anthropic API key
- Calculation Engine URL (optional for testing)

### Local Development

1. **Clone and setup:**
```bash
git clone https://github.com/Hasanpercin/Pydantic-AI.git
cd Pydantic-AI
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
  -d '{"message": "Merhaba! Güneşim hangi burçta?"}'
```

## 🏗️ Architecture

```
┌─────────────────────────────┐
│   FastAPI Server            │
│   (main.py)                 │
├─────────────────────────────┤
│   Pydantic AI Agent         │
│   (agent.py)                │
│   - 3 Active Tools          │
├─────────────────────────────┤
│   External Services         │
│   ├── Claude Sonnet 4.5     │
│   ├── Calculation Engine    │
│   └── N8N Webhooks          │
└─────────────────────────────┘
```

## 📁 Project Structure

```
Pydantic-AI/
├── main.py                  # FastAPI application
├── agent.py                 # Pydantic AI agent with tools
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Multi-container setup
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment variables
├── tools/                   # Agent tools directory
│   ├── __init__.py
│   ├── basic.py            # Basic tools (get_current_date)
│   ├── calculation.py      # Calculation Engine integration
│   └── report.py           # N8N webhook integration
└── README.md               # This file
```

## 🛠️ Agent Tools (Level 2)

### 1. get_current_date
**Purpose:** Get current date in Turkish format.

**Usage:**
- "Bugün hangi gün?"
- "Tarih nedir?"

**Response:** "Bugün 17 Ekim 2025 Cuma"

---

### 2. get_sun_sign ⭐ NEW
**Purpose:** Calculate user's sun sign using Calculation Engine.

**Required Parameters:**
- `year`: Birth year (e.g., 1990)
- `month`: Birth month (1-12)
- `day`: Birth day (1-31)
- `hour`: Birth hour (0-23)
- `minute`: Birth minute (0-59)
- `tz_offset`: UTC offset (default: 3.0 for Istanbul)

**Usage:**
- "Güneşim hangi burçta?"
- "Burcum ne?"
- "1990-03-15 saat 14:30'da doğdum, burcum ne?"

**Response Example:**
```
🌞 Güneş Burcunuz: Balık

📊 Detaylar:
- Derece: 354°
- UTC Zaman: 1990-03-15T11:30:00Z

Balık burcu, sizin temel karakterinizi ve ego yapınızı temsil eder.
```

**Integration:** Connects to Calculation Engine API via `CALC_ENGINE_URL`.

---

### 3. generate_chart_report ⭐ NEW
**Purpose:** Generate full natal chart report via N8N webhook.

**Required Parameters:**
- `year`: Birth year
- `month`: Birth month
- `day`: Birth day
- `hour`: Birth hour
- `minute`: Birth minute
- `tz_offset`: UTC offset (default: 3.0)

**Usage:**
- "Doğum haritamı çıkar"
- "Tam rapor istiyorum"
- "Detaylı analiz yap"

**Response:** Full astrological chart report with all planets, houses, and aspects.

**Integration:** Sends data to N8N webhook via `N8N_WEBHOOK_URL`.

---

## 🔧 Configuration

Key environment variables (see `.env.example`):

```env
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxx
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
ANTHROPIC_MODEL_FAST=claude-haiku-4

# Calculation Engine (Level 2)
CALC_ENGINE_URL=https://engine.hasanpercin.xyz
CALC_ENGINE_API_KEY=testkey

# N8N Webhook (Level 2)
N8N_WEBHOOK_URL=https://n8n.hasanpercin.xyz/webhook/c33b37b1-46ef-4cd2-807c-594a3f329719

# Optional
ENVIRONMENT=production
PORT=8585
LOG_LEVEL=INFO
CORS_ORIGINS=* 
```

## 📡 API Endpoints

### GET /
Root endpoint, returns service info.

**Response:**
```json
{
  "service": "AstraCalc Agent Server",
  "version": "0.1.0",
  "status": "running"
}
```

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
Chat with the AI agent (async).

**Request:**
```json
{
  "message": "Güneşim hangi burçta? 1990-03-15 14:30'da doğdum.",
  "user_id": "optional-user-id"
}
```

**Response:**
```json
{
  "response": "🌞 Güneş Burcunuz: Balık\n\n📊 Detaylar:\n- Derece: 354°\n- UTC Zaman: 1990-03-15T11:30:00Z\n\nBalık burcu, sizin temel karakterinizi ve ego yapınızı temsil eder.",
  "model": "claude-sonnet-4-5-20250929"
}
```

## 🐳 Deployment (Dokploy)

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Level 2: Calculation Engine + N8N Integration"
git push origin main
```

### Step 2: Dokploy Setup

1. **Create Application:**
   - Go to Dokploy Dashboard
   - Applications → New Application
   - Name: `astrocalc-agent-server`

2. **Connect GitHub:**
   - Source: GitHub
   - Repository: `Hasanpercin/Pydantic-AI`
   - Branch: `main`

3. **Build Configuration:**
   - Build Type: Dockerfile
   - Dockerfile Path: `./Dockerfile`
   - Build Context: `.`

4. **Environment Variables:**
   ```
   ANTHROPIC_API_KEY=your-key
   ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
   ANTHROPIC_MODEL_FAST=claude-haiku-4
   ENVIRONMENT=production
   PORT=8585
   LOG_LEVEL=INFO
   
   # Calculation Engine
   CALC_ENGINE_URL=https://engine.hasanpercin.xyz
   CALC_ENGINE_API_KEY=testkey
   
   # N8N Webhook
   N8N_WEBHOOK_URL=https://n8n.hasanpercin.xyz/webhook/xxx
   
   # Redis (Level 5)
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
   - CPU: `0.5-1.0` core
   - Memory: `512-1024` MB

9. **Deploy!**

### Step 3: Verify Deployment

```bash
# Health check
curl https://agent.yourdomain.com/health

# Chat test with tool calling
curl -X POST https://agent.yourdomain.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Güneşim hangi burçta? 1990-03-15 14:30 İstanbul"}'
```

## 🧪 Testing

### Manual Testing
```bash
# Test agent directly
python agent.py

# Test API with date tool
curl -X POST http://localhost:8585/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bugün hangi gün?"}'

# Test API with sun sign calculation
curl -X POST http://localhost:8585/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "1990-03-15 14:30 İstanbul doğumluyum, güneşim hangi burçta?"}'

# Test API with full report
curl -X POST http://localhost:8585/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Doğum haritamı çıkar: 1990-03-15 14:30 İstanbul"}'
```

### Expected Responses

**Date Query:**
```json
{
  "response": "Bugün 17 Ekim 2025 Cuma",
  "model": "claude-sonnet-4-5-20250929"
}
```

**Sun Sign Query:**
```json
{
  "response": "🌞 Güneş Burcunuz: Balık\n\n📊 Detaylar:\n- Derece: 354°\n- UTC Zaman: 1990-03-15T11:30:00Z\n\nBalık burcu, sizin temel karakterinizi ve ego yapınızı temsil eder.",
  "model": "claude-sonnet-4-5-20250929"
}
```

## 📈 Development Roadmap

### ✅ Level 0: Hello World Agent (COMPLETED)
- FastAPI server
- Pydantic AI agent
- Claude Sonnet 4 integration
- Basic chat endpoint

### ✅ Level 1: First Tool (COMPLETED)
- `get_current_date()` tool
- Tool calling implementation
- Response contextualization

### ✅ Level 2: Calculation Engine (COMPLETED - CURRENT)
- Connect to Calculation Engine API
- Real astrology calculations
- Sun sign tool
- N8N webhook integration for reports
- 3 active tools

### ⏳ Level 3: Zep Memory (NEXT)
- Conversation history
- User context preservation
- Fact extraction
- Personalized responses

### ⏳ Level 4: WebSocket (AG-UI)
- Real-time communication
- Streaming responses
- Mobile app integration
- Socket.IO implementation

### ⏳ Level 5: Redis Cache
- Response caching
- Performance optimization
- Session management

### ⏳ Level 6: Intent Classification
- User intent detection
- Smart routing
- Multi-model strategy

## 🔍 Key Features (Level 2)

### Async Agent Support
- Full async/await implementation
- Non-blocking operations
- Better performance for concurrent requests

### Tool System
- 3 registered tools
- Automatic tool selection by AI
- Smart parameter extraction
- Error handling and logging

### External Integrations
1. **Calculation Engine:** Real astronomical calculations
2. **N8N Workflows:** Complex report generation
3. **Claude Sonnet 4.5:** Advanced language understanding

### System Prompt Engineering
- Detailed tool usage guidelines
- Clear decision rules
- Empathetic communication style
- Turkish language support

## 🐛 Troubleshooting

### Issue: "ANTHROPIC_API_KEY not configured"
**Solution:** Make sure `.env` file has valid API key.

### Issue: Docker build fails
**Solution:** Check Docker daemon is running and requirements.txt is correct.

### Issue: Agent returns empty response
**Solution:** Check logs: `docker-compose logs -f agent-server`

### Issue: Health check fails
**Solution:** Verify port 8585 is not in use: `lsof -i :8585`

### Issue: Calculation Engine timeout
**Solution:** 
- Verify `CALC_ENGINE_URL` is correct
- Check API key is valid
- Test engine endpoint directly

### Issue: N8N webhook not working
**Solution:**
- Verify `N8N_WEBHOOK_URL` is correct
- Check webhook is active in N8N
- Test webhook with curl

## 📝 Logs

View logs in real-time:
```bash
# Docker Compose
docker-compose logs -f agent-server

# Filter by level
docker-compose logs -f agent-server | grep ERROR

# Dokploy
# Dashboard → Application → Logs tab
```

## 🔒 Security

- ✅ API keys in environment variables
- ✅ CORS configured
- ✅ No sensitive data in git
- ✅ HTTPS in production (via Dokploy)
- ✅ Input validation via Pydantic
- ⏳ Rate limiting (coming soon)
- ⏳ Authentication (coming soon)

## 🎯 Performance Tips

1. **Use Fast Model for Simple Queries:**
   - Set `ANTHROPIC_MODEL_FAST=claude-haiku-4`
   - Switch based on query complexity

2. **Cache Calculation Results:**
   - Implement Redis caching (Level 5)
   - Reduce API calls to Calculation Engine

3. **Async Everything:**
   - All tools use async/await
   - Non-blocking I/O operations

4. **Monitor with Logfire:**
   - Set `LOGFIRE_API_KEY` for monitoring
   - Track performance metrics

## 📚 Resources

- [Pydantic AI Docs](https://ai.pydantic.dev/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Dokploy Docs](https://dokploy.com/docs)
- [Redis Docs](https://redis.io/docs/)

## 🤝 Contributing

This is a private project. For questions or contributions, contact [@Hasanpercin](https://github.com/Hasanpercin).

## 📄 License

Private project - All rights reserved.

---

**Current Version:** 0.1.0 (Level 2)  
**Last Updated:** 2025-01-17  
**Status:** 🟢 Production Ready (Level 2)  
**Active Tools:** 3 (get_current_date, get_sun_sign, generate_chart_report)