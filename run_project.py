#!/usr/bin/env python3
"""
Script to run both backend and frontend simultaneously
for the File Comparison System
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path

class ProjectRunner:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent
        self.backend_dir = self.base_dir / "backend"
        self.frontend_dir = self.base_dir / "frontend"

    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")

        # Check if directories exist
        if not self.backend_dir.exists():
            print(f"❌ Backend directory not found: {self.backend_dir}")
            return False

        if not self.frontend_dir.exists():
            print(f"❌ Frontend directory not found: {self.frontend_dir}")
            return False

        # Check if virtual environment exists
        venv_dir = self.backend_dir / "venv"
        if not venv_dir.exists():
            print(f"❌ Virtual environment not found: {venv_dir}")
            print("💡 Please create virtual environment first:")
            print(f"   cd {self.backend_dir}")
            print("   python3 -m venv venv")
            print("   source venv/bin/activate")
            print("   pip install -r requirements.txt")
            return False

        # Check if required files exist
        main_py = self.backend_dir / "main.py"
        if not main_py.exists():
            print(f"❌ Backend main file not found: {main_py}")
            return False

        index_html = self.frontend_dir / "index.html"
        if not index_html.exists():
            print(f"❌ Frontend index file not found: {index_html}")
            return False

        print("✅ All prerequisites check passed!")
        return True

    def run_backend(self):
        """Run backend server"""
        # Kill existing servers first
        self.kill_existing_servers()
        try:
            # Activate virtual environment and run backend
            venv_python = None
            possible_paths = [
                str(self.backend_dir / "venv/bin/python"),
                str(self.base_dir / "backend/venv/bin/python"),  # Root-relative path
                str(self.backend_dir / "venv/bin/python3"), 
                str(self.base_dir / "backend/venv/bin/python3"),  # Root-relative path
                str(self.backend_dir / "venv/Scripts/python.exe"),  # Windows
                str(self.base_dir / "backend/venv/Scripts/python.exe"),  # Windows root-relative
                "python3",  # System fallback
                "python"   # Final fallback
            ]
            
            for path in possible_paths:
                if path.startswith("python"):
                    # System python - check if it exists
                    try:
                        result = subprocess.run(["which", path], capture_output=True, text=True)
                        if result.returncode == 0:
                            venv_python = path
                            break
                    except:
                        continue
                else:
                    # File path - check if it exists
                    if os.path.exists(path):
                        venv_python = path
                        break
            
            if not venv_python:
                raise Exception("No suitable Python interpreter found")

            cmd = [venv_python, "main.py"]
            print(f"🚀 Starting backend server with command: {' '.join(cmd)}")

            process = subprocess.Popen(
                cmd,
                cwd=str(self.backend_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Stream output
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    print(f"[BACKEND] {line.strip()}")

            process.wait()

        except Exception as e:
            print(f"❌ Backend error: {e}")

    def run_frontend(self):
        """Run frontend server"""
        # Kill existing servers first
        self.kill_existing_servers()
        try:
            # Try different frontend servers
            servers = [
                ("python3", ["-m", "http.server", "3000"]),
                ("python", ["-m", "http.server", "3000"]),
                ("npx", ["http-server", "-p", "3000"]),
                ("php", ["-S", "localhost:3000"])
            ]

            for server_cmd in servers:
                try:
                    # Check if command exists
                    result = subprocess.run(["which", server_cmd[0]],
                                          capture_output=True, text=True)
                    if result.returncode != 0:
                        continue

                    print(f"🚀 Starting frontend server with: {server_cmd[0]} {' '.join(server_cmd[1])}")

                    # Construct full command list
                    full_cmd = [server_cmd[0]] + server_cmd[1]
                    
                    process = subprocess.Popen(
                        full_cmd,
                        cwd=str(self.frontend_dir),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                        bufsize=1
                    )

                    # Stream output
                    for line in iter(process.stdout.readline, ''):
                        if line.strip():
                            print(f"[FRONTEND] {line.strip()}")

                    process.wait()
                    break

                except FileNotFoundError:
                    continue

            else:
                print("❌ No suitable frontend server found")
                print("💡 Please install one of the following:")
                print("   - Python 3")
                print("   - Node.js with http-server")
                print("   - PHP")

        except Exception as e:
            print(f"❌ Frontend error: {e}")

    def run_tests(self):
        """Run tests before starting"""
        print("🧪 Running tests...")

        try:
            # Activate virtual environment
            venv_python = None
            possible_paths = [
                str(self.backend_dir / "venv/bin/python"),
                str(self.base_dir / "backend/venv/bin/python"),  # Root-relative path
                str(self.backend_dir / "venv/bin/python3"), 
                str(self.base_dir / "backend/venv/bin/python3"),  # Root-relative path
                str(self.backend_dir / "venv/Scripts/python.exe"),  # Windows
                str(self.base_dir / "backend/venv/Scripts/python.exe"),  # Windows root-relative
                "python3",  # System fallback
                "python"   # Final fallback
            ]
            
            for path in possible_paths:
                if path.startswith("python"):
                    # System python - check if it exists
                    try:
                        result = subprocess.run(["which", path], capture_output=True, text=True)
                        if result.returncode == 0:
                            venv_python = path
                            break
                    except:
                        continue
                else:
                    # File path - check if it exists
                    if os.path.exists(path):
                        venv_python = path
                        break
            
            if not venv_python:
                raise Exception("No suitable Python interpreter found")

            # Run backend tests
            test_files = [
                "test_sample_processing.py",
                "test_sample_files.py"
            ]

            all_passed = True

            for test_file in test_files:
                test_file_path = self.backend_dir / test_file
                if test_file_path.exists():
                    print(f"🧪 Running {test_file}...")
                    result = subprocess.run([venv_python, test_file],
                                          cwd=str(self.backend_dir),
                                          capture_output=True, text=True)

                    if result.returncode == 0:
                        print(f"✅ {test_file} passed")
                    else:
                        print(f"❌ {test_file} failed:")
                        print(result.stderr)
                        all_passed = False
                else:
                    print(f"⚠️  Test file not found: {test_file}")

            if all_passed:
                print("✅ All tests passed!")
                return True
            else:
                print("❌ Some tests failed. Continue anyway? (y/N)")
                response = input().strip().lower()
                return response == 'y'

        except Exception as e:
            print(f"❌ Test error: {e}")
            print("⚠️  Continuing without tests...")
            return True

    def run_browser(self):
        """Open browser after servers are ready"""
        time.sleep(3)  # Wait for servers to start

        try:
            import webbrowser
            url = "http://localhost:3000"
            print(f"🌐 Opening browser at {url}")
            webbrowser.open(url)
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
            print(f"💡 Please manually open: http://localhost:3000")

    def cleanup(self):
        """Clean up processes"""
        print("\n🧹 Cleaning up...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        print("✅ Cleanup completed!")

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C"""
        print(f"\n📡 Received signal {signum}")
        self.cleanup()
        sys.exit(0)

    def kill_existing_servers(self):
        """Kill any existing servers on ports 3000 and 8000"""
        print("🔄 Checking for existing servers...")
        
        ports_to_kill = [3000, 8000]
        killed_any = False
        
        try:
            # Try to use psutil for more elegant process killing
            import psutil
            
            for port in ports_to_kill:
                try:
                    # Find process using the port
                    for proc in psutil.process_iter(['pid', 'name', 'connections']):
                        try:
                            for conn in proc.info['connections'] or []:
                                if conn.laddr.port == port:
                                    print(f"🔄 Killing process {proc.info['pid']} ({proc.info['name']}) using port {port}")
                                    proc.terminate()
                                    proc.wait(timeout=3)
                                    killed_any = True
                                    break
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            continue
                except Exception:
                    continue
                    
        except ImportError:
            # Fallback if psutil not available - use lsof and kill
            print("📦 psutil not available, using fallback method...")
            import subprocess
            
            for port in ports_to_kill:
                try:
                    result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                          capture_output=True, text=True)
                    if result.stdout.strip():
                        pids = result.stdout.strip().split('\n')
                        for pid in pids:
                            print(f"🔄 Killing process {pid} using port {port}")
                            subprocess.run(['kill', '-9', pid])
                            killed_any = True
                except subprocess.SubprocessError:
                    pass
        
        if killed_any:
            print("✅ Existing servers killed")
            time.sleep(1)  # Give ports time to be released
        else:
            print("✅ No existing servers found")

    def run(self):
        """Main run method"""
        print("🚀 File Comparison System Starting...")
        print("=" * 50)

        # Kill existing servers first
        self.kill_existing_servers()

        # Setup signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # Check prerequisites
        if not self.check_prerequisites():
            return 1

        # Run tests
        if not self.run_tests():
            return 1

        print("\n🎯 Starting servers...")
        print("📊 Backend will run at: http://localhost:8000")
        print("🌐 Frontend will run at: http://localhost:3000")
        print("📝 API Documentation: http://localhost:8000/docs")
        print("\n💡 Press Ctrl+C to stop all servers")
        print("=" * 50)

        try:
            # Start backend in separate thread
            backend_thread = threading.Thread(target=self.run_backend, daemon=True)
            backend_thread.start()

            # Start frontend in separate thread
            frontend_thread = threading.Thread(target=self.run_frontend, daemon=True)
            frontend_thread.start()

            # Open browser after delay
            browser_thread = threading.Thread(target=self.run_browser, daemon=True)
            browser_thread.start()

            # Wait for threads (they run indefinitely)
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Received keyboard interrupt")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.cleanup()

        return 0

def main():
    """Main entry point"""
    runner = ProjectRunner()

    # Check command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "--help" or arg == "-h":
            print("""
File Comparison System Runner

Usage:
    python run_project.py [OPTIONS]

Options:
    --help, -h      Show this help message
    --test-only     Run tests only, don't start servers
    --backend-only  Start only backend server
    --frontend-only Start only frontend server

Examples:
    python run_project.py           # Start both servers
    python run_project.py --test-only    # Run tests only
    python run_project.py --backend-only # Start backend only
    python run_project.py --frontend-only # Start frontend only
""")
            return 0

        elif arg == "--test-only":
            if not runner.check_prerequisites():
                return 1
            return 0 if runner.run_tests() else 1

        elif arg == "--backend-only":
            if not runner.check_prerequisites():
                return 1
            print("🚀 Starting backend only...")
            signal.signal(signal.SIGINT, runner.signal_handler)
            signal.signal(signal.SIGTERM, runner.signal_handler)
            try:
                runner.run_backend()
            except KeyboardInterrupt:
                print("\n🛑 Stopping backend...")
            finally:
                runner.cleanup()
            return 0

        elif arg == "--frontend-only":
            print("🚀 Starting frontend only...")
            signal.signal(signal.SIGINT, runner.signal_handler)
            signal.signal(signal.SIGTERM, runner.signal_handler)
            try:
                runner.run_frontend()
            except KeyboardInterrupt:
                print("\n🛑 Stopping frontend...")
            finally:
                runner.cleanup()
            return 0

        else:
            print(f"❌ Unknown option: {arg}")
            print("💡 Use --help for available options")
            return 1

    # Default: run both servers
    return runner.run()

if __name__ == "__main__":
    sys.exit(main())