# A curated list of LDS speeches.

## Sources

- [General Conference Addresses](https://www.lds.org/general-conference/conferences?lang=eng)
- [CES Devotionals](https://www.lds.org/broadcasts/archive/ces-devotionals/2014/01?lang=eng)
- [Worldwide Devotionals](https://www.lds.org/broadcasts/archive/worldwide-devotionals/2016/01?lang=eng)
- [BYU Devotionals](https://speeches.byu.edu)
- [BYU Idaho Devotionals](https://web.byui.edu/devotionalsandspeeches/)

## EPUB Creation

Example commands to create an epub manually:

    zip -0Xq cr-2016-04.epub mimetype
    zip -Xr9Dq cr-2016-04.epub *

## Conference Report Creation

- `python core.py download YYYY MM`
- `python core.py convert YYYY MM`
- `python core.py publish YYYY MM`
