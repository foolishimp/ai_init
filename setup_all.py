#!/usr/bin/env python3
"""
AI Init - Complete Setup Script

This script installs all AI development tools and components into a project:
- Claude Task Management System
- Test Dashboard Module

Usage:
    python setup_all.py [options]
    
Options:
    --target PATH       Target directory for installation (default: current directory)
    --force            Overwrite existing files
    --claude-only      Install only Claude task management system
    --dashboard-only   Install only test dashboard module
    --dashboard-port PORT  Port for test dashboard (default: 8085)
    --no-git           Don't add .gitignore entries
    --help             Show this help message
"""

import sys
import argparse
import subprocess
from pathlib import Path

class AIInitSetup:
    """Complete AI development tools setup orchestrator."""
    
    def __init__(self, target: str = ".", force: bool = False, 
                 claude_only: bool = False, dashboard_only: bool = False,
                 dashboard_port: int = 8085, no_git: bool = False):
        self.target = Path(target).resolve()
        self.force = force
        self.claude_only = claude_only
        self.dashboard_only = dashboard_only
        self.dashboard_port = dashboard_port
        self.no_git = no_git
        
        # Get the directory where this script is located (ai_init root)
        self.ai_init_root = Path(__file__).parent
        
        # Paths to individual installers
        self.claude_installer = self.ai_init_root / "claude_init" / "setup_claude_tasks.py"
        self.dashboard_installer = self.ai_init_root / "setup_test_dashboard.py"
        
    def run(self):
        """Execute the complete setup process."""
        print("🚀 AI Init - Complete Development Tools Setup")
        print(f"📁 Target directory: {self.target}")
        print(f"📁 AI Init source: {self.ai_init_root}")
        
        # Validate installers exist
        if not self._validate_installers():
            return False
        
        # Determine what to install
        install_claude = not self.dashboard_only
        install_dashboard = not self.claude_only
        
        print(f"\n📋 Installation plan:")
        if install_claude:
            print("   ✅ Claude Task Management System")
        else:
            print("   ⏭️  Claude Task Management System (skipped)")
            
        if install_dashboard:
            print("   ✅ Test Dashboard Module")
        else:
            print("   ⏭️  Test Dashboard Module (skipped)")
        
        success = True
        
        # Install Claude task management system
        if install_claude:
            print(f"\n" + "="*60)
            print("🧠 Installing Claude Task Management System...")
            print("="*60)
            success &= self._run_claude_installer()
        
        # Install test dashboard module
        if install_dashboard:
            print(f"\n" + "="*60)
            print("📊 Installing Test Dashboard Module...")
            print("="*60)
            success &= self._run_dashboard_installer()
        
        # Final summary
        print(f"\n" + "="*60)
        if success:
            print("✅ AI Init Setup Complete!")
            self._print_final_summary(install_claude, install_dashboard)
        else:
            print("❌ Setup completed with errors - see messages above")
            return False
        
        return True
    
    def _validate_installers(self) -> bool:
        """Validate that all required installer scripts exist."""
        missing = []
        
        if not self.claude_installer.exists():
            missing.append(f"Claude installer: {self.claude_installer}")
            
        if not self.dashboard_installer.exists():
            missing.append(f"Dashboard installer: {self.dashboard_installer}")
            missing.append(f"Note: Dashboard installer should be at ai_init root, not in test-dashboard-module/")
        
        if missing:
            print(f"\n❌ Missing installer scripts:")
            for item in missing:
                print(f"   - {item}")
            print(f"\nEnsure you're running this script from the ai_init directory")
            return False
        
        return True
    
    def _run_claude_installer(self) -> bool:
        """Run the Claude task management installer."""
        cmd = [
            sys.executable,  # Use same Python interpreter
            str(self.claude_installer),
            "--target", str(self.target)
        ]
        
        if self.force:
            cmd.append("--force")
        if self.no_git:
            cmd.append("--no-git")
        
        try:
            result = subprocess.run(cmd, check=False)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error running Claude installer: {e}")
            return False
    
    def _run_dashboard_installer(self) -> bool:
        """Run the test dashboard installer."""
        cmd = [
            sys.executable,  # Use same Python interpreter  
            str(self.dashboard_installer),
            "--target", str(self.target),
            "--port", str(self.dashboard_port)
        ]
        
        if self.force:
            cmd.append("--force")
        if self.no_git:
            cmd.append("--no-git")
        
        try:
            result = subprocess.run(cmd, check=False)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error running dashboard installer: {e}")
            return False
    
    def _print_final_summary(self, installed_claude: bool, installed_dashboard: bool):
        """Print final setup summary and next steps."""
        print(f"\n🎉 Your project is now equipped with AI development tools!")
        
        if installed_claude:
            print(f"\n🧠 Claude Task Management System:")
            print(f"   📁 claude_tasks/ - Task management framework")
            print(f"   📄 CLAUDE.md - AI development guidance")
            print(f"   🎯 Start with: cat claude_tasks/SESSION_STARTER.md")
        
        if installed_dashboard:
            print(f"\n📊 Test-Driven Development Dashboard:")
            print(f"   📁 test-dashboard-module/ - Web-based test management")
            print(f"   🌐 Repository: https://github.com/foolishimp/test_dd_dashboard")
            print(f"   🚀 Start with: cd test-dashboard-module && npm start")
            print(f"   🌐 Then open: http://localhost:{self.dashboard_port}")
        
        print(f"\n📚 Recommended next steps:")
        step = 1
        
        if installed_claude:
            print(f"{step}. Review development methodology:")
            print(f"   cat claude_tasks/PRINCIPLES_QUICK_CARD.md")
            step += 1
        
        if installed_dashboard:
            print(f"{step}. Start the test dashboard and configure your project")
            step += 1
        
        if installed_claude and installed_dashboard:
            print(f"{step}. Use both tools together:")
            print(f"   - Plan tasks in claude_tasks/active/ACTIVE_TASKS.md")
            print(f"   - Monitor tests in the dashboard")
            print(f"   - Follow TDD: RED → GREEN → REFACTOR")
            step += 1
        
        print(f"{step}. Commit your setup:")
        print(f"   git add .")
        if installed_claude and installed_dashboard:
            print(f"   git commit -m 'Add AI development tools: Claude tasks + test dashboard'")
        elif installed_claude:
            print(f"   git commit -m 'Add Claude task management system'")
        elif installed_dashboard:
            print(f"   git commit -m 'Add test dashboard module'")
        
        print(f"\n🚀 Happy coding with AI-assisted development!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Setup complete AI development tools suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install everything in current directory
  python setup_all.py
  
  # Install in specific directory
  python setup_all.py --target ./myproject
  
  # Install only Claude task management
  python setup_all.py --claude-only
  
  # Install only test dashboard with custom port
  python setup_all.py --dashboard-only --dashboard-port 3000
  
  # Force reinstall everything
  python setup_all.py --force
        """
    )
    
    parser.add_argument(
        "--target",
        help="Target directory for installation (default: current directory)",
        default="."
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files"
    )
    
    parser.add_argument(
        "--claude-only",
        action="store_true", 
        help="Install only Claude task management system"
    )
    
    parser.add_argument(
        "--dashboard-only",
        action="store_true",
        help="Install only test dashboard module"
    )
    
    parser.add_argument(
        "--dashboard-port",
        type=int,
        help="Port for test dashboard (default: 8085)",
        default=8085
    )
    
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Don't add .gitignore entries"
    )
    
    # Validate conflicting options
    args = parser.parse_args()
    
    if args.claude_only and args.dashboard_only:
        print("❌ Error: Cannot specify both --claude-only and --dashboard-only")
        sys.exit(1)
    
    # Run setup
    setup = AIInitSetup(
        target=args.target,
        force=args.force,
        claude_only=args.claude_only,
        dashboard_only=args.dashboard_only,
        dashboard_port=args.dashboard_port,
        no_git=args.no_git
    )
    
    try:
        success = setup.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()