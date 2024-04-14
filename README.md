# Metacritic-MongoDB
Metacritic-MongoDB è un progetto effettuato per l'esame di Basi Di Dati II in cui è stata effettuata un'analisi relativa a dati raccolti da Metacritic sui videogiochi.
Il dataset utilizzato, reperibile al seguente link [https://www.kaggle.com/datasets/brunovr/metacritic-videogames-data], è composto da 17944 tuple con 10 campi.
 Le tecnologie utilizzate per lo svolgimento del progetto sono state:
- Database NoSQL MongoDB, 
- Python per le operazioni di Data Cleaning e la creazione delle query, 
- Tkinter, libreria di Python, per lo sviluppo dell'interfaccia grafica.

Le operazioni di Data Cleaning effettuate sono state:
- Rimozione del campo "players",
- Rimozioni delle tuple che non presentavano alcun score,
- Lower-case delle stringhe relative ai campi "nome", "piattaforma", "genere", "developer",
- Trasformare il campo "user score" in un valore intero, più consono per le analisi effettuate,
- Rimozione dei valori duplicati nel campo "genere".

Sono state create un totale di 14 query:
- Inserimento di un videogioco,
- Cancellazione tramite "nome" e "piattaforma",
- Ricerca dei videogiochi in base al "nome",
- Ricerca dei videogiochi in base al "nome" e alla "piattaforma",
- Cancellazione tramite "nome",
- Cancellazione tramite "score",
- Ricerca dei videogiochi in base al "genere",
- Ricerca dei videogiochi in base a "score", "user score", "critics" e "users",
- Ricerca dei videogiochi in base al "developer",
- Modifica di un videogioco,
- Calcolo della media di "score", "user score", "critiche" e differenza tra "score" e "user score" dei videogiochi di un dato "developer",
- Calcolo della media di "score", "user score", "critiche" e differenza tra "score" e "user score" dei videogiochi di un dato "genere",
- Ordinamento ascendente e discendente in base alla data di rilascio dei videogiochi,
- Ricerca in base ai parametri scelti dall'utente
