import zipfile

from lxml import etree
archive = zipfile.ZipFile('test.docx', 'r')
with archive.open('word/document.xml') as document:
    document_xml = document.read()
root = etree.fromstring(document_xml)


def extraText(root):
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


def extraSingleReference(wt_elems):
    """
    state1: wiat '['
    state2: wiat '\d' or ']'
    """
    ref_list = []
    state = 1
    temp_ref = []
    temp_ref_str = ""
    ref_order = []
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
                    ref_list.append(temp_ref)
                    temp_ref = []
                    ref_order.append(temp_ref_str)
                    temp_ref_str = ""
                else:
                    temp_ref = []
                    temp_ref_str = ""
                    state = 1
    return ref_list, ref_order


def extraComplexReference(wt_elems):
    """
    state1: wiat '['
    state2: wiat '\d' or ' '
    state3: wiat '\d' or ',' or ']'
    """
    ref_list = []
    state = 1
    temp_ref = []
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
                    state = 3
                elif c == ' ':
                    pass
                else:
                    temp_ref = []
                    state = 1
            elif state == 3:
                if t is not temp_ref[-1]:
                    temp_ref.append(t)
                if ord('0') <= ord(c) <= ord('9'):
                    pass
                elif c == ',':
                    state = 2
                elif c == ']':
                    state = 1
                    ref_list.append(temp_ref)
                    temp_ref = []
                else:
                    temp_ref = []
                    state = 1
    return ref_list

def sortReference(ref_order):
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
            new_id[ref] = len(count)
    return count, new_id
            

texts = extraText(root)
ref_list, ref_order = extraSingleReference(texts)
for ts in texts:
    for t in ts:
        print(t.text)

count, new_id = sortReference(ref_order)


print(count, new_id)