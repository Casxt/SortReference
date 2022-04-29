
def ExtraTextBlock(root):
    """extra all <w:t> element in dfs order"""
    w_namespace = root.nsmap['w']
    wt_tag = "{%s}t" % (w_namespace)
    wt_elems = []
    stack = [root]
    while len(stack) > 0:
        t = stack.pop()
        if t.tag == wt_tag:
            wt_elems.append(t)
        else:
            for i in range(len(t) - 1, -1, -1):
                stack.append(t[i])
    return wt_elems


def ExtraSimpleReference(wt_elems):
    """
    extra reference in [num] format
    state1: wiat '['
    state2: wiat '\d' or ']'
    """
    ref_texts = []
    state = 1
    temp_ref = []
    temp_ref_str = ""
    refs = []
    for t in wt_elems:
        for c in t.text:
            if state == 1:
                if c == '[':
                    state = 2
                    temp_ref.append(t)
                else:
                    pass
            elif state == 2:
                if t is not temp_ref[-1]:
                    temp_ref.append(t)
                if ord('0') <= ord(c) <= ord('9'):
                    temp_ref_str = temp_ref_str + c
                elif c == ']':
                    state = 1
                    ref_texts.append(temp_ref)
                    temp_ref = []
                    refs.append(temp_ref_str)
                    temp_ref_str = ""
                else:
                    temp_ref = []
                    temp_ref_str = ""
                    state = 1
    return refs, ref_texts

def ReorderReference(ref_order):
    """
    count reference usage
    sort reference to new order by using order
    """
    count = {}
    new_id = {}
    for ref in ref_order:
        if ref in count:
            count[ref] += 1
        else:
            count[ref] = 1
            new_id[ref] = str(len(count))
    return count, new_id


def ReplaceSimpleReference(wt_elems, replace_map):
    """
    state1: wiat '['
    state2: wiat '\d' or ']'
    """
    state = 1
    temp_ref = []
    temp_ref_str = ""
    for t in wt_elems:
        p = 0
        while p < len(t.text):
            c = t.text[p]
            if state == 1:
                if c == '[':
                    state = 2
                else:
                    pass
            elif state == 2:
                if ord('0') <= ord(c) <= ord('9'):
                    temp_ref_str = temp_ref_str + c
                    if len(temp_ref) == 0 or t is not temp_ref[-1][0]:
                        temp_ref.append([t, p, p])
                    else:
                        temp_ref[-1][2] = p
                elif c == ']':
                    assert len(temp_ref) == 1, f"replace multi text block not support yet, total {len(temp_ref)} text sinppet: '{''.join([t.text for t in temp_ref])}' "
                    temp_t, s, e = temp_ref[-1][0], temp_ref[-1][1], temp_ref[-1][2]
                    new_idx = replace_map[temp_ref_str]
                    # update `p` if `p` still in current text
                    if t is temp_t:
                        p = p + len(new_idx) - len(temp_ref_str)
                    temp_t.text = temp_t.text[0:s] + new_idx + temp_t.text[e+1:]
                    state = 1
                    temp_ref = []
                    temp_ref_str = ""
                else:
                    temp_ref = []
                    temp_ref_str = ""
                    state = 1
            p += 1

            


