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

```
anycat /some/local/file
anycat s3://bucket/key.txt -
anycat https://example.com
anycat host cat /path/to/file
```

# How?

To install:

    pip install -U anycat

and `anycat` from your shell.

You can save yourself some typing and make a bash [alias](http://tldp.org/LDP/abs/html/aliases.html):

    alias cat=anycat

If you suspect something is broken, you can temporarily revert to the actual `cat` binary by prefixing with a backslash:

    \cat /path/to/file

or remove the alias completely:

    unalias cat
