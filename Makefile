.PHONY: build release-major release-minor release-patch publish publish-csdu docs
build:
	python3 -m build

release-major:
	bump2version major
	make build

release-minor:
	bump2version minor
	make build

release-patch:
	bump2version patch
	make build

publish:
	python3 -m twine upload --repository pypi dist/*

docs:
	pydoctor src/dudraw --html-output=docs

sync:
	rsync -ravP docs/* intropython@linux.cs.du.edu:~/public_html/dudraw