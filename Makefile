.PHONY: validate audit build check help

help:
	@echo "Available targets:"
	@echo "  validate  - Run validation and audit checks"
	@echo "  audit     - Alias for validate"
	@echo "  build     - Alias for validate"
	@echo "  check     - Alias for validate"
	@echo "  help      - Show this help message"

validate audit build check:
	@python3 scripts/validate_audit.py
