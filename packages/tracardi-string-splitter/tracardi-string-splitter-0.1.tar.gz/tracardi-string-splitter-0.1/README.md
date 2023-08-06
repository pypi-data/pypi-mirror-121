# String splitter plugin

This plugin split any string with a given delimiter

# Requirements

no requirements

# Configuration

Example:

```json
{
  "string": "a.b.c",
  "delimiter": "."
}
```

This configuration will split `a.b.c` string into ["a", "b", "c"], using '.' as delimiter.

# Input

This plugin does not process input.

# Output

Returns array with splitted values.

Example:

```json
{
  "result": [
    "a",
    "b",
    "c"
  ]
}
```

