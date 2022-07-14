build:
	python3 -m build

publish:
	python3 -m twine upload --repository pypi dist/*

.PHONY: docs
docs:
	pydoctor src/dudraw --html-output=docs
