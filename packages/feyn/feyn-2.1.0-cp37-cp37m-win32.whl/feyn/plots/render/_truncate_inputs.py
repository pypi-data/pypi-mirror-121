def truncate_input_names(features, trunc_size=8, lb=3):
    regions = _isolate_interesting_regions(features, trunc_size, lb)
    trunc_names = []
    for i, f in enumerate(features):
        if len(f) <= 8:
            trunc_names.append(f)
            continue

        start = regions[i]
        end = start + trunc_size
        suffix = '..'
        prefix = '..'
        if len(f) <= end:
            start = max(len(f) - trunc_size, 0)
            end = len(f)
            suffix = ''

        if start == 0:
            prefix = ''

        tname = f[start:end]
        tname = prefix + tname + suffix
        trunc_names.append(tname)
    return trunc_names

def _isolate_interesting_regions(strs, trunc_size, lb):
    regions = []
    for i, me in enumerate(strs):
        i_regions = []
        others = strs[:i]+strs[i+1:]
        if i < len(strs):
            for other in others:
                if _compare(me, other, trunc_size) > 0:
                    reg_start = _spool(me, other, lb=lb)
                    i_regions.append(reg_start)


        any_safe = False
        for reg in i_regions:
            if _is_region_cross_safe(me, others, reg, trunc_size):
                regions.append(reg)
                any_safe |= True
                break
        if not any_safe:
            regions.append(0)

    return regions

def _compare(me, other, trunc_size):
    if me == other:
        return -1
    if me[:trunc_size] == other[:trunc_size]:
        return 1
    else:
        return 0

def _spool(me, other, lb):
    start = 0
    for i, (c1, c2) in enumerate(zip(me, other)):
        if c1 == c2:
            continue
        start = i-lb
        break
    return max(start, 0)

def _is_region_cross_safe(me, others, region, trunc_size):
    safe = True
    for other in others:
        safe &= me[region:region+trunc_size] != other[region:region+trunc_size]

    return safe
