# -*- coding: utf-8 -*-

import tuxsuite.cli.colors as colors


def datediff(one, two):
    if one is None:
        return two

    if one == two:
        return f"{colors.white}{two}{colors.reset}"

    index = 0
    for (o, t) in zip(one, two):
        if o != t:
            break
        index += 1

    return f"{colors.white}{two[0:index]}{colors.reset}{two[index:]}"
