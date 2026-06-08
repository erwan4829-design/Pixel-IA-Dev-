import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

DATA_STORE = {
    "pages": ["Accueil", "Historique IA"],
    "historique": []
}

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA Multi-Fonctions v1.0.2</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #121212; color: #ffffff; margin: 0; padding: 0; }
        .hamburger-btn { font-size: 30px; background: none; border: none; color: white; cursor: pointer; padding: 15px; position: fixed; top: 0; left: 0; z-index: 100; }
        .sidebar { position: fixed; top: 0; left: -250px; width: 250px; height: 100%; background: #1e1e1e; transition: 0.3s; padding-top: 60px; box-shadow: 2px 0 5px rgba(0,0,0,0.5); z-index: 99; }
        .sidebar.active { left: 0; }
        .sidebar a, .sidebar button { display: block; width: 100%; padding: 15px; background: none; border: none; color: #bbb; text-align: left; font-size: 16px; cursor: pointer; text-decoration: none; }
        .sidebar a:hover, .sidebar button:hover { background: #2a2a2a; color: white; }
        .container { max-width: 800px; margin: 80px auto; padding: 20px; text-align: center; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-bottom: 20px; }
        input, select, textarea { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #333; background: #252525; color: white; border-radius: 5px; }
        button.action-btn { background: #ff4757; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 5px; cursor: pointer; font-weight: bold; }
        button.action-btn:hover { background: #ff6b81; }
        button.audio-btn { background: #2ed573; color: white; border: none; padding: 10px 20px; font-size: 14px; border-radius: 5px; cursor: pointer; margin-top: 10px; font-weight: bold; display: none; }
        button.audio-btn:hover { background: #26af5f; }
        #output-zone { margin-top: 20px; padding: 15px; background: #252525; border-radius: 5px; min-height: 50px; text-align: left; white-space: pre-wrap; }
        .code-box { background: #000; color: #00ff00; font-family: monospace; padding: 10px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>

    <button class="hamburger-btn" onclick="toggleMenu()">☰</button>
    <div class="sidebar" id="sidebar">
        <h3 style="color: white; text-align: center;">Menu Hamburger</h3>
        <hr style="border-color: #333;">
        <div id="hamburger-pages">
            <a href="#" onclick="showSection('connexion')">🔑 Connexion (Email/Code)</a>
            <a href="#" onclick="showSection('ia-core')">🤖 Générateur IA</a>
            <a href="#" onclick="showSection('creer-page')">📄 Ajouter une page LPD</a>
        </div>
    </div>

    <div class="container">
        <div id="sec-connexion" class="card">
            <h2>🔑 Accès Version 1.0.2</h2>
            <input type="email" id="user-email" placeholder="Entre ton adresse email">
            <input type="password" id="user-code" placeholder="Entre ton code d'accès">
            <button class="action-btn" onclick="connectUser()">Se connecter</button>
        </div>

        <div id="sec-ia-core" class="card" style="display:none;">
            <h2>🤖 Super IA Multi-Fonctions</h2>
            
            <label>Choisis ce que l'IA doit fabriquer :</label>
            <select id="ia-mode">
                <option value="text">💬 Texte Standard</option>
                <option value="voice">🗣️ Voix Personnalisée (Garçon/Grasse)</option>
                <option value="image">🖼️ Générer une Image</option>
                <option value="video">🎬 Clip Vidéo (Max 3 secondes)</option>
                <option value="code_python">🐍 Code Python</option>
                <option value="code_js">🌐 Code JavaScript</option>
                <option value="code_unity">🎮 Code Unity (C#)</option>
                <option value="code_roblox">🧱 Code Roblox (Lua)</option>
            </select>

            <textarea id="ia-prompt" rows="4" placeholder="Écris ta demande ici..."></textarea>
            
            <button class="action-btn" onclick="launchIA()">Lancer la génération 🚀</button>
            
            <h3>Résultat de l'IA :</h3>
            <div id="output-zone">En attente de tes ordres...</div>
            <button id="speak-btn" class="audio-btn" onclick="speakOutput()">🔊 Écouter la réponse</button>
        </div>

        <div id="sec-creer-page" class="card" style="display:none;">
            <h2>📄 Créer une nouvelle page LPD</h2>
            <input type="text" id="new-page-title" placeholder="Nom de ta nouvelle page">
            <textarea id="new-page-content" rows="4" placeholder="Contenu ou code de la page..."></textarea>
            <button class="action-btn" onclick="createNewPage()">Ajouter au Hamburger</button>
        </div>
    </div>

    <script>
        let lastTextToSpeak = "";

        function toggleMenu() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showSection(sectionId) {
            document.getElementById('sec-connexion').style.display = 'none';
            document.getElementById('sec-ia-core').style.display = 'none';
            document.getElementById('sec-creer-page').style.display = 'none';
            document.getElementById('sec-' + sectionId).style.display = 'block';
            toggleMenu();
        }

        function connectUser() {
            const email = document.getElementById('user-email').value;
            const code = document.getElementById('user-code').value;
            if(email && code) {
                alert("Connexion réussie sur la version 1.0.2 !");
                document.getElementById('sec-connexion').style.display = 'none';
                document.getElementById('sec-ia-core').style.display = 'block';
            } else {
                alert("Rentre ton adresse email et ton code d'accès !");
            }
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
                container.appendChild(link);
                document.getElementById('new-page-title').value = '';
                document.getElementById('new-page-content').value = '';
            });
        }

        function launchIA() {
            const mode = document.getElementById('ia-mode').value;
            const prompt = document.getElementById('ia-prompt').value;
            const output = document.getElementById('output-zone');
            const speakBtn = document.getElementById('speak-btn');

            if(!prompt) { output.innerText = "Dis-moi ce que je doit faire !"; return; }

            output.innerText = "⚡ Génération en cours par l'IA...";
            speakBtn.style.display = 'none';

            setTimeout(() => {
                if(mode === 'text' || mode === 'voice') {
                    let responseText = "Voici l'analyse de ta demande : " + prompt;
                    if(mode === 'voice') {
                        output.innerHTML = "🗣️ <b>Génération Vocale (Voix Garçon Grave activée) :</b><br>" + responseText;
                    } else {
                        output.innerHTML = "💬 <b>Réponse Textuelle :</b><br>" + responseText;
                    }
                    lastTextToSpeak = responseText;
                    speakBtn.style.display = 'inline-block'; // Afficher le bouton micro/audio !
                } 
                else if(mode === 'image') {
                    output.innerHTML = `🖼️ <b>Image Générée :</b><br><div style="width:100%; height:200px; background:#444; border-radius:5px; display:flex; align-items:center; justify-content:center;">[Image IA : ${prompt}]</div>`;
                }
                else if(mode === 'video') {
                    output.innerHTML = `🎬 <b>Vidéo IA (3 secondes) :</b><br><div style="width:100%; height:200px; background:#000; border-radius:5px; display:flex; align-items:center; justify-content:center; color:red;">⏳ Clip de 3s : ${prompt}</div>`;
                }
                else if(mode.startsWith('code_')) {
                    let lang = mode.split('_')[1].toUpperCase();
                    output.innerHTML = `💻 <b>Bloc de Code Généré (${lang}) :</b><br><pre class="code-box">// Code pour ${lang}\\n// Requête : ${prompt}\\n\\nfunction init() {\\n    // Prêt\\n}</pre>`;
                }
            }, 1000);
        }

        // Système de lecture vocale automatique (Voix de garçon / Grave)
        function speakOutput() {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel(); // Stopper si déjà en cours
                let utterance = new SpeechSynthesisUtterance(lastTextToSpeak);
                utterance.lang = 'fr-FR';
                
                // Réglage de la voix : pitch plus bas (grave) et vitesse normale
                utterance.pitch = 0.6; 
                utterance.rate = 0.9;
                
                window.speechSynthesis.speak(utterance);
            } else {
                alert("Désolé, ton téléphone ne supporte pas la synthèse vocale !");
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
    
