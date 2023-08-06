def get_overlap(overlaper):
    mod = __import__(f'{__name__}.{overlaper}', fromlist=[''])
    return getattr(mod, 'Model')
