#!/usr/bin/env python3
"""
Test Dashboard Module Installer

This script installs the Test-Driven Development Dashboard from GitHub into any project,
providing a web-based interface for test management and monitoring.

Repository: https://github.com/foolishimp/test_dd_dashboard

Usage:
    python setup_test_dashboard.py [options]
    
Options:
    --target PATH       Target directory for installation (default: current directory)
    --force            Overwrite existing files
    --port PORT        Default port for the dashboard (default: 8085)
    --version TAG      Install specific version/tag (default: v1.0.0)
    --no-git           Don't add .gitignore entries
    --offline          Use existing clone if available (don't pull updates)
"""

import os
import sys
import shutil
import argparse
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import json

class TestDashboardSetup:
    """Setup Test-Driven Development Dashboard in a project."""
    
    def __init__(self, target: str = ".", force: bool = False, 
                 port: int = 8085, version: Optional[str] = "v1.0.0",
                 no_git: bool = False, offline: bool = False):
        self.target = Path(target).resolve()
        self.force = force
        self.port = port
        self.version = version
        self.no_git = no_git
        self.offline = offline
        self.dashboard_dir = self.target / "test_dd_dashboard"
        
        # GitHub repository details
        self.repo_url = "https://github.com/foolishimp/test_dd_dashboard.git"
        self.repo_ssh = "git@github.com:foolishimp/test_dd_dashboard.git"
        
    def run(self):
        """Execute the setup process."""
        print("📊 Test-Driven Development Dashboard Setup")
        print(f"📁 Target directory: {self.target}")
        print(f"🌐 Repository: {self.repo_url}")
        if self.version:
            print(f"🏷️  Version: {self.version}")
        
        # Check what already exists
        dashboard_exists = self.dashboard_dir.exists()
        
        print(f"\n📋 Current state:")
        print(f"   test_dd_dashboard/: {'✅ exists' if dashboard_exists else '❌ missing'}")
        
        # Install dashboard if missing or force flag is set
        if not dashboard_exists or self.force:
            if dashboard_exists and self.force:
                print(f"\n🔄 Reinstalling test_dd_dashboard (--force flag)")
            else:
                print(f"\n📊 Installing test_dd_dashboard...")
            
            self._install_dashboard()
        else:
            print(f"\n⏭️  Skipping test_dd_dashboard (already exists)")
            if not self.offline:
                print(f"💡 Use --force to reinstall or --offline to skip updates")
        
        # Add .gitignore entries
        if not self.no_git:
            self._update_gitignore()
        
        print("\n✅ Setup complete!")
        self._print_next_steps()
    
    def _install_dashboard(self):
        """Install the test dashboard module from GitHub."""
        
        # Remove existing if force flag is set
        if self.dashboard_dir.exists() and self.force:
            print(f"🗑️  Removing existing dashboard...")
            shutil.rmtree(self.dashboard_dir)
        
        # Clone or update dashboard from GitHub
        self._clone_dashboard()
        
        # Update configuration for target
        self._update_dashboard_config()
        
        # Create project-specific configuration
        self._create_project_config()
        
        # Install Node.js dependencies
        self._install_node_dependencies()
    
    def _clone_dashboard(self):
        """Clone dashboard from GitHub repository."""
        temp_dir = None
        
        try:
            print(f"📥 Cloning from GitHub...")
            
            # Try SSH first, fallback to HTTPS
            clone_url = self.repo_ssh
            try:
                # Test SSH connection
                result = subprocess.run(
                    ["ssh", "-T", "git@github.com"],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode not in [0, 1]:  # SSH not available
                    clone_url = self.repo_url
                    print(f"🔄 SSH not available, using HTTPS...")
            except:
                clone_url = self.repo_url
                print(f"🔄 Using HTTPS for cloning...")
            
            # Clone to temporary directory
            temp_dir = tempfile.mkdtemp()
            clone_cmd = ["git", "clone"]
            
            if not self.version:
                clone_cmd.extend(["--depth", "1"])  # Shallow clone for latest
            
            clone_cmd.extend([clone_url, temp_dir])
            
            result = subprocess.run(
                clone_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, clone_cmd, result.stderr
                )
            
            # Checkout specific version if requested
            if self.version:
                print(f"🏷️  Checking out version: {self.version}")
                result = subprocess.run(
                    ["git", "checkout", self.version],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"⚠️  Could not checkout version {self.version}, using latest")
            
            # Copy files to target (exclude .git directory)
            self._copy_dashboard_files(Path(temp_dir))
            
            print(f"✅ Successfully cloned dashboard")
            
        except subprocess.TimeoutExpired:
            print(f"❌ Clone timed out - check your internet connection")
            raise
        except subprocess.CalledProcessError as e:
            print(f"❌ Git clone failed: {e.stderr}")
            print(f"💡 Make sure you have git installed and access to GitHub")
            raise
        except Exception as e:
            print(f"❌ Error cloning repository: {e}")
            raise
        finally:
            # Clean up temp directory
            if temp_dir and Path(temp_dir).exists():
                shutil.rmtree(temp_dir)
    
    def _copy_dashboard_files(self, source_dir: Path):
        """Copy dashboard files from source directory."""
        
        # Create target directory
        self.dashboard_dir.mkdir(parents=True, exist_ok=True)
        
        # Files and directories to copy (exclude git and installer-specific files)
        exclude_patterns = {".git", ".gitignore", "__pycache__", "node_modules", ".DS_Store"}
        
        copied_count = 0
        for item in source_dir.iterdir():
            if item.name in exclude_patterns:
                continue
                
            target_path = self.dashboard_dir / item.name
            
            if item.is_file():
                shutil.copy2(item, target_path)
                print(f"📄 Copied: {item.name}")
                copied_count += 1
            elif item.is_dir():
                if target_path.exists():
                    shutil.rmtree(target_path)
                shutil.copytree(item, target_path)
                print(f"📁 Copied: {item.name}/")
                copied_count += 1
        
        print(f"📊 Copied {copied_count} items to: {self.dashboard_dir.relative_to(self.target)}")
    
    def _update_dashboard_config(self):
        """Update dashboard configuration for target project."""
        package_json_path = self.dashboard_dir / "package.json"
        
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                # Update name to reflect target project
                original_name = package_data.get("name", "test-dd-dashboard")
                package_data["name"] = f"{self.target.name}-test-dashboard"
                
                # Update description
                package_data["description"] = f"Test dashboard for {self.target.name} project (from {original_name})"
                
                # Add reference to original repository
                if "repository" not in package_data:
                    package_data["repository"] = {
                        "type": "git",
                        "url": self.repo_url
                    }
                
                with open(package_json_path, 'w') as f:
                    json.dump(package_data, f, indent=2)
                
                print(f"📝 Updated package.json for project: {self.target.name}")
            
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️  Could not update package.json: {e}")
        
        # Update server configuration if needed
        server_js_path = self.dashboard_dir / "server.js"
        if server_js_path.exists() and self.port != 8085:
            try:
                content = server_js_path.read_text()
                # Update default port
                content = content.replace("PORT || 8085", f"PORT || {self.port}")
                server_js_path.write_text(content)
                print(f"📝 Updated default port to: {self.port}")
            except Exception as e:
                print(f"⚠️  Could not update server port: {e}")
    
    def _create_project_config(self):
        """Create project-specific configuration file."""
        config_path = self.dashboard_dir / "project-config.json"
        
        # Generate project-specific port (8085 + hash of project path for uniqueness)
        import hashlib
        path_hash = abs(hash(str(self.target))) % 100  # 0-99
        project_port = self.port + path_hash if self.port == 8085 else self.port
        
        project_config = {
            "projectName": self.target.name,
            "projectPath": str(self.target),
            "port": project_port,
            "created": datetime.now().isoformat(),
            "description": f"Test dashboard configuration for {self.target.name}"
        }
        
        try:
            with open(config_path, 'w') as f:
                json.dump(project_config, f, indent=2)
            print(f"📝 Created project config: {self.target.name} on port {project_port}")
        except Exception as e:
            print(f"⚠️  Could not create project config: {e}")
    
    def _install_node_dependencies(self):
        """Install Node.js dependencies for the test dashboard."""
        package_json = self.dashboard_dir / "package.json"
        if not package_json.exists():
            print("⚠️  No package.json found, skipping npm install")
            return
        
        try:
            print("📦 Installing Node.js dependencies...")
            result = subprocess.run(
                ["npm", "install"],
                cwd=self.dashboard_dir,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                print("✅ Node.js dependencies installed successfully")
            else:
                print(f"⚠️  npm install completed with warnings")
                if result.stderr:
                    print(f"   stderr: {result.stderr[:200]}...")
                    
        except subprocess.TimeoutExpired:
            print("⚠️  npm install timed out, but dashboard was created")
        except FileNotFoundError:
            print("⚠️  npm not found - install Node.js to use test dashboard")
            print("   Visit https://nodejs.org to download Node.js")
        except Exception as e:
            print(f"⚠️  Error installing dependencies: {e}")
            print("   You can run 'npm install' manually in the test_dd_dashboard directory")

    def _update_gitignore(self):
        """Add appropriate .gitignore entries."""
        gitignore_path = self.target / ".gitignore"
        
        entries_to_add = [
            "\n# Test Dashboard Module (from test_dd_dashboard)",
            "test_dd_dashboard/node_modules/",
            "test_dd_dashboard/package-lock.json",
            "test_dd_dashboard/test-registry.json",
            "test_dd_dashboard/project-config.json",
            "test_dd_dashboard/*.log",
            "test-registry.json",  # Generated at project root
        ]
        
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            
            # Check if already has test dashboard entries
            if "test_dd_dashboard" in content:
                print("✓ .gitignore already configured for test dashboard")
                return
            
            # Append entries
            if not content.endswith("\n"):
                content += "\n"
            
            content += "\n".join(entries_to_add) + "\n"
            gitignore_path.write_text(content)
            print("📝 Updated .gitignore")
        else:
            # Create new .gitignore
            content = "\n".join(entries_to_add) + "\n"
            gitignore_path.write_text(content)
            print("📝 Created .gitignore")
    
    def _print_next_steps(self):
        """Print next steps for the user."""
        dashboard_exists = self.dashboard_dir.exists()
        
        print("\n📚 Next Steps:")
        
        if dashboard_exists:
            print("1. Start the test dashboard (from project root):")
            print(f"   PROJECT_DIRS=\".\" node {self.dashboard_dir.relative_to(self.target)}/server.js")
            print()
            print(f"2. Open http://localhost:{self.port} in your browser")
            print()
            print("3. Configure your project:")
            print("   - Add your project root directory")
            print("   - Configure test file patterns")
            print("   - Set up test commands")
            print()
            print("4. Use for TDD workflow:")
            print("   - RED: Write failing tests first")
            print("   - GREEN: Write minimal code to pass")
            print("   - REFACTOR: Improve while keeping tests green")
            print()
            print("📝 Optional: Commit the changes:")
            print("   git add test_dd_dashboard/")
            print("   git commit -m 'Add test dashboard module'")
            print()
            print("🔄 To update dashboard later:")
            print(f"   python {Path(__file__).name} --force")
        
        # Get the configured port for final instructions
        config_path = self.dashboard_dir / "project-config.json"
        display_port = self.port
        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    display_port = config.get('port', self.port)
        except:
            pass
            
        print(f"\n🎯 Start dashboard: PROJECT_DIRS=\".\" node {self.dashboard_dir.relative_to(self.target)}/server.js")
        print(f"🌐 Dashboard URL: http://localhost:{display_port}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Setup Test-Driven Development Dashboard from GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install latest version in current directory
  python setup_test_dashboard.py
  
  # Install in specific directory
  python setup_test_dashboard.py --target ./myproject
  
  # Force overwrite existing installation
  python setup_test_dashboard.py --force
  
  # Install specific version
  python setup_test_dashboard.py --version v1.2.0
  
  # Use custom port
  python setup_test_dashboard.py --port 3000
  
  # Offline mode (don't pull updates)
  python setup_test_dashboard.py --offline
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
        "--port",
        type=int,
        help="Default port for the dashboard (default: 8085)",
        default=8085
    )
    
    parser.add_argument(
        "--version",
        help="Install specific version/tag (default: latest)",
        default=None
    )
    
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Don't add .gitignore entries"
    )
    
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use existing installation if available (don't pull updates)"
    )
    
    args = parser.parse_args()
    
    # Run setup
    setup = TestDashboardSetup(
        target=args.target,
        force=args.force,
        port=args.port,
        version=args.version,
        no_git=args.no_git,
        offline=args.offline
    )
    
    try:
        setup.run()
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()