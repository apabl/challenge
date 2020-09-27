import pyRofex
import argparse

def main():
    desc = """Se comunica con el mercado y para el instrumento dado consulta el
              último precio; si hay un BID ingresa una orden a $0,01 por debajo
              del mismo, en caso contrario a $75,25"""

    #Arguments checking and parsing
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('instrument')
    parser.add_argument('-u', '--remarkets_user', required=True)
    parser.add_argument('-p', '--remarkets_password', required=True)
    parser.add_argument('-a', '--remarkets_account', required=True)
    
    args = parser.parse_args()
    user = args.remarkets_user
    password = args.remarkets_password
    account = args.remarkets_account
    instrument = args.instrument

    #Start session
    try:
        print("\nIniciando sesión en Remarkets")
        pyRofex.initialize(user=user,
                           password=password,
                           account=account,
                           environment=pyRofex.Environment.REMARKET)
    except Exception as e:
        print("\nProblema en la comunicación con Remarkets:\n", e, sep='')
        return

    #Get ticker's market data
    print("\nConsultando símbolo")
    md = pyRofex.get_market_data(ticker=instrument,
                                 entries=[pyRofex.MarketDataEntry.BIDS,
                                          pyRofex.MarketDataEntry.LAST])
    if md['status'] == 'ERROR':
        print(f"Símbolo inválido ({md['description']})")
        print("\nCerrando sesión en Remarkets")
        return

    #Show last price
    if md['marketData']['LA']:
        lp = f"{md['marketData']['LA']['price']:.2f}".replace('.', ',')
        print("Último precio operado: $" + lp)
    else:
        print("Último precio operado: Sin datos")

    print("\nConsultando BID")

    #If there are no active BIDs input a $75,25 order
    if not md['marketData']['BI']:
        print("No hay BIDs activos\nIngresando orden a $75,25")
        order = pyRofex.send_order(ticker=instrument,
                                   side=pyRofex.Side.BUY,
                                   size=1,
                                   price=75.25,
                                   order_type=pyRofex.OrderType.LIMIT)

    #If there is a BID, input an order, 1 cent below it
    else:
        bidp = f"{md['marketData']['BI'][0]['price']:.2f}".replace('.', ',')
        print("Precio de BID: $" + bidp)

        new_price = float(md['marketData']['BI'][0]['price']) - 0.01
        print(f"Ingresando orden a ${new_price:.2f}".replace('.', ','))
        order = pyRofex.send_order(ticker=instrument,
                                   side=pyRofex.Side.BUY,
                                   size=1,
                                   price=new_price,
                                   order_type=pyRofex.OrderType.LIMIT)

    #Show the order status
    #(although it's not explicitly in the requirements, it's very useful)
    if order:
        r = pyRofex.get_order_status(order['order']['clientId'])
        print("Estado de su última orden:",
               r['order']['status'], "-", r['order']['text'])

    print("\nCerrando sesión en Remarkets")

if __name__ == "__main__":
    main()





