def format_streaming_response(iterable):
    """
    Takes care of making an iterable over items into a stream
    of strings forming, overall, a valid JSON (which is 'assembled manually').
    Commas require special care.
    Return a generator over the pieces of the complete JSON string.
    """
    yield '['
    for index, item in enumerate(iterable):
        yield '%s%s' % (
            '' if index == 0 else ',',
            # the `.json()` method is available for Pydantic models
            # and it is equivalent to calling `json.dumps(some_dict)`.
            item.json(),
        )
    yield ']'
