def preprocess_exclude_path_format(endpoints, **kwargs):
    """
        preprocessing hook that filters out {format} suffixed paths, in case
        format_suffix_patterns is used and {format} path params are unwanted.
    """
    path_to_exclude = [
        '/api/user-management/auth/user/',
        '/api/user-management/auth/password/reset/',
        '/api/user-management/auth/password/reset/confirm/',
        '/api/user-management/auth/registration/resend-email/',
        '/api/user-management/auth/registration/verify-email/',
    ]
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if path not in path_to_exclude
    ]
