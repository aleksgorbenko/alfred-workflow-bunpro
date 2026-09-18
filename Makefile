DIST := dist
NAME := BunPro.alfredworkflow
BUILD := $(DIST)/.build

.PHONY: test lint format format-check check clean build release sync-plist link-live

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
	mkdir -p $(BUILD)/data $(BUILD)/src/bunpro $(BUILD)/icons "$(BUILD)/List Filter Images" "$(BUILD)/images/about"
	cp info.plist $(BUILD)/
	cp icon.png $(BUILD)/
	cp *.png $(BUILD)/
	cp data/grammar.json $(BUILD)/data/
	cp src/bunpro/*.py $(BUILD)/src/bunpro/
	cp images/about/*.png "$(BUILD)/images/about/"
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

link-live:
	@test -n "$(WORKFLOW_DIR)" || (echo "usage: make link-live WORKFLOW_DIR=/path/to/bundle" && exit 1)
	ln -sfn "$(CURDIR)/src" "$(WORKFLOW_DIR)/src"
	ln -sfn "$(CURDIR)/icons" "$(WORKFLOW_DIR)/icons"
	ln -sfn "$(CURDIR)/images" "$(WORKFLOW_DIR)/images"
	ln -sfn "$(CURDIR)/icon.png" "$(WORKFLOW_DIR)/icon.png"
	for icon in *.png; do \
		[ "$$icon" = "icon.png" ] || ln -sfn "$(CURDIR)/$$icon" "$(WORKFLOW_DIR)/$$icon"; \
	done
	ln -sfn "$(CURDIR)/Makefile" "$(WORKFLOW_DIR)/Makefile"
	@echo "linked $(WORKFLOW_DIR) to this repo"
