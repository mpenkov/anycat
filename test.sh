set -ex

#
# All the below commands should exit without error.
#
anycat -h
anycat --help
anycat --version
anycat -AnTv anycat README.md
cat anycat | anycat - README.md
cat anycat | anycat - README.md http://example.com s3://commoncrawl/robots.txt
