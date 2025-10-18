#!/bin/bash

# monitor.sh - Real-time monitoring for YouTube API
# Usage: ./monitor.sh

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

REFRESH_INTERVAL=5

# Use docker-compose or docker compose
DOCKER_COMPOSE="docker-compose"
if ! command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
fi

show_dashboard() {
    while true; do
        clear
        
        echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${CYAN}║  YouTube API - Real-time Monitoring Dashboard         ║${NC}"
        echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
        echo -e "$(date '+%Y-%m-%d %H:%M:%S') | Refresh: ${REFRESH_INTERVAL}s | Press Ctrl+C to exit"
        echo ""
        
        # Service Status
        echo -e "${GREEN}┌─ 📡 Service Status${NC}"
        $DOCKER_COMPOSE ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null
        
        echo ""
        
        # Container Stats
        echo -e "${GREEN}├─ 📊 Resource Usage${NC}"
        docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | head -n 3
        
        echo ""
        
        # API Health
        echo -e "${GREEN}├─ 🏥 API Health Check${NC}"
        HEALTH_RESPONSE=$(curl -sf http://localhost:8000/api/v1/health 2>/dev/null)
        if [ $? -eq 0 ]; then
            STATUS=$(echo $HEALTH_RESPONSE | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
            CACHE_TYPE=$(echo $HEALTH_RESPONSE | grep -o '"cache_type":"[^"]*"' | cut -d'"' -f4)
            CACHE_AVAILABLE=$(echo $HEALTH_RESPONSE | grep -o '"cache_available":[^,}]*' | cut -d':' -f2)
            
            echo -e "   Status: ${GREEN}${STATUS}${NC}"
            echo -e "   Cache Type: ${CACHE_TYPE}"
            echo -e "   Cache Available: ${CACHE_AVAILABLE}"
        else
            echo -e "   ${RED}⚠️  API not responding${NC}"
        fi
        
        echo ""
        
        # Redis Stats
        echo -e "${GREEN}└─ 💾 Redis Statistics${NC}"
        REDIS_INFO=$($DOCKER_COMPOSE exec -T youtube-api-redis redis-cli INFO stats 2>/dev/null)
        if [ $? -eq 0 ]; then
            COMMANDS=$(echo "$REDIS_INFO" | grep "total_commands_processed:" | cut -d':' -f2 | tr -d '\r')
            HITS=$(echo "$REDIS_INFO" | grep "keyspace_hits:" | cut -d':' -f2 | tr -d '\r')
            MISSES=$(echo "$REDIS_INFO" | grep "keyspace_misses:" | cut -d':' -f2 | tr -d '\r')
            
            if [ ! -z "$HITS" ] && [ ! -z "$MISSES" ]; then
                TOTAL=$((HITS + MISSES))
                if [ $TOTAL -gt 0 ]; then
                    HIT_RATE=$(awk "BEGIN {printf \"%.2f\", ($HITS / $TOTAL) * 100}")
                else
                    HIT_RATE="0.00"
                fi
            else
                HIT_RATE="N/A"
            fi
            
            echo -e "   Total Commands: ${COMMANDS:-N/A}"
            echo -e "   Cache Hits: ${HITS:-N/A}"
            echo -e "   Cache Misses: ${MISSES:-N/A}"
            echo -e "   Hit Rate: ${HIT_RATE}%"
        else
            echo -e "   ${RED}⚠️  Redis not responding${NC}"
        fi
        
        echo ""
        echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
        echo -e "Commands: ${YELLOW}Ctrl+C${NC} (Exit) | ${YELLOW}./manage.sh${NC} (Management)"
        echo ""
        
        sleep $REFRESH_INTERVAL
    done
}

# Run dashboard
show_dashboard
