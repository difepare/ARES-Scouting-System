import yagmail

EMAIL_ARES = "diegof.palomino@gmail.com"        # <--- TU CORREO
PASSWORD_APP = "ylcu nrbn fezd szrl"     # <--- TU CONTRASEÑA DE 16 DÍGITOS
EMAIL_DESTINO = "diegof.palomino@gmail.com"     # <--- DONDE QUIERES RECIBIR LA ALERTA

try:
    yag = yagmail.SMTP(EMAIL_ARES, PASSWORD_APP)
    yag.send(
        to=EMAIL_DESTINO,
        subject="🔔 ARES - Prueba de notificación",
        contents="Si estás leyendo esto, ARES puede enviarte correos. ¡El sistema está listo!"
    )
    print("✅ Correo de prueba enviado correctamente.")
except Exception as e:
    print(f"❌ Error al enviar: {e}")