set -euxo pipefail

#
# All the below commands should exit without error.
#
python anycat.py -h
python anycat.py --help
python anycat.py --version
python anycat.py -AnTv anycat.py README.md
cat anycat.py | python anycat.py - README.md
cat anycat.py | python anycat.py - README.md http://example.com s3://commoncrawl/robots.txt
