# What?

A wrapper around the standard [cat](https://en.wikipedia.org/wiki/Cat_%28Unix%29) utility that can read from:

- HTTP and HTTPS
- S3
- SSH
- HDFS and WebHDFS

Example:

```
$ echo THIS | cat - https://example.com s3://silo-open-data/README -b | grep -i th.s
     1  THIS
    40      <p>This domain is for use in illustrative examples in documents. You may use this
    52  These data are hosted under the AWS Public Data program, courtesy of Amazon Web Services Inc.
```

# Why?

The standard [cat](https://en.wikipedia.org/wiki/Cat_%28Unix%29) utility is very useful for writing [command pipelines](https://en.wikipedia.org/wiki/Pipeline_%28Unix%29).
Unfortunately, it only reads from the local file system.

We frequently need to access files from a variety of sources.
The command syntax to achieve this differs for each source.
For example:

```
cat /some/local/file
aws s3 cp s3://bucket/key.txt -
curl https://example.com
ssh host cat /path/to/file
```

This is inconvenient.
Wouldn't it be better if you could use a single command to do all these things?

Now you can.

# How?

This script uses [smart_open](https://github.com/RaRe-Technologies/smart_open) to do the hard work and read the remote content.
