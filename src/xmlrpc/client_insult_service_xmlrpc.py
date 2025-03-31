import xmlrpc.client

def main():
    # Connectem amb el servidor XMLRPC a la ruta /RPC2
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")
    
    # Afegim alguns insults
    resultat1 = proxy.add_insult("insult1")
    resultat2 = proxy.add_insult("insult2")
    resultat3 = proxy.add_insult("insult1")  # Ja existeix; hauria de retornar False
    
    print("Resultats d'afegir insults:")
    print(resultat1, resultat2, resultat3)
    
    # Recuperem la llista d'insults
    insults = proxy.get_insults()
    print("Llista d'insults:")
    print(insults)

if __name__ == "__main__":
    main()
