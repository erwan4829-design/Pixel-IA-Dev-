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
    <title>IA Multi-Fonctions v1.2.6</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c20 0%, #15102a 100%); color: #ffffff; margin: 0; padding: 0; min-height: 100vh; }
        
        /* Menu Hamburger Épique */
        .hamburger-btn { font-size: 32px; background: none; border: none; color: #00d2ff; cursor: pointer; padding: 15px; position: fixed; top: 0; left: 0; z-index: 100; transition: 0.3s; }
        .sidebar { position: fixed; top: 0; left: -280px; width: 280px; height: 100%; background: rgba(20, 15, 35, 0.95); backdrop-filter: blur(10px); transition: 0.3s; padding-top: 70px; box-shadow: 4px 0 20px rgba(0,0,0,0.7); z-index: 99; border-right: 2px solid #00d2ff; }
        .sidebar.active { left: 0; }
        .sidebar h3 { color: #00d2ff; text-align: center; font-size: 20px; }
        .sidebar a, .sidebar button { display: block; width: 100%; padding: 15px 20px; background: none; border: none; color: #cbd5e1; text-align: left; font-size: 16px; cursor: pointer; text-decoration: none; box-sizing: border-box; }
        .sidebar a:hover, .sidebar button:hover { background: rgba(0, 210, 255, 0.1); color: #00f6ff; }
        
        .container { max-width: 800px; margin: 80px auto; padding: 20px; text-align: center; box-sizing: border-box; }
        .card { background: rgba(30, 25, 50, 0.6); padding: 30px; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.05); backdrop-filter: blur(5px); }
        h2 { background: linear-gradient(90deg, #00d2ff, #00f6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        input, select, textarea { width: 100%; padding: 12px; margin: 12px 0; border: 1px solid rgba(0, 210, 255, 0.3); background: #110b22; color: white; border-radius: 8px; box-sizing: border-box; }
        button.action-btn { background: linear-gradient(90deg, #ff4757, #ff6b81); color: white; border: none; padding: 14px 28px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4); }
        button.audio-btn { background: linear-gradient(90deg, #2ed573, #7bed9f); color: white; border: none; padding: 12px 24px; font-size: 15px; border-radius: 8px; cursor: pointer; margin-top: 15px; font-weight: bold; display: none; box-shadow: 0 4px 15px rgba(46, 213, 115, 0.4); }
        
        /* Zone de la Barre de Progression Intégrée */
        .loader-box { display: none; background: #05020c; padding: 20px; border-radius: 12px; border: 1px solid #00d2ff; margin-top: 20px; }
        .progress-bar { width: 100%; background: #110b22; height: 16px; border-radius: 8px; overflow: hidden; border: 1px solid rgba(0, 210, 255, 0.4); margin: 12px 0; }
        .progress-fill { width: 0%; height: 100%; background: linear-gradient(90deg, #00d2ff, #00ffaa); transition: 1s linear; }
        .status-text { font-family: monospace; color: #00ffaa; font-size: 14px; min-height: 24px; }
        
        #output-container { display: none; }
        #output-zone { margin-top: 25px; padding: 20px; background: #0b0718; border-radius: 8px; text-align: left; white-space: pre-wrap; line-height: 1.6; border-left: 4px solid #00d2ff; }
    </style>
</head>
<body>

    <button class="hamburger-btn" onclick="toggleMenu()">☰</button>
    <div class="sidebar" id="sidebar">
        <h3>Menu IA v1.2.6</h3>
        <hr style="border-color: rgba(0, 210, 255, 0.2);">
        <div id="hamburger-pages">
            <a href="#" onclick="showSection('ia-core')">🤖 Générateur IA</a>
            <button onclick="disconnectUser()" style="color: #ff4757;">🚪 Se déconnecter</button>
        </div>
    </div>

    <div class="container">
        <div id="sec-connexion" class="card">
            <h2>🔑 Connexion Google Account</h2>
            <input type="email" id="user-email" placeholder="Entre ton adresse @gmail.com">
            <input type="password" id="user-code" placeholder="Code secret de sécurité">
            <button class="action-btn" onclick="connectUser()">Se connecter via Google</button>
        </div>

        <div id="sec-ia-core" class="card" style="display:none;">
            <h2>🤖 Super IA Multi-Fonctions</h2>
            <label>Choisis ton module :</label>
            <select id="ia-mode">
                <option value="text">💬 Explications Textuelles</option>
                <option value="voice">🗣️ Voix Personnalisée (Grave)</option>
            </select>
            <textarea id="ia-prompt" rows="3" placeholder="Écris ta demande ici..."></textarea>
            <button class="action-btn" id="generate-btn" onclick="launchIA()">Lancer la génération 🚀</button>
            
            <div class="loader-box" id="analysis-loader-box">
                <div class="status-text" id="loader-status">Initialisation de l'analyse...</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="my-bar"></div>
                </div>
                <div style="font-family: monospace; color: #888; font-size: 13px;" id="loader-timer">Analyse en cours : 60s restantes</div>
            </div>

            <div id="output-container">
                <h3>Résultat de l'IA :</h3>
                <div id="output-zone">En attente...</div>
                <button id="speak-btn" class="audio-btn" onclick="speakOutput()">🔊 Écouter la réponse</button>
            </div>
        </div>
    </div>

    <script>
        let lastTextToSpeak = "";

        window.onload = function() {
            if (localStorage.getItem("ia_user_connected") === "true") {
                document.getElementById('sec-connexion').style.display = 'none';
                document.getElementById('sec-ia-core').style.display = 'block';
            }
        }

        function toggleMenu() { document.getElementById('sidebar').classList.toggle('active'); }

        function showSection(sectionId) {
            document.getElementById('sec-connexion').style.display = 'none';
            document.getElementById('sec-ia-core').style.display = 'none';
            document.getElementById('sec-' + sectionId).style.display = 'block';
            toggleMenu();
        }

        function connectUser() {
            const email = document.getElementById('user-email').value.trim();
            if (!email.toLowerCase().endsWith("@gmail.com")) return alert("Utilise un e-mail @gmail.com !");
            localStorage.setItem("ia_user_connected", "true");
            alert("Connexion enregistrée !");
            document.getElementById('sec-connexion').style.display = 'none';
            document.getElementById('sec-ia-core').style.display = 'block';
        }

        function disconnectUser() {
            localStorage.removeItem("ia_user_connected");
            location.reload();
        }

        function launchIA() {
            const mode = document.getElementById('ia-mode').value;
            const prompt = document.getElementById('ia-prompt').value.toLowerCase().trim();
            const generateBtn = document.getElementById('generate-btn');
            const loaderBox = document.getElementById('analysis-loader-box');
            const outputContainer = document.getElementById('output-container');
            const bar = document.getElementById('my-bar');
            const status = document.getElementById('loader-status');
            const timerText = document.getElementById('loader-timer');
            const speakBtn = document.getElementById('speak-btn');
            const output = document.getElementById('output-zone');

            if(!prompt) return alert("Écris quelque chose !");

            outputContainer.style.display = 'none';
            generateBtn.style.display = 'none';
            loaderBox.style.display = 'block';
            
            let timeLeft = 60;
            bar.style.width = "0%";

            let interval = setInterval(() => {
                timeLeft--;
                bar.style.width = (((60 - timeLeft) / 60) * 100) + "%";
                timerText.innerText = "Analyse en cours : " + timeLeft + "s restantes";

                if (timeLeft === 30) {
                    status.innerText = "🔑 [SECRET ARRIVÉ] : Déchiffrement des paquets informatiques...";
                }
                else if (timeLeft <= 0) {
                    clearInterval(interval);
                    loaderBox.style.display = 'none';
                    generateBtn.style.display = 'block';
                    outputContainer.style.display = 'block';

                    let textResult = "Voici la réponse experte complète : pour coder votre projet efficacement, vous devez initialiser vos scripts de boucle et synchroniser vos bases de données en arrière-plan.";
                    output.innerHTML = "💬 <b>Réponse de l'IA :</b><br>" + textResult;
                    lastTextToSpeak = textResult;
                    if(mode === 'voice') speakBtn.style.display = 'inline-block';
                }
                else if (timeLeft > 30) {
                    status.innerText = "⚡ Analyse des mots-clés...";
                }
                else {
                    status.innerText = "🛸 Compilation des données de l'espace...";
                }
            }, 1000);
        }

        function speakOutput() {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                let u = new SpeechSynthesisUtterance(lastTextToSpeak);
                u.lang = 'fr-FR'; u.pitch = 0.55; u.rate = 0.88;
                window.speechSynthesis.speak(u);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
