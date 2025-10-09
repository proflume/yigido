#!/bin/bash
# Frontend development helper script

set -e

case "$1" in
  setup)
    echo "Setting up frontend..."
    npm install
    cp .env.local.example .env.local
    echo "Setup complete! Edit .env.local and run './frontend.sh dev'"
    ;;
  
  dev)
    echo "Starting development server..."
    npm run dev
    ;;
  
  build)
    echo "Building for production..."
    npm run build
    ;;
  
  start)
    echo "Starting production server..."
    npm run start
    ;;
  
  test)
    echo "Running tests..."
    npm test
    ;;
  
  lint)
    echo "Running linter..."
    npm run lint
    ;;
  
  type-check)
    echo "Running type checker..."
    npm run type-check
    ;;
  
  *)
    echo "Usage: ./frontend.sh {setup|dev|build|start|test|lint|type-check}"
    exit 1
    ;;
esac
