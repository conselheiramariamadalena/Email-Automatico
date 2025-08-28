import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr # Importa a função para formatar o nome
import mimetypes # Para descobrir o tipo do arquivo de imagem
