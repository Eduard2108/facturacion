from components import Menu,Valida, functions
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient, VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
from components import user_session
path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        new_client = functions()
        new_client.create_client()
    def update(self):
        borrarPantalla()
        func_instance = functions()
        text = "Actualizar cliente"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        print(blue_color + Company.get_business_name())
        dni = input("Ingrese el dni que desea buscar: ")
        up = functions()
        up.update_client(dni)
    def delete(self):
        borrarPantalla()
        func_instance = functions()
        text = "Eliminar cliente"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        dni = input("Ingrese el dni que desea buscar: ")
        dele = functions()
        dele.delete_client(dni)
    def consult(self):
        borrarPantalla()
        func_instance = functions()
        text = "Consultar cliente"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        dni = input("Ingrese el dni que desea buscar: ")
        consu = functions()
        consu.consult_client(dni)

class CrudProducts(ICrud):
    def create(self):
        borrarPantalla()
        func_instance = functions()
        text = "Crear producto"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        description_product = input(cyan_color + "Ingresar descripción del producto: ")
        price_product = input(cyan_color + "Ingresar precio del producto: ")
        stock_product = input(cyan_color + "Ingresar stock del producto. ")
        crea_produ = functions()
        crea_produ.create_product(description_product, price_product, stock_product)
    
    def update(self):
        borrarPantalla()
        func_instance = functions()
        text = "Actualizar producto"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        id_product = input(cyan_color + "Ingrese el id del producto que desea buscar: ").replace(" ","")
        actu_produ = functions()
        actu_produ.update_product(id_product)
    
    def delete(self):
        borrarPantalla()
        func_instance = functions()
        text = "Borrar producto"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        descri_product = input(cyan_color + "Ingrese el id del producto que desea eliminar: ").replace(" ", "")
        dele_produ = functions()
        dele_produ.delete_product(descri_product)
    
    def consult(self):
        borrarPantalla()
        func_instance = functions()
        text = "Consultar producto"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        consult_product = input(cyan_color + "Ingrese el ID del producto que desea buscar: ").replace(" ", "")
        cons_produ = functions()
        cons_produ.consult_product(consult_product)

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            time.sleep(2)
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True)
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color)
        gotoxy(5,9);print(purple_color+"Linea")
        gotoxy(12,9);print("Id_Articulo")
        gotoxy(24,9);print("Descripcion")
        gotoxy(38,9);print("Precio")
        gotoxy(48,9);print("Cantidad")
        gotoxy(58,9);print("Subtotal")
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line = 1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);
                print(product.descrip)
                gotoxy(38,9+line);
                print(product.preci)
                gotoxy(49,9+line);
                qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                sale.add_detail(product,qyt)
                gotoxy(59, 9 + line);print(sale.subtotal)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            if invoices:
                ult_invoices = invoices[-1]["factura"]+1
            else:
                ult_invoices = 1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)
        time.sleep(2)
    
    def update(self):
        borrarPantalla()
        func_instance = functions()
        text = "Actualizar factura"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        number_invoice = input(red_color + "Ingrese el número de la factura: ")
        update_invoice = functions()
        update_invoice.update_invoice(number_invoice)
    
    def delete(self):
        borrarPantalla()
        func_instance = functions()
        text = "Borrar factura"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        number_invoice = input(red_color + "Ingrese el número de la factura que desea eliminar: ")
        delete_invo = functions()
        delete_invo.delete_invoice(number_invoice)

    def consult(self):
        print('\033c', end='')
        gotoxy(2, 1);print(green_color + "█" * 90)
        gotoxy(2, 2);print("██" + " " * 34 + "Consulta de Venta" + " " * 35 + "██")
        gotoxy(2, 4);invoice = input(red_color + "Ingrese Factura: ")
        borrarPantalla()
        func_instance = functions()
        text = "Consultar factura"
        gotoxy(1, 8);func_instance.print_in_frame(text, 3, len(text) + 40)
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.find("factura", invoice)
            print(f"Impresion de la Factura#{invoice}")
            if invoices:
                print()
            else:
                print("No existe ninguna factura asociada a ese número")
            for invoice in invoices:
                for key, value in invoice.items():
                    if key == 'detalle':
                        print("Detalle:")
                        for item in value:
                            print(
                                f"Producto: {item['producto']}, Precio: {item['precio']}, Cantidad: {item['cantidad']}")
                    else:
                        print(f"{key}: {value}")
        else:
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")

            suma = reduce(lambda total, invoice: round(total + invoice["total"], 2),invoices, 0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ", total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x = input("presione una tecla para continuar...")
symbol = ''
while True:  # strip() elimina los espacios en blanco al inicio y al final
    symbol = input(green_color + "Ingresar simbolo del marco: ")
    if len(symbol) == 1:  # Verifica que el símbolo ingresado tenga exactamente un carácter
        break
    else:
        print("Por favor, ingrese solo un símbolo")

Menu.symbol = symbol  # Almacena el símbolo en la variable de clase de la clase Menu

opc = ''
while opc != '4':
    borrarPantalla()
    menu_main = Menu("Menú Facturacion", ["1) Clientes", "2) Productos", "3) Ventas", "4) Salir"], 20, 10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()
            menu_clients = Menu("Menú Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                cr_client = CrudClients()
                cr_client.create()
                time.sleep(2)
            elif opc1 == "2":
                cr_client = CrudClients()
                cr_client.update()
            elif opc1 == "3":
                cr_client = CrudClients()
                cr_client.delete()
            elif opc1 == "4":
                cr_client = CrudClients()
                cr_client.consult()
            elif opc1 == "5":
                print("saliendo...")
                break
            else:
                print("Opción incorrecta")
                time.sleep(2)
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menú Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                cr_product = CrudProducts()
                cr_product.create()
            elif opc2 == "2":
                cr_product = CrudProducts()
                cr_product.update()
            elif opc2 == "3":
                cr_product = CrudProducts()
                cr_product.delete()
            elif opc2 == "4":
                cr_product = CrudProducts()
                cr_product.consult()
            elif opc2 == "5":
                break
            else:
                print("Opción invalida")
                time.sleep(2)

    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menú Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
            elif opc3 == "5":
                print("saliendo...")
            else:
                print("Opción invalida")
                time.sleep(2)
    elif opc == "4":
        print("Saliendo del sistema")
        break
    else:
        print("Opción incorrecta")
        time.sleep(2)
    print("Regresando al menu Principal...")
    time.sleep(2)

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()
