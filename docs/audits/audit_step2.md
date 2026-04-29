# Audit de sécurité — Étape 2 : Chiffrement symétrique simple (César / Vigenère)

## Description
Implémentation des chiffrements César et Vigenère sur les messages du chat.

## Vulnérabilités identifiées

### V1 — Clé hardcodée dans le code source (HAUTE)
- **Description** : La clé est écrite en dur dans `client.py`
- **Preuve** : `CESAR_KEY = 3` et `VIGENERE_KEY = "guardia"` visibles dans le code
- **Détection** : Bandit lève une alerte **B105 HIGH**
- **Impact** : Toute personne ayant accès au code a la clé

### V2 — César : espace des clés insuffisant (CRITIQUE)
- **Description** : Seulement 25 clés possibles
- **Impact** : Cassable par force brute en moins d'une milliseconde
- **Preuve** : Script `crack_cesar.py` casse la clé en 26 essais

### V3 — Vigenère : vulnérable à l'analyse de fréquences (HAUTE)
- **Description** : La répétition cyclique de la clé crée des patterns statistiques
- **Impact** : Cassable par analyse de fréquences sur texte suffisamment long
- **Preuve** : Script `crack_vigenere.py` estime la longueur de clé via l'IC

### V4 — Absence d'intégrité (CRITIQUE)
- **Description** : Aucun mécanisme d'authentification des messages
- **Impact** : Les messages peuvent être modifiés sans détection

## Tableau CIA

| Propriété | Statut | Détail |
|-----------|--------|--------|
| Confidentialité | ⚠️ | Faible — cassable facilement |
| Intégrité | ❌ | Aucune vérification |
| Disponibilité | ⚠️ | Pas de protection DoS |

## Remédiation
- Ne jamais hardcoder les clés — utiliser des variables d'environnement
- Remplacer César/Vigenère par AES-GCM — voir Étape 4
