Stuff to do with counters, sequences and iterables.

*Latest release 20210924*:
New greedy(iterable) or @greedy(generator_function) to let generators precompute.

Note that any function accepting an iterable
will consume some or all of the derived iterator
in the course of its function.

## Function `common_prefix_length(*seqs)`

Return the length of the common prefix of sequences `seqs`.

## Function `common_suffix_length(*seqs)`

Return the length of the common suffix of sequences `seqs`.

## Function `first(iterable)`

Return the first item from an iterable; raise IndexError on empty iterables.

## Function `get0(iterable, default=None)`

Return first element of an iterable, or the default.

## Function `greedy(g=None, queue_depth=0)`

A decorator or function for greedy computation of iterables.

If `g` is omitted or callable
this is a decorator for a generator function
causing it to compute greedily,
capacity limited by `queue_depth`.

If `g` is iterable
this function dispatches it in a `Thread` to compute greedily,
capacity limited by `queue_depth`.

Example with an iterable:

    for packet in greedy(parse_data_stream(stream)):
        ... process packet ...

which does some readahead of the stream.

Example as a function decorator:

    @greedy
    def g(n):
        for item in range(n):
            yield n

This can also be used directly on an existing iterable:

    for item in greedy(range(n)):
        yield n

Normally a generator runs on demand.
This function dispatches a `Thread` to run the iterable
(typically a generator)
putting yielded values to a queue
and returns a new generator yielding from the queue.

The `queue_depth` parameter specifies the depth of the queue
and therefore how many values the original generator can compute
before blocking at the queue's capacity.

The default `queue_depth` is `0` which creates a `Channel`
as the queue - a zero storage buffer - which lets the generator
compute only a single value ahead of time.

A larger `queue_depth` allocates a `Queue` with that much storage
allowing the generator to compute as many as `queue_depth+1` values
ahead of time.

Here's a comparison of the behaviour:

Example without `@greedy`
where the "yield 1" step does not occur until after the "got 0":

    >>> from time import sleep
    >>> def g():
    ...   for i in range(2):
    ...     print("yield", i)
    ...     yield i
    ...   print("g done")
    ...
    >>> G = g(); sleep(0.1)
    >>> for i in G:
    ...   print("got", i)
    ...   sleep(0.1)
    ...
    yield 0
    got 0
    yield 1
    got 1
    g done

Example with `@greedy`
where the "yield 1" step computes before the "got 0":

    >>> from time import sleep
    >>> @greedy
    ... def g():
    ...   for i in range(2):
    ...     print("yield", i)
    ...     yield i
    ...   print("g done")
    ...
    >>> G = g(); sleep(0.1)
    yield 0
    >>> for i in G:
    ...   print("got", repr(i))
    ...   sleep(0.1)
    ...
    yield 1
    got 0
    g done
    got 1

Example with `@greedy(queue_depth=1)`
where the "yield 1" step computes before the "got 0":

    >>> from cs.x import X
    >>> from time import sleep
    >>> @greedy
    ... def g():
    ...   for i in range(3):
    ...     X("Y")
    ...     print("yield", i)
    ...     yield i
    ...   print("g done")
    ...
    >>> G = g(); sleep(2)
    yield 0
    yield 1
    >>> for i in G:
    ...   print("got", repr(i))
    ...   sleep(0.1)
    ...
    yield 2
    got 0
    yield 3
    got 1
    g done
    got 2

## Function `imerge(*iters, **kw)`

Merge an iterable of ordered iterables in order.

Parameters:
* `iters`: an iterable of iterators
* `reverse`: keyword parameter: if true, yield items in reverse order.
  This requires the iterables themselves to also be in
  reversed order.

This function relies on the source iterables being ordered
and their elements being comparable, through slightly misordered
iterables (for example, as extracted from web server logs)
will produce only slightly misordered results, as the merging
is done on the basis of the front elements of each iterable.

## Function `isordered(items, reverse=False, strict=False)`

Test whether an iterable is ordered.
Note that the iterable is iterated, so this is a destructive
test for nonsequences.

## Function `last(iterable)`

Return the last item from an iterable; raise IndexError on empty iterables.

## Function `onetomany(func)`

A decorator for a method of a sequence to merge the results of
passing every element of the sequence to the function, expecting
multiple values back.

Example:

      class X(list):
            @onetomany
            def chars(self, item):
                  return item
      strs = X(['Abc', 'Def'])
      all_chars = X.chars()

## Function `onetoone(func)`

A decorator for a method of a sequence to merge the results of
passing every element of the sequence to the function, expecting a
single value back.

Example:

      class X(list):
            @onetoone
            def lower(self, item):
                  return item.lower()
      strs = X(['Abc', 'Def'])
      lower_strs = X.lower()

## Class `Seq`

A thread safe wrapper for itertools.count().

## Function `seq()`

Return a new sequential value.

## Function `splitoff(sq, *sizes)`

Split a sequence into (usually short) prefixes and a tail,
for example to construct subdirectory trees based on a UUID.

Example:

    >>> from uuid import UUID
    >>> uuid = 'd6d9c510-785c-468c-9aa4-b7bda343fb79'
    >>> uu = UUID(uuid).hex
    >>> uu
    'd6d9c510785c468c9aa4b7bda343fb79'
    >>> splitoff(uu, 2, 2)
    ['d6', 'd9', 'c510785c468c9aa4b7bda343fb79']

## Class `StatefulIterator`

A trivial iterator which wraps another iterator to expose some tracking state.

This has 2 attributes:
* `.it`: the internal iterator which should yield `(item,new_state)`
* `.state`: the last state value from the internal iterator

The originating use case is resuse of an iterator by independent
calls that are typically sequential, specificly the .read
method of file like objects. Naive sequential reads require
the underlying storage to locate the data on every call, even
though the previous call has just performed this task for the
previous read. Saving the iterator used from the preceeding
call allows the iterator to pick up directly if the file
offset hasn't been fiddled in the meantime.

## Function `tee(iterable, *Qs)`

A generator yielding the items from an iterable
which also copies those items to a series of queues.

Parameters:
* `iterable`: the iterable to copy
* `Qs`: the queues, objects accepting a `.put` method.

Note: the item is `.put` onto every queue
before being yielded from this generator.

## Function `the(iterable, context=None)`

Returns the first element of an iterable, but requires there to be
exactly one.

## Class `TrackingCounter`

A wrapper for a counter which can be incremented and decremented.

A facility is provided to wait for the counter to reach a specific value.
The .inc and .dec methods also accept a `tag` argument to keep
individual counts based on the tag to aid debugging.

TODO: add `strict` option to error and abort if any counter tries
to go below zero.

### Method `TrackingCounter.__init__(self, value=0, name=None, lock=None)`

Initialise the counter to `value` (default 0) with the optional `name`.

### Method `TrackingCounter.check(self)`

Internal consistency check.

### Method `TrackingCounter.dec(self, tag=None)`

Decrement the counter.
Wake up any threads waiting for its new value.

### Method `TrackingCounter.inc(self, tag=None)`

Increment the counter.
Wake up any threads waiting for its new value.

### Method `TrackingCounter.wait(self, value)`

Wait for the counter to reach the specified `value`.

## Function `unrepeated(it, seen=None, signature=None)`

A generator yielding items from the iterable `it` with no repetitions.

Parameters:
* `it`: the iterable to process
* `seen`: an optional setlike container supporting `in` and `.add()`
* `signature`: an optional signature function for items from `it`
  which produces the value to compare to recognise repeated items;
  its values are stored in the `seen` set

The default `signature` function is identity - items are stored and compared.
This requires the items to be hashable and support equality tests.
The same applies to whatever values the `signature` function produces.

Since `seen` accrues all the signature values for yielded items
generally it will grow monotonicly as iteration proceeeds.
If the items are complaex or large it is well worth providing a signature
function even it the items themselves can be used in a set.

# Release Log



*Release 20210924*:
New greedy(iterable) or @greedy(generator_function) to let generators precompute.

*Release 20210913*:
New unrepeated() generator removing duplicates from an iterable.

*Release 20201025*:
New splitoff() function to split a sequence into (usually short) prefixes and a tail.

*Release 20200914*:
New common_prefix_length and common_suffix_length for comparing prefixes and suffixes of sequences.

*Release 20190103*:
Documentation update.

*Release 20190101*:
* New and UNTESTED class StatefulIterator to associate some externally visible state with an iterator.
* Seq: accept optional `lock` parameter.

*Release 20171231*:
* Python 2 backport for imerge().
* New tee function to duplicate an iterable to queues.
* Function isordered() is now a test instead of an assertion.
* Drop NamedTuple, NamedTupleClassFactory (unused).

*Release 20160918*:
* New function isordered() to test ordering of a sequence.
* imerge: accept new `reverse` parameter for merging reversed iterables.

*Release 20160828*:
Modify DISTINFO to say "install_requires", fixes pypi requirements.

*Release 20160827*:
TrackingCounter: accept presupplied lock object. Python 3 exec fix.

*Release 20150118*:
metadata update

*Release 20150111*:
Initial PyPI release.
