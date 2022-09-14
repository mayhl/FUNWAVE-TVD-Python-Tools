###################################################################
# Verifies the current version of repo using git tags and commits #
#   - Versions are of the form MAJOR.MINOR.PATCH                  #
#   - Tags denote the  MAJOR.MINOR version                        #
#   - PATCH is the number of commits since last tag               #
###################################################################

# git describe returns X-Y-Z, where
#   - X is the most recent tag before current commit, 
#     if commit is tagged, just X is returned.
#   - Y is the number of commits since last tag
#   - Z is the letter 'g' follow by commit ID
DESCRIPTION=$(git describe)

# Flag just return X
TAG=$(git describe --abbrev=0)

# Checking if current commit is tagged
if [ ${TAG} == ${DESCRIPTION} ]; then

	# If commit is is tagged, use tag as version
	VERSION=${TAG}

else
	# If commit is not tagged, stripping commit number and
        # replacing PATCH in TAG cuurent PATCH
	COMMIT=$(git rev-parse --short HEAD)
	VERSION=${DESCRIPTION/-g${COMMIT}/}
	VERSION=${VERSION/0-/}	
fi

echo ${VERSION} > .VERSION

