#!/usr/bin/env python3
"""
Build, Validate, and Audit Script for Safety for Agentic AI
This script validates project structure, configurations, dependencies, and provides an audit report.
"""

import os
import sys
import json
import yaml
import subprocess
import ast
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ValidationResult:
    """Container for validation results"""
    passed: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditReport:
    """Container for audit report"""
    timestamp: str
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    results: Dict[str, ValidationResult] = field(default_factory=dict)


class ProjectValidator:
    """Validates the Safety for Agentic AI project"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.report = AuditReport(timestamp=datetime.now().isoformat())
    
    def validate(self) -> AuditReport:
        """Run all validation checks"""
        print("🔍 Starting Build, Validate, and Audit Process...\n")
        
        checks = [
            ("Project Structure", self.validate_project_structure),
            ("Python Dependencies", self.validate_python_dependencies),
            ("Docker Compose Files", self.validate_docker_compose),
            ("YAML Configurations", self.validate_yaml_configs),
            ("Python Syntax", self.validate_python_syntax),
            ("Required Files", self.validate_required_files),
            ("Script Permissions", self.validate_script_permissions),
        ]
        
        for check_name, check_func in checks:
            print(f"✓ Checking {check_name}...")
            result = check_func()
            self.report.results[check_name] = result
            self.report.total_checks += 1
            
            if result.passed:
                self.report.passed_checks += 1
                print(f"  ✅ {check_name}: PASSED")
                if result.message:
                    print(f"     {result.message}")
            else:
                self.report.failed_checks += 1
                self.report.errors.append(f"{check_name}: {result.message}")
                print(f"  ❌ {check_name}: FAILED")
                print(f"     {result.message}")
                if result.details:
                    for key, value in result.details.items():
                        print(f"     {key}: {value}")
            print()
        
        return self.report
    
    def validate_project_structure(self) -> ValidationResult:
        """Validate project directory structure"""
        required_dirs = [
            "notebooks",
            "notebooks/scripts",
            "notebooks/configs",
            "deploy",
            "docs",
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)
        
        if missing_dirs:
            return ValidationResult(
                passed=False,
                message=f"Missing required directories: {', '.join(missing_dirs)}",
                details={"missing": missing_dirs}
            )
        
        return ValidationResult(
            passed=True,
            message=f"All required directories present ({len(required_dirs)} checked)"
        )
    
    def validate_python_dependencies(self) -> ValidationResult:
        """Validate Python dependencies in pyproject.toml"""
        pyproject_path = self.project_root / "pyproject.toml"
        
        if not pyproject_path.exists():
            return ValidationResult(
                passed=False,
                message="pyproject.toml not found"
            )
        
        try:
            # Try tomli first (Python 3.11+), then tomli-w, then fallback
            try:
                import tomli as tomllib
            except ImportError:
                try:
                    import tomli_w as tomllib
                except ImportError:
                    tomllib = None
            
            if tomllib:
                with open(pyproject_path, 'rb') as f:
                    pyproject = tomllib.load(f)
                
                dependencies = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
                
                if not dependencies:
                    return ValidationResult(
                        passed=False,
                        message="No dependencies found in pyproject.toml"
                    )
                
                required_deps = [
                    "garak",
                    "huggingface_hub",
                    "vllm",
                    "datasets",
                    "wildguard",
                ]
                
                missing_deps = []
                for dep in required_deps:
                    if dep not in dependencies:
                        missing_deps.append(dep)
                
                if missing_deps:
                    return ValidationResult(
                        passed=False,
                        message=f"Missing required dependencies: {', '.join(missing_deps)}",
                        details={"missing": missing_deps, "total": len(dependencies)}
                    )
                
                return ValidationResult(
                    passed=True,
                    message=f"All required dependencies present ({len(required_deps)} checked, {len(dependencies)} total)",
                    details={"total_dependencies": len(dependencies)}
                )
            else:
                # Fallback: try to parse manually
                with open(pyproject_path, 'r') as f:
                    content = f.read()
                
                required_deps = ["garak", "huggingface_hub", "vllm", "datasets", "wildguard"]
                missing_deps = [dep for dep in required_deps if dep not in content]
                
                if missing_deps:
                    return ValidationResult(
                        passed=False,
                        message=f"Could not parse pyproject.toml properly. Missing deps: {', '.join(missing_deps)}"
                    )
                
                return ValidationResult(
                    passed=True,
                    message="Dependencies found in pyproject.toml (basic string check)"
                )
        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"Error reading pyproject.toml: {str(e)}"
            )
    
    def validate_docker_compose(self) -> ValidationResult:
        """Validate Docker Compose files"""
        compose_files = [
            "deploy/docker-compose.yaml",
            "deploy/docker-compose-guardrails.yaml",
        ]
        
        errors = []
        for compose_file in compose_files:
            file_path = self.project_root / compose_file
            if not file_path.exists():
                errors.append(f"Missing: {compose_file}")
                continue
            
            try:
                # Validate YAML syntax
                with open(file_path, 'r') as f:
                    yaml.safe_load(f)
                
                # Check for docker-compose command availability
                try:
                    result = subprocess.run(
                        ["docker", "compose", "config", "--file", str(file_path)],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode != 0:
                        errors.append(f"Invalid docker-compose syntax in {compose_file}: {result.stderr[:200]}")
                except FileNotFoundError:
                    # Docker compose not available, skip syntax check
                    pass
                except subprocess.TimeoutExpired:
                    errors.append(f"Timeout validating {compose_file}")
                except Exception as e:
                    # Non-critical: docker-compose might not be installed
                    pass
                    
            except yaml.YAMLError as e:
                errors.append(f"Invalid YAML in {compose_file}: {str(e)}")
            except Exception as e:
                errors.append(f"Error reading {compose_file}: {str(e)}")
        
        if errors:
            return ValidationResult(
                passed=False,
                message=f"Docker Compose validation failed",
                details={"errors": errors}
            )
        
        return ValidationResult(
            passed=True,
            message=f"All Docker Compose files valid ({len(compose_files)} checked)"
        )
    
    def validate_yaml_configs(self) -> ValidationResult:
        """Validate YAML configuration files"""
        yaml_files = [
            "notebooks/configs/garak_base_config.yaml",
            "notebooks/configs/deepseek_sft.yaml",
        ]
        
        errors = []
        for yaml_file in yaml_files:
            file_path = self.project_root / yaml_file
            if not file_path.exists():
                errors.append(f"Missing: {yaml_file}")
                continue
            
            try:
                with open(file_path, 'r') as f:
                    yaml.safe_load(f)
            except yaml.YAMLError as e:
                errors.append(f"Invalid YAML in {yaml_file}: {str(e)}")
            except Exception as e:
                errors.append(f"Error reading {yaml_file}: {str(e)}")
        
        if errors:
            return ValidationResult(
                passed=False,
                message=f"YAML configuration validation failed",
                details={"errors": errors}
            )
        
        return ValidationResult(
            passed=True,
            message=f"All YAML configurations valid ({len(yaml_files)} checked)"
        )
    
    def validate_python_syntax(self) -> ValidationResult:
        """Validate Python syntax in all Python files"""
        python_files = list(self.project_root.rglob("*.py"))
        
        # Exclude common directories
        exclude_dirs = {".git", "__pycache__", ".pytest_cache", "node_modules"}
        python_files = [
            f for f in python_files
            if not any(excluded in f.parts for excluded in exclude_dirs)
        ]
        
        syntax_errors = []
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    source = f.read()
                ast.parse(source, filename=str(py_file))
            except SyntaxError as e:
                syntax_errors.append(f"{py_file.relative_to(self.project_root)}: {e.msg} (line {e.lineno})")
            except Exception as e:
                syntax_errors.append(f"{py_file.relative_to(self.project_root)}: {str(e)}")
        
        if syntax_errors:
            return ValidationResult(
                passed=False,
                message=f"Python syntax errors found in {len(syntax_errors)} file(s)",
                details={"errors": syntax_errors[:10]}  # Limit to first 10
            )
        
        return ValidationResult(
            passed=True,
            message=f"All Python files have valid syntax ({len(python_files)} checked)"
        )
    
    def validate_required_files(self) -> ValidationResult:
        """Validate that required files exist"""
        required_files = [
            "README.md",
            "pyproject.toml",
            "LICENSE",
            "notebooks/README.md",
            "notebooks/Step0_Setup.ipynb",
            "notebooks/Step1_Evaluation.ipynb",
            "notebooks/Step2_Safety_Post_Training.ipynb",
            "notebooks/Step3_Post_Training_Eval.ipynb",
            "notebooks/Step4_Run_Inference_with_NeMo_Guardrails_Docker.ipynb",
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            return ValidationResult(
                passed=False,
                message=f"Missing required files: {', '.join(missing_files)}",
                details={"missing": missing_files}
            )
        
        return ValidationResult(
            passed=True,
            message=f"All required files present ({len(required_files)} checked)"
        )
    
    def validate_script_permissions(self) -> ValidationResult:
        """Validate that shell scripts have execute permissions"""
        script_files = list(self.project_root.rglob("*.sh"))
        
        # Exclude .git directory
        script_files = [
            f for f in script_files
            if ".git" not in f.parts
        ]
        
        missing_exec = []
        for script_file in script_files:
            if not os.access(script_file, os.X_OK):
                missing_exec.append(str(script_file.relative_to(self.project_root)))
        
        if missing_exec:
            return ValidationResult(
                passed=False,
                message=f"Scripts missing execute permissions: {', '.join(missing_exec)}",
                details={"scripts": missing_exec}
            )
        
        if script_files:
            return ValidationResult(
                passed=True,
                message=f"All shell scripts have execute permissions ({len(script_files)} checked)"
            )
        else:
            return ValidationResult(
                passed=True,
                message="No shell scripts found (skipped)"
            )
    
    def generate_report(self) -> str:
        """Generate a formatted audit report"""
        report_lines = [
            "=" * 70,
            "BUILD, VALIDATE, AND AUDIT REPORT",
            "=" * 70,
            f"Timestamp: {self.report.timestamp}",
            f"Total Checks: {self.report.total_checks}",
            f"Passed: {self.report.passed_checks}",
            f"Failed: {self.report.failed_checks}",
            "=" * 70,
            "",
        ]
        
        if self.report.errors:
            report_lines.append("ERRORS:")
            for error in self.report.errors:
                report_lines.append(f"  ❌ {error}")
            report_lines.append("")
        
        if self.report.warnings:
            report_lines.append("WARNINGS:")
            for warning in self.report.warnings:
                report_lines.append(f"  ⚠️  {warning}")
            report_lines.append("")
        
        report_lines.append("DETAILED RESULTS:")
        for check_name, result in self.report.results.items():
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            report_lines.append(f"\n{check_name}: {status}")
            report_lines.append(f"  {result.message}")
            if result.details:
                for key, value in result.details.items():
                    if isinstance(value, list) and len(value) > 5:
                        report_lines.append(f"  {key}: {len(value)} items (showing first 5)")
                        for item in value[:5]:
                            report_lines.append(f"    - {item}")
                    else:
                        report_lines.append(f"  {key}: {value}")
        
        report_lines.append("")
        report_lines.append("=" * 70)
        
        return "\n".join(report_lines)


def main():
    """Main entry point"""
    project_root = Path(__file__).parent.parent
    
    validator = ProjectValidator(project_root)
    report = validator.validate()
    
    # Print summary
    print("\n" + "=" * 70)
    print("AUDIT SUMMARY")
    print("=" * 70)
    print(f"Total Checks: {report.total_checks}")
    print(f"✅ Passed: {report.passed_checks}")
    print(f"❌ Failed: {report.failed_checks}")
    print("=" * 70)
    
    # Generate and save report
    report_text = validator.generate_report()
    
    report_file = project_root / "audit_report.txt"
    with open(report_file, 'w') as f:
        f.write(report_text)
    
    print(f"\n📄 Full report saved to: {report_file}")
    
    # Save JSON report
    report_json = {
        "timestamp": report.timestamp,
        "total_checks": report.total_checks,
        "passed_checks": report.passed_checks,
        "failed_checks": report.failed_checks,
        "warnings": report.warnings,
        "errors": report.errors,
        "results": {
            name: {
                "passed": result.passed,
                "message": result.message,
                "details": result.details
            }
            for name, result in report.results.items()
        }
    }
    
    report_json_file = project_root / "audit_report.json"
    with open(report_json_file, 'w') as f:
        json.dump(report_json, f, indent=2)
    
    print(f"📄 JSON report saved to: {report_json_file}")
    
    # Exit with appropriate code
    if report.failed_checks > 0:
        print("\n⚠️  Some validation checks failed. Please review the report.")
        sys.exit(1)
    else:
        print("\n✅ All validation checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
