# Secure Chat — GCS2-UE7-3 DevSecOps

Serveur de discussion sécurisé développé progressivement de la communication en clair jusqu'au chiffrement hybride RSA+AES-GCM, dans un environnement DevSecOps complet.

**Guardia Cybersecurity School — 2025-2026**

---

## Équipe

| Rôle | Responsabilités |
|------|----------------|
| Lead Developer | Architecture technique, revues de code |
| Security Officer | Pipeline Bandit/Safety, rapports d'audit |
| Ops | Docker, docker-compose, infrastructure |
| Project Manager | Suivi planning, contact intervenant |

---

## Stack technique

- Python 3 — socket, threading
- Module cryptography — AES-GCM, RSA-OAEP
- Docker + docker-compose
- Gitea + Act Runner (CI/CD)
- Wireshark (captures réseau)
- Bandit (SAST), Safety (SCA)

---

## Lancement en une commande

```bash
