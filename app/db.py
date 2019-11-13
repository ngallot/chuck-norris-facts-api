"""Fake database to simulate calls to a real database. Here, database composed of a dictionary of id -> value"""
DB = {
    0: "Chuck Norris a déjà compté jusqu'à l'infini. Deux fois.",
    1: "Google, c'est le seul endroit où tu peux taper Chuck Norris...",
    2: "Certaines personnes portent un pyjama Superman. Superman porte un pyjama Chuck Norris.",
    3: "Chuck Norris donne fréquemment du sang à la Croix-Rouge. Mais jamais le sien.",
    4: "Chuck Norris et Superman ont fait un bras de fer, le perdant devait mettre son slip par dessus son pantalon.",
    5: "Chuck norris se souvient très bien de son futur",
    6: "Peter Parker a été mordu par une araignée, Clark Kent a été mordu par Chuck Norris",
    7: "Chuck Norris peut écrire un traitement de texte avec la souris.",
    8: "Chuck Norris peut faire des ronds avec une equerre",
    9: " La seule chose qui arrive à la cheville de Chuck Norris... c'est sa chaussette."
}


def get_next_id():
    return max(DB.keys()) + 1
