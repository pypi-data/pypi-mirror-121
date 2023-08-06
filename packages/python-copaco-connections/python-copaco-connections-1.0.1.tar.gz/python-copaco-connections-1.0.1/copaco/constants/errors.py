class NotFoundError(ValueError):
    '''raise this when a variable has no value when it is expected'''

class NoMethodFound(ValueError):
    ''' raise this when no method is found for your logic'''

class FailedRequest(RuntimeError):
    ''' raise this when a request to a copaco endpoint has failed '''