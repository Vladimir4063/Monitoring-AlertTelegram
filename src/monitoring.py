import requests 
import pyodbc

try:
    #Conexion BBDD
    db = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=NUMBERIP;DATABASE=Wallet;UID=sa;PWD=Pass.001')

    lista = []
    #Connector
    cursor = db.cursor()

    #Querys
    cursor.execute("SELECT count(idTransaccion) FROM [FraudControl].[dbo].[TransactionWallet] where contado = 0")
    saldo_noprocess = cursor.fetchval()
    lista.append(saldo_noprocess)  # Prueba
    print(saldo_noprocess)

    cursor.execute("SELECT count(IdTxGateway) FROM [FraudControl].[dbo].[Transaction] where TransactionStatusId = 2")
    transf_noprocess = cursor.fetchval()
    lista.append(transf_noprocess)
    print(transf_noprocess)

    cursor.execute("SELECT count (Id)   FROM [FraudControl].[dbo].[OnboardingApiCodes] where StatusApiHttp = 400 and actiondate  >=  DATEADD(MINUTE, -10, GETDATE())")
    onboard_fail = cursor.fetchval()
    lista.append(onboard_fail)
    print(onboard_fail)

    cursor.execute("SELECT count (Id) FROM [FraudControl].[dbo].[OnboardingApiCodes] where StatusApiHttp = 200 and actiondate  >=  DATEADD(MINUTE, -10, GETDATE())")
    onboard_success = cursor.fetchval()
    lista.append(onboard_success)
    print(onboard_success)

    print(lista)
    for i in lista:
        if i > 100:
            print(i)
            send = "Alerta en Fraude"
            id = "@PruebasBotvlady"

            token = "TOKEN"
            url = "https://api.telegram.org/bot" + token + "/sendMessage"
            data = {
                'chat_id': id,
                'text': send
            }

            requests.post(url, params=data)
            
except Exception as ex:
    print(ex)

finally:
    db.close()
    print("Monitoreo finalizado.")
