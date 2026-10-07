.PHONY: install update push

install:
	bash "$(CURDIR)/scripts/install.sh"

update:
	bash "$(CURDIR)/scripts/update.sh"

push:
	git -C "$(CURDIR)" push
