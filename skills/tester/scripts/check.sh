#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Step 1: Running pytest...${NC}"
uv run pytest test/

echo -e "\n${GREEN}Step 2: Running ty (type checking)...${NC}"
uv run ty check

echo -e "\n${GREEN}Step 3: Running ruff check...${NC}"
uv run ruff check

echo -e "\n${GREEN}Step 4: Running ruff format check...${NC}"
uv run ruff format --check

echo -e "\n${GREEN}All checks passed successfully!${NC}"
