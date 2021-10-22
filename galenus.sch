<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron"
  queryBinding="xslt2" 
  xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
  >
  <!-- 
Schematron est une syntaxe de validation permettant d’ajouter des règles plus serrées
au schéma Relax-NG Epidoc requis par Perseus.
  -->
  <sch:ns uri="http://www.tei-c.org/ns/1.0" prefix="tei"/>
  <sch:pattern>
    <!-- Change the attribute to point the element being the context of the assert expression. -->
    <sch:rule context="tei:div/tei:div/*">
      <sch:report test="not(self::tei:head) and not(self::tei:p) and not(self::tei:pb)">Élément non prévu dans une section</sch:report>
    </sch:rule>
    <sch:rule context="tei:div/tei:p/*">
      <sch:report test="not(self::tei:lb) and not(self::tei:pb)">Dans un paragraphe, rien d’autre que des sauts de ligne et des sauts de page</sch:report>
    </sch:rule>
  </sch:pattern>
</sch:schema>
