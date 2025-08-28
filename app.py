import streamlit as st
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr
import mimetypes
import re

def enviar_emails(lista_destinatarios):
    email_remetente = st.secrets["gmail"]["email"]
    senha_app = st.secrets["gmail"]["app_password"]
    nome_remetente = st.secrets["gmail"]["nome"]

    # --- Montagem do E-mail (feito uma vez, pois o conteúdo é o mesmo para todos) ---
    assunto = "✨ Maria Madalena tem um conselho (e um convite!) para você..."
    corpo_texto = "Olá! Chega de sofrer por amor!..." # Fallback de texto puro
    corpo_html = f"""
    <html>
    <head>
        <style>
            .container {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f4f9; border-radius: 12px; text-align: center; color: #333; }}
            .content h1 {{ color: #d63384; font-size: 28px; }}
            .content p {{ font-size: 16px; line-height: 1.6; color: #555; }}
            .cta-button {{ display: inline-block; background-color: #d63384; color: #ffffff; padding: 15px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            .footer {{ margin-top: 30px; font-size: 14px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <h1>Chega de sofrer por amor!</h1>
                <p>Olá! Meu nome é <strong>Maria Madalena</strong>, sua nova conselheira amorosa com um toque de IA e muito bom humor.</p>
                <p>Seu coração está confuso? O 'dedo podre' ataca novamente? Deixa comigo! Estou aqui para te ajudar a decifrar os mistérios do coração e encontrar o caminho para um amor mais leve e divertido.</p>
                <table border="0" cellpadding="0" cellspacing="0" style="width:100%; margin-top: 25px; margin-bottom: 20px;">
                    <tr>
                        <td align="right" style="padding-right: 10px; vertical-align: middle;">
                            <img src="cid:image1" alt="Maria Madalena IA" style="width: 80px; height: 80px; border-radius: 50%; border: 2px solid #d63384; object-fit: cover;">
                        </td>
                        <td align="left" style="padding-left: 10px; vertical-align: middle;">
                            <a href="https://mariamadalenai.streamlit.app" class="cta-button">Conversar com a<br>Maria Madalena!</a>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="footer">
                <p>Te espero para um papo. 😉</p>
                <p><em>Com carinho (e um pouco de código),<br>Maria Madalena IA</em></p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = formataddr((nome_remetente, email_remetente))
    # Junta a lista de e-mails em uma string separada por vírgulas
    msg['To'] = ", ".join(lista_destinatarios)
    msg.set_content(corpo_texto)
    msg.add_alternative(corpo_html, subtype='html')

    caminho_imagem = 'Arquivos/mariamada.jpg'
    maintype, subtype = mimetypes.guess_type(caminho_imagem)[0].split('/')
    with open(caminho_imagem, 'rb') as img_file:
        msg.get_payload()[1].add_related(img_file.read(), maintype=maintype, subtype=subtype, cid='image1')
    
    try:
        contexto_ssl = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto_ssl) as servidor:
            servidor.login(email_remetente, senha_app)
            servidor.send_message(msg)
        return True, f"E-mail enviado com sucesso para {len(lista_destinatarios)} destinatário(s)!"
    except Exception as e:
        return False, f"Ocorreu um erro inesperado: {e}"

# --- Interface do App Streamlit ---
senha = st.text_area()

if senha == st.secrets["senha"]:
    st.set_page_config(layout="centered", page_title="Disparador de E-mail")
    st.title("💌 Disparador de Convites da Maria Madalena IA")
    st.write("Cole a lista de e-mails abaixo (um por linha ou separados por vírgula/espaço) para enviar os convites.")

    emails_input = st.text_area(
        "Lista de E-mails:",
        height=200
    )

    if st.button("Enviar Convites em Massa", use_container_width=True):
        if emails_input:
            # Extrai todos os e-mails válidos do texto, ignorando o que não for e-mail
            lista_emails = re.findall(r'[\w\.-]+@[\w\.-]+', emails_input)
            
            if lista_emails:
                with st.spinner(f"Enviando {len(lista_emails)} convites... Por favor, aguarde."):
                    sucesso, mensagem = enviar_emails(lista_emails)
                
                if sucesso:
                    st.success(f"🎉 {mensagem}")
                    st.balloons()
                else:
                    st.error(f"🚨 {mensagem}")
            else:
                st.warning("Nenhum endereço de e-mail válido foi encontrado no texto.")
        else:
            st.warning("Por favor, insira pelo menos um endereço de e-mail.")