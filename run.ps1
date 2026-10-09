# File Comparison System Runner Script
# For Windows PowerShell

param(
    [string]$Mode = "both",
    [switch]$Help,
    [switch]$TestOnly,
    [switch]$BackendOnly,
    [switch]$FrontendOnly,
    [switch]$Stop,
    [switch]$Status,
    [switch]$Logs,
    [switch]$NoBrowser,
    [switch]$SkipTests
)

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    Purple = "Magenta"
    Cyan = "Cyan"
    White = "White"
}

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Write-Status {
    param([string]$Message)
    Write-ColorOutput "[INFO] $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "[WARNING] $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "[ERROR] $Message" "Red"
}

function Write-Header {
    param([string]$Message)
    Write-ColorOutput "=== $Message ===" "Purple"
}

function Write-Command {
    param([string]$Message)
    Write-ColorOutput "[COMMAND] $Message" "Cyan"
}

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $ScriptDir "backend"
$FrontendDir = Join-Path $ScriptDir "frontend"

# PID file for tracking processes
$PidFile = Join-Path $ScriptDir ".pids"

# Global variables for process tracking
$Script:Processes = @()

# Function to cleanup processes
function Cleanup-Processes {
    Write-Status "Cleaning up processes..."

    if (Test-Path $PidFile) {
        $pids = Get-Content $PidFile
        foreach ($pid in $pids) {
            try {
                $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
                if ($process) {
                    Write-Status "Stopping process $pid"
                    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                    Start-Sleep -Seconds 1
                }
            } catch {
                Write-Warning "Could not stop process $pid: $_"
            }
        }
        Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
    }

    # Stop tracked processes
    foreach ($process in $Script:Processes) {
        try {
            if (!$process.HasExited) {
                Write-Status "Stopping process $($process.Id)"
                $process.Kill()
            }
        } catch {
            Write-Warning "Could not stop process: $_"
        }
    }

    Write-Status "Cleanup completed!"
}

# Function to handle Ctrl+C
$Script:CleanupRequested = $false

function Handle-Signal {
    if (!$Script:CleanupRequested) {
        $Script:CleanupRequested = $true
        Write-Host ""
        Write-Warning "Received interrupt signal"
        Cleanup-Processes
        exit 0
    }
}

# Setup signal handlers
$null = Register-ObjectEvent -InputObject ([Console]) -EventName CancelKeyPress -Action Handle-Signal

# Function to check prerequisites
function Test-Prerequisites {
    Write-Header "Checking Prerequisites"

    # Check directories
    if (!(Test-Path $BackendDir)) {
        Write-Error "Backend directory not found: $BackendDir"
        return $false
    }

    if (!(Test-Path $FrontendDir)) {
        Write-Error "Frontend directory not found: $FrontendDir"
        return $false
    }

    # Check virtual environment
    $VenvDir = Join-Path $BackendDir "venv"
    if (!(Test-Path $VenvDir)) {
        Write-Error "Virtual environment not found"
        Write-Status "Please create virtual environment first:"
        Write-Command "cd $BackendDir"
        Write-Command "python -m venv venv"
        Write-Command "venv\Scripts\activate"
        Write-Command "pip install -r requirements.txt"
        return $false
    }

    # Check required files
    $MainPy = Join-Path $BackendDir "main.py"
    if (!(Test-Path $MainPy)) {
        Write-Error "Backend main file not found: $MainPy"
        return $false
    }

    $IndexHtml = Join-Path $FrontendDir "index.html"
    if (!(Test-Path $IndexHtml)) {
        Write-Error "Frontend index file not found: $IndexHtml"
        return $false
    }

    Write-Status "All prerequisites check passed!"
    return $true
}

# Function to run tests
function Invoke-Tests {
    Write-Header "Running Tests"

    Set-Location $BackendDir

    # Activate virtual environment
    $VenvPython = Join-Path $BackendDir "venv\Scripts\python.exe"
    if (!(Test-Path $VenvPython)) {
        $VenvPython = Join-Path $BackendDir "venv\bin\python.exe"
    }

    $testFiles = @("test_sample_processing.py", "test_sample_files.py")
    $allPassed = $true

    foreach ($testFile in $testFiles) {
        if (Test-Path $testFile) {
            Write-Status "Running $testFile..."
            try {
                $result = & $VenvPython $testFile
                if ($LASTEXITCODE -eq 0) {
                    Write-Status "✅ $testFile passed"
                } else {
                    Write-Error "❌ $testFile failed"
                    $allPassed = $false
                }
            } catch {
                Write-Error "❌ $testFile failed: $_"
                $allPassed = $false
            }
        } else {
            Write-Warning "⚠️ Test file not found: $testFile"
        }
    }

    if ($allPassed) {
        Write-Status "✅ All tests passed!"
        return $true
    } else {
        Write-Error "❌ Some tests failed"
        if (!$SkipTests) {
            $response = Read-Host "Continue anyway? (y/N)"
            if ($response -notmatch '^[Yy]') {
                return $false
            }
        }
        return $true
    }
}

# Function to start backend
function Start-Backend {
    Write-Status "Starting backend server..."
    Set-Location $BackendDir

    # Activate virtual environment
    $VenvPython = Join-Path $BackendDir "venv\Scripts\python.exe"
    if (!(Test-Path $VenvPython)) {
        $VenvPython = Join-Path $BackendDir "venv\bin\python.exe"
    }

    # Start backend in background
    $backendLog = Join-Path $ScriptDir "backend.log"
    $process = Start-Process -FilePath $VenvPython -ArgumentList "main.py" -RedirectStandardOutput $backendLog -RedirectStandardError $backendLog -PassThru

    $Script:Processes += $process
    $process.Id | Out-File -FilePath $PidFile -Append

    Write-Status "Backend started with PID: $($process.Id)"
    Write-Status "Backend URL: http://localhost:8000"
    Write-Status "API Docs: http://localhost:8000/docs"

    # Wait for backend to start
    Start-Sleep -Seconds 3

    # Check if backend is running
    if (Get-Process -Id $process.Id -ErrorAction SilentlyContinue) {
        Write-Status "✅ Backend is running"
        return $true
    } else {
        Write-Error "❌ Backend failed to start"
        if (Test-Path $backendLog) {
            Write-Error "Backend logs:"
            Get-Content $backendLog | Select-Object -Last 10
        }
        return $false
    }
}

# Function to start frontend
function Start-Frontend {
    Write-Status "Starting frontend server..."
    Set-Location $FrontendDir

    # Try different servers
    $frontendLog = Join-Path $ScriptDir "frontend.log"
    $process = $null

    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        Write-Command "python3 -m http.server 3000"
        $process = Start-Process -FilePath "python3" -ArgumentList "-m", "http.server", "3000" -RedirectStandardOutput $frontendLog -RedirectStandardError $frontendLog -PassThru
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        Write-Command "python -m http.server 3000"
        $process = Start-Process -FilePath "python" -ArgumentList "-m", "http.server", "3000" -RedirectStandardOutput $frontendLog -RedirectStandardError $frontendLog -PassThru
    }
    elseif (Get-Command npx -ErrorAction SilentlyContinue) {
        Write-Command "npx http-server -p 3000"
        $process = Start-Process -FilePath "npx" -ArgumentList "http-server", "-p", "3000" -RedirectStandardOutput $frontendLog -RedirectStandardError $frontendLog -PassThru
    }
    elseif (Get-Command php -ErrorAction SilentlyContinue) {
        Write-Command "php -S localhost:3000"
        $process = Start-Process -FilePath "php" -ArgumentList "-S", "localhost:3000" -RedirectStandardOutput $frontendLog -RedirectStandardError $frontendLog -PassThru
    }

    if ($process) {
        $Script:Processes += $process
        $process.Id | Out-File -FilePath $PidFile -Append

        Write-Status "Frontend started with PID: $($process.Id)"
        Write-Status "Frontend URL: http://localhost:3000"

        # Wait for frontend to start
        Start-Sleep -Seconds 3

        # Check if frontend is running
        if (Get-Process -Id $process.Id -ErrorAction SilentlyContinue) {
            Write-Status "✅ Frontend is running"
            return $true
        } else {
            Write-Error "❌ Frontend failed to start"
            if (Test-Path $frontendLog) {
                Write-Error "Frontend logs:"
                Get-Content $frontendLog | Select-Object -Last 10
            }
            return $false
        }
    } else {
        Write-Error "No suitable frontend server found"
        Write-Status "Please install one of: Python 3, Node.js, or PHP"
        return $false
    }
}

# Function to open browser
function Open-Browser {
    Start-Sleep -Seconds 3  # Wait for servers to start

    try {
        Start-Process "http://localhost:3000"
        Write-Status "Opening browser at http://localhost:3000"
    } catch {
        Write-Warning "Could not open browser: $_"
        Write-Status "Please manually open: http://localhost:3000"
    }
}

# Function to show logs
function Show-Logs {
    Write-Header "Showing Logs"

    $backendLog = Join-Path $ScriptDir "backend.log"
    if (Test-Path $backendLog) {
        Write-Status "Backend logs:"
        Write-Host "---"
        Get-Content $backendLog | Select-Object -Last 20
        Write-Host ""
    }

    $frontendLog = Join-Path $ScriptDir "frontend.log"
    if (Test-Path $frontendLog) {
        Write-Status "Frontend logs:"
        Write-Host "---"
        Get-Content $frontendLog | Select-Object -Last 20
        Write-Host ""
    }
}

# Function to show status
function Show-Status {
    Write-Header "System Status"

    if (Test-Path $PidFile) {
        Write-Status "Running processes:"
        $pids = Get-Content $PidFile
        foreach ($pid in $pids) {
            try {
                $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
                if ($process) {
                    Write-Status "  PID $pid`: $($process.ProcessName)"
                } else {
                    Write-Warning "  PID $pid`: not running (stale)"
                }
            } catch {
                Write-Warning "  PID $pid`: not accessible"
            }
        }
    } else {
        Write-Status "No running processes"
    }

    Write-Host ""
    Write-Status "Services:"
    Write-Status "  Backend:  http://localhost:8000"
    Write-Status "  Frontend: http://localhost:3000"
    Write-Status "  API Docs: http://localhost:8000/docs"
}

# Function to stop services
function Stop-Services {
    Write-Header "Stopping Services"
    Cleanup-Processes
}

# Main execution logic
function Main {
    # Parse parameters
    if ($Help) {
        Write-Host "File Comparison System Runner"
        Write-Host ""
        Write-Host "Usage: .\run.ps1 [OPTIONS]"
        Write-Host ""
        Write-Host "Options:"
        Write-Host "  -Help              Show this help message"
        Write-Host "  -TestOnly          Run tests only, don't start servers"
        Write-Host "  -BackendOnly       Start only backend server"
        Write-Host "  -FrontendOnly      Start only frontend server"
        Write-Host "  -Stop              Stop all running services"
        Write-Host "  -Status            Show system status"
        Write-Host "  -Logs              Show recent logs"
        Write-Host "  -NoBrowser         Don't open browser automatically"
        Write-Host "  -SkipTests         Skip tests"
        Write-Host ""
        Write-Host "Examples:"
        Write-Host "  .\run.ps1              # Start both servers"
        Write-Host "  .\run.ps1 -TestOnly    # Run tests only"
        Write-Host "  .\run.ps1 -BackendOnly # Start backend only"
        Write-Host "  .\run.ps1 -Stop         # Stop all services"
        return
    }

    if ($TestOnly) {
        if (Test-Prerequisites) {
            Invoke-Tests
        }
        return
    }

    if ($BackendOnly) {
        if (Test-Prerequisites -and Invoke-Tests) {
            Write-Header "Starting Backend Only"
            if (Start-Backend) {
                Write-Status "Backend is running. Press Ctrl+C to stop."
                try {
                    while ($true) { Start-Sleep -Seconds 1 }
                } finally {
                    Cleanup-Processes
                }
            }
        }
        return
    }

    if ($FrontendOnly) {
        Write-Header "Starting Frontend Only"
        if (Start-Frontend) {
            Write-Status "Frontend is running. Press Ctrl+C to stop."
            try {
                while ($true) { Start-Sleep -Seconds 1 }
            } finally {
                Cleanup-Processes
            }
        }
        return
    }

    if ($Stop) {
        Stop-Services
        return
    }

    if ($Status) {
        Show-Status
        return
    }

    if ($Logs) {
        Show-Logs
        return
    }

    # Default: start both servers
    Write-Header "File Comparison System Starting..."

    if (!(Test-Prerequisites)) {
        return
    }

    if (!$SkipTests) {
        if (!(Invoke-Tests)) {
            return
        }
    }

    Write-Header "Starting Servers"
    Write-Status "Backend:  http://localhost:8000"
    Write-Status "Frontend: http://localhost:3000"
    Write-Status "API Docs: http://localhost:8000/docs"
    Write-Host ""
    Write-Status "Press Ctrl+C to stop all servers"
    Write-Host "=" * 50

    # Start backend
    if (!(Start-Backend)) {
        Cleanup-Processes
        return
    }

    # Start frontend
    if (!(Start-Frontend)) {
        Cleanup-Processes
        return
    }

    # Open browser if not disabled
    if (!$NoBrowser) {
        Write-Status "Opening browser..."
        Open-Browser
    }

    Write-Host ""
    Write-Status "🎉 All services started successfully!"
    Write-Status "📊 Access the application at: http://localhost:3000"
    Write-Status "📝 API documentation at: http://localhost:8000/docs"

    # Wait for interrupt
    try {
        while ($true) { Start-Sleep -Seconds 1 }
    } finally {
        Cleanup-Processes
    }
}

# Run main function
Main