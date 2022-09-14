

PIP=pip
PKG_NAME='funwavetvdtools'

uninstall:
	${PIP} uninstall --yes ${PKG_NAME}

install: uninstall
	${PIP} install .


# Creating a symbolic link to src directory since installing package
# in developer mode use src as the package name instead of PKG_NAME. 
# NOTE 1: Normal installation is not affected.
# NOTE 2: Package will be still be importable via 'src', e.g. import src. 
develop: uninstall
	ln -s src ${PKG_NAME}
	${PIP} install -e .
