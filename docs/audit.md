# Rapport d'audit de sécurité

## Étape 1 — Communication en clair

**Vulnérabilités :**
- Aucune confidentialité — messages lisibles dans Wireshark
- Aucune intégrité — messages modifiables en transit
- Aucune authentification — impossible de vérifier l'identité

**Preuve :** Capture Wireshark montrant les messages en clair.

---

## Étape 2 — César et Vigenère

**Vulnérabilités :**
- César : espace des clés = 25 valeurs, cassable par force brute en microsecondes
- Vigenère : cassable par analyse de fréquences sur texte suffisamment long
- Clé hardcodée dans le code source (Bandit B105 HIGH)
- Aucune intégrité — messages modifiables

**Remédiation :** Utiliser un algorithme moderne (AES-GCM).

---

## Étape 3 — Cryptanalyse

**Résultats :**
- César cassé en 25 essais, clé trouvée : 3 ✅
- Vigenère : longueur de clé estimée correctement (IC = 0.091 à longueur 7)
- Clé approximative trouvée `guardio` au lieu de `guardia`
- Limite : analyse de fréquences nécessite 300+ caractères pour être fiable

---

## Étape 4 — AES-GCM

**Améliorations :**
- Confidentialité : messages illisibles dans Wireshark ✅
- Intégrité : authentication tag AES-GCM ✅
- Nonce aléatoire unique par message ✅

**Vulnérabilité restante :**
- Clé AES échangée en clair lors de la connexion
- Un attaquant MITM peut intercepter la clé

---

## Étape 5 — Attaque MITM

**Démonstration :**
- Attaquant intercepte la clé AES lors de l'échange ✅
- Déchiffre tous les messages en temps réel ✅
- Modifie les messages à la volée ✅
- Les victimes ne détectent rien ✅

**Conclusion :** Le chiffrement seul ne suffit pas sans authentification.

---

## Étape 6 — RSA + AES-GCM

**Améliorations :**
- Chaque client génère sa paire RSA
- La clé AES est chiffrée avec RSA avant envoi
- Un attaquant MITM intercepte une clé AES chiffrée — inutilisable sans clé privée
- Confidentialité + Intégrité + Résistance MITM ✅

**Vulnérabilité restante :**
- Pas de PKI (infrastructure à clés publiques)
- Un attaquant sophistiqué pourrait substituer sa propre clé publique (MITM RSA)
- Solution : certificats signés par une autorité de certification (CA)
