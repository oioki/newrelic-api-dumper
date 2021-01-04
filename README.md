# newrelic-api-dumper

```
usage: newrelic_api_dumper.py [-h] -k KEY [-o OUTPUT]

Dump all available data having New Relic API key

optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     New Relic API key
  -o OUTPUT, --output OUTPUT
                        Local directory to dump data
```

## Example

```
$ ./newrelic_api_dumper.py -k REDACTED
... applications
... applications/XXXXXX/hosts
... applications/XXXXXX/instances
... applications/XXXXXX/deployments
    [SNIP]
```
