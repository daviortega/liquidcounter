# liquidcounter
[![Build Status](https://travis-ci.org/daviortega/liquidcounter.svg?branch=master)](https://travis-ci.org/daviortega/liquidcounter)

Counter of votes for liquid democracy

## Install
`pip install liquidcounter`

## Usage
```python
import liquidcounter as lc
vote_counts = lc.resolveIt(input_vote)
```

Input:
```
input vote = _
    'yes': ['a', 'b', 'c'],
    'no': ['d'],
    'abstain': ['e'],
    'd': ['g', 'h'],
    'a': ['i'],
    'f': ['j'],
    'j': ['l', 'm', 'n']
}
```

resolves in:
```json
vote_counts = {
    'yes': 4,
    'no': 3,
    'abstain': 1,
    'liquid': 4
}
