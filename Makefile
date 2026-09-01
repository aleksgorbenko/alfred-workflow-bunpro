DIST := dist
NAME := BunPro.alfredworkflow
BUILD := $(DIST)/.build

.PHONY: test lint format format-check check clean build release sync-plist

test:
	python3 -m pytest

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

check: lint format-check test

clean:
	find . -name '__pycache__' -not -path './.git/*' -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache

build: check
	rm -rf $(DIST)
	mkdir -p $(BUILD)/data $(BUILD)/src/bnapi $(BUILD)/icons "$(BUILD)/List Filter Images"
	cp info.plist $(BUILD)/
	cp icon.png $(BUILD)/
	cp data/grammar.json $(BUILD)/data/
	cp src/bnapi/*.py $(BUILD)/src/bnapi/
	cp icons/*.png $(BUILD)/icons/
	cp icons/icon_summary.png icons/icon_stats.png icons/icon_levels.png \
		icons/icon_forecast.png icons/icon_leeches.png "$(BUILD)/List Filter Images/"
	cd $(BUILD) && zip -r -q ../$(NAME) .
	rm -rf $(BUILD)
	@echo "built $(DIST)/$(NAME)"

release: build
	@test -n "$(VERSION)" || (echo "usage: make release VERSION=v1.0.0" && exit 1)
	git tag $(VERSION)
	git push origin $(VERSION)
	gh release create $(VERSION) $(DIST)/$(NAME) --generate-notes

# pulls info.plist from the live Alfred workflow bundle after editing
# keywords/objects/connections in the Alfred UI. WORKFLOW_DIR is
# machine-specific, never hardcoded here - pass it at invocation.
sync-plist:
	@test -n "$(WORKFLOW_DIR)" || (echo "usage: make sync-plist WORKFLOW_DIR=/path/to/bundle" && exit 1)
	cp "$(WORKFLOW_DIR)/info.plist" info.plist
	@echo "synced info.plist from $(WORKFLOW_DIR)"
