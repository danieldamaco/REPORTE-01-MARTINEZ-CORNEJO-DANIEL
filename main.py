from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
from datetime import datetime
import random, os
import statistics

"""Función que permite borrar los datos previos de la terminal"""
def clear(): 
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system("cls")


"""Función decoradora que permite acceder o no a otra función si el usuario coloca bien
su username y su contraseña"""
def login(func):
    def wrapper():
        usuarioAccedio = False
        intentos = 0        
        # Bienvenida!
        print('Bienvenide al sistema!\nInicio de sesión')

        # Recibo constantemente sus intentos
        while not usuarioAccedio:
            # Primero ingresa Credenciales
            usuario = input('Usuario: ')
            contras = input('Contraseña: ')
            intentos += 1
            # Reviso si el par coincide
            if usuario == 'daniel' and contras == 'daniel':
                usuarioAccedio = True
                clear()
                print(f'Hola de nuevo {usuario}!\n\nDatos del análisis. \n\n')
                func() #Correr función. 
            else:
                clear()
                print(f'Tienes {3 - intentos} intentos restantes')
                if usuario == 'daniel':
                    print('Te equivocaste en la contraseña')
                else:
                    print(f'El usuario: "{usuario}" no esta registrado')
                    
            if intentos == 3:
                exit()
    return wrapper


"""Función que itera los elementos de un diccionario con las respuestas y los imprime en forma de tabla
emparejando el ID del producto y el nombre genérico del producto"""
def printing_dict(dict, title, word):
    string= '\n'+title 
    for key, value in dict.items():
        string += '\n' +'El producto ' +'con ID '+ str(key) + ' con ' + str(value) + ' ' + word +' es ' + str(lifestore_products[int(key)-1][1])
    return print(string)


"""Función que itera los elementos de una lista con las respuestas y los imprime en forma de tabla
emparejando el ID del producto y el nombre genérico del producto"""
def printing_list(list, title, word):
    print('\n\n'+title)
    for i in list:
        printing_dict(i[1], title=str(i[0]).capitalize(), word=word)


"""Funcion para ordenar los valores de un diccionario utilizando el algortimo de ordenamiento 
    de burbuja. 
    Se requiere primero realizar una lista con los valores del diccionario y otra de las llaves
    para que amabas listas sean ordenadas en funcion de los valores del diccionaro. Posteriormente,
    se devuelven los datos en un diccionario pero con los elementos con el nuevo orden.  
    """
def bubble_sort(dict):
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


"""Función que agrupa los elementos por categoria con la estructura [nombre de la categoría, 
    los n últimos valores (ventas/búsquedas)]. 
    Devuelve los elementos agrupados en una lista en orden ascendente y solo los n 
    primeros números. 
    """


def groupby(categories, sorted_categories, n):
    
    less_cate=[]
    for j in categories:
        temp=[]
        for i in range(0, len(sorted_categories)):
            if sorted_categories[i][2] == j:
                temp.append([sorted_categories[i][0], sorted_categories[i][1]])
        temp_sorted = dict(list(bubble_sort(dict(temp)).items())[::-1][0:n])
        less_cate.append([j, temp_sorted])
    return less_cate

@login #Decorador para el login
def main():
    """
    - Generar un listado de los 5 productos con mayores ventas y con los 10 
    productos con mayores búsquedas. 
    """

    #5 PRODUCTOS CON MAYORES VENTAS________________________________________________________________
    #Creación de un diccionario de id_product y número de ventas por producto, y ordenamiento 
    # de ellos en orden descendente. 
    products = [a[0] for a in lifestore_products]
    id_prod_sales = [a[1] for a in lifestore_sales]

    count_sales = {int(product): id_prod_sales.count(product) for product in products} 
    sales_sorted = bubble_sort(count_sales)
    
    #Primeros 5 números de sales ordenado.  
    head_sales = dict(list(sales_sorted.items())[0:5])
    printing_dict(head_sales, title='\nLos 5 productos con mayores ventas son:', word= 'ventas')
    
    #PRIMEROS 10 PRODUCTOS CON MAYOR BUSQUEDA_______________________________________________________
    #Creación de diccionario de id_product y número de búsqueda por producto, y ordenamiento 
    # descendente.
    id_prod_searches = [a[1] for a in lifestore_searches]
    count_searches = {int(product): id_prod_searches.count(int(product)) for product in products}
    searches_sorted = bubble_sort(count_searches)
    
    #Primeros 10 números de búsquedas  
    head_searches = dict(list(searches_sorted.items())[0:10])
    printing_dict(head_searches, title='\nLos 10 productos con mayores busquedas:', word='búsquedas')

    """
     - Por categorías, generar un listado con los 5 productos con menores ventas y 
    con los 10 productos con menores búsquedas. 
    """
    #Creación de lista "categories" que contiene todas las categorías de los productos, 
    # y una lista "category" que contenga id_producto y categoría. 
    categories = ['procesadores', 'tarjetas de video', 'tarjetas madre', 'discos duros', 
                'memorias usb', 'pantallas', 'bocinas', 'audifonos']
    category = [[a[0], a[3]] for a in lifestore_products]
    
    #5 PRODUCTOS CON MENORES VENTAS POR CATEGORÍA_____________________________________________________________
    #Creacion de matriz con id product, número de ventas, categoría 
    sorted_sales_cate = [[key, value, category[key-1][1]] 
                        for key, value in count_sales.items()]
    less_saled_cate = groupby(categories, sorted_sales_cate, 5)

    printing_list(less_saled_cate, title='Los 5 productos con menos ventas por categoría son:', word='ventas')
    
    #10 PRODUCTOS CON MENORES BUSQUEDAS POR CATEGORÍAS_________________________________________________________
    # Uso de la función grouby para aparear datos según datos contenidos en lista categories. 
    # arrojando solo los 10 últimos productos.  
    sorted_searches_cate = [[key, value, category[key-1][1]] 
                            for key, value in count_searches.items()]
    less_searches_cate = groupby(categories, sorted_searches_cate, 10)
    
    printing_list(less_searches_cate, title='Los 10 productos con menos búsquedas por categoría son:', word='búsquedas')
    
    """
    Mostrar dos listados de 5 productos cada una, un listado para
    productos con las mejores reseñas y otro para las peores, considerando
    los productos con devolución. (No cosiderar sin reseña)
    """
    #Arreglo con id_producto y score de reseña. 
    sales_reviewed = [[a[1], a[2]] for a in lifestore_sales]

    #Agrupa de scores según id_product y sacar promedio de scores. 
    average_scores=[]
    for j in range(1, 97):
        temp=[]
        for i in range(0, len(sales_reviewed)):
            if str(sales_reviewed[i][0]) == str(j):
                temp.append(sales_reviewed[i][1])
        #Para no considerar los productos sin reseñas. 
        if temp != []:
            average_scores.append([j, round(statistics.mean(temp), 2)])
    
    #Ordenamiento descendente de id_producto y score promedio por producto. 
    sorted_scores = bubble_sort(dict(average_scores))
    
    printing_dict(dict(list(sorted_scores.items())[0:5]), title='\nLa lista con los 5 productos con mejores reseñas son:', word='de score')
    printing_dict(dict(list(sorted_scores.items())[::-1][0:5]), title='\nLa lista con los 5 productos con peores reseñas son:', word='de score')
    
    """
    Total de ingresos y ventas promedio mensuales, total anual y meses con más ventas al año. 
    (número de ventas, total de ingresos)
    """
    
    # Creación de matriz con precio del producto vendido y fecha de venta,
    # se omiten los produtos devueltos.
    # conversión de un string con formato <día>/<mes>/<año> en datetime.
    date_count_sales =[[
            lifestore_products[int(id_product)-1][2],
            datetime.strptime(date, '%d/%m/%Y')] 
            for  i, id_product, score, date, returned in lifestore_sales
            if int(returned) != 1] 

    #Creación de matriz de mes vs lista de los precios de los productos vendidos en ese mes. 
    #Se omite 2019 porque la única venta que se realizó fue devuelta. 
    sales_per_month=[]
    for j in range(1, 13):
        temp=[i[0] for i in date_count_sales if int(i[1].month) == j]

        sales_per_month.append([j, len(temp), sum(temp)])
    
    sum_annual= sum([a[2] for a in sales_per_month])

    #Creación de diccionario que tenga mes:número de ventas 
    #Ordenamiento con la función ordenamiento de burbuja para mostrar los meses con más ventas en orden 
    #descendente  
    months_sales = {i[0]:i[1] for i in sales_per_month}
    month_highest_sales = bubble_sort(months_sales)
    
    #Recorrer diccionario month_highest_sales para motrar en pantalla su contenido. 
    m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    string= '\n\nLos meses con más ventas del año 2020 son:'
    for key, value in month_highest_sales.items():
        string += '\n' + m[int(key)-1] +' con ' + str(value) + ' ventas.'
    print(string)

    print('\n\nEn ingreso anual del 2020 es:\n$' + str(sum_annual))
   
   #Recorrer lista sales_per_month para mostrar en pantalla su contenido. 
    string= '\n\nEl ingreso neto y el número de ventas por mes del 2020:'
    for i in sales_per_month:
        string += '\n' + m[int(i[0])-1] +' con ' + str(i[1]) + ' ventas ' + 'y $' + str(i[2]) + ' de ingreso neto.'
    print(string)

if __name__ == '__main__':
    main()