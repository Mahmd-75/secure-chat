# Audit de sécurité — Étape 5 : Attaque Man In The Middle (MITM)

## Description
Démonstration d'une attaque MITM exploitant la faiblesse de l'échange de clé de l'Étape 4.

## Déroulement de l'attaque
Client A → MITM (port 5557) → Serveur (port 5556)
Client B → MITM (port 5557) → Serveur (port 5556)

### Phase 1 — Interception de la clé
- L'attaquant écoute sur le port 5557
- Il relaie les connexions vers le vrai serveur
- Lors de l'échange, la clé AES passe en clair → interceptée

### Phase 2 — Déchiffrement en temps réel
- L'attaquant possède la clé AES
- Il déchiffre tous les messages des deux clients
- Les victimes ne détectent rien

### Phase 3 — Modification des messages
- L'attaquant peut modifier n'importe quel message
- Il rechiffre le message modifié avec la même clé AES
- La victime reçoit le faux message sans pouvoir le détecter

## Résultats

| Action | Résultat |
|--------|---------|
| Interception clé AES | ✅ Réussie |
| Lecture messages en clair | ✅ Réussie |
| Modification messages | ✅ Réussie |
| Détection par les victimes | ❌ Impossible |

## Conclusion
Le chiffrement seul ne suffit pas. Sans authentification des participants,
un attaquant peut s'intercaler et compromettre toute la communication.

## Remédiation
Utiliser RSA pour sécuriser l'échange de clé — voir Étape 6.
