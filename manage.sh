#!/bin/bash

#!/bin/bash
# manage.sh - Management script for YTBridge
# Usage: ./manage.sh [command]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Use docker-compose or docker compose
DOCKER_COMPOSE="docker-compose"
if ! command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
fi

# Functions
show_help() {
    echo -e "${CYAN}🌉 YTBridge - Management Script${NC}"
    echo ""
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo -e "${GREEN}Available commands:${NC}"
    echo ""
    echo "  start          Start all services"
    echo "  stop           Stop all services"
    echo "  restart        Restart all services"
    echo "  status         Show services status"
    echo "  logs           Show all logs (follow mode)"
    echo "  logs-api       Show API logs only"
    echo "  logs-redis     Show Redis logs only"
    echo "  build          Build/rebuild images"
    echo "  clean          Stop and remove containers, networks, volumes"
    echo "  shell-api      Open shell in API container"
    echo "  shell-redis    Open Redis CLI"
    echo "  test           Run API health check and basic tests"
    echo "  monitor        Monitor container stats"
    echo "  dev            Start in development mode (hot reload)"
    echo "  prod           Start in production mode"
    echo "  help           Show this help message"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./manage.sh start"
    echo "  ./manage.sh logs"
    echo "  ./manage.sh test"
    echo ""
}

start_services() {
    echo -e "${YELLOW}🚀 Starting services...${NC}"
    $DOCKER_COMPOSE up -d
    echo -e "${GREEN}✅ Services started${NC}"
    echo ""
    $DOCKER_COMPOSE ps
}

stop_services() {
    echo -e "${YELLOW}⏸️  Stopping services...${NC}"
    $DOCKER_COMPOSE down
    echo -e "${GREEN}✅ Services stopped${NC}"
}

restart_services() {
    echo -e "${YELLOW}🔄 Restarting services...${NC}"
    $DOCKER_COMPOSE restart
    echo -e "${GREEN}✅ Services restarted${NC}"
}

show_status() {
    echo -e "${CYAN}📊 Services Status:${NC}"
    $DOCKER_COMPOSE ps
}

show_logs() {
    echo -e "${CYAN}📋 Showing logs (Ctrl+C to exit)...${NC}"
    $DOCKER_COMPOSE logs -f
}

show_logs_api() {
    echo -e "${CYAN}📋 Showing API logs (Ctrl+C to exit)...${NC}"
    $DOCKER_COMPOSE logs -f youtube-api
}

show_logs_redis() {
    echo -e "${CYAN}📋 Showing Redis logs (Ctrl+C to exit)...${NC}"
    $DOCKER_COMPOSE logs -f youtube-api-redis
}

build_images() {
    echo -e "${YELLOW}🔨 Building images...${NC}"
    $DOCKER_COMPOSE build --no-cache
    echo -e "${GREEN}✅ Build completed${NC}"
}

clean_all() {
    echo -e "${YELLOW}🧹 Cleaning up...${NC}"
    read -p "This will remove all containers, networks, and volumes. Continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        $DOCKER_COMPOSE down -v
        echo -e "${GREEN}✅ Cleanup completed${NC}"
    else
        echo -e "${YELLOW}Cancelled${NC}"
    fi
}

shell_api() {
    echo -e "${CYAN}🐚 Opening shell in API container...${NC}"
    $DOCKER_COMPOSE exec youtube-api bash
}

shell_redis() {
    echo -e "${CYAN}💾 Opening Redis CLI...${NC}"
    $DOCKER_COMPOSE exec youtube-api-redis redis-cli
}

run_tests() {
    echo -e "${CYAN}🧪 Running tests...${NC}"
    echo ""
    
    # Health check
    echo -e "${YELLOW}1. Health Check:${NC}"
    if curl -sf http://localhost:8000/api/v1/health > /dev/null; then
        echo -e "   ${GREEN}✅ API is healthy${NC}"
    else
        echo -e "   ${RED}❌ API is not responding${NC}"
        return 1
    fi
    
    # Search test
    echo -e "${YELLOW}2. Search Test:${NC}"
    if curl -sf "http://localhost:8000/api/v1/search/?q=Python&max_results=1" > /dev/null; then
        echo -e "   ${GREEN}✅ Search endpoint working${NC}"
    else
        echo -e "   ${RED}❌ Search endpoint failed${NC}"
        return 1
    fi
    
    # Redis test
    echo -e "${YELLOW}3. Redis Test:${NC}"
    if $DOCKER_COMPOSE exec -T youtube-api-redis redis-cli ping | grep -q "PONG"; then
        echo -e "   ${GREEN}✅ Redis is responding${NC}"
    else
        echo -e "   ${RED}❌ Redis is not responding${NC}"
        return 1
    fi
    
    echo ""
    echo -e "${GREEN}✅ All tests passed!${NC}"
}

monitor_stats() {
    echo -e "${CYAN}📊 Monitoring container stats (Ctrl+C to exit)...${NC}"
    docker stats
}

start_dev() {
    echo -e "${YELLOW}🔧 Starting in development mode...${NC}"
    $DOCKER_COMPOSE -f docker-compose.yml -f docker-compose.dev.yml up -d
    echo -e "${GREEN}✅ Development mode started${NC}"
    echo ""
    echo -e "${CYAN}🔗 Access URLs:${NC}"
    echo -e "   API:   ${GREEN}http://localhost:8000${NC}"
    echo -e "   Docs:  ${GREEN}http://localhost:8000/api/v1/docs${NC}"
    echo -e "   Redis Commander: ${GREEN}http://localhost:8081${NC}"
}

start_prod() {
    echo -e "${YELLOW}🚀 Starting in production mode...${NC}"
    $DOCKER_COMPOSE up -d
    echo -e "${GREEN}✅ Production mode started${NC}"
}

# Main script
case "${1:-help}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    logs-api)
        show_logs_api
        ;;
    logs-redis)
        show_logs_redis
        ;;
    build)
        build_images
        ;;
    clean)
        clean_all
        ;;
    shell-api)
        shell_api
        ;;
    shell-redis)
        shell_redis
        ;;
    test)
        run_tests
        ;;
    monitor)
        monitor_stats
        ;;
    dev)
        start_dev
        ;;
    prod)
        start_prod
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
