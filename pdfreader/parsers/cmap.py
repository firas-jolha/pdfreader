from ..exceptions import ParserException
from ..types import Name, Token, HexString
from .base import BasicTypesParser


class Range(object):

    def __init__(self, begin, end):
        if isinstance(begin, HexString):
            begin = begin.as_int
        if isinstance(end, HexString):
            end = end.as_int
        self.begin = begin
        self.end = end

    def __contains__(self, item):
        """
        >>> 2 in Range(0, 4)
        True
        >>> HexString("0a") in Range(0, 4)
        False
        >>> HexString("02") in Range(0, 4)
        True
        """
        if isinstance(item, HexString):
            item = item.as_int
        return self.begin <= item <= self.end

    def __repr__(self):
        return "<Range:{self.begin}-{self.end}>".format(self=self)

    def __len__(self):
        """
        >>> len(Range(0, 0))
        1
        >>> len(Range(0, 100))
        101
        """
        return self.end - self.begin + 1


class MapRange(Range):

    def __init__(self, begin, end, map_to_start):
        super(MapRange, self).__init__(begin, end)
        if isinstance(map_to_start, HexString):
            map_to_start = map_to_start.as_int
        self.map_to_start = map_to_start

    def __getitem__(self, item):
        """
        >>> r = MapRange(0, 4, 5)
        >>> r[0], r[1], r[4]
        (5, 6, 9)
        >>> r[5]
        Traceback (most recent call last):
        ...
        KeyError: 5
        """
        if item not in self:
            raise KeyError(item)
        return self.map_to_start + (item - self.begin)

    def get(self, item, default=None):
        """
        >>> r = MapRange(0, 4, 5)
        >>> r.get(0), r.get(1, None), r.get(4)
        (5, 6, 9)
        >>> r.get(5) is None
        True
        >>> r.get(5, -1)
        -1
        """
        try:
            res = self[item]
        except KeyError:
            res = default
        return res

    def __repr__(self):
        return "<MapRange:{self.begin}-{self.end},{self.map_to_start}>".format(self=self)


class CodespaceRanges(object):

    def __init__(self, begin=None, end=None):
        self.ranges = []
        if begin is not None and end is not None:
            self.add(begin, end)

    def __contains__(self, item):
        """
        >>> cr = CodespaceRanges()
        >>> cr.add(2, 30)
        >>> cr.add(HexString("FA"), HexString("FF"))
        >>> 10 in cr
        True
        >>> 2 in cr
        True
        >>> HexString('1e') in cr
        True
        >>> HexString('fb') in cr
        True
        >>> HexString("2f") in cr
        False
        >>> HexString("f9") in cr
        False
        >>> 256 in cr
        False
        >>> cr = CodespaceRanges(2, 2)
        >>> 2 in cr
        True
        >>> 3 in cr
        False
        """
        if isinstance(item, HexString):
            item = item.as_int
        return any(item in r for r in self.ranges)

    def add(self, begin, end):
        self.ranges.append(Range(begin, end))

    @property
    def as_list(self):
        """
        >>> cr = CodespaceRanges()
        >>> cr.add(2, 5)
        >>> cr.add(HexString("FA"), HexString("FF"))
        >>> cr.as_list
        [2, 3, 4, 5, 250, 251, 252, 253, 254, 255]
        """
        res = set({})
        for r in self.ranges:
            res.update(list(range(r.begin, r.end + 1)))
        return sorted(res)

    def __len__(self):
        """
        >>> cr = CodespaceRanges()
        >>> cr.add(2, 5)
        >>> cr.add(HexString("FA"), HexString("FF"))
        >>> len(cr)
        10
        """
        return len(self.as_list)

    def __repr__(self):
        rr = repr(self.ranges)
        if len(rr) > 50:
            rr = rr[:50] + " ..."
        return "<CodespaceRanges:ranges={}>".format(rr)

    def merge(self, other):
        """
        >>> cr1 = CodespaceRanges()
        >>> cr1.add(2, 5)
        >>> cr2 = CodespaceRanges()
        >>> cr2.add(102, 105)
        >>> cr1.merge(cr2)
        >>> cr1.as_list
        [2, 3, 4, 5, 102, 103, 104, 105]
        """
        self.ranges.extend(other.ranges)


class MappedCodespaceRanges(CodespaceRanges):

    def __init__(self, begin=None, end=None, map_to_start=None):
        self.ranges = []
        if begin is not None and end is not None and map_to_start is not None:
            self.add(begin, end, map_to_start)

    def add(self, begin, end, map_to_start):
        self.ranges.append(MapRange(begin, end, map_to_start))

    def __getitem__(self, item):
        """
        >>> r = MappedCodespaceRanges(0, 4, 5)
        >>> r.add(6, 10, 106)
        >>> r[0], r[4], r[6], r[7], r[8]
        (5, 9, 106, 107, 108)
        >>> r[5]
        Traceback (most recent call last):
        ...
        KeyError: 5
        >>> r[20]
        Traceback (most recent call last):
        ...
        KeyError: 20
        """
        for r in self.ranges:
            if item in r:
                return r[item]
        raise KeyError(item)

    def get(self, item, default=None):
        """
        >>> r = MappedCodespaceRanges(0, 4, 5)
        >>> r.add(6, 10, 106)
        >>> r.get(5) is None
        True
        >>> r.get(5, -1)
        -1
        >>> r.get(0), r.get(4), r.get(6, -1), r.get(7, None), r.get(8)
        (5, 9, 106, 107, 108)
        """
        try:
            res = self[item]
        except KeyError:
            res = default
        return res

    @property
    def as_dict(self):
        """
        >>> r = MappedCodespaceRanges(0, 4, 5)
        >>> r.add(6, 10, 106)
        >>> r.as_dict == {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 6: 106, 7:107, 8:108, 9:109, 10:110}
        True
        """
        return {item: self[item] for item in self.as_list}

    def __repr__(self):
        rr = repr(self.ranges)
        if len(rr) > 50:
            rr = rr[:50] + " ..."
        return "<MappedCodespaceRanges:ranges={}>".format(rr)


class CMapParser(BasicTypesParser):

    def object_or_token(self):
        try:
            obj = super(CMapParser, self).object()
        except ParserException:
            obj = self.token()
        return obj

    def skip_until_name(self, name):
        while True:
            if self.current is None:
                break
            self.maybe_spaces_or_comments()
            obj = self.object_or_token()
            if isinstance(obj, Name) and obj == name:
                for _ in range(len(name)):
                    self.prev()
                return True
        return False

    def skip_until_token(self, name):
        while True:
            if self.current is None:
                break
            self.maybe_spaces_or_comments()
            obj = self.object_or_token()
            if isinstance(obj, Token) and obj == name:
                for _ in range(len(name)):
                    self.prev()
                return True
        return False

    def cmap_name(self):
        self.skip_until_name('CMapName')
        self.maybe_spaces_or_comments()
        return self.name()

    def cmap(self):
        #/CIDInit /ProcSet findresource begin
        self.maybe_spaces_or_comments()
        self.expected_name('CIDInit')
        self.maybe_spaces_or_comments()
        self.expected_name('ProcSet')
        self.maybe_spaces_or_comments()
        self.expected_token("findresource")
        self.maybe_spaces_or_comments()
        self.expected_token("begin")
        self.maybe_spaces_or_comments()

        # <n> dict begin
        self.non_negative_int()
        self.maybe_spaces_or_comments()
        self.expected_token('dict')
        self.maybe_spaces_or_comments()
        self.expected_token('begin')

        # begincmap
        self.expected_token('begincmap')
        state = self.get_state() # save parser state

        cmap_name = self.cmap_name()
        self.set_state(state)

        codespaceranges = CodespaceRanges()
        while self.skip_until_token("begincodespacerange"):
            codespaceranges.merge(self.codespacerange())

        # Extarct CID mappings: range & chars
        self.set_state(state)
        cidranges = MappedCodespaceRanges()
        while self.skip_until_token("begincidrange"):
            cidranges.merge(self.mapped_codespacerange("cid"))
        self.set_state(state)
        while self.skip_until_token("begincidchar"):
            cidranges.merge(self.mapped_char("cid"))

        # Extracts NotDef mappings: range & chars
        self.set_state(state)
        notdefranges = MappedCodespaceRanges()
        while self.skip_until_token("beginnotdefrange"):
            notdefranges.merge(self.mapped_codespacerange("notdef"))
        self.set_state(state)
        while self.skip_until_token("beginnotdefchar"):
            notdefranges.merge(self.mapped_char("notdef"))

        # Extracts BF mappings: range & chars
        self.set_state(state)
        bfranges = MappedCodespaceRanges()
        while self.skip_until_token("beginbfrange"):
            bfranges.merge(self.mapped_codespacerange("bf"))
        self.set_state(state)
        while self.skip_until_token("beginbfchar"):
            bfranges.merge(self.mapped_char("bf"))
       
        # Class CMap - can decode a character

    def codespacerange(self):
        self.expected_token("begincodespacerange")
        self.maybe_spaces_or_comments()
        res = CodespaceRanges()
        while self.current == "<":
            cr_from = self.hexstring()
            self.maybe_spaces_or_comments()
            cr_to = self.hexstring()
            self.maybe_spaces_or_comments()
            res.add(cr_from, cr_to)
        self.expected_token("endcodespacerange")
        return res

    def mapped_codespacerange(self, rangename):
        self.expected_token("begin{}range".format(rangename))
        self.maybe_spaces_or_comments()
        res = MappedCodespaceRanges()
        while self.current == "<":
            cr_from = self.hexstring()
            self.maybe_spaces_or_comments()
            cr_to = self.hexstring()
            self.maybe_spaces_or_comments()
            cid_from = self.non_negative_int()
            self.maybe_spaces_or_comments()
            res.add(cr_from, cr_to, cid_from)
        self.expected_token("end{}range".format(rangename))
        return res

    def mapped_char(self, rangename):
        self.expected_token("begin{}char".format(rangename))
        self.maybe_spaces_or_comments()
        res = MappedCodespaceRanges()
        while self.current == "<":
            src_code = self.hexstring()
            self.maybe_spaces_or_comments()
            dst_code = self.hexstring()
            self.maybe_spaces_or_comments()
            res.add(src_code, src_code, dst_code)
        self.expected_token("end{}char".format(rangename))
        return res


if __name__ == "__main__":
    import doctest
    doctest.testmod()
