# Audit de sécurité — Étape 4 : AES-GCM + Échange de clé

## Description
Implémentation du chiffrement AES-256-GCM avec échange de clé via le serveur.

## Améliorations apportées

| Propriété | Étape 2 | Étape 4 |
|-----------|---------|---------|
| Algorithme | César/Vigenère | AES-256-GCM |
| Confidentialité | ⚠️ Faible | ✅ Forte |
| Intégrité | ❌ | ✅ Authentication tag |
| Nonce | ❌ | ✅ 96 bits aléatoires |

## Vulnérabilités identifiées

### V1 — Échange de clé en clair (CRITIQUE)
- **Description** : La clé AES est transmise en clair lors de la connexion
- **Impact** : Un attaquant MITM peut intercepter la clé et déchiffrer tout le trafic
- **Preuve** : Démonstration à l'Étape 5

### V2 — Absence d'authentification des participants (HAUTE)
- **Description** : Impossible de vérifier l'identité du serveur ou des clients
- **Impact** : Vulnérable à l'usurpation d'identité

## Tableau CIA

| Propriété | Statut | Détail |
|-----------|--------|--------|
| Confidentialité | ✅ | AES-256-GCM |
| Intégrité | ✅ | Authentication tag 16 octets |
| Disponibilité | ⚠️ | Pas de protection DoS |

## Remédiation
Sécuriser l'échange de clé avec RSA — voir Étape 6.
