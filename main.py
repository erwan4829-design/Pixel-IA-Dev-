import os
import time
import random
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Base de données de réponses aléatoires pour simuler une vraie IA multi-fonctions
IA_RESPONSES = {
    "texte": [
        "Après analyse approfondie de tes circuits graphiques, voici la solution optimale pour ton projet.",
        "Le protocole réseau indique une compatibilité maximale avec tes scripts actuels.",
        "Requête traitée avec succès. Les performances du système mobile sont à 100% de leurs capacités.",
        "Analyse terminée. Ton environnement de développement est parfaitement synchronisé.",
        "Voici les explications demandées : le système Flask répond instantanément à tes exigences."
    ],
    "banania": [
        "Mode Banania activé ! Énergie maximale injectée dans les serveurs ! 🍌",
        "Protocole Banania en ligne : optimisation jaune et survitaminée pour ton code !",
        "Choc thermique Banania ! Les performances de traitement viennent de doubler.",
        "Banania IA : 'Tout est au top, Maître, prêt à lancer la puissance maximum !'"
    ],
    "images": [
        "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800", # Image abstraite futuriste
        "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=800", # Dégradé design
        "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=800", # Technologie cyber
        "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800"  # Univers spatial retro
    ],
    "videos": [
        "https://www.w3schools.com/html/mov_bbb.mp4", # Ours d'animation (vrai fichier vidéo)
        "https://www.w3schools.com/html/movie.mp4"    # Clip de test de film (vrai fichier vidéo)
    ]
}

# Interface HTML/CSS/JS unique ultra-optimisée pour mobile
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super IA Multi-Fonctions v1.8.9.1.0.1</title>
    <style>
        :root {
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --accent-color: #00d2ff;
            --btn-color: #ff5e62;
            --text-color: #ffffff;
            --border-color: #30363d;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }

        /* Barre de navigation supérieure */
        header {
            width: 100%;
            background-color: var(--card-bg);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            box-sizing: border-box;
            position: relative;
        }

        .burger-menu {
            font-size: 24px;
            cursor: pointer;
            color: var(--accent-color);
            user-select: none;
        }

        .search-container {
            flex: 1;
            margin: 0 15px;
            position: relative;
        }

        .search-bar {
            width: 100%;
            background-color: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 8px 15px;
            color: var(--text-color);
            box-sizing: border-box;
            outline: none;
        }

        .search-bar:focus {
            border-color: var(--accent-color);
        }

        /* Menu déroulant latéral Burger */
        .nav-panel {
            position: absolute;
            top: 60px;
            left: -250px;
            width: 230px;
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 10px 0;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
            transition: left 0.3s ease;
            z-index: 100;
            display: flex;
            flex-direction: column;
            padding: 10px 0;
        }

        .nav-panel.open {
            left: 0;
        }

        .nav-item {
            padding: 12px 20px;
            color: var(--text-color);
            text-decoration: none;
            font-weight: bold;
            display: flex;
            align-items: center;
            cursor: pointer;
            border-bottom: 1px solid #21262d;
        }

        .nav-item:hover {
            background-color: var(--bg-color);
            color: var(--accent-color);
        }

        /* Conteneur principal */
        .container {
            width: 100%;
            max-width: 450px;
            padding: 20px;
            box-sizing: border-box;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        h1 {
            color: var(--accent-color);
            font-size: 22px;
            margin-top: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .subtitle {
            font-size: 14px;
            color: #8b949e;
            margin-bottom: 20px;
        }

        label {
            display: block;
            text-align: left;
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 14px;
        }

        select, textarea {
            width: 100%;
            background-color: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            color: var(--text-color);
            box-sizing: border-box;
            margin-bottom: 20px;
            font-size: 14px;
            outline: none;
        }

        select:focus, textarea:focus {
            border-color: var(--accent-color);
        }

        textarea {
            resize: none;
            height: 100px;
        }

        .btn-submit {
            background-color: var(--btn-color);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 14px;
            width: 100%;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(255, 94, 98, 0.4);
            transition: background 0.2s;
        }

        .btn-submit:active {
            background-color: #e04f53;
        }

        /* Module de chargement / Timer */
        .timer-box {
            display: none;
            background-color: var(--bg-color);
            border: 1px solid var(--accent-color);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }

        .timer-title {
            color: #ff5e62;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .progress-bar-bg {
            width: 100%;
            background-color: #21262d;
            border-radius: 10px;
            height: 12px;
            overflow: hidden;
            margin-bottom: 8px;
        }

        .progress-bar-fill {
            width: 0%;
            background-color: var(--accent-color);
            height: 100%;
            transition: width 1s linear;
        }

        .timer-text {
            font-size: 13px;
            color: #8b949e;
        }

        /* Section Résultats */
        .result-box {
            display: none;
            background-color: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            text-align: left;
            word-wrap: break-word;
        }

        .result-box img, .result-box video {
            width: 100%;
            border-radius: 8px;
            margin-top: 10px;
            border: 1px solid var(--border-color);
        }
    </style>
</head>
<body>

    <header>
        <div class="burger-menu" onclick="toggleMenu()">☰</div>
        <div class="search-container">
            <input type="text" class="search-bar" placeholder="Rechercher un module...">
        </div>
        <div style="font-weight: bold; color: var(--accent-color);">v1.8.9</div>

        <!-- Menu Burger de Gauche -->
        <div class="nav-panel" id="navPanel">
            <div class="nav-item" onclick="createNewPage()">📄 Nouvelle Page</div>
            <div class="nav-item" onclick="toggleMenu()">➕ Ajouter Module</div>
            <div class="nav-item" onclick="location.reload()">🔄 Actualiser l'IA</div>
        </div>
    </header>

    <div class="container">
        <div class="card">
            <h1>🤖 Super IA Multi-Fonctions</h1>
            <div class="subtitle">Version Pro 1.8.9.1.0.1 — Mode Direct</div>

            <form id="iaForm" onsubmit="handleGeneration(event)">
                <label>Choisis ton module de traitement :</label>
                <select id="moduleSelect">
                    <option value="texte">💬 Texte Standard / Explications</option>
                    <option value="banania">🍌 Mode Banania spécial</option>
                    <option value="images">🖼️ Générateur d'Images Réelles</option>
                    <option value="videos">🎬 Générateur de Vidéos Réelles (15s)</option>
                </select>

                <label>Écris ta demande ici :</label>
                <textarea id="promptInput" placeholder="Pose ta question ou décris ton image/vidéo..."></textarea>

                <button type="submit" class="btn-submit">Lancer la génération 🚀</button>
            </form>

            <!-- Boîte de traitement et Compteur dynamique -->
            <div class="timer-box" id="timerBox">
                <div class="timer-title" id="timerTitle">Analyse des mots-clés...</div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" id="progressBar"></div>
                </div>
                <div class="timer-text" id="timerText">Analyse en cours : --s restantes</div>
            </div>

            <!-- Boîte de Résultat -->
            <div class="result-box" id="resultBox">
                <strong style="color: var(--accent-color);">Réponse de l'IA :</strong>
                <div id="resultContent" style="margin-top: 10px; line-height: 1.5;"></div>
            </div>
        </div>
    </div>

    <script>
        // Gestion de l'affichage du menu burger
        function toggleMenu() {
            document.getElementById('navPanel').classList.toggle('open');
        }

        // Action bouton "Nouvelle Page"
        function createNewPage() {
            document.getElementById('promptInput').value = '';
            document.getElementById('resultBox').style.display = 'none';
            document.getElementById('timerBox').style.display = 'none';
            toggleMenu();
            alert("Nouvelle page blanche prête pour tes tests, Maître !");
        }

        // Traitement de la génération avec minuteurs personnalisés
        function handleGeneration(event) {
            event.preventDefault();
            
            const moduleSelected = document.getElementById('moduleSelect').value;
            const promptValue = document.getElementById('promptInput').value.trim();

            if (!promptValue) {
                alert("Écris d'abord quelque chose dans la case, mon ami !");
                return;
            }

            // Détermination précise du temps requis selon tes règles de calcul
            let durationSeconds = 2; // Temps par défaut pour le texte
            if (moduleSelected === 'images') {
                durationSeconds = 30;
            } else if (moduleSelected === 'videos') {
                // Pour 15 secondes max de vidéo, traitement configuré à 10 minutes (600 secondes) !
                durationSeconds = 600; 
            }

            // Masquer l'ancien résultat et afficher le compteur
            document.getElementById('resultBox').style.display = 'none';
            const timerBox = document.getElementById('timerBox');
            const progressBar = document.getElementById('progressBar');
            const timerText = document.getElementById('timerText');
            const timerTitle = document.getElementById('timerTitle');

            timerBox.style.display = 'block';
            progressBar.style.width = '0%';
            
            if (moduleSelected === 'videos') {
                timerTitle.innerText = "Traitement vidéo lourd en cours (Vrai fichier)...";
            } else if (moduleSelected === 'images') {
                timerTitle.innerText = "Génération de l'image réelle haute définition...";
            } else {
                timerTitle.innerText = "Analyse informatique ultra-rapide...";
            }

            let timeLeft = durationSeconds;
            timerText.innerText = `Analyse en cours : ${timeLeft}s restantes`;

            // Lancement de l'animation de la barre de chargement
            setTimeout(() => {
                progressBar.style.transition = `width ${durationSeconds}s linear`;
                progressBar.style.width = '100%';
            }, 50);

            // Compte à rebours textuel
            const interval = setInterval(() => {
                timeLeft--;
                if (timeLeft <= 0) {
                    clearInterval(interval);
                    // Lancement de la requête vers le serveur Python dès que le temps est écoulé
                    fetch('/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ module: moduleSelected, prompt: promptValue })
                    })
                    .then(res => res.json())
                    .then(data => {
                        timerBox.style.display = 'none';
                        const resultBox = document.getElementById('resultBox');
                        const resultContent = document.getElementById('resultContent');
                        
                        // Injection du vrai contenu généré
                        if (data.type === 'texte' || data.type === 'banania') {
                            resultContent.innerHTML = `<p>${data.content}</p><br><small style="color:#8b949e;">[Prompt analysé : "${data.prompt}"]</small>`;
                        } else if (data.type === 'images') {
                            resultContent.innerHTML = `<p>Voici ton image générée pour : <strong>${data.prompt}</strong></p><img src="${data.content}" alt="Génération IA">`;
                        } else if (data.type === 'videos') {
                            resultContent.innerHTML = `<p>Vidéo réelle de 15 secondes générée pour : <strong>${data.prompt}</strong></p><video controls autoplay loop><source src="${data.content}" type="video/mp4">Ton navigateur ne supporte pas les vidéos.</video>`;
                        }
                        
                        resultBox.style.display = 'block';
                    });
                } else {
                    timerText.innerText = `Analyse en cours : ${timeLeft}s restantes`;
                }
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    module = data.get('module', 'texte')
    prompt = data.get('prompt', '')

    # Sélection de la réponse correspondante dans le dictionnaire
    choices = IA_RESPONSES.get(module, IA_RESPONSES['texte'])
    content = random.choice(choices)

    # Si c'est du texte ou du banania, on ajoute un petit côté personnalisé au hasard
    if module in ['texte', 'banania']:
        content = f"{content} (Analyse complétée en direct pour pixelnomade37)."

    return jsonify({
        "type": module,
        "prompt": prompt,
        "content": content
    })

if __name__ == '__main__':
    # Écoute sur le port obligatoire fourni par Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
            
