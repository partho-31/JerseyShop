from djoser.email import ActivationEmail

class CustomActivationEmail(ActivationEmail):
    template_name ='emails/ActivationEmail.html'
