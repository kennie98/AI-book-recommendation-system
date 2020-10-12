#!/bin/bash

YELLOW='\033[1;33m'
GREEN='\033[1;32m'
NC='\033[0m' # No Color

print_header() {
  echo -e "${YELLOW}$1${NC}"
}

print_info() {
  echo -e "${GREEN}$1${NC}"
}
