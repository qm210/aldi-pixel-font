import construct
from typing import Optional, List
from glyph import *

class Font:
    BinarySaveFormat = construct.GreedyRange(
        Glyph.BinarySaveFormat,
    )

    def __init__(self,
        ordinals: List[int] = [ord('a'), ord('b')],
    ) -> None:
        self._glyphs = list(map(
            lambda ordinal: Glyph(ordinal),
            ordinals,
        ))

    def toBytes(self) -> bytes:
        return Font.BinarySaveFormat.build(list(map(
            lambda glyph: glyph.toObject(),
            self._glyphs,
        )))
    
    def fromBytes(self,
        data: bytes,
    ):
        self._glyphs = list(map(
            lambda glyphConstruct: Glyph(glyphConstruct['ordinal'], glyphConstruct['pixels']),
            Font.BinarySaveFormat.parse(data),
        ))

    def ordinals(self) -> List[int]:
        return sorted(list(map(
            lambda glyph: glyph._ordinal,  
            self._glyphs,
        )))

    def glyphWithOrdinal(self,
        ordinal: int,
    ) -> Glyph:
        result = list(filter(
            lambda glyph: glyph._ordinal == ordinal,
            self._glyphs,
        ))

        if result == []:
            return None
        
        return result[0]

if __name__ == '__main__':
    font = Font()
    font.glyphWithOrdinal(ord('a')).toggle(1, 1, True)
    serialized = font.toBytes()

    font = Font()
    font.fromBytes(serialized)
    assert font.glyphWithOrdinal(ord('a')).isOn(1,1)
