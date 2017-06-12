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
```javascript
input_vote = {
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
```javascript
vote_counts = {
    'yes': 4,
    'no': 3,
    'abstain': 1,
    'liquid': 4
}
```

## Conventions

|vote| explanation |
|:-:|:-:|
|yes| vote for |
|no| vote against |
|abstain| abstation, null and blank votes |
|liquid| votes delagated yet to be resolved in yes, no or abstain |

## Behavior

Cyclic voting resolves in abstain of all involved. For example:

`a -> b -> c -> a`  
resolves in 3 abstentions.

`a -> b -> c -> f`  
`d -> e -> f -> c`  
resolves in 6 abstentions.
