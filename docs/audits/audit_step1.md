# Audit de sécurité — Étape 1 : Communication en clair

## Description
Serveur TCP multi-clients sans aucun chiffrement.

## Vulnérabilités identifiées

### V1 — Absence de confidentialité (CRITIQUE)
- **Description** : Tous les messages transitent en clair sur le réseau
- **Preuve** : Capture Wireshark montrant `Mahmoud: Ca va et toi` lisible directement
- **Impact** : N'importe qui sur le réseau peut lire toutes les communications
- **CVSS Score** : 9.1 (Critical)

### V2 — Absence d'intégrité (CRITIQUE)
- **Description** : Aucun mécanisme de vérification de l'intégrité des messages
- **Impact** : Un attaquant peut modifier les messages en transit sans détection

### V3 — Absence d'authentification (HAUTE)
- **Description** : Impossible de vérifier l'identité des participants
- **Impact** : N'importe qui peut se connecter et usurper une identité

## Tableau CIA

| Propriété | Statut | Détail |
|-----------|--------|--------|
| Confidentialité | ❌ | Messages lisibles en clair |
| Intégrité | ❌ | Aucune vérification |
| Disponibilité | ⚠️ | Pas de protection DoS |

## Remédiation
Implémenter un algorithme de chiffrement — voir Étape 2.
