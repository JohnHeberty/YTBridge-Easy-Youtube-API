#!/bin/bash

# start.sh - Quick start script for YouTube API
# This script builds and starts the API + Redis containers

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════╗"
echo "║       YouTube API - Quick Start                ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    echo "   https://docs.docker.com/engine/install/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

# Use docker-compose or docker compose
DOCKER_COMPOSE="docker-compose"
if ! command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
fi

echo -e "${YELLOW}🔍 Checking Docker daemon...${NC}"
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running. Please start Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is running${NC}\n"

# Build images
echo -e "${YELLOW}🔨 Building Docker images...${NC}"
$DOCKER_COMPOSE build

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed. Check the error messages above.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build completed${NC}\n"

# Start services
echo -e "${YELLOW}🚀 Starting services (API + Redis)...${NC}"
$DOCKER_COMPOSE up -d

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start services. Check the error messages above.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Services started${NC}\n"

# Wait for health checks
echo -e "${YELLOW}⏳ Waiting for services to be healthy (max 60s)...${NC}"

MAX_WAIT=60
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
    API_HEALTH=$($DOCKER_COMPOSE ps youtube-api 2>/dev/null | grep -c "healthy" || echo "0")
    
    if [ "$API_HEALTH" -gt 0 ]; then
        echo -e "${GREEN}✅ API is healthy!${NC}\n"
        break
    fi
    
    echo -e "   Waiting... ${ELAPSED}s"
    sleep 5
    ELAPSED=$((ELAPSED + 5))
done

if [ $ELAPSED -ge $MAX_WAIT ]; then
    echo -e "${RED}⚠️  Health check timeout. Services may still be starting...${NC}"
    echo -e "${YELLOW}   Check status with: ./manage.sh status${NC}\n"
fi

# Show service status
echo -e "${CYAN}📊 Service Status:${NC}"
$DOCKER_COMPOSE ps

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🎉 YTBridge is ready!                        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}🔗 Access URLs:${NC}"
echo -e "   API:   ${GREEN}http://localhost:8000${NC}"
echo -e "   Docs:  ${GREEN}http://localhost:8000/api/v1/docs${NC}"
echo -e "   Health: ${GREEN}http://localhost:8000/api/v1/health${NC}"
echo ""
echo -e "${CYAN}📊 Useful commands:${NC}"
echo -e "   ./manage.sh logs     - View logs"
echo -e "   ./manage.sh status   - Check status"
echo -e "   ./manage.sh stop     - Stop services"
echo -e "   ./manage.sh restart  - Restart services"
echo ""
echo -e "${YELLOW}📚 Documentation: docs/QUICK-START.md${NC}"
echo ""
