#!/usr/bin/env python3
"""Zet de inhoudsvingerafdruk van stijl.css achter elke verwijzing ernaar.

Waarom dit bestaat. Een browser die stijl.css al eens heeft opgehaald, houdt hem vast:
de naam verandert immers niet. Bij een gewone tekstwijziging valt dat niet op, maar bij
een verbouwing wel, want dan krijgt de bezoeker nieuwe HTML met de oude opmaak. Op
5 september 2026 kostte dat vier rondes heen en weer, met twee keer de conclusie "dit
klopt voor geen meter" terwijl de site op de server allang goed stond.

Verversen helpt, maar dat kun je niet aan een bezoeker vragen. Een vingerafdruk in de
URL wel: verandert het bestand, dan verandert de URL, en dan is de oude kopie niet meer
van toepassing. Verandert het bestand niet, dan blijft de URL gelijk en blijft de cache
gewoon werken.

Draaien vóór elke push waarin stijl.css is gewijzigd.
"""
import re
import sys
import hashlib
import pathlib

HIER = pathlib.Path(__file__).resolve().parent
STIJL = HIER / "stijl.css"


def main():
    merk = hashlib.sha256(STIJL.read_bytes()).hexdigest()[:8]
    patroon = re.compile(r'(href="stijl\.css)(\?v=[0-9a-f]+)?(")')
    geraakt = []
    for pad in sorted(HIER.glob("*.html")):
        tekst = pad.read_text(encoding="utf-8")
        nieuw = patroon.sub(r'\1?v=%s\3' % merk, tekst)
        if nieuw != tekst:
            pad.write_text(nieuw, encoding="utf-8")
            geraakt.append(pad.name)
    print("stijl.css draagt merk %s" % merk)
    print("bijgewerkt: %s" % (", ".join(geraakt) if geraakt else "niets, stond al goed"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
