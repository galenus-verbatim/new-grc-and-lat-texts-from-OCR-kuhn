"""Améliorer du latin acquis par OCR

Programme adapté au XML Galien latin, généré par odette.
Certaines fonctions sont sans doute réutilisables.
"""

import os, re, argparse

parser = argparse.ArgumentParser(description='Galenus/la, nettoyage de TEI.')
parser.add_argument(
    'srctei',
    metavar='45674x0?.xml',
    nargs='+',
    help='Un ou plusieurs fichier xml/tei'
)


# programme d’expressions régulières à appliquer dans l’ordre à un fichier XML sorti d’Odette
reg_galien = [
    # cacographie en début de ligne
    ('<space rend="tab">    </space>[^\w<>]*', ""), # cacographie, tabulation suivie de non-lettres
    ('\n *<space unit="line" quantity="1"/> *', ''), # fausse ligne vide
    ('\n *<ab type="dinkus">\*</ab> *', ''), # cacographie, un astérisme inadapté
#    (' *<hi rend="sup">[^\w\-]*\n<lb/>[^\w]*</hi> *', '\n<lb/>'), # cacographie en bout de ligne
    (' *<hi rend="(sub|sup)">([^-–\w]|\d)\n<lb/> *</hi>', '\n<lb/>'), # cacographie en bout de ligne
    (' *<hi rend="(sub|sup)">([A-Z])</hi>', '\\1'), # majuscule en exposant, on garde
    ('<hi rend="(sub|sup)">([^\w<>]|\d)</hi>', ''), # cacographie, non lettre en exposant
    ("[-—]\n<lb/>([^\s<>]+) *", '\\1\n<lb/>'), # césure autour d’un saut de ligne (attention aux balises)
    ("\s*</p>\s*(<pb[^/>]+/>)\s*<p>\s*", "\n\\1\n"), # pas de rupture de paragraphe au saut de page
    ("[-—]\n(<pb[^/>]+/>)\n([^\s]+) *", "\\2\n\\1\n"), # césure au saut de page
    ("<div>", '<div type="textpart">'), # EpiDoc TEI
    # ^\W*[CG] *a *p[\Wi]*([XIiHVΠlL]+)[,'\. ]* repérer des têtes de chapitres
]


def reg_file(file, pairs):
    path, ext = os.path.splitext(file)
    file_new = path + '_new' + ext
    with open(file, 'r', encoding='utf-8') as r:
        text_new = reg_replace(pairs, r.read())
    with open(file_new, "w") as w:
        w.write(text_new)

def reg_replace(pairs, text):
    """Boucler sur une liste de motifs de recherche/remplace

    Pas très optimisé (denmande à repasser tout le texte à chaque fois)
    Mais les autres techniques sensées optimiser sont dangereuses.
    Le programmes d’expressions régulières doit être qppliqué dans l’ordre,
    en gardant aussi l’ordre des motifs de remplacement
    (on ne peut pas optimiser avec un gros recherche concaténé).
    PHP est ici meilleur avec preg_replace
    https://www.php.net/manual/fr/function.preg-replace.php
    """
    for search, replace in pairs:
        text = re.sub(search, replace, text, 0, re.UNICODE)
    return text

args = parser.parse_args()
print(args)
for srctei in args.srctei:
    reg_file(srctei, reg_galien)
