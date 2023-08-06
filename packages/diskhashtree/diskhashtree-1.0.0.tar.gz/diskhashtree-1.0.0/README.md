# Disk Hash Tree Python Package

An implementation for storing and searching through a large set of hashes.

## What's this for?

This project was originally being developed for [MLC@home](https://www.mlcathome.org/) as a solution to storing and testing membership for a large amounts of hashes in a memory-cheap, fast and persistent data structure. It uses the optimisations of the filesystem to do all the hard work of storing and checking membership of a hash in a set.

## Why make this?

Other than pickling and managing a `set()` object on-disk with a custom script, I couldn't find any other Python solution to implement a quick, persistent `set()`-like object that could support big data.

At the time of making this, I am studying Advanced Computer Science at Western Sydney Univeristy and was tasked with this as an extra-cirricula activity, so why not turn this into something a little bit bigger?

## Getting started

This package can be run standalone or imported into any Python script.

### Installing

`pip install diskhashtree`

### Importing and quickstart

```
from diskhashtree import DiskHashTree

dht = DiskHashTree('./mydht/')

dht.add('aaaaaa')
dht.add('zzzzzz')

print(dht.contains('aaaaaa'))

print(dht.pop())

dht.discard('aaaaaa')
dht.discard('zzzzzz')

print(dht.is_empty())
```

### Running standalone

DiskHashTree can be run straight from the commandline with no additional overhead compared to running it natively in Python. All the information is in the help function:

`diskhashtree -h`

## The maths

The following math and explanations assume that the hashes being used are of a fixed length M and contain purely alphabetical characters.

The data structure is hierarchical tree where a new subdirectory is created on every prefix collission at the current depth of the tree. For example, if we insert `abc` and `abd` while we have a prefix length (P) of 2 (the default), then a new subdirectory will be created as `ab/` and the keys will be emplaced as empty files into this subdirectory.

Hence for any level of this tree (except for the very last possible prefix), there is a constant search complexity within the level of `26^P`.

And hence the maximal depth of the tree is also constant with `M/P`.

If we take into consideration the number of keys in the set as N, the complexity is in the order of or better than `O(log(N))` for a single tree-traversal key search. This is because for every level of the tree, we have a constant worst-case search space and constant maximum tree depth.

This is better than managing a pickle object because the read and write operations to the disk would be `O(K)` and the object would have to be loaded into memory every single time.
