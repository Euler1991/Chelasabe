# data.py — Catálogos de Chelasabe

# ── Cervezas comerciales (8) ──────────────────────────────────────────────────
# Selección que cubre el espectro: rubias, oscuras, malta, sin alcohol, importadas
CERVEZAS_COMERCIALES = [
    {
        "id": "corona",
        "nombre": "Corona Extra",
        "estilo": "Lager adjunto (clara)",
        "abv": 4.5,
        "desc": "La más internacional de México. Ligera, refrescante, poco maltosa.",
    },
    {
        "id": "modelo_esp",
        "nombre": "Modelo Especial",
        "estilo": "Lager Pilsner (clara)",
        "abv": 4.4,
        "desc": "Ligera con algo más de cuerpo que Corona. La más vendida del país.",
    },
    {
        "id": "pacifico",
        "nombre": "Pacífico Clara",
        "estilo": "Lager adjunto (clara)",
        "abv": 4.5,
        "desc": "Suave y refrescante, con ligero sabor a malta y lúpulo discreto.",
    },
    {
        "id": "victoria",
        "nombre": "Victoria",
        "estilo": "Lager Viena (ámbar)",
        "abv": 4.0,
        "desc": "Color ámbar suave, maltosa, dulce, con ligero carácter de malta tostada.",
    },
    {
        "id": "negra_modelo",
        "nombre": "Negra Modelo",
        "estilo": "Dunkel / Munich Dark",
        "abv": 5.4,
        "desc": "Oscura, maltosa, notas de caramelo y café suave. Referente oscura nacional.",
    },
    {
        "id": "indio",
        "nombre": "Indio",
        "estilo": "Lager Premium (clara)",
        "abv": 4.1,
        "desc": "Clara, ligera y muy refrescante. Más seca que Modelo.",
    },
    {
        "id": "heineken",
        "nombre": "Heineken",
        "estilo": "European Pale Lager",
        "abv": 5.0,
        "desc": "Importada holandesa. Algo más lupulada y amarga que las nacionales.",
    },
    {
        "id": "xx_oscura",
        "nombre": "Dos Equis Ámbar",
        "estilo": "Vienna Lager",
        "abv": 4.7,
        "desc": "Color ámbar rojizo, cuerpo medio, notas de caramelo y lúpulo equilibrado.",
    },
]

# ── Estilos artesanales (8 total) ─────────────────────────────────────────────
ESTILOS_ARTESANAL = {
    "🌾 Lager": [
        {
            "id": "mexican_lager",
            "nombre": "Mexican Craft Lager",
            "desc": "Como las comerciales pero con mejor materia prima. Refrescante, limpia, ideal para iniciar.",
        },
        {
            "id": "vienna_lager",
            "nombre": "Vienna Lager",
            "desc": "Ámbar, maltosa, con notas de pan y caramelo. Base de muchas artesanales mexicanas.",
        },
        {
            "id": "pilsner",
            "nombre": "Czech/German Pilsner",
            "desc": "Clara, bien lupulada, floral o herbal. Más amarga y aromática que una lager comercial.",
        },
    ],
    "🍂 Ale": [
        {
            "id": "pale_ale",
            "nombre": "Pale Ale / APA",
            "desc": "Clara a dorada, cítrica o floral por el lúpulo americano. Amarga moderada. Gran puerta de entrada.",
        },
        {
            "id": "ipa",
            "nombre": "IPA (India Pale Ale)",
            "desc": "Lupulada al máximo — cítrico, tropical, resinoso. Alta amargura. Para paladares aventureros.",
        },
        {
            "id": "stout_porter",
            "nombre": "Stout / Porter",
            "desc": "Oscura, con chocolate, café, caramelo tostado. Robusta y compleja. El lado oscuro delicioso.",
        },
        {
            "id": "wheat_beer",
            "nombre": "Wheat Beer / Witbier",
            "desc": "Turbia, ligera, con notas de trigo, cítrico (naranja), cilantro. Muy refrescante.",
        },
    ],
    "🍇 Belgas / Levadúrgicos": [
        {
            "id": "belgian_ale",
            "nombre": "Belgian Ale / Saison",
            "desc": "Perfil único de la levadura: especiado, frutal (pera, banana), seco y complejo. Totalmente diferente.",
        },
    ],
}

# ── Notas de aroma ────────────────────────────────────────────────────────────
NOTAS_AROMA = [
    "🍋 Cítrico (limón, naranja, toronja)",
    "🌸 Floral",
    "🌿 Herbal / Vegetal",
    "🍍 Tropical (mango, piña, maracuyá)",
    "🍞 Pan / Galleta / Malta",
    "☕ Café / Tostado",
    "🍫 Chocolate",
    "🍬 Caramelo / Dulce",
    "🌶️ Especiado",
    "🍌 Frutal (banana, pera, manzana)",
    "🌾 Cereal / Trigo",
    "🍷 Frutas oscuras (ciruela, uva, pasas)",
]

# ── Notas de sabor ────────────────────────────────────────────────────────────
NOTAS_SABOR = [
    "😋 Dulce",
    "😣 Amargo",
    "😌 Seco / Seco-amargo",
    "🧂 Salado (mineral)",
    "😮 Ácido / Agrio",
    "🍬 Caramelizado",
    "☕ Tostado / Ahumado",
    "🍫 Achocolatado",
    "🌿 Herbal",
    "🍋 Cítrico / Frutal fresco",
    "🍇 Frutal maduro",
    "🌶️ Especiado / Picante",
    "🥛 Cremoso / Lácteo",
]
