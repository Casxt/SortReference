import zipfile
from lxml import etree
archive = zipfile.ZipFile('test.docx', 'r')

with archive.open('word/document.xml') as document:
    document_xml = document.read()
# configure XML parser
element_class_lookup = etree.ElementNamespaceClassLookup()
oxml_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
oxml_parser.set_element_class_lookup(element_class_lookup)
root = etree.fromstring(document_xml, oxml_parser)



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
            new_id[ref] = str(len(count))
    return count, new_id


def replaceSingleReference(wt_elems, replace_map):
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
                    assert len(temp_ref) == 1, f"replace multi text block not support yet, total {len(temp_ref)} text block"
                    temp_t, s, e = temp_ref[-1][0], temp_ref[-1][1], temp_ref[-1][2]
                    new_idx = replace_map[temp_ref_str]
                    # update `p` if still in current text
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

            

texts = extraText(root)
ref_list, ref_order = extraSingleReference(texts)
# for ts in texts:
#     for t in ts:
#         print(t.text)
print("origin", ref_order)

count, new_id = sortReference(ref_order)
print(count, new_id)

replaceSingleReference(texts, new_id)
ref_list, ref_order = extraSingleReference(texts)
print("new", ref_order)



# archive.writestr(test.filename, test.extra)
dest = zipfile.ZipFile('test_dest.docx', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=archive.compresslevel)
for file in archive.filelist:
    # print(file, len(file.))
    if file.filename == "word/document.xml":
        print("word/document.xml")
        continue
    data = archive.read(file.filename)
    dest.writestr(file.filename, data)

data = etree.tostring(root, encoding='UTF-8', standalone=True)
# data = data.replace(b'\n', b'\r\n')
# data = data.replace(b'&#10', b'&#xA')
# data = data.replace(b'version=\'1.0\'', b'version="1.0"')
# data = data.replace(b'encoding=\'UTF-8\'', b'encoding="UTF-8"')
# data = data.replace(b'tandalone=\'yes\'', b'tandalone="yes"')
dest.writestr('word/document.xml', data)
# dest.close()
# with archive.open('word/document.xml', "w") as document:
#     # document.truncate()
#     document.writestr(data)
dest.close()
# print(len(data), len(document_xml), data == document_xml)
# for i in range(0, len(data)):
#     if data[i] != document_xml[i]:
#         print(i, data[i-10:i+10], document_xml[i-10:i+10])
        