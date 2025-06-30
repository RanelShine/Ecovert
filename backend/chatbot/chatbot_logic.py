import google.generativeai as genai
from PIL import Image

def my_chat(message, image=None):
    genai.configure(api_key="AIzaSyCr3HcjVK7eeLssWCe_6jIa82j6inEPt2w") # Remplacez par votre véritable clé API Gemini

    # Initialisez le modèle, potentiellement avec des instructions système pour la redevabilité verte
    # Vous pouvez expérimenter avec différents modèles Gemini comme 'gemini-1.5-pro' ou 'gemini-1.5-flash'
    # 'gemini-1.5-pro' est généralement plus performant pour le raisonnement complexe.
    model = genai.GenerativeModel(
        'gemini-1.5-pro',
        # Ajoutez une instruction système pour guider les réponses du modèle
        system_instruction=(
            "Vous êtes un chatbot utile et informatif spécialisé dans la redevabilité verte. "
            "Fournissez des informations précises et exploitables concernant la responsabilité environnementale, "
            "les pratiques durables, le changement climatique, l'empreinte carbone, l'impact écologique, "
            "et la responsabilité sociale des entreprises (RSE) dans un contexte environnemental. "
            "Concentrez-vous sur des réponses factuelles, fondées sur des preuves. "
            "Si l'on vous pose une question en dehors de ce domaine, redirigez gentiment l'utilisateur vers des sujets liés à la redevabilité verte."
        )
    )

    try:
        if image:
            # Si une image est fournie, utilisez-la avec le message
            # Pour la redevabilité verte, les images pourraient être des produits, des étiquettes,
            # des problèmes environnementaux, etc., où le bot peut analyser et fournir un contexte.
            response = model.generate_content([message, image])
        else:
            # Si seul le texte est fourni
            response = model.generate_content(message)

        return response.text
    except Exception as e:
        # Il est bon de consigner l'erreur complète pour le débogage dans une application réelle
        print(f"Erreur lors de l'appel de l'API Gemini : {e}")
        return "Je suis désolé, je rencontre un problème technique. Veuillez réessayer plus tard."