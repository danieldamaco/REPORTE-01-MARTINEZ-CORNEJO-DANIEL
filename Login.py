from lifestore_file import lifestore_searches, lifestore_sales, lifestore_products
"""
La info de lifestore_file:

lifestore_searches = [id_search, id product]
lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
lifestore_products = [id_product, name, price, category, stock]
"""

# # Imprimir los primeros 10 prod.
# lista_diez = lifestore_products[:10]
# for producto in lista_diez:
#     print(producto[2], '\n')


# # sumatoria de los precios los primeros 10 prod.
# suma = 0
# for producto in lista_diez:
#     # Obtener el precio del producto
#     precio = producto[2]
#     suma += precio

# print('El valor de la suma de los primeros 10 prod: ', suma)
# print('El valor promedio de los primeros 10 prod: ', suma/10)

"""
Login
credenciales:

usuario:
    jimmy
contrase;a:
    ymmij
"""



usuarioAccedio = False
intentos = 0

# Bienvenida!
mensaje_bienvenida = 'Bienvenide al sistema!\nAccede con tus credenciales'
print(mensaje_bienvenida)

# Recibo constantemente sus intentos
while not usuarioAccedio:
    # Primero ingresa Credenciales
    usuario = input('Usuario: ')
    contras = input('Contrase;a: ')
    intentos += 1
    # Reviso si el par coincide
    if usuario == 'jimmy' and contras == 'ymmij':
        usuarioAccedio = True
        print('Hola de nuevo!')
    else:
        # print('Tienes', 3 - intentos, 'intentos restantes')
        print(f'Tienes {3 - intentos} intentos restantes')
        if usuario == 'jimmy':
            print('Te equivocaste en la contrase;a')
        else:
            print(f'El usuario: "{usuario}" no esta registrado')
            
    if intentos == 3:
        exit()

print('Solamente llegaste aca si ingresaste correctamente')


"""
continuacion ...
"""

