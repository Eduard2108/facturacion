from utilities import borrarPantalla, gotoxy
import time
from clsJson import JsonFile
import os
import json
import time
from customer import RegularClient, VipClient
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
path, _ = os.path.split(os.path.abspath(__file__))
class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   

class Valida:
    def solo_numeros(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)            
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor

    def solo_letras(self,mensaje,mensajeError): 
        while True:
            valor = str(input("          ------>   | {} ".format(mensaje)))
            if valor.isalpha():
                break
            else:
                print("          ------><  | {} ".format(mensajeError))
        return valor

    def solo_decimales(self,mensaje,mensajeError):
        while True:
            valor = str(input("          ------>   | {} ".format(mensaje)))
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except:
                print("          ------><  | {} ".format(mensajeError))
        return valor

    def only_letters(self, word_to_validate):
        if word_to_validate is None:
            print("No se ha ingresado nada")
            return
        word_to_validate = word_to_validate.replace(" ", "")
        return True if word_to_validate.isalpha() else False

    def only_numbers(self, number_to_validate):
        return str(number_to_validate).isdigit()

    def dni_valited(self, dni):
        if dni is None:
            print("No se ha ingresado nada")
            return False
        if not (len(dni) <= 10 and len(dni) > 9 and str(dni).isdigit()):
            return False
        try:
            file_path = path + '/archivos/clients.json'
            with open(file_path, 'r') as file:
                clients = json.load(file)
        except FileNotFoundError:
            print("Archivo no encontrado")

        for client in clients:
            if client['dni'] == dni:
                print("El DNI ya existe")
                return False

        return True

    def card_valited(self, card):
        if card is None:
            print("No se ha ingresado nada")
            return
        return True if len(card) == 16 and str(card).isdigit() else False

class functions:
    def create_client(self):
        while True:
            print(purple_color + "Seleccione el tipo de cliente:")
            type_client = input("1--> CLiente regular\n2--> Cliente VIP\n3--> Salir\n")
            if type_client == "1":
                name = input("Ingresar nombre: ").replace(" ", "")
                validated = Valida()
                bool_name = validated.only_letters(name)
                surname = input("Ingresar apellido: ").replace(" ", "")
                bool_surname = validated.only_letters(surname)
                dni = input("Ingresar el DNI: ").replace(" ", "")
                bool_dni = validated.dni_valited(dni)
                card = input("Ingresar el número de la tarjeta: ").replace(" ", "")
                bool_card = validated.card_valited(card)

                while True:
                    if bool_name and bool_surname and bool_dni and bool_card:
                        new_client = RegularClient(name, surname, dni, card)
                        break
                    elif bool_name == False:
                        name = input("Ingresar un nombre valido: ")
                        bool_name = validated.only_letters(name)
                    elif bool_surname == False:
                        name = input("Ingresar un apellido valido: ")
                        bool_surname = validated.only_letters(name)
                    elif bool_dni == False:
                        dni = input("Ingresar un DNI valido: ")
                        bool_dni = validated.dni_valited(dni)
                    elif bool_card == False:
                        card = input("Ingresar un número de tarjeta valido: ")
                        bool_card = validated.card_valited(card)
                break

            elif type_client == "2":
                name = input("Ingresar nombre: ")
                validated = Valida()
                bool_name = validated.only_letters(name)
                surname = input("Ingresar apellido: ")
                bool_surname = validated.only_letters(surname)
                dni = input("Ingresar el DNI: ")
                bool_dni = validated.dni_valited(dni)
                while True:
                    if bool_name and bool_surname and bool_dni:
                        new_client = VipClient(name, surname, dni)
                        break
                    elif bool_name == False:
                        name = input("Ingresar un nombre valido: ")
                        bool_name = validated.only_letters(name)
                    elif bool_surname == False:
                        name = input("Ingresar un apellido valido: ")
                        bool_surname = validated.only_letters(name)
                    elif bool_dni == False:
                        dni = input("Ingresar un DNI valido: ")
                        bool_dni = validated.dni_valited(dni)
                break
            elif type_client == "3":
                break
            else:
                print("Opción invalida")
                time.sleep(2)
        if new_client is not None:
            file_json = JsonFile(path + '/archivos/clients.json')
            clients = file_json.read()
            clients.append(new_client.getJson())
            file_json.save(clients)
            print("EL cliente se ha guardado con exito")
            time.sleep(2)

    def update_client(self, dni):
        file_json = JsonFile(path + '/archivos/clients.json')
        valida = Valida()
        try:
            clients = file_json.read()
            if clients is None:
                print("No hay clientes para actualizar")
                return
            for client in clients:
                if client['dni'] == dni:
                    print("Información del cliente:")
                    for key, value in client.items():
                        print(f"{key}: {value}")

                    new_name = input("Ingresar el nuevo nombre (dejar en blanco si no desea cambiarlo)")
                    new_surname = input("Ingresar el nuevo apellido (dejar en blanco si no desea cambiarlo)")
                    new_dni = input("Ingresar el nuevo dni (dejar en blanco si no desea cambiarlo)")
                    if new_dni:
                        while True:
                            if valida.dni_valited(new_dni):
                                break
                            else:
                                print("Por favor, ingrese un DNI válido")

                    if new_name:
                        client['nombre'] = new_name
                    if new_surname:
                        client['apellido'] = new_surname
                    if new_dni:
                        client['dni'] = new_dni

                    file_json.save(clients)
                    print("El cliente se ha actualizado con éxito")

                    return
            print("No se ha encontrado al cliente")
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
        except Exception as e:
            print(f"Error: {e}")

    def delete_client(self, dni):
        file_json = JsonFile(path + '/archivos/clients.json')
        try:
            clients = file_json.read()
            if clients is None:
                print("No hay clientes para eliminar")
                return
            for i, client in enumerate(clients):
                if client['dni'] == dni:
                    del clients[i]
                    file_json.save(clients)
                    print("El cliente se ha eliminado con éxito")
                    time.sleep(2)
                    return
            print("No se ha encontrado al cliente")
            time.sleep(2)
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
        except Exception as e:
            print(f"Error: {e}")

    def consult_client(self, dni):
        file_json = JsonFile(path + '/archivos/clients.json')
        try:
            clients = file_json.read()
            if clients is None:
                print("No hay clientes para consultar")
                return
            for client in clients:
                if client['dni'] == dni:
                    print("Información del cliente:")
                    print(json.dumps(client, indent=4))
                    time.sleep(5)
                    return
            print("No se ha encontrado al cliente")
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
        except Exception as e:
            print(f"Error: {e}")

    def create_product(self, descripcion, precio, stock):
        file_json = JsonFile(path + '/archivos/products.json')
        valida = Valida()
        try:
            products = file_json.read()
            if products is None:
                products = []

            while True:
                if valida.only_numbers(precio):
                    precio = float(precio)
                    break
                else:
                    print("Por favor, ingrese un número válido para el precio")
                    precio = input("Ingrese el precio del producto: ")

            while True:
                if valida.only_numbers(stock):
                    stock = int(stock)
                    break
                else:
                    print("Por favor, ingrese un número válido para el stock")
                    stock = input("Ingrese el stock del producto: ")

            new_product = {
                "id": len(products) + 1,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock
            }
            products.append(new_product)
            file_json.save(products)
            print("El producto se ha creado con éxito")
            print("Regresando al menu de productos")
            time.sleep(2)
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
        except Exception as e:
            print(f"Error: {e}")

    def update_product(self, id):
        valida = Valida()
        while True:
            if not valida.only_numbers(id):
                print("El ID del producto debe ser un número")
                id = input("Ingresar id valido: ")
            else:
                break
        id = int(id)
        file_json = JsonFile(path + '/archivos/products.json')
        try:
            products = file_json.read()
            if products is None:
                print("No hay productos para actualizar")
                return
            for product in products:
                if product['id'] == id:
                    new_description = input("Ingresar la nueva descripción (dejar en blanco si no desea cambiarlo)")
                    new_price = input("Ingresar el nuevo precio (dejar en blanco si no desea cambiarlo)")
                    if new_price:
                        while True:
                            if valida.only_numbers(new_price):
                                new_price = float(new_price)
                                break
                            else:
                                print("Por favor, ingrese un número válido para el precio")
                                new_price = input("Ingrese el nuevo precio del producto: ")

                    new_stock = input("Ingresar el nuevo stock (dejar en blanco si no desea cambiarlo)")
                    if new_stock:
                        while True:
                            if valida.only_numbers(new_stock):
                                new_stock = int(new_stock)
                                break
                            else:
                                print("Por favor, ingrese un número válido para el stock")
                                new_stock = input("Ingrese el nuevo stock del producto: ")

                    if new_description:
                        product['descripcion'] = new_description
                    if new_price:
                        product['precio'] = new_price
                    if new_stock:
                        product['stock'] = new_stock

                    file_json.save(products)
                    print("El producto se ha actualizado con éxito")
                    print("Regresando al menú de productos")
                    time.sleep(2)
                    return
            print("No se ha encontrado el producto")
            time.sleep(2)
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
        except Exception as e:
            print(f"Error: {e}")

    def delete_product(self, description):
        file_json = JsonFile(path + '/archivos/products.json')
        try:
            products = file_json.read()
            if products is None:
                print("No hay productos para eliminar")
                time.sleep(2)
                return
            if not description:
                print("Por favor, ingrese una descripción válida")
                time.sleep(2)
                return
            for i, product in enumerate(products):
                if product['descripcion'] == description:
                    del products[i]
                    file_json.save(products)
                    print("El producto se ha eliminado con éxito")
                    time.sleep(2)
                    return
            print("No se ha encontrado el producto")
            time.sleep(2)
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

    def consult_product(self, id=None):
        file_json = JsonFile(path + '/archivos/products.json')
        valida = Valida()
        while True:
            if id is None or not valida.only_numbers(id):
                id = input("Ingrese un ID valido: ")
            else:
                break
        id = int(id)
        try:
            products = file_json.read()
            if products is None:
                print("No hay productos para consultar")
                time.sleep(2)
                return
            for product in products:
                if product['id'] == id:
                    print("Información del producto:")
                    product_info = ', '.join([f"{key}: {value}" for key, value in product.items()])
                    print(product_info)
                    time.sleep(4)
                    return
            print("No se ha encontrado el producto")
            time.sleep(2)
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
        except Exception as e:
            print(f"Error: {e}")

    def update_invoice(self, invoice_number):
        file_json = JsonFile(path + '/archivos/invoices.json')
        product_json = JsonFile(path + '/archivos/products.json')
        invoice_number = int(invoice_number)
        valida = Valida()
        try:
            invoices = file_json.read()
            products = product_json.read()
            if invoices is None:
                print("No hay facturas para actualizar")
                time.sleep(2)
                return
            for invoice in invoices:
                if invoice['factura'] == invoice_number:
                    print("Información de la factura:")
                    for key, value in invoice.items():
                        if key != 'detalle':
                            print(f"{key}: {value}")
                    print("Información del cliente:")
                    print(invoice['cliente'])
                    print("Productos en la factura:")
                    for product in invoice['detalle']:
                        product_info = ', '.join([f"{key}: {value}" for key, value in product.items()])
                        print(product_info)
                    while True:
                        print("1. Añadir producto")
                        print("2. Eliminar producto")
                        print("3. Cambiar cantidad de producto")
                        print("4. Salir y actualizar factura")
                        option = input("Seleccione una opción: ")

                        if option == "1":
                            while True:
                                product_id = input("Ingrese el ID del producto que desea añadir: ")
                                if valida.only_numbers(product_id):
                                    product_id = int(product_id)
                                    break
                                else:
                                    print("Por favor, ingrese un número válido para el ID del producto")
                                    time.sleep(2)
                            product_to_add = None
                            for product in products:
                                if product['id'] == product_id:
                                    product_to_add = product
                                    break
                            if product_to_add is None:
                                print("Producto no encontrado")
                                time.sleep(2)
                                continue
                            while True:
                                product_quantity = input("Ingrese la cantidad del producto que desea añadir: ")
                                if valida.only_numbers(product_quantity):
                                    product_quantity = int(product_quantity)
                                    break
                                else:
                                    print("Por favor, ingrese un número válido para la cantidad")
                                    time.sleep(2)
                            new_product = {
                                "producto": product_to_add['descripcion'],
                                "cantidad": product_quantity,
                                "precio": product_to_add['precio']
                            }
                            invoice['detalle'].append(new_product)
                            invoice['subtotal'] = sum([float(product['precio']) * int(product['cantidad']) for product in invoice['detalle']])
                            invoice['descuento'] = invoice['subtotal'] * 0.10
                            invoice['iva'] = invoice['subtotal'] * 0.12
                            invoice['total'] = invoice['subtotal'] - invoice['descuento'] + invoice['iva']

                            print("Se ha añadido el producto")
                        elif option == "2":
                            product_description = input("Ingrese la descripción del producto que desea eliminar: ")
                            for i, product in enumerate(invoice['detalle']):
                                if product['producto'] == product_description:
                                    del invoice['detalle'][i]
                                    invoice['subtotal'] = sum([float(product['precio']) * int(product['cantidad']) for product in invoice['detalle']])
                                    invoice['descuento'] = invoice['subtotal'] * 0.10  # Assuming a 10% discount
                                    invoice['iva'] = invoice['subtotal'] * 0.12  # Assuming a 12% iva
                                    invoice['total'] = invoice['subtotal'] - invoice['descuento'] + invoice['iva']
                                    print("Se ha eliminado el producto")
                                    time.sleep(2)
                                    break
                            else:
                                print("Producto no encontrado")
                        elif option == "3":
                            product_description = input("Ingrese la descripción del producto cuya cantidad desea cambiar: ")
                            for product in invoice['detalle']:
                                if product['producto'] == product_description:
                                    while True:
                                        new_quantity = input("Ingrese la nueva cantidad del producto: ")
                                        if valida.only_numbers(new_quantity):
                                            new_quantity = int(new_quantity)
                                            break
                                        else:
                                            print("Por favor, ingrese un número válido para la cantidad")
                                            time.sleep(2)
                                    product['cantidad'] = new_quantity
                                    invoice['subtotal'] = sum([float(product['precio']) * int(product['cantidad']) for product in invoice['detalle']])
                                    invoice['descuento'] = invoice['subtotal'] * 0.10  # Assuming a 10% discount
                                    invoice['iva'] = invoice['subtotal'] * 0.12  # Assuming a 12% iva
                                    invoice['total'] = invoice['subtotal'] - invoice['descuento'] + invoice['iva']
                                    print("Se ha actualizado el producto")
                                    time.sleep(2)
                                    break
                            else:
                                print("Producto no encontrado")
                                time.sleep(2)
                        elif option == "4":
                            print("Datos guardados con exito")
                            time.sleep(2)
                            break
                        else:
                            print("Opción no válida")
                            time.sleep(2)

                    file_json.save(invoices)
                    print("La factura se ha actualizado con éxito")
                    return
            print("No se ha encontrado la factura")
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
        except Exception as e:
            print(f"Error: {e}")

    def delete_invoice(self, invoice_number):
        valida = Valida()
        if not valida.only_numbers(invoice_number):
            print("El número de factura debe ser un número")
            return

        file_json = JsonFile(path + '/archivos/invoices.json')
        invoice_number = int(invoice_number)
        try:
            invoices = file_json.read()
            if invoices is None:
                print("No hay facturas para eliminar")
                return
            for i, invoice in enumerate(invoices):
                if invoice['factura'] == invoice_number:
                    del invoices[i]
                    file_json.save(invoices)
                    print("La factura se ha eliminado con éxito")
                    return
            print("No se ha encontrado la factura")
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON")
        except Exception as e:
            print(f"Error: {e}")










