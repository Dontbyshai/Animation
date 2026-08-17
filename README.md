# TikTok Math & Science Animations 🎬📊

Bienvenue dans ce projet de création d'animations générées par code, optimisées pour **TikTok / Reels / Shorts** (format vertical 9:16). Ce projet utilise la bibliothèque Python **Manim** pour produire des visuels mathématiques et scientifiques de haute qualité, ultra-dynamiques et précis.

## 🌟 Ce que fait ce projet
Il génère des vidéos explicatives courtes (30-50 secondes) sur des concepts complexes, vulgarisés à travers des animations fluides, des formules mathématiques (LaTeX) et des graphiques.

### 🎥 Scripts disponibles :

1. **`bitcoin_math.py`** (Bitcoin)
   - *Sujet :* Le fonctionnement cryptographique du Bitcoin (Courbes elliptiques, hachage, blocs).
   - *Visuels :* Formules de l'ECDSA, courbe de secp256k1, Satoshi Nakamoto.
   
2. **`trading_math.py`** (Finance / Trading)
   - *Sujet :* Pourquoi perdre 50% demande de gagner 100% pour se refaire.
   - *Visuels :* Chute en cascade des pourcentages, courbe exponentielle de composition.
   
3. **`birthday_paradox.py`** (Probabilités)
   - *Sujet :* Le paradoxe des anniversaires (pourquoi 23 personnes suffisent pour avoir ~50% de chance d'avoir la même date).
   - *Visuels :* Cercles de personnes, compteurs de combinaisons explosifs (253 paires).
   
4. **`monty_hall.py`** (Maths contre-intuitives)
   - *Sujet :* Le problème des 3 portes de Monty Hall.
   - *Visuels :* Portes avec chèvres et voiture, simulation de 10 000 parties en direct.
   
5. **`avalanche_effect.py`** (Cybersécurité)
   - *Sujet :* L'effet avalanche dans le hash SHA-256 (Cybersécurité).
   - *Visuels :* "bitcoin" vs "Bitcoin", comparaison des bits, distance de Hamming.
   
6. **`time_dilation.py`** (Physique)
   - *Sujet :* La dilatation du temps près d'un trou noir.
   - *Visuels :* Déformation de la grille de l'espace-temps, horloges désynchronisées, rayon de Schwarzschild.
   
7. **`llm_tokens.py`** (Intelligence Artificielle)
   - *Sujet :* Comment un LLM (comme ChatGPT) devine le prochain mot.
   - *Visuels :* Tokens, espace latent vectoriel, Matrice d'Attention (Q, K, V), et calcul Softmax.

## 🛠 Prérequis et Utilisation

### Prérequis
- Python 3.9+
- `manim` (la version communautaire)
- FFmpeg (pour le rendu vidéo)
- LaTeX (pour le rendu des formules)

### Comment lancer un rendu ?
Pour générer une vidéo, activez votre environnement virtuel et lancez la commande manim en ciblant la classe correspondante :

```bash
# Activation de l'environnement virtuel (Mac/Linux)
source venv/bin/activate

# Rendu d'une scène spécifique (Ex: Paradoxe des anniversaires)
manim render birthday_paradox.py BirthdayParadox
```

Les vidéos générées seront disponibles dans le dossier `media/videos/`.

## 🎨 Direction Artistique
- **Format :** 1080x1920 (9:16) à 60 FPS
- **Fond :** Noir profond (`#000000`)
- **Couleurs :** Orange Bitcoin, Cyan, Vert Néon, Blanc, Rouge, Jaune.
- **Style :** Pas de voix-off nécessaire, pensé pour être accompagné de musiques dynamiques (Phonk/Sigma). Tout est basé sur le mouvement visuel !
