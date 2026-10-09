#!/bin/bash

# File Comparison System Runner Script
# For macOS and Linux

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}=== $1 ===${NC}"
}

print_command() {
    echo -e "${CYAN}[COMMAND]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# PID file for tracking processes
PID_FILE="$SCRIPT_DIR/.pids"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to cleanup processes
cleanup() {
    print_status "Cleaning up processes..."

    if [[ -f "$PID_FILE" ]]; then
        while IFS= read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                print_status "Stopping process $pid"
                kill "$pid" 2>/dev/null || true
                sleep 1
                if kill -0 "$pid" 2>/dev/null; then
                    print_warning "Force killing process $pid"
                    kill -9 "$pid" 2>/dev/null || true
                fi
            fi
        done < "$PID_FILE"
        rm -f "$PID_FILE"
    fi

    print_status "Cleanup completed!"
}

# Function to handle signals
signal_handler() {
    echo -e "\n${YELLOW}Received interrupt signal${NC}"
    cleanup
    exit 0
}

# Setup signal handlers
trap signal_handler SIGINT SIGTERM

# Function to check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check directories
    if [[ ! -d "$BACKEND_DIR" ]]; then
        print_error "Backend directory not found: $BACKEND_DIR"
        return 1
    fi

    if [[ ! -d "$FRONTEND_DIR" ]]; then
        print_error "Frontend directory not found: $FRONTEND_DIR"
        return 1
    fi

    # Check virtual environment
    if [[ ! -d "$BACKEND_DIR/venv" ]]; then
        print_error "Virtual environment not found"
        print_status "Please create virtual environment first:"
        print_command "cd $BACKEND_DIR"
        print_command "python3 -m venv venv"
        print_command "source venv/bin/activate"
        print_command "pip install -r requirements.txt"
        return 1
    fi

    # Check required files
    if [[ ! -f "$BACKEND_DIR/main.py" ]]; then
        print_error "Backend main file not found: $BACKEND_DIR/main.py"
        return 1
    fi

    if [[ ! -f "$FRONTEND_DIR/index.html" ]]; then
        print_error "Frontend index file not found: $FRONTEND_DIR/index.html"
        return 1
    fi

    print_status "All prerequisites check passed!"
    return 0
}

# Function to run tests
run_tests() {
    print_header "Running Tests"

    cd "$BACKEND_DIR"

    # Activate virtual environment
    source venv/bin/activate

    test_files=("test_sample_processing.py" "test_sample_files.py")
    all_passed=true

    for test_file in "${test_files[@]}"; do
        if [[ -f "$test_file" ]]; then
            print_status "Running $test_file..."
            if python "$test_file"; then
                print_status "✅ $test_file passed"
            else
                print_error "❌ $test_file failed"
                all_passed=false
            fi
        else
            print_warning "⚠️ Test file not found: $test_file"
        fi
    done

    if [[ "$all_passed" == true ]]; then
        print_status "✅ All tests passed!"
        return 0
    else
        print_error "❌ Some tests failed"
        if [[ "$SKIP_TESTS" != "true" ]]; then
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                return 1
            fi
        fi
        return 0
    fi
}

# Function to start backend
start_backend() {
    print_status "Starting backend server..."
    cd "$BACKEND_DIR"

    # Activate virtual environment
    source venv/bin/activate

    # Start backend in background
    python main.py > "$SCRIPT_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!

    # Save PID
    echo "$BACKEND_PID" >> "$PID_FILE"

    print_status "Backend started with PID: $BACKEND_PID"
    print_status "Backend URL: http://localhost:8000"
    print_status "API Docs: http://localhost:8000/docs"

    # Wait a bit for backend to start
    sleep 2

    # Check if backend is running
    if kill -0 "$BACKEND_PID" 2>/dev/null; then
        print_status "✅ Backend is running"
    else
        print_error "❌ Backend failed to start"
        if [[ -f "$SCRIPT_DIR/backend.log" ]]; then
            print_error "Backend logs:"
            tail -10 "$SCRIPT_DIR/backend.log"
        fi
        return 1
    fi

    return 0
}

# Function to start frontend
start_frontend() {
    print_status "Starting frontend server..."
    cd "$FRONTEND_DIR"

    # Try different servers
    if command_exists python3; then
        print_command "python3 -m http.server 3000"
        python3 -m http.server 3000 > "$SCRIPT_DIR/frontend.log" 2>&1 &
        FRONTEND_PID=$!
    elif command_exists python; then
        print_command "python -m http.server 3000"
        python -m http.server 3000 > "$SCRIPT_DIR/frontend.log" 2>&1 &
        FRONTEND_PID=$!
    elif command_exists npx; then
        print_command "npx http-server -p 3000"
        npx http-server -p 3000 > "$SCRIPT_DIR/frontend.log" 2>&1 &
        FRONTEND_PID=$!
    elif command_exists php; then
        print_command "php -S localhost:3000"
        php -S localhost:3000 > "$SCRIPT_DIR/frontend.log" 2>&1 &
        FRONTEND_PID=$!
    else
        print_error "No suitable frontend server found"
        print_status "Please install one of: Python 3, Node.js, or PHP"
        return 1
    fi

    # Save PID
    echo "$FRONTEND_PID" >> "$PID_FILE"

    print_status "Frontend started with PID: $FRONTEND_PID"
    print_status "Frontend URL: http://localhost:3000"

    # Wait a bit for frontend to start
    sleep 2

    # Check if frontend is running
    if kill -0 "$FRONTEND_PID" 2>/dev/null; then
        print_status "✅ Frontend is running"
    else
        print_error "❌ Frontend failed to start"
        if [[ -f "$SCRIPT_DIR/frontend.log" ]]; then
            print_error "Frontend logs:"
            tail -10 "$SCRIPT_DIR/frontend.log"
        fi
        return 1
    fi

    return 0
}

# Function to open browser
open_browser() {
    sleep 3  # Wait for servers to start

    if command_exists open; then
        # macOS
        open http://localhost:3000
    elif command_exists xdg-open; then
        # Linux
        xdg-open http://localhost:3000
    elif command_exists google-chrome; then
        google-chrome http://localhost:3000
    elif command_exists firefox; then
        firefox http://localhost:3000
    else
        print_warning "Could not detect browser"
        print_status "Please manually open: http://localhost:3000"
    fi
}

# Function to show logs
show_logs() {
    print_header "Showing Logs"

    if [[ -f "$SCRIPT_DIR/backend.log" ]]; then
        print_status "Backend logs:"
        echo "---"
        tail -20 "$SCRIPT_DIR/backend.log"
        echo
    fi

    if [[ -f "$SCRIPT_DIR/frontend.log" ]]; then
        print_status "Frontend logs:"
        echo "---"
        tail -20 "$SCRIPT_DIR/frontend.log"
        echo
    fi
}

# Function to show status
show_status() {
    print_header "System Status"

    if [[ -f "$PID_FILE" ]]; then
        print_status "Running processes:"
        while IFS= read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                cmd=$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")
                print_status "  PID $pid: $cmd"
            else
                print_warning "  PID $pid: not running (stale)"
            fi
        done < "$PID_FILE"
    else
        print_status "No running processes"
    fi

    print_status
    print_status "Services:"
    print_status "  Backend:  http://localhost:8000"
    print_status "  Frontend: http://localhost:3000"
    print_status "  API Docs: http://localhost:8000/docs"
}

# Function to stop services
stop_services() {
    print_header "Stopping Services"
    cleanup
}

# Main function
main() {
    # Parse command line arguments
    case "${1:-}" in
        --help|-h)
            echo "File Comparison System Runner"
            echo
            echo "Usage: $0 [OPTIONS]"
            echo
            echo "Options:"
            echo "  --help, -h         Show this help message"
            echo "  --test-only        Run tests only, don't start servers"
            echo "  --backend-only     Start only backend server"
            echo "  --frontend-only    Start only frontend server"
            echo "  --stop             Stop all running services"
            echo "  --status           Show system status"
            echo "  --logs             Show recent logs"
            echo "  --no-browser       Don't open browser automatically"
            echo "  --skip-tests       Skip tests"
            echo
            echo "Examples:"
            echo "  $0                # Start both servers"
            echo "  $0 --test-only    # Run tests only"
            echo "  $0 --backend-only # Start backend only"
            echo "  $0 --stop         # Stop all services"
            exit 0
            ;;
        --test-only)
            if check_prerequisites; then
                run_tests
            else
                exit 1
            fi
            ;;
        --backend-only)
            if check_prerequisites && run_tests; then
                print_header "Starting Backend Only"
                start_backend
                print_status "Backend is running. Press Ctrl+C to stop."
                wait
            else
                exit 1
            fi
            ;;
        --frontend-only)
            print_header "Starting Frontend Only"
            start_frontend
            print_status "Frontend is running. Press Ctrl+C to stop."
            wait
            ;;
        --stop)
            stop_services
            ;;
        --status)
            show_status
            ;;
        --logs)
            show_logs
            ;;
        --no-browser)
            NO_BROWSER=true
            ;;
        --skip-tests)
            SKIP_TESTS=true
            ;;
        "")
            # Default: start both servers
            print_header "File Comparison System Starting..."

            if ! check_prerequisites; then
                exit 1
            fi

            if [[ "$SKIP_TESTS" != "true" ]]; then
                if ! run_tests; then
                    exit 1
                fi
            fi

            print_header "Starting Servers"
            print_status "Backend:  http://localhost:8000"
            print_status "Frontend: http://localhost:3000"
            print_status "API Docs: http://localhost:8000/docs"
            print_status
            print_status "Press Ctrl+C to stop all servers"
            print "=" * 50

            # Start backend
            if ! start_backend; then
                cleanup
                exit 1
            fi

            # Start frontend
            if ! start_frontend; then
                cleanup
                exit 1
            fi

            # Open browser if not disabled
            if [[ "${NO_BROWSER:-}" != "true" ]]; then
                print_status "Opening browser..."
                open_browser &
            fi

            print_status
            print_status "🎉 All services started successfully!"
            print_status "📊 Access the application at: http://localhost:3000"
            print_status "📝 API documentation at: http://localhost:8000/docs"

            # Wait for processes
            wait
            ;;
        *)
            print_error "Unknown option: $1"
            print_status "Use --help for available options"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"