def immutable(attribute_name, default=None):
    """ 
        Used to annotate setters to check whether the 
        attribute is set

        Usage @immutable('attribute', default)
            'attribute' -> attribute to test
            default -> default value, which is None by default
    """
    def decorator_immutable(method):
        def inner(ref, attribute=None):
            keys_as_list = (list(ref.__dict__.keys()))
            interesting_attribute = next((
                x for x in keys_as_list if x.endswith(attribute_name)), None)
            assert(interesting_attribute !=
                   None), f"Attribute not found {interesting_attribute}"
            assert(ref.__dict__[interesting_attribute]
                   == default), f"Attribute already set {interesting_attribute}"
            return method(ref, attribute)
        return inner
    return decorator_immutable
