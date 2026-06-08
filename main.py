import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

DATA_STORE = {
    "pages": ["Accueil", "Historique IA"]
}

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA Multi-Fonctions v1.2.5</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c20 0%, #15102a 100%); color: #ffffff; margin: 0; padding: 0; min-height: 100vh; }
        
        /* Menu Hamburger Épique */
        .hamburger-btn { font-size: 32px; background: none; border: none; color: #00d2ff; cursor: pointer; padding: 15px; position: fixed; top: 0; left: 0; z-index: 100; transition: 0.3s; }
        .hamburger-btn:hover { transform: scale(1.1); color: #00f6ff; }
        .sidebar { position: fixed; top: 0; left: -280px; width: 280px; height: 100%; background: rgba(20, 15, 35, 0.95); backdrop-filter: blur(10px); transition: 0.3s; padding-top: 70px; box-shadow: 4px 0 20px rgba(0,0,0,0.7); z-index: 99; border-right: 2px solid #00d2ff; }
        .sidebar.active { left: 0; }
        .sidebar h3 { color: #00d2ff; text-align: center; font-size: 20px; letter-spacing: 1px; }
        .sidebar a, .sidebar button { display: block; width: 100%; padding: 15px 20px; background: none; border: none; color: #cbd5e1; text-align: left; font-size: 16px; cursor: pointer; text-decoration: none; box-sizing: border-box; transition: 0.2s; }
        .sidebar a:hover, .sidebar button:hover { background: rgba(0, 210, 255, 0.1); color: #00f6ff; padding-left: 30px; }
        
        /* Conteneur principal */
        .container { max-width: 800px; margin: 80px auto; padding: 20px; text-align: center; box-sizing: border-box; }
        .card { background: rgba(30, 25, 50, 0.6); padding: 30px; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.05); backdrop-filter: blur(5px); }
        h2 { background: linear-gradient(90deg, #00d2ff, #00f6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }
        
        /* Formulaires */
        input, select, textarea { width: 100%; padding: 12px; margin: 12px 0; border: 1px solid rgba(0, 210, 255, 0.3); background: #110b22; color: white; border-radius: 8px; box-sizing: border-box; font-size: 15px; transition: 0.3s; }
        input:focus, select:focus, textarea:focus { border-color: #00f6ff; box-shadow: 0 0 10px rgba(0, 246, 255, 0.3); outline: none; }
        
        /* Boutons */
        button.action-btn { background: linear-gradient(90deg, #ff4757, #ff6b81); color: white; border: none; padding: 14px 28px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.3s; box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4); }
        button.action-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 71, 87, 0.6); }
        button.audio-btn { background: linear-gradient(90deg, #2ed573, #7bed9f); color: white; border: none; padding: 12px 24px; font-size: 15px; border-radius: 8px; cursor: pointer; margin-top: 15px; font-weight: bold; display: none; transition: 0.3s; box-shadow: 0 4px 15px rgba(46, 213, 115, 0.4); }
        button.audio-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(46, 213, 115, 0.6); }
        
        /* Zone d'affichage */
        #output-zone { margin-top: 25px; padding: 20px; background: #0b0718; border-radius: 8px; min-height: 60px; text-align: left; white-space: pre-wrap; line-height: 1.6; border-left: 4px solid #00d2ff; }
        .code-box { background: #05020c; color: #00ffaa; font-family: 'Courier New', monospace; padding: 15px; border-radius: 6px; overflow-x: auto; border: 1px solid rgba(0, 255, 170, 0.2); margin-top: 10px; }
    </style>
</head>
<body>

    <button class="hamburger-btn" onclick="toggleMenu()">☰</button>
    <div class="sidebar" id="sidebar">
        <h3>Menu Hamburger</h3>
        <hr style="border-color: rgba(0, 210, 255, 0.2);">
        <div id="hamburger-pages">
            <a href="#" onclick="showSection('ia-core')">🤖 Générateur IA</a>
            <a href="#" onclick="showSection('creer-page')">📄 Ajouter une page LPD</a>
            <button onclick="disconnectUser()" style="color: #ff4757;">🚪 Se déconnecter</button>
        </div>
    </div>

    <div class="container">
        <!-- 1. SECTION CONNEXION -->
        <div id="sec-connexion" class="card">
            <h2>🔑 Connexion Google / Gmail Obligatoire (v1.2.5)</h2>
            <p style="color: #aaa; font-size: 14px;">Une fois connecté, ton compte restera enregistré sur ce téléphone.</p>
            <input type="email" id="user-email" placeholder="Entre ton adresse Gmail (ex: nom@gmail.com)">
            <input type="password" id="user-code" placeholder="Entre ton code d'accès de sécurité">
            <button class="action-btn" onclick="connectUser()">Se connecter via Google Account</button>
        </div>

        <!-- 2. SECTION CORE IA -->
        <div id="sec-ia-core" class="card" style="display:none;">
            <h2>🤖 Super IA Multi-Fonctions</h2>
            
            <label>Choisis le module de traitement :</label>
            <select id="ia-mode">
                <option value="text">💬 Texte Standard / Explications</option>
                <option value="voice">🗣️ Voix Personnalisée (Garçon/Grasse)</option>
                <option value="image">🖼️ Générer une Image</option>
                <option value="video">🎬 Clip Vidéo (Max 3 secondes)</option>
                <option value="code_python">🐍 Code Python</option>
                <option value="code_js">🌐 Code JavaScript</option>
                <option value="code_unity">🎮 Code Unity (C#)</option>
                <option value="code_roblox">🧱 Code Roblox (Lua)</option>
            </select>

            <textarea id="ia-prompt" rows="4" placeholder="Écris ta demande ici... (Ex: comment coder un saut, crée un monstre...)"></textarea>
            
            <button class="action-btn" onclick="launchIA()">Lancer la génération 🚀</button>
            
            <h3>Résultat de l'IA :</h3>
            <div id="output-zone">En attente de tes ordres...</div>
            <button id="speak-btn" class="audio-btn" onclick="speakOutput()">🔊 Écouter la réponse</button>
        </div>

        <!-- 3. SECTION CRÉER UNE PAGE LPD -->
        <div id="sec-creer-page" class="card" style="display:none;">
            <h2>📄 Créer une nouvelle page LPD</h2>
            <input type="text" id="new-page-title" placeholder="Nom de ta nouvelle page">
            <textarea id="new-page-content" rows="4" placeholder="Contenu ou code de la page..."></textarea>
            <button class="action-btn" onclick="createNewPage()">Ajouter au Hamburger</button>
        </div>
    </div>

    <script>
        let lastTextToSpeak = "";

        // Vérification de connexion automatique au démarrage de la page
        window.onload = function() {
            const savedUser = localStorage.getItem("ia_user_connected");
            if (savedUser === "true") {
                document.getElementById('sec-connexion').style.display = 'none';
                document.getElementById('sec-ia-core').style.display = 'block';
            }
        }

        function toggleMenu() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showSection(sectionId) {
            if (localStorage.getItem("ia_user_connected") !== "true") {
                alert("Tu dois d'abord te connecter !");
                return;
            }
            document.getElementById('sec-connexion').style.display = 'none';
            document.getElementById('sec-ia-core').style.display = 'none';
            document.getElementById('sec-creer-page').style.display = 'none';
            document.getElementById('sec-' + sectionId).style.display = 'block';
            toggleMenu();
        }

        function connectUser() {
            const email = document.getElementById('user-email').value.trim();
            const code = document.getElementById('user-code').value;
            
            // Vérification stricte que l'adresse finit par @gmail.com
            if (!email.toLowerCase().endsWith("@gmail.com")) {
                alert("Erreur : Tu dois utiliser une adresse email Google valide finissant par @gmail.com !");
                return;
            }

            if(email && code) {
                localStorage.setItem("ia_user_connected", "true"); // Sauvegarde la connexion !
                alert("Connexion Google réussie ! Enregistrée sur ton appareil.");
                document.getElementById('sec-connexion').style.display = 'none';
                document.getElementById('sec-ia-core').style.display = 'block';
            } else {
                alert("Rentre ton adresse Gmail et ton code d'accès !");
            }
        }

        function disconnectUser() {
            localStorage.removeItem("ia_user_connected");
            alert("Déconnexion réussie.");
            document.getElementById('sec-ia-core').style.display = 'none';
            document.getElementById('sec-creer-page').style.display = 'none';
            document.getElementById('sec-connexion').style.display = 'block';
            toggleMenu();
        }

        function createNewPage() {
            const title = document.getElementById('new-page-title').value;
            const content = document.getElementById('new-page-content').value;
            if(!title) return alert("Donne un titre à la page !");

            fetch('/api/add-page', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ title: title, content: content })
            })
            .then(res => res.json())
            .then(data => {
                alert("Page ajoutée !");
                const container = document.getElementById('hamburger-pages');
                const link = document.createElement('a');
                link.href = "#";
                link.innerText = "📄 " + title;
                link.onclick = function() {
                    document.getElementById('output-zone').innerHTML = `<h3>${title}</h3><p>${content}</p>`;
                    document.getElementById('speak-btn').style.display = 'none';
                    toggleMenu();
                };
                // Insérer avant le bouton de déconnexion
                container.insertBefore(link, container.lastElementChild);
                document.getElementById('new-page-title').value = '';
                document.getElementById('new-page-content').value = '';
            });
        }

        // Moteur d'intelligence artificielle avec réponses expertes simulées
        function launchIA() {
            const mode = document.getElementById('ia-mode').value;
            const prompt = document.getElementById('ia-prompt').value.toLowerCase().trim();
            const output = document.getElementById('output-zone');
            const speakBtn = document.getElementById('speak-btn');

            if(!prompt) { output.innerText = "Dis-moi ce que l'IA doit fabriquer !"; return; }

            output.innerHTML = "⚡ Analyse neuronale en cours par l'IA v1.2.5...";
            speakBtn.style.display = 'none';

            setTimeout(() => {
                let textResult = "";
                let htmlResult = "";

                // Générateur intelligent basé sur ce que l'utilisateur écrit
                if (mode === 'text' || mode === 'voice') {
                    if (prompt.includes("comment coder") || prompt.includes("creer un truc") || prompt.includes("comment créer")) {
                        textResult = "Pour créer un projet ou coder un élément, la méthode universelle consiste d'abord à structurer votre logique. On commence par définir les variables d'état (comme le score ou la position), puis on met en place une boucle d'exécution ou des écouteurs d'événements pour détecter les actions des utilisateurs. Ensuite, on sépare l'affichage visuel de la logique système. C'est la base absolue pour que l'application reste fluide et ne plante jamais.";
                    } else if (prompt.includes("salut") || prompt.includes("bonjour")) {
                        textResult = "Salutations ! Je suis ton intelligence artificielle v1.2.5. Je suis pleinement opérationnelle et prête à t'assister pour générer du texte informatif, du code informatique complexe pour Roblox ou Unity, ainsi que des rendus multimédias de pointe.";
                    } else {
                        textResult = "Analyse approfondie terminée. Votre requête nécessite l'activation de mes bases de données étendues. Voici la réponse optimale : l'implémentation de cette idée demande une configuration modulaire et l'application rigoureuse de scripts d'automatisation afin d'éviter les erreurs d'exécution.";
                    }

                    if(mode === 'voice') {
                        htmlResult = "🗣️ <b>Génération Vocale active :</b><br>" + textResult;
                    } else {
                        htmlResult = "💬 <b>Réponse Textuelle Experte :</b><br>" + textResult;
                    }
                    lastTextToSpeak = textResult;
                    output.innerHTML = htmlResult;
                    speakBtn.style.display = 'inline-block';
                } 
                else if(mode === 'image') {
                    output.innerHTML = `🖼️ <b>Moteur Graphique IA :</b><br><div style="width:100%; height:230px; background:linear-gradient(45deg, #1e154a, #ff4757); border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:bold; border: 2px dashed #00f6ff;">[Rendu Épique IA Généré pour : ${prompt}]</div>`;
                }
                else if(mode === 'video') {
                    output.innerHTML = `🎬 <b>Générateur Vidéo (Séquence de 3 secondes max) :</b><br><div style="width:100%; height:230px; background:#05020c; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#ff4757; font-weight:bold; border: 2px solid #ff4757;">⏳ [Clip Vidéo de 3s en boucle : ${prompt}]</div>`;
                }
                else if(mode.startsWith('code_')) {
                    let lang = mode.split('_')[1].toUpperCase();
                    let codeSnippet = "";

                    if (lang === "ROBLOX") {
                        codeSnippet = "-- Script Roblox Luas\\nlocal Player = game.Players.LocalPlayer\\nlocal Character = Player.Character or Player.CharacterAdded:Wait()\\n\\nfunction onAction()\\n    print('IA v1.2.5 active sur Roblox')\\n    Character.Humanoid.JumpPower = 60\\nend";
                    } else if (lang === "UNITY") {
                        codeSnippet = "// Script Unity C#\\nusing UnityEngine;\\n\\npublic class IACore : MonoBehaviour {\\n    void Start() {\\n        Debug.Log(\\"Système IA v1.2.5 Initialisé\\");\\n    }\\n}";
                    } else {
                        codeSnippet = "# Script Automatique " + lang + "\\ndef main_system():\\n    print('Lancement des modules de l\\'IA v1.2.5')\\n\\nif __name__ == '__main__':\\n    main_system()";
                    }

                    output.innerHTML = `💻 <b>Bloc de Code Pro Généré (${lang}) :</b><br><pre class="code-box">${codeSnippet}</pre>`;
                }
            }, 1100);
        }

        function speakOutput() {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                let utterance = new SpeechSynthesisUtterance(lastTextToSpeak);
                utterance.lang = 'fr-FR';
                utterance.pitch = 0.55; // Grosse voix de bonhomme / robot grave
                utterance.rate = 0.88;
                window.speechSynthesis.speak(utterance);
            } else {
                alert("La synthèse vocale n'est pas disponible.");
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/add-page', methods=['POST'])
def add_page():
    data = request.json
    if data and "title" in data:
        DATA_STORE["pages"].append(data["title"])
        return jsonify({"status": "success", "pages": DATA_STORE["pages"]})
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
