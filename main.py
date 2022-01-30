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

def main():
    """
    1) Productos más vendidos y productos rezagados a partir del análisis de
    las categorías con menores ventas y categorías con menores búsquedas.

    - Generar un listado de los 5 productos con mayores ventas y con los 10 
    productos con mayores búsquedas. 
    - Por categorías, generar un listado con los 5 productos con menores ventas y 
    con los 10 productos con menores búsquedas. 

    ifestore_searches = [id_search, id product]
    lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
    lifestore_products = [id_product, name, price, category, stock]
    sales[:,1].count(product)
    """
    #5 PRODUCTOS CON MAYORES VENTAS
    count_sales = {}
    sales = np.array(lifestore_sales)
    products = np.array(lifestore_products)
    searches = np.array(lifestore_searches)

    id_prod_sales = list(sales[:,1])

    for product in products[:,0]:
        count_sales.update({
            int(product): id_prod_sales.count(product)})

    sales_sorted = ordenamineto_de_burbuja(count_sales)
    
    #Primeros n numeros de sales 
    n=5
    head_sales = dict(list(sales_sorted.items())[0:n])

    print(head_sales)
    
    #PRIMEROS 10 PRODUCTOS CON MAYOR BUSQUEDA 
    id_prod_searches = list(searches[:,1])
    count_searches = {}
    for product in products[:,0]:
        count_searches.update({
            int(product): id_prod_searches.count(int(product))})
        

    #print(count_searches)
    
    searches_sorted = ordenamineto_de_burbuja(count_searches)
    
    #Primeros n numeros de sales 
    n=10
    head_searches = dict(list(searches_sorted.items())[0:n])
    print(head_searches)


if __name__ == '__main__':
    main()









"""
2) Productos por reseña en el servicio a partir del análisis de categorías
con mayores ventas y categorías con mayores búsquedas.
3) Sugerir una estrategia de productos a retirar del mercado así como
sugerencia de cómo reducir la acumulación de inventario considerando los
datos de ingresos y ventas mensuales.
"""

