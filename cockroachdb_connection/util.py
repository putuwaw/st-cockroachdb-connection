def extract_conn_kwargs(params: set, target: dict) -> dict:
    """
    Description:
    Extracts the connection parameters from the given keywords argument 
    and returns a dictionary containing the connection parameters.
    """
    # return {key: target[key] for key in params if key in target}
    result = {}
    for p in params:
        if p in target:
            result[p] = target[p]
    return result
