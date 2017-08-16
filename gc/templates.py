#!/usr/bin/env python3

"""
Template snippets for constructing an epub ebook.
"""

__author__ = "Greg Reeve"
__version__ = "0.1.0"
__license__ = "MIT"


MIMETYPE = """application/epub+zip"""

CONTAINER = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
    <rootfiles>
        <rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>"""

PACKAGE = """<?xm version="1.0" encoding="utf-8" standalone="no"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:dcterms="http://purl.org/dc/terms/" version="3.0" xml:lang="en"
unique-identifier="bookid">
<metadata>
    <dc:identifier id="bookid">urn:uuid:{uuid}</dc:identifier>
    <dc:title id="pub-title">{month} {year} Conference Report</dc:title>
    <dc:language id="pub-language">en</dc:language>
    <dc:date>{date}</dc:date> <!-- yyyy-mm-dd -->
    <meta property="dcterms:modified">{date}T15:30:00Z</meta>
    <dc:creator id="pub-creator12">Greg Reeve</dc:creator>
    <dc:contributor>The Church of Jesus Christ of Latter-day Saints</dc:contributor>
    <dc:publisher>The Church of Jesus Christ of Latter-day Saints</dc:publisher>
    <dc:rights>Copyright © {year} The Church of Jesus Christ of Latter-day Saints</dc:rights>
</metadata>
<manifest>
    <item href="xhtml/title.xhtml" id="title" media-type="application/xhtml+xml"/>
    <item href="xhtml/nav.xhtml" id="nav" media-type="application/xhtml+xml" properties="nav"/>
    {items}
</manifest>
<spine>
    <itemref idref="title"/>
    <itemref idref="nav" linear="no"/>
    {refs}
</spine>
</package>"""

PACKAGE_ITEM_LANG_PART = """
    <item href="xhtml/{lang}.xhtml" id="{lang}" media-type="application/xhtml+xml" />"""

PACKAGE_ITEM_LANG = """
    <item href="xhtml/{lang}/{filename}" id="{fileid}" media-type="application/xhtml+xml"/>"""

PACKAGE_REF_LANG_PART = """
    <itemref idref="{lang}" />"""

PACKAGE_REF_LANG = """
    <itemref idref="{fileid}" />"""

LANG_PART = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
        <meta charset="utf-8" />
        <title>{language} Conference Addresses</title>
    </head>
    <body>
        <section class="part" title="{language} Conference Addresses" epub:type="part">
            <h1>{language} Conference Addresses</h1>
        </section>
    </body>
</html>"""

TITLE = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset="utf-8"/>
        <title>{month} {year} Conference Report</title>
    </head>
    <body>
        <h1 class="titlepage">{month} {year} Conference Report</h1>
        <div class="legalnotice">
            <p>This edition is not affiliated with The Church of Jesus Christ of Latter-day Saints in any way. Any errors in this edition are the responsibility of the author.</p>
        </div>
    </body>
</html>"""

NAV = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
        <meta charset="utf-8" />
        <title>{month} {year} Conference Report - Table of Contents</title>
    </head>
    <body>
        <nav epub:type="toc" id="toc">
            <h1 class="title">Table of Contents</h1>
            <ol>
                {contents}
            </ol>
        </nav>
    </body>
</html>"""

NAV_LANG = """
                <li><a href="{lang}.xhtml">{language} Conference Addresses</a>
                    <ol>
                        {talks}
                    </ol>
                </li>"""

NAV_TALK = """
                        <li><a href="{lang}/{filename}">{author} - {title}</a></li>"""

TALK = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
        <meta charset="utf-8" />
        <title>{title}</title>
    </head>
    <body>
        <section class="chapter" title="{title}" epub:type="chapter">
            {body}
        </section>
    </body>
</html>"""
