from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
import numpy as np 
def ordenamineto_de_burbuja(dict):
    """
    Funcion para ordenar los valores de un diccionario utilizando el algortimo de ordenamiento 
    de burbuja. 
    Se requiere primero realizar una lista con los valores del diccionario y otra de las llaves
    para que amabas listas sean ordenadas en funcion de los valores del diccionaro. Posteriormente,
    con un ciclo for se realiza de nuevo un diccionario pero con los elementos con el nuevo orden
    y se retrona dicho diccionario ordenado.  
    """

    values = list(dict.values())
    keys = list(dict.keys())
    sorted_dict = {}
    n = len(values) #siempre que hagamos un len y queremos usarlo 
                    #tenemos que restarle uno (n-1)

    for i in range(n):
        for j in range(0, n - i - 1):
            if values[j] < values[j+1]:
                values[j], values[j+1] = values[j+1], values[j]
                keys[j], keys[j+1] = keys[j+1], keys[j]

    for i in range(len(values)):
        sorted_dict.update({
            keys[i]: values[i]})
    
    return sorted_dict

def groupby(categories, sorted_sales_cate, n):
    """
    Función que genera una matriz que agrupa los elementos por categoria
    con la estructura [nombre de la categoría, los n últimos valores (ventas/búsquedas)]
    """

    less_saled_cate=[]
    for j in categories:
        temp=[]
        for i in range(0, len(sorted_sales_cate)):
            if sorted_sales_cate[i][2] == j:
                temp.append([sorted_sales_cate[i][0], sorted_sales_cate[i][1]])
        temp_sorted = list(ordenamineto_de_burbuja(dict(temp)))[::-1]
        less_saled_cate.append([j,temp_sorted[0:n]])
    return less_saled_cate

def main():
    """
    1) Productos más vendidos y productos rezagados a partir del análisis de
    las categorías con menores ventas y categorías con menores búsquedas.

    - Generar un listado de los 5 productos con mayores ventas y con los 10 
    productos con mayores búsquedas. 
    """
    sales = np.array(lifestore_sales)
    products = np.array(lifestore_products)
    searches = np.array(lifestore_searches)

#5 PRODUCTOS CON MAYORES VENTAS
    id_prod_sales = list(sales[:,1])
    count_sales = {}

    for product in products[:,0]:
        count_sales.update({
            int(product): id_prod_sales.count(product)})

    sales_sorted = ordenamineto_de_burbuja(count_sales)
    
    #Primeros n numeros de sales 
    n=5
    head_sales = dict(list(sales_sorted.items())[0:n])

    print(f"\n\n Los {n} productos con mayores ventas \n" + str(head_sales))
    
#PRIMEROS 10 PRODUCTOS CON MAYOR BUSQUEDA 
    id_prod_searches = list(searches[:,1])
    count_searches = {}
    for product in products[:,0]:
        count_searches.update({
            int(product): id_prod_searches.count(int(product))})
    
    searches_sorted = ordenamineto_de_burbuja(count_searches)
    
    #Primeros n numeros de sales 
    n=10
    head_searches = dict(list(searches_sorted.items())[0:n])
    print(f"\n\n Los {n} productos con mayores busquedas \n" + str(head_searches))

    """
 - Por categorías, generar un listado con los 5 productos con menores ventas y 
con los 10 productos con menores búsquedas. 
"""

    categories = ['procesadores', 'tarjetas de video', 'tarjetas madre', 'discos duros', 
            'memorias usb', 'pantallas', 'bocinas', 'audifonos']
    category = []

   #Creación de matriz id_product y category 
    for product in products[:,0]:
        category.append([product, products[int(product)-1,3]])
    
#5 PRODUCTOS CON MENORES VENTAS POR CATEGORÍA 
    #Creacion de matriz con id product, no de ventas, categoría 
    sorted_sales_cate = []
    for key, value in count_sales.items():
        sorted_sales_cate.append([key, value, category[key-1][1]])

    less_saled_cate = groupby(categories, sorted_sales_cate, 5)
    print(f'\n\n Los 5 productos con menos ventas por categoría son: \n' + str(less_saled_cate))

#10 PRODUCTOS CON MENORES BUSQUEDAS POR CATEGORÍAS 
    sorted_searches_cate = []
    for key, value in count_searches.items():
        sorted_searches_cate.append([key, value, category[key-1][1]])

    less_searches_cate = groupby(categories, sorted_searches_cate, 10)
    print(f'\n\n Los 10 productos con menos busquedas por categoría son: \n' + str(less_searches_cate))
    
    """
    2) Productos por reseña en el servicio a partir del análisis de categorías
    con mayores ventas y categorías con mayores búsquedas.

    Mostrar dos listados de 5 productos cada una, un listado para
    productos con las mejores reseñas y otro para las peores, considerando
    los productos con devolución. (No cosiderar sin reseña)

    ifestore_searches = [id_search, id product]
        lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
        lifestore_products = [id_product, name, price, category, stock]
        sales[:,1].count(product)
    """

    
    sales_reviewed = sales[:,(1,2)]
    categories = str(list(range(1, 97)))

#Futura función que agrupa según score. No considera los productos sin reseñas. 
    top_products_reviewed=[]
    for j in range(1, 97):
        temp=[]
        for i in range(0, len(sales_reviewed)):
            if sales_reviewed[i, 0] == str(j):
                temp.append(sales_reviewed[i, 1])

        if temp != []:
            top_products_reviewed.append([j, temp])
    
#Futura variable que calcula el promedio redondeado a dos decimales de la lista de scores por producto 
    average_scores = []
    for id, scores in top_products_reviewed:
        sum = 0
        for i in scores:
            sum += int(i)
        mean = round(sum/len(scores), 2)

        average_scores.append([id, mean])
    
    sorted_scores = ordenamineto_de_burbuja(dict(average_scores))
    
    
    print("\n\nLa lista con los 5 productos con mejores reseñas son: \n" + 
        str(list(sorted_scores)[0:5]))

    print("\n\nLa lista con los 5 productos con peores reseñas son: \n" + 
        str(list(sorted_scores)[::-1][0:5]))

    
    
    




if __name__ == '__main__':
    main()