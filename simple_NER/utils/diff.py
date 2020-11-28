from difflib import SequenceMatcher


class TextDiff:
    """Create diffs of text snippets."""

    def __init__(self, source, target):
        """source = source text - target = target text"""
        self.source = source.split()
        self.target = target.split()
        self.deleteCount, self.insertCount, self.replaceCount = 0, 0, 0
        self.cruncher = SequenceMatcher(None, self.source,
                                        self.target)

    def dif_tags(self):
        """Create a tagged diff."""
        for tag, alo, ahi, blo, bhi in self.cruncher.get_opcodes():
            inserted = ""
            deleted = ""
            if tag == 'replace':
                deleted = " ".join(self.source[alo:ahi])
                inserted = " ".join(self.target[blo:bhi])
                yield (tag, deleted, inserted), (alo, ahi), (blo, bhi)
                self.replaceCount += 1
            elif tag == 'delete':
                # Text deleted
                deleted = " ".join(self.source[alo:ahi])
                self.deleteCount += 1
                yield (tag, deleted, inserted), (alo, ahi), (blo, bhi)
            elif tag == 'insert':
                # Text inserted
                inserted = " ".join(self.target[alo:ahi])
                self.insertCount += 1
                yield (tag, deleted, inserted), (alo, ahi), (blo, bhi)


if __name__ == "__main__":
    ch1 = """Today, a generation raised in the shadows of the Cold
     War assumes new responsibilities in a world warmed by the sunshine of
     freedom"""

    ch2 = """Today, pythonistas raised in the shadows of the Cold
     War assumes responsibilities in a world warmed by the sunshine of
     spam and freedom"""

    differ = TextDiff(ch1, ch2)

    for tag, span in differ.dif_tags():
        print(tag, span)
        print(ch2.split()[span[0]:span[1]])
