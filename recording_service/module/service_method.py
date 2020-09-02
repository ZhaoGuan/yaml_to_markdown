#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'

def request_params_check(necessary_keys, args_keys):
    miss_keys = []
    if set(necessary_keys) != set(args_keys):
        for key in necessary_keys:
            if key not in args_keys:
                miss_keys.append(key)
    miss_message = "Miss Params: "
    if miss_keys:
        for key in miss_keys:
            miss_message += key
            miss_message += " "
        return False, miss_message
    else:
        return True, None
