#!/bin/bash
# Unix shell script for running pyqt-mvvm-example management scripts
# Usage: ./run.sh [script] [command] [args...]

if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh [script] [command] [args...]"
    echo ""
    echo "Available scripts:"
    echo "  dev     - Development utilities"
    echo "  build   - Build utilities"
    echo "  setup   - Setup utilities"
    echo "  deploy  - Deployment utilities"
    echo "  clean   - Cleanup utilities"
    echo "  check   - Health check utilities"
    echo ""
    echo "Examples:"
    echo "  ./run.sh dev check-all"
    echo "  ./run.sh setup all --dev"
    echo "  ./run.sh build exe"
    echo "  ./run.sh clean all"
    echo "  ./run.sh check all"
    exit 1
fi

python scripts/run.py "$@" 