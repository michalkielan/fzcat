# fzcat
[![Build](https://github.com/michalkielan/logcat-sort/actions/workflows/build.yml/badge.svg)](https://github.com/michalkielan/logcat-sort/actions/workflows/build.yml)
> Command line tool to fuzzy find the same log line in logcat file.

## Usage
```
$ ./logcat-sort/main.py -h
-i <logcat file>
-l <log levels - filter output by specified log level(s)>
-t <tag> - filter output by specified tag(s)>
```

## Output
```
[<log count>]: <log message>
```
