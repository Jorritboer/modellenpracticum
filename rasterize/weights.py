from layer import Layer

layers = [
    Layer(
        gml_filename="bgt_waterdeel.gml",
        layer_name="Waterdeel",
        features=[("water", "", 126)],
    ),
    Layer(
        gml_filename="bgt_ondersteunendwaterdeel.gml",
        layer_name="OndersteunendWaterdeel",
        # name is not 'oever_slootkant' for some reason
        # 2
        features=[
            ("oever-slootkant", "class = 'oever, slootkant'", 126),
            ("slik", "class = slik", 126),
        ],
    ),
    Layer(
        gml_filename="bgt_wegdeel.gml",
        layer_name="wegdeel",
        features=[  # 20
            ("voetpad", "function = 'voetpad'", 10),
            ("parkeervlak", "function = 'parkeervlak'", 50),
            ("spoorbaan", "function = 'spoorbaan'", 126),
            ("overweg", "function = 'overweg'", 125),
            ("voetgangersgebied", "function = 'voetgangersgebied'", 10),
            ("voetpad-op-trap", "function = 'voetpad op trap'", 10),
            ("fietspad", "function = 'fietspad'", 20),
            ("rijbaan-autoweg", "function = 'rijbaan autoweg'", 40),
            ("rijbaan-lokale-weg", "function = 'rijbaan lokale weg'", 50),
            ("rijbaan-regionale-weg", "function = 'rijbaan regionale weg'", 80),
            ("baan-voor-vliegverkeer", "function = 'baan voor vliegverkeer'", 126),
            ("rijbaan-autosnelweg", "function = 'rijbaan autosnelweg'", 126),
            ("inrit", "function = 'inrit'", 10),
            ("woonerf", "function = 'woonerf'", 10),
            ("ruiterpad", "function = 'ruiterpad'", 10),
            ("ov-baan", "function = 'ov baan'", 30),
            ("open-verharding", "surfaceMaterial = 'open verharding'", 2),
            ("half-verhard", "surfaceMaterial = 'half verhard'", 3),
            ("onverhard", "surfaceMaterial = 'onverhard'", 4),
            ("gesloten-verharding", "surfaceMaterial = 'gesloten verharding'", 5),
        ],
    ),
    Layer(
        gml_filename="bgt_ondersteunendwegdeel.gml",
        layer_name="AuxiliaryTrafficArea",
        features=[  # 7
            ("verkeerseiland", "function = 'verkeerseiland", 10),
            ("berm", "function = 'berm", -10),
            ("groenvoorziening", "surfaceMaterial = 'groenvoorziening'", -10),
            ("half-verhard", "surfaceMaterial = 'half verhard'", 5),
            ("onverhard", "surfaceMaterial = 'onverhard'", 3),
            ("open-verharding", "surfaceMaterial = 'open verharding'", 3),
            ("gesloten-verharding", "surfaceMaterial = 'gesloten verharding'", 7),
        ],
    ),
    Layer(
        gml_filename="bgt_onbegroeidterreindeel.gml",
        layer_name="OnbegroeidTerreindeel",
        features=[  # 6
            ("zand", "`bgt-fysiekVoorkomen` = 'zand'", 10),
            ("erf", "`bgt-fysiekVoorkomen` = 'erf'", 126),
            ("half-verhard", "`bgt-fysiekVoorkomen` = 'half verhard'", 126),
            ("onverhard", "`bgt-fysiekVoorkomen` = 'onverhard'", 10),
            ("open-verharding", "`bgt-fysiekVoorkomen` = 'open verharding'", 10),
            (
                "gesloten-verharding",
                "`bgt-fysiekVoorkomen` = 'gesloten verharding'",
                10,
            ),
        ],
    ),
    Layer(
        gml_filename="bgt_begroeidterreindeel.gml",
        layer_name="begroeidterreindeel",
        features=[  # 16
            ("grasland-overig", "class = 'grasland overig'", 10),
            ("heide", "class = 'heide'", 120),
            ("moeras", "class = 'moeras'", 119),
            ("grasland-agrarisch", "class = 'grasland agrarisch'", 120),
            ("fruitteelt", "class = 'fruitteelt'", 120),
            ("boomteelt", "class = 'boomteelt'", 120),
            ("kwelder", "class = 'kwelder'", 120),
            ("groenvoorziening", "class = 'groenvoorziening'", 10),
            ("naaldbos", "class = 'naaldbos'", 120),
            ("rietland", "class = 'rietland'", 120),
            ("houtwal", "class = 'houtwal'", 120),
            ("bouwland", "class = 'bouwland'", 120),
            ("struiken", "class = 'struiken'", 10),
            ("gemengd_bos", "class = 'gemengd bos'", 120),
            ("loofbos", "class = 'loofbos'", 120),
            ("duin", "class = 'duin'", 120),
        ],
    ),
    Layer(
        gml_filename="bgt_pand.gml",
        layer_name="pand",
        # 1
        features=[
            # TODO: niet punten
            ("pand", None, 120)
        ],  # no where clause because all objects should be taken
    ),
    Layer(
        gml_filename="bgt_vegetatieobject.gml",
        layer_name="SolitaryVegetationObject",
        features=[  # 3
            ("boom", "`plus-type` = 'boom'", 80),
            ("haag", "`plus-type` = 'haag'", 80),
            (
                "waarde_onbekend",
                "`plus-type` = 'waardeOnbekend'",
                80,
            ),  # don't know if it's 'waardeOnbekend' or 'waarde onbekend'
        ],
    ),
    Layer(
        gml_filename="bgt_scheiding.gml",
        layer_name="Scheiding",
        features=[  # 7
            ("hek", "`bgt-type` = 'hek'", 5),
            ("damwand", "`bgt-type` = 'damwand", 5),
            ("geluidsscherm", "`bgt-type` = 'geluidsscherm'", 5),
            (
                "niet_bgt",
                "`bgt-type` = 'niet-bgt'",
                5,
            ),  # not sure if it's 'niet-bgt' or 'niet bgt'
            ("kademuur", "`bgt-type` = 'kademuur'", 120),
            ("walbescherming", "`bgt-type` = 'walbescherming'", 5),
            ("muur", "`bgt-type` = 'muur'", 5),
        ],
    ),
    Layer(
        gml_filename="bgt_functioneelgebied.gml", layer_name="?", features=[]
    ),  # cannot find layers
]
