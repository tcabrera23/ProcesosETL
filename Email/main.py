import yagmail

# Datos del remitente
email = 'tusuario@gmail.com'
contraseña = 'kqaaeibjxnfqnocy'

# Acceso
yag = yagmail.SMTP(user=email, password=contraseña)

# Mail
destinatarios = ['usuario1@gmail.com','usuario2@gmail.com']
asunto = 'Programa de prueba'
mensaje = 'Estás recibiendo un mail desde Python con un excel acerca de los precios de las casas en Boston'
adjunto = '/BostonHousePrices.csv'

# Envío
yag.send(destinatarios,asunto,mensaje,attachments=[adjunto])

