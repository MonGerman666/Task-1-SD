import xmlrpc.client

def main():
    # Connectem amb el servidor InsultFilter al port 8001, ruta /RPC2
    proxy = xmlrpc.client.ServerProxy("http://localhost:8001/RPC2")
    
    # Textos d'exemple per provar el filtrat
    text1 = "Aquest text conté insult1 i altres coses."
    text2 = "Aquest text està net sense cap insult."
    text3 = "Aquí apareixen insult2 i insult1 en el mateix text."
    
    filtered1 = proxy.filter_text(text1)
    filtered2 = proxy.filter_text(text2)
    filtered3 = proxy.filter_text(text3)
    
    print("Textos filtrats:")
    print(filtered1)
    print(filtered2)
    print(filtered3)
    
    # Recuperem la llista completa de textos filtrats
    all_filtered = proxy.get_filtered_texts()
    print("\nLlista de textos filtrats:")
    print(all_filtered)

if __name__ == "__main__":
    main()
