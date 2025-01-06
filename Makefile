
################################################################################
### General configuration

# Default target that does nothing
.PHONY: default
default:

# Set the shell to bash for executing commands
SHELL := bash

# Ensure each command in a recipe is executed in a single shell instance
.ONESHELL:

# Set shell flags to:
# -e: Exit immediately if a command exits with a non-zero status
# -u: Treat unset variables as an error and exit immediately
# -o pipefail: Return the exit status of the last command in the pipeline that failed
.SHELLFLAGS := -eu -o pipefail -c

# Delete target files if a command in the recipe fails
.DELETE_ON_ERROR:

# Enable secondary expansion for prerequisites
.SECONDEXPANSION:

# Warn about the usage of undefined variables
MAKEFLAGS += --warn-undefined-variables

# Disable the built-in rules
MAKEFLAGS += --no-builtin-rules

################################################################################
### Config variables

# Load them from an optional .env file
-include .env
.EXPORT_ALL_VARIABLES: ;

################################################################################
### Automatically include components' extensions and ad-hoc rules (makefile.mk)
###
-include */makefile.mk

COMPONENTS := $(shell find * -name "makefile.mk" -exec sh -c '\
    for path; do \
        dir=$$(dirname "$$path"); \
        name=$$(echo "$$dir" | tr "/" "-"); \
        echo "$$name:$$dir"; \
    done' sh {} + | sort -u)

###
### Arguments:
### $1: component name (e.g. metaflowinfra_service)
### $2: component path (e.g. metaflowinfra/service)
###
define make-component-targets

.PHONY: $1.create $1.activate $1.remove

$1.create::
	./workspace/env/create.sh $1 $2

$1.activate::
	./workspace/env/activate.sh $1 $2

$1.run_tests::
	./workspace/env/run_tests.sh $1

$1.remove::
	./workspace/env/remove.sh

endef

# Split each "name path" pair and call the function
# Update foreach loop
$(foreach pair,$(COMPONENTS),\
    $(eval name := $(shell echo $(pair) | cut -d':' -f1)) \
    $(eval path := $(shell echo $(pair) | cut -d':' -f2)) \
    $(eval $(call make-component-targets,$(name),$(path))))

init_workspace::
	./workspace/init.sh

create_all_envs::
	$(foreach component,$(COMPONENTS),$(MAKE) $(component).create;)

run_all_tests::
	$(foreach component,$(COMPONENTS),$(MAKE) $(component).run_tests;)