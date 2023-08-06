Gene Enrichment using Python package GSEApy.

Ausführung:
python GeneEnrichment.py --Custom True --gmt /Pfad/zum/gmtfile --gene_list /Pfad/zur/Tabelle/csvfile (optional: --ranked True)

Gmt file beinhaltet Beschreibung von Pathways, Datenbank und alle beinhalteten Gene mit Tabs getrennt. Beispiel einer Zeile:
http://identifiers.org/kegg.pathway/hsa00020	name: Citrate cycle (TCA cycle); datasource: kegg; organism: 9606; idtype: hgnc symbol	ACLY	ACO1	ACO2	CS	DLAT	DLD	DLST	FH	IDH1	IDH2	IDH3A	IDH3B	IDH3G	MDH1	OGDH	OGDHL	PC	PCK2	PDHB	SDHA	SUCLA2	SUCLG1	SUCLG2												

Die csv Datei beinhaltet die untersuchten Gene. Die drei notwendigen Spalten, die benötigt werden, lauten: "fisher_p_withinCluster", "fisher_q_withinCluster" und "geneID" und sind jeweils der p-Wert, der q-Wert und die ID des untersuchten Gens.

Die erforderten Bibliotheken findet man in requirements.txt
