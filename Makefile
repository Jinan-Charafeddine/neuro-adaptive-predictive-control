.PHONY: all test clean

all:
	python scripts/run_all.py

test:
	python -c "from tests.test_integrity import test_profile_leakage,test_virtual_profile_count; test_profile_leakage(); test_virtual_profile_count()"

clean:
	@echo "Generated data and results are versioned for reproducibility; remove them manually only if regeneration is intended."

