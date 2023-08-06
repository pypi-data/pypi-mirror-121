#   -*- coding: utf-8 -*-
#  Copyright (C) 2021 John "Preston" Mille <john@compose-x.io>
#  SPDX-License-Identifier: GPL-2.0


import re
from copy import deepcopy


def replace_string_in_dict_values(input_dict, src_value, new_value, copy=False):
    """

    :param input_dict:
    :param src_value:
    :param new_value:
    :return:
    """

    src_re = re.compile(re.escape(src_value))
    if copy:
        updated_dict = deepcopy(input_dict)
    else:
        updated_dict = input_dict
    for key, value in updated_dict.items():
        if isinstance(value, str) and src_re.findall(value):
            updated_dict[key] = src_re.sub(new_value, value)
        elif not isinstance(value, str):
            print(f"The value for {key} is not a string. Skipping")
    if copy:
        return updated_dict
