
PYTHON=python3
PIP=pip
PKG_NAME='funwavetvdtools'

uninstall:
	rm -f funwavetvdtools
	${PIP} uninstall --yes ${PKG_NAME}

install: uninstall
	${PIP} install .

update_pypi:
	${PYTHON} -m ${PIP} install --upgrade build twine

upload_pypi_test:
	${PYTHON} -m build
	${PYTHON} -m twine upload --repository testpypi dist/*

develop: uninstall
	${PIP} install -e .
