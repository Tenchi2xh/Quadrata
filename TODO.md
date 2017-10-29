# TODO

- Separate character from glyph name
  Right now, the name of a glyph is the same as the character it maps to.
  Have a better system, as we don't want something like `æ.glif`
- Support for ligatures ([`features.fea`](http://unifiedfontobject.org/versions/ufo3/features.fea/))
- Calculate and store width of letters
- Kerning system
- Full fledged letter preview
    - Shows lines (ascending, descending, capheight, xheight, width, ..)
    - Produces an HTML file with the svg in it for styling
    - Remove style from path itself, do it in CSS
    - On hover: hide lines, use fill instead
- Variable angle
