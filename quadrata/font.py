import os

from fontTools.misc.py23 import SimpleNamespace
from fontTools.svgLib import parse_path
from fontTools.pens.transformPen import TransformPen

from ufoLib.pointPen import SegmentToPointPen
from ufoLib.glifLib import writeGlyphToString
from ufoLib import UFOWriter, writePlist

from fontmake.font_project import FontProject

from .hands.foundational import foundational


def svg2glif(path, name, width=0, height=0, unicodes=None, version=2, transform=(1, 0, 0, 1, 0, 0)):
    glyph = SimpleNamespace(width=width, height=height, unicodes=unicodes)

    def drawPoints(pointPen):
        pen = TransformPen(SegmentToPointPen(pointPen), transform)
        parse_path(path, pen)

    return writeGlyphToString(name,
                              glyphObject=glyph,
                              drawPointsFunc=drawPoints,
                              formatVersion=version)


def generate_glyphs(hand):
    glyphs = []
    for character, letter in hand.glyphs.items():
        path = letter.path(hand.nib)
        glyph = svg2glif(path=path,
                         name=character,
                         width=hand.em,  # TODO: Find way to have correct width here
                         height=hand.x_height,
                         unicodes=[ord(character)],
                         transform=(1, 0, 0, -1, hand.nib.stem_width, hand.x_height))
        glyphs.append((character, glyph))
    return glyphs


def write_ufo_glyphs(glyphs, root):
    path = os.path.join

    glyphs_root = path(root, "glyphs")
    os.mkdir(glyphs_root)

    for character, glyph in glyphs:
        with open(path(root, "glyphs", "%s.glif" % character), "w") as f:
            f.write(glyph)

    with open(path(root, "glyphs", "contents.plist"), "wb") as f:
        writePlist({character: "%s.glif" % character for character, _ in glyphs}, f)

    with open(path(root, "layercontents.plist"), "wb") as f:
        writePlist([["public.default", "glyphs"]], f)


def font_info(hand):
    font_info = lambda: None
    font_info.familyName = hand.name
    font_info.styleName = "Regular"

    font_info.unitsPerEm = hand.em
    font_info.xHeight = hand.x_height
    font_info.ascender = hand.ascender
    font_info.descender = hand.descender
    font_info.capHeight = font_info.ascender  # TODO: Fix this

    return font_info


def write_ufo_font(path, hand):
    glyphs = generate_glyphs(hand)

    import shutil
    root = "%s.ufo" % path
    shutil.rmtree(root)

    writer = UFOWriter(root, fileCreator="net.team2xh.tenchi")
    writer.writeGroups({character: [character] for character in hand.glyphs})
    writer.writeInfo(font_info(hand))
    write_ufo_glyphs(glyphs, root)

    #writer._readLayerContents()

    return root


def write_binary_fonts(path, hand):
    ufo_path = write_ufo_font(path, foundational)
    builder = FontProject(verbose="ERROR")
    builder._output_dir = lambda *args, **kwargs: path
    builder.run_from_ufos([ufo_path], output=("otf", "ttf"), remove_overlaps=False)


write_binary_fonts("bin/foundational", foundational)