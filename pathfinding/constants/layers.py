from ..classes.tile_attribute import TileAttribute
from ..classes.layer import Feature, Layer

layers = [
    Layer(
        gml_filename="bgt_waterdeel.gml",
        layer_name="waterdeel",
        features=[Feature("water", None, TileAttribute.Waterdeel, 126)],
    ),
    Layer(
        gml_filename="bgt_ondersteunendwaterdeel.gml",
        layer_name="ondersteunendwaterdeel",
        # name is not 'oever_slootkant' for some reason
        # 2
        features=[
            Feature(
                "oever-slootkant",
                "class = 'oever, slootkant'",
                TileAttribute.OndersteunendWaterdeel_OeverSlootkant,
                126,
            ),
            Feature(
                "slik", "class = 'slik'", TileAttribute.OndersteunendWaterdeel_Slik, 126
            ),
        ],
    ),
    Layer(
        gml_filename="bgt_wegdeel.gml",
        layer_name="wegdeel",
        features=[  # 20
            Feature(
                "voetpad", "function = 'voetpad'", TileAttribute.Wegdeel_Voetpad, 10
            ),
            Feature(
                "parkeervlak",
                "function = 'parkeervlak'",
                TileAttribute.Wegdeel_Parkeervlak,
                50,
            ),
            Feature(
                "spoorbaan",
                "function = 'spoorbaan'",
                TileAttribute.Wegdeel_Spoorbaan,
                126,
            ),
            Feature(
                "overweg", "function = 'overweg'", TileAttribute.Wegdeel_Overweg, 125
            ),
            Feature(
                "voetgangersgebied",
                "function = 'voetgangersgebied'",
                TileAttribute.Wegdeel_Voetgangersgebied,
                10,
            ),
            Feature(
                "voetpad-op-trap",
                "function = 'voetpad op trap'",
                TileAttribute.Wegdeel_VoetpadOpTrap,
                10,
            ),
            Feature(
                "fietspad", "function = 'fietspad'", TileAttribute.Wegdeel_Fietspad, 20
            ),
            Feature(
                "rijbaan-autoweg",
                "function = 'rijbaan autoweg'",
                TileAttribute.Wegdeel_RijbaanAutoweg,
                40,
            ),
            Feature(
                "rijbaan-lokale-weg",
                "function = 'rijbaan lokale weg'",
                TileAttribute.Wegdeel_RijbaanLokaleWeg,
                50,
            ),
            Feature(
                "rijbaan-regionale-weg",
                "function = 'rijbaan regionale weg'",
                TileAttribute.Wegdeel_RijbaanLokaleWeg,
                80,
            ),
            Feature(
                "baan-voor-vliegverkeer",
                "function = 'baan voor vliegverkeer'",
                TileAttribute.Wegdeel_BaanVoorVliegverkeer,
                126,
            ),
            Feature(
                "rijbaan-autosnelweg",
                "function = 'rijbaan autosnelweg'",
                TileAttribute.Wegdeel_RijbaanAutosnelweg,
                126,
            ),
            Feature(
                "inrit",
                "function = 'inrit'",
                TileAttribute.Wegdeel_RijbaanAutosnelweg,
                10,
            ),
            Feature(
                "woonerf", "function = 'woonerf'", TileAttribute.Wegdeel_Woonerf, 10
            ),
            Feature(
                "ruiterpad",
                "function = 'ruiterpad'",
                TileAttribute.Wegdeel_Ruiterpad,
                10,
            ),
            Feature(
                "ov-baan", "function = 'ov baan'", TileAttribute.Wegdeel_OvBaan, 30
            ),
            Feature(
                "open-verharding",
                "surfaceMaterial = 'open verharding'",
                TileAttribute.Wegdeel_OpenVerharding,
                2,
            ),
            Feature(
                "half-verhard",
                "surfaceMaterial = 'half verhard'",
                TileAttribute.Wegdeel_HalfVerhard,
                3,
            ),
            Feature(
                "onverhard",
                "surfaceMaterial = 'onverhard'",
                TileAttribute.Wegdeel_Onverhard,
                4,
            ),
            Feature(
                "gesloten-verharding",
                "surfaceMaterial = 'gesloten verharding'",
                TileAttribute.Wegdeel_GeslotenVerharding,
                5,
            ),
        ],
    ),
    Layer(
        gml_filename="bgt_ondersteunendwegdeel.gml",
        layer_name="ondersteunendwegdeel",
        features=[  # 7
            Feature(
                "verkeerseiland",
                "function = 'verkeerseiland'",
                TileAttribute.OndersteunendWegdeel_Verkeerseiland,
                10,
            ),
            Feature(
                "berm",
                "function = 'berm'",
                TileAttribute.OndersteunendWegdeel_Berm,
                1,
            ),
            Feature(
                "groenvoorziening",
                "surfaceMaterial = 'groenvoorziening'",
                TileAttribute.OndersteunendWegdeel_Groenvoorziening,
                1,
            ),
            Feature(
                "half-verhard",
                "surfaceMaterial = 'half verhard'",
                TileAttribute.OndersteunendWegdeel_HalfVerhard,
                5,
            ),
            Feature(
                "onverhard",
                "surfaceMaterial = 'onverhard'",
                TileAttribute.OndersteunendWegdeel_Onverhard,
                3,
            ),
            Feature(
                "open-verharding",
                "surfaceMaterial = 'open verharding'",
                TileAttribute.OndersteunendWegdeel_OpenVerharding,
                3,
            ),
            Feature(
                "gesloten-verharding",
                "surfaceMaterial = 'gesloten verharding'",
                TileAttribute.OndersteunendWegdeel_GeslotenVerharding,
                7,
            ),
        ],
    ),
    Layer(
        gml_filename="bgt_onbegroeidterreindeel.gml",
        layer_name="onbegroeidterreindeel",
        features=[  # 6
            Feature(
                "zand",
                "`bgt-fysiekVoorkomen` = 'zand'",
                TileAttribute.OnbegroeidTerreindeel_Zand,
                10,
            ),
            Feature(
                "erf",
                "`bgt-fysiekVoorkomen` = 'erf'",
                TileAttribute.OnbegroeidTerreindeel_Erf,
                126,
            ),
            Feature(
                "half-verhard",
                "`bgt-fysiekVoorkomen` = 'half verhard'",
                TileAttribute.OnbegroeidTerreindeel_HalfVerhard,
                126,
            ),
            Feature(
                "onverhard",
                "`bgt-fysiekVoorkomen` = 'onverhard'",
                TileAttribute.OnbegroeidTerreindeel_Onverhard,
                10,
            ),
            Feature(
                "open-verharding",
                "`bgt-fysiekVoorkomen` = 'open verharding'",
                TileAttribute.OnbegroeidTerreindeel_OpenVerharding,
                10,
            ),
            Feature(
                "gesloten-verharding",
                "`bgt-fysiekVoorkomen` = 'gesloten verharding'",
                TileAttribute.OnbegroeidTerreindeel_GeslotenVerharding,
                10,
            ),
        ],
    ),
    Layer(
        gml_filename="bgt_begroeidterreindeel.gml",
        layer_name="begroeidterreindeel",
        features=[  # 16
            Feature(
                "grasland-overig",
                "class = 'grasland overig'",
                TileAttribute.BegroeidTerreindeel_GraslandOverig,
                10,
            ),
            Feature(
                "heide", "class = 'heide'", TileAttribute.BegroeidTerreindeel_Heide, 120
            ),
            Feature(
                "moeras",
                "class = 'moeras'",
                TileAttribute.BegroeidTerreindeel_Moeras,
                119,
            ),
            Feature(
                "grasland-agrarisch",
                "class = 'grasland agrarisch'",
                TileAttribute.BegroeidTerreindeel_GraslandAgrarisch,
                120,
            ),
            Feature(
                "fruitteelt",
                "class = 'fruitteelt'",
                TileAttribute.BegroeidTerreindeel_Fruitteelt,
                120,
            ),
            Feature(
                "boomteelt",
                "class = 'boomteelt'",
                TileAttribute.BegroeidTerreindeel_Boomteelt,
                120,
            ),
            Feature(
                "kwelder",
                "class = 'kwelder'",
                TileAttribute.BegroeidTerreindeel_Kwelder,
                120,
            ),
            Feature(
                "groenvoorziening",
                "class = 'groenvoorziening'",
                TileAttribute.BegroeidTerreindeel_Groenvoorziening,
                10,
            ),
            Feature(
                "naaldbos",
                "class = 'naaldbos'",
                TileAttribute.BegroeidTerreindeel_Naaldbos,
                120,
            ),
            Feature(
                "rietland",
                "class = 'rietland'",
                TileAttribute.BegroeidTerreindeel_Rietland,
                120,
            ),
            Feature(
                "houtwal",
                "class = 'houtwal'",
                TileAttribute.BegroeidTerreindeel_Houtwal,
                120,
            ),
            Feature(
                "bouwland",
                "class = 'bouwland'",
                TileAttribute.BegroeidTerreindeel_Bouwland,
                120,
            ),
            Feature(
                "struiken",
                "class = 'struiken'",
                TileAttribute.BegroeidTerreindeel_Struiken,
                10,
            ),
            Feature(
                "gemengd_bos",
                "class = 'gemengd bos'",
                TileAttribute.BegroeidTerreindeel_Gemengd_bos,
                120,
            ),
            Feature(
                "loofbos",
                "class = 'loofbos'",
                TileAttribute.BegroeidTerreindeel_Loofbos,
                120,
            ),
            Feature(
                "duin", "class = 'duin'", TileAttribute.BegroeidTerreindeel_Duin, 120
            ),
        ],
    ),
    Layer(
        gml_filename="bgt_pand.gml",
        layer_name="pand",
        # 1
        features=[
            # TODO: niet punten
            Feature("pand", None, TileAttribute.Pand, 120)
        ],  # no where clause because all objects should be taken
    ),
    Layer(
        gml_filename="bgt_vegetatieobject.gml",
        layer_name="vegetatieobject",
        features=[  # 3
            Feature(
                "boom", "`plus-type` = 'boom'", TileAttribute.Vegetatieobject_Boom, 80
            ),
            Feature(
                "haag", "`plus-type` = 'haag'", TileAttribute.Vegetatieobject_Haag, 80
            ),
            Feature(
                "waarde-onbekend",
                "`plus-type` = 'waardeOnbekend'",
                TileAttribute.Vegetatieobject_WaardeOnbekend,
                80,
            ),  # don't know if it's 'waardeOnbekend' or 'waarde onbekend'
        ],
    ),
    Layer(
        gml_filename="bgt_scheiding.gml",
        layer_name="scheiding",
        features=[  # 7
            Feature("hek", "`bgt-type` = 'hek'", TileAttribute.Scheiding_Hek, 5),
            Feature(
                "damwand", "`bgt-type` = 'damwand'", TileAttribute.Scheiding_Damwand, 5
            ),
            Feature(
                "geluidsscherm",
                "`bgt-type` = 'geluidsscherm'",
                TileAttribute.Scheiding_Geluidsscherm,
                5,
            ),
            Feature(
                "niet-bgt",
                "`bgt-type` = 'niet-bgt'",
                TileAttribute.Scheiding_Geluidsscherm,
                5,
            ),  # not sure if it's 'niet-bgt' or 'niet bgt'
            Feature(
                "kademuur",
                "`bgt-type` = 'kademuur'",
                TileAttribute.Scheiding_Kademuur,
                120,
            ),
            Feature(
                "walbescherming",
                "`bgt-type` = 'walbescherming'",
                TileAttribute.Scheiding_Walbescherming,
                5,
            ),
            Feature("muur", "`bgt-type` = 'muur'", TileAttribute.Scheiding_Muur, 5),
        ],
    ),
    Layer(
        gml_filename="bgt_functioneelgebied.gml",
        layer_name="functioneelgebied",
        features=[],
    ),  # cannot find layers
]
