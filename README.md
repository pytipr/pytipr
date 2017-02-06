# pytipr
The Python Template In-Place Replacer

[![Chat Room](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/pytipr/Lobby)
[![Build Status](https://travis-ci.org/pytipr/pytipr.svg?branch=master)](https://travis-ci.org/pytipr/pytipr)
[![Coverage Status](https://coveralls.io/repos/github/pytipr/pytipr/badge.svg?branch=master)](https://coveralls.io/github/pytipr/pytipr?branch=master)

## Example
Input:
```python
## user comment 1
user code 1
## tipr_code_start
## tipr_result_is="foo"
## tipr_code_end
## tipr_result_start
## tipr_result_end
## user comment 2
user code 2
```

Output (note the ``foo``) line:
```python
## user comment 1
user code 1
## tipr_code_start
## tipr_result_is="foo"
## tipr_code_end
## tipr_result_start
foo
## tipr_result_end
## user comment 2
user code 2

```
