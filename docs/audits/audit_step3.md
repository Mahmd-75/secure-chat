# Audit de sécurité — Étape 3 : Cryptanalyse

## Description
Attaque des chiffrements César et Vigenère sans connaissance préalable de la clé.

## Attaques réalisées

### A1 — Force brute sur César
- **Méthode** : Test exhaustif des 26 clés possibles
- **Résultat** : Clé 3 trouvée instantanément
- **Temps** : < 1 milliseconde
- **Outil** : `docs/crack_cesar.py`

### A2 — Analyse de fréquences sur Vigenère
- **Méthode** : Indice de coïncidence + analyse lettre par lettre
- **Résultat** : Longueur de clé 7 trouvée (IC = 0.091), clé `guardio` au lieu de `guardia`
- **Limite** : Nécessite 300+ caractères pour être fiable
- **Outil** : `docs/crack_vigenere.py`

## Concepts démontrés

| Concept | Explication |
|---------|-------------|
| COA (Ciphertext Only Attack) | On ne dispose que du texte chiffré capturé sur Wireshark |
| Indice de coïncidence | Français IC ≈ 0.074 / Aléatoire IC ≈ 0.038 |
| Analyse de fréquences | E est la lettre la plus fréquente en français (17.39%) |

## Conclusion
César et Vigenère sont des algorithmes historiques sans valeur sécuritaire moderne.
Ils démontrent les principes fondamentaux mais ne doivent jamais être utilisés en production.

## Remédiation
Utiliser AES-GCM — standard NIST depuis 2001 — voir Étape 4.
