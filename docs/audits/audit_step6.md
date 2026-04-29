# Audit de sécurité — Étape 6 : RSA + AES-GCM (Chiffrement hybride)

## Description
Implémentation du chiffrement hybride RSA-2048 + AES-256-GCM.
La clé AES n'est plus échangée en clair — elle est chiffrée avec RSA.

## Architecture de sécurité

Serveur génère clé AES-256 aléatoire
Chaque client génère sa paire RSA-2048
Client envoie sa clé publique RSA au serveur
Serveur chiffre la clé AES avec la clé publique RSA du client
Client reçoit la clé AES chiffrée et la déchiffre avec sa clé privée
Chat chiffré AES-256-GCM


## Améliorations apportées

| Propriété | Étape 4 | Étape 6 |
|-----------|---------|---------|
| Échange de clé | En clair ❌ | Chiffré RSA ✅ |
| Résistance MITM | ❌ | ✅ |
| Confidentialité | ✅ | ✅ |
| Intégrité | ✅ | ✅ |

## Pourquoi RSA-OAEP ?

RSA sans padding (textbook RSA) est vulnérable :
- Déterministe — même message = même chiffré
- Malléable — l'attaquant peut modifier le chiffré
- Attaquable par exposant faible

OAEP ajoute de l'aléatoire et une structure cryptographique robuste.

## Vulnérabilités résiduelles

### V1 — Absence de PKI (MOYENNE)
- **Description** : Pas d'infrastructure à clés publiques
- **Impact** : Un attaquant sophistiqué pourrait substituer sa propre clé publique
- **Remédiation** : Certificats signés par une autorité de certification (CA)

### V2 — Clés non persistantes (FAIBLE)
- **Description** : Les clés RSA sont régénérées à chaque démarrage
- **Impact** : Pas de continuité de l'identité entre les sessions

## Tableau CIA final

| Propriété | Statut | Détail |
|-----------|--------|--------|
| Confidentialité | ✅ | AES-256-GCM |
| Intégrité | ✅ | Authentication tag + RSA-OAEP |
| Disponibilité | ⚠️ | Pas de protection DoS |
| Authentification | ⚠️ | Partielle — sans PKI |

## Conclusion
Le chiffrement hybride RSA+AES-GCM est la solution industrielle standard.
C'est exactement ce qu'utilise TLS/HTTPS pour sécuriser le web.
