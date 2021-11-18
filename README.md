# Git-Object-Parser

This script will extract, decompress, and output the contents of Git objects in a given repository. Normally this isn't needed when you have full access to a code repository, as you can view previous commits and check for files containing potentially sensitive information.

However, there are times where hidden object files can be included in a repo that are not apparent, so this script will output the object data in a way that it can be easily viewed and searched.

## Requirements

- Python 3.x
- Git command line tools
  - `apt-get install git`
  - `brew install git`

The script may need to be modified if using on Windows systems.
