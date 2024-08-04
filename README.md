
![Logo](https://scontent-mxp2-1.xx.fbcdn.net/v/t1.6435-9/75569679_125225412250507_8608695627624218624_n.png?_nc_cat=107&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=H5QYKCipmO4AX_JZ7a4&_nc_ht=scontent-mxp2-1.xx&oh=00_AT9zwz8LYu2lB7LdWHF2xBnY0CJoU8BkPlCJlHYrvBBAKA&oe=62C010E3)

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
# Richard Benson Python Telegram Bot

Questo bot è un tributo a Richard Philip Henry John Benson (1955 - 2022) ed è totalmente gratuito. A una specifica ora del giorno (default 12:00), invia una clip random di 30 secondi da un video di Richard Benson a tutti gli iscritti.
Disclaimer: Il progetto è stato realizzato in un pomeriggio appositamente come test di velocità. Non utilizzare l'organizzazione del codice come riferimento ;)

## Installazione

Installare con pip le seguenti librerie:

- pyTube

- dotenv

- pyTelegramBotAPI

- moviePy

Dopodichè, clonare il progetto e preparare il .env all'interno della cartella:

```bash
  cp .env.example .env
```

Successivamente, compilare i campi nell'env con i propri valori:

- BOT_TOKEN = Token del Bot Telegram (Generato creando un nuovo bot su @BotFather)
- DB_NAME = Nome del file database SQLite (deve finire con .db)
- LOG_FILE = Percorso del file log (es. debug.log)
- OWNER_ID = ID Telegram del creatore del bot (Si può recuperare con diversi bot come @UserInfoBot)


Infine, lanciare il bot da terminale:

```bash
  python bot.py
```
## Comandi

- /start - Avvia il Bot e registra lo user ID sul database
- /attivarichard - Attiva il bot nei gruppi (solo amministratori)
- /disattivarichard - Disattiva il bot nei gruppi (solo amministratori)
- /test - Scatena la schedulazione in maniera manuale (non ferma quella automatica)
- /dona - Info donazioni

## Problemi di funzionamento

Da un aggiornamento di Youtube dello 01/06/2022 la libreria moviePy non riesce a recuperare i video (per il momento), per sistemare è necessario andare in /usr/local/lib/python3/moviepy/cypher.py e sostituire il pattern sulla riga 30 ("^\w+\W") con il seguente: "^\$*\w+\W"


## Licenza

[MIT](https://choosealicense.com/licenses/mit/)


## Autore

- [@sim1-dev](https://www.simonetenisci.it/) 


## Offrimi un caffè ☕

[![alt text][image]][hyperlink]

[hyperlink]:https://www.paypal.com/donate/?hosted_button_id=AS2MJZNHSQEQA
[image]:https://pics.paypal.com/00/s/NDI2ZTExZWQtODY4MS00ZTZiLTg4OGEtZjc1MmEyNjYwNzRj/file.PNG
(Donate with PayPal)
