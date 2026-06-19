# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Makefile                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/19 19:29:48 by roandrie        #+#    #+#               #
#  Updated: 2026/06/19 19:33:11 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# ===================
# =		VARIABLES	=
# ===================
PYTHON			=	python3
PDB 			=	python3 -m pdb
UV_PYTHON		=	uv run python
UV_FLAKE8		=	uv run flake8
UV_MYPY 		=	uv run mypy
MYPY_FLAGS		=	--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
INSTALL_UV		=	curl -LsSf https://astral.sh/uv/install.sh | sh
CHECK_UV		=	command -v uv

SRC				=	src


# ===================
# =		RULES		=
# ===================

.PHONY:		all install run run-debug debug build clean fclean lint lint-strict delete-uv
.SILENT:

all:		install run

install:
			@if	! $(CHECK_UV) > /dev/null 2>&1; then \
					echo "$(BRED)UV not installed. Installing...$(RESET)"; \
					$(INSTALL_UV); \
			fi
			@echo "$(BGREEN)Installing project dependencies using uv...$(RESET)"
			$(UV_SKIP_WHEEL) uv sync $(UV_WARN)

run:		install
			$(UV_PYTHON) -m $(SRC)

run-debug:	install
			$(UV_PYTHON) pac-man.py $(CONFIG) --debug

clean:
			@echo "$(YELLOW)Cleaning temporary files, and caches... 🗑️$(RESET)"
			find . -type d -name "__pycache__" -exec rm -rf {} +
			find . -type f -name "*.pyc" -delete
			find . -type f -name "*.pyo" -delete
			rm -rf .mypy_cache
			rm -rf .pytest_cache

fclean:		clean
			@echo "$(YELLOW)Cleaning .venv, build and dist folder... 🗑️$(RESET)"
			rm -rf .venv
			rm -rf dist

lint:
			@clear
			@echo "$(BMAGENTA)Running standard linting...$(RESET)"
			@status=0; \
			$(UV_FLAKE8) $(LINT_TESTER) || status=$$?; \
			$(UV_MYPY) $(LINT_TESTER) $(MYPY_FLAGS) || status=$$?; \
			exit $$status

lint-strict:
			@clear
			@echo "$(BMAGENTA)Running strict linting...$(RESET)"
			@status=0; \
			$(UV_FLAKE8) $(LINT_TESTER) || status=$$?; \
			$(UV_MYPY) $(LINT_TESTER) $(MYPY_FLAGS) --strict || status=$$?; \
			exit $$status

delete-uv:
			@if $(CHECK_UV) > /dev/null 2>&1; then \
					echo "$(BRED)Deleting uv...$(RESET)"; \
					rm -f $$(which uv); \
			else \
					echo "$(BRED)UV not installed. Cannot delete. Abording.$(RESET)"; \
			fi

# ===================
# =		COLORS		=
# ===================

RESET		=	\033[0m
BGREEN		=	\033[92m
BMAGENTA	=	\033[95m
YELLOW		=	\033[93m
BRED		=	\033[91m
