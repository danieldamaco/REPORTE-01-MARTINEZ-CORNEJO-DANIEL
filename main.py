from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
import numpy as np 
from datetime import datetime

"""Función decoradora que permite acceder o no a otra función si el autentificando al usuario 
con un username y una contraseña"""
def login(func):
    def wrapper():
        usuarioAccedio = False
        intentos = 0        
        # Bienvenida!
        mensaje_bienvenida = 'Bienvenide al sistema!\nAccede con tus credenciales'
        print(mensaje_bienvenida)

        # Recibo constantemente sus intentos
        while not usuarioAccedio:
            # Primero ingresa Credenciales
            usuario = input('Usuario: ')
            contras = input('Contraseña: ')
            intentos += 1
            # Reviso si el par coincide
            if usuario == 'jimmy' and contras == 'ymmij':
                usuarioAccedio = True
                print('\n\nHola de nuevo!\n\nDatos del análisis. \n\n')
                func() #Correr función. 
            else:
                # print('Tienes', 3 - intentos, 'intentos restantes')
                print(f'Tienes {3 - intentos} intentos restantes')
                if usuario == 'jimmy':
                    print('Te equivocaste en la contraseña')
                else:
                    print(f'El usuario: "{usuario}" no esta registrado')
                    
            if intentos == 3:
                exit()
    return wrapper

def showing_products(a):
    pass

"""
    Funcion para ordenar los valores de un diccionario utilizando el algortimo de ordenamiento 
    de burbuja. 
    Se requiere primero realizar una lista con los valores del diccionario y otra de las llaves
    para que amabas listas sean ordenadas en funcion de los valores del diccionaro. Posteriormente,
    se devuelven los datos en un diccionario pero con los elementos con el nuevo orden.  
    """
def ordenamineto_de_burbuja(dict):
    values = list(dict.values())
    keys = list(dict.keys())
    n = len(values) #siempre que hagamos un len y queremos usarlo 
                    #tenemos que restarle uno (n-1)

    for i in range(n):
        for j in range(0, n - i - 1):
            if values[j] < values[j+1]:
                values[j], values[j+1] = values[j+1], values[j]
                keys[j], keys[j+1] = keys[j+1], keys[j]

    sorted_dict = {keys[i]: values[i] for i in range(n)}
    return sorted_dict

"""
    Función que agrupa los elementos por categoria con la estructura [nombre de la categoría, 
    los n últimos valores (ventas/búsquedas)]. 
    Devuelve los elementos agrupados en una lista en orden ascendente y solo los n 
    primeros números. 
    """
def groupby(categories, sorted_sales_cate, n):
    
    less_saled_cate=[]
    for j in categories:
        temp=[]
        for i in range(0, len(sorted_sales_cate)):
            if sorted_sales_cate[i][2] == j:
                temp.append([sorted_sales_cate[i][0], sorted_sales_cate[i][1]])
        temp_sorted = list(ordenamineto_de_burbuja(dict(temp)))[::-1]
        less_saled_cate.append([j,temp_sorted[0:n]])
    return less_saled_cate

@login #Decorador para el login
def main():
    """
    1) Productos más vendidos y productos rezagados a partir del análisis de
    las categorías con menores ventas y categorías con menores búsquedas.

    - Generar un listado de los 5 productos con mayores ventas y con los 10 
    productos con mayores búsquedas. 
    """
    #Conversión de las matrices en arreglos con Numpy 
    sales = np.array(lifestore_sales)
    products = np.array(lifestore_products)
    searches = np.array(lifestore_searches)

    #5 PRODUCTOS CON MAYORES VENTAS
    #Creación de un diccionario de id_product y número de ventas por producto, y ordenamiento 
    # de ellos en orden descendente. 
    id_prod_sales = list(sales[:,1])
    count_sales = {int(product): id_prod_sales.count(product) for product in products[:,0]}
    sales_sorted = ordenamineto_de_burbuja(count_sales)
    
    #Primeros 5 números de sales ordenado.  
    head_sales = dict(list(sales_sorted.items())[0:5])
    print(f"Los 5 productos con mayores ventas: \n" + str(head_sales))
    
    #PRIMEROS 10 PRODUCTOS CON MAYOR BUSQUEDA 
    #Creación de diccionario de id_product y número de búsqueda por producto, y ordenamiento 
    # descendente. 
    id_prod_searches = list(searches[:,1])
    count_searches = {int(product): id_prod_searches.count(int(product)) for product in products[:,0]}
    searches_sorted = ordenamineto_de_burbuja(count_searches)
    
    #Primeros 10 números de búsquedas  
    head_searches = dict(list(searches_sorted.items())[0:10])
    print(f"\n Los 10 productos con mayores busquedas: \n" + str(head_searches))

    """
     - Por categorías, generar un listado con los 5 productos con menores ventas y 
    con los 10 productos con menores búsquedas. 
    """
    #Creación de lista "categories" que contiene todas las categorías de los productos, 
    # y una lista "category" que contenga id_producto y categoría. 
    categories = ['procesadores', 'tarjetas de video', 'tarjetas madre', 'discos duros', 
                'memorias usb', 'pantallas', 'bocinas', 'audifonos']
    category = [[product, products[int(product)-1, 3]] for product in products[:,0]]
    
    #5 PRODUCTOS CON MENORES VENTAS POR CATEGORÍA 
    #Creacion de matriz con id product, número de ventas, categoría 
    sorted_sales_cate = [[key, value, category[key-1][1]] 
                        for key, value in count_sales.items()]
    less_saled_cate = groupby(categories, sorted_sales_cate, 5)
    print(f'\n Los 5 productos con menos ventas por categoría son: \n' + str(less_saled_cate))

    #10 PRODUCTOS CON MENORES BUSQUEDAS POR CATEGORÍAS
    # Uso de la función grouby para aparear datos según datos contenidos en lista categories. 
    # arrojando solo los 10 últimos productos.  
    sorted_searches_cate = [[key, value, category[key-1][1]] 
                            for key, value in count_searches.items()]
    less_searches_cate = groupby(categories, sorted_searches_cate, 10)
    print(f'\n Los 10 productos con menos busquedas por categoría son: \n' + str(less_searches_cate))
    
    """
    2) Productos por reseña en el servicio a partir del análisis de categorías
    con mayores ventas y categorías con mayores búsquedas.

    Mostrar dos listados de 5 productos cada una, un listado para
    productos con las mejores reseñas y otro para las peores, considerando
    los productos con devolución. (No cosiderar sin reseña)
    """
    #Arreglo con id_producto y score de reseña. 
    sales_reviewed = sales[:,(1,2)]

    #Agrupa de scores según id_product. No considera los productos sin reseñas. 
    top_products_reviewed=[]
    for j in range(1, 97):
        temp=[]
        for i in range(0, len(sales_reviewed)):
            if sales_reviewed[i, 0] == str(j):
                temp.append(sales_reviewed[i, 1])

        if temp != []:
            top_products_reviewed.append([j, temp])
    
    #Cálculo del promedio redondeado a dos decimales de la lista de scores por producto. 
    average_scores = []
    for id, scores in top_products_reviewed:
        sum = 0

        for i in scores:
            sum += int(i)

        mean = round(sum/len(scores), 2)

        average_scores.append([id, mean])
    
    #Ordenamiento descendente de id_producto y score promedio por producto. 
    sorted_scores = ordenamineto_de_burbuja(dict(average_scores))
    
    print("\nLa lista con los 5 productos con mejores reseñas son: \n" + 
        str(list(sorted_scores)[0:5]))

    print("\nLa lista con los 5 productos con peores reseñas son: \n" + 
        str(list(sorted_scores)[::-1][0:5]))

    """
    Total de ingresos y ventas promedio mensuales, total anual y meses con más ventas al año. 
    (número de ventas, total de ingresos)
    """

    # Creación de matriz con precio del producto vendido y fecha de venta.
    # conversión de un string con formato <día>/<mes>/<año> en datetime.
    date_count_sales =[[
            products[int(id_product)-1, 2],
            datetime.strptime(date, '%d/%m/%Y')] 
            for  id_product, date in sales[:,(1,3)]] 

    #Creación de matriz de mes vs lista de los precios de los productos vendidos en ese mes. 
    #Se omite 2019 porque solo hay una venta. 
    sales_per_month_year=[]
    for j in range(1, 13):
        temp=[date_count_sales[i][0] 
            for i in range(0, len(date_count_sales)) 
            if int(date_count_sales[i][1].month) == j and int(date_count_sales[i][1].year) > 2019]

        sales_per_month_year.append([j, temp])
    
    #Creación de matriz con mes vs número de ventas, suma de ventas por mes
    #Sacar el ingreso neto anual (sum_annual) del 2020
    sales_per_month = []
    sum_annual = 0
    for month, prices in sales_per_month_year:
        sum = 0
        no_sales = len(prices)
        for i in prices:
            sum += int(i)
            sum_annual += int(i)

        sales_per_month.append([month, no_sales, sum])

    #Creación de diccionario que tenga mes:número de ventas 
    #Ordenamiento con la función ordenamiento de burbuja para mostrar los meses con más ventas en orden 
    #descendente  
    months_sales = {sales_per_month[i][0]:sales_per_month[i][1] for i in range(len(sales_per_month))}
    month_highest_sales = ordenamineto_de_burbuja(months_sales)
    
    print("\n\nLos meses con más ventas del año 2020 son: " + str(month_highest_sales))
    print("\n\nEn ingreso anual del 2020 es: " + str(sum_annual))
    print("\n\nEl ingreso neto y el número de ventas por mes del 2020: \n"+ str(sales_per_month))

if __name__ == '__main__':
    main()