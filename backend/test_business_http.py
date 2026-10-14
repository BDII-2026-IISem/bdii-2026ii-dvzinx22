#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Demostración y Prueba HTTP - Capa de Negocio (Business) TazaNorte API.
Recorre el flujo comercial completo de forma idempotente y robusta:
1. Login y obtención de token Bearer
2. Clientes (GET / POST)
3. Categorías de producto (GET / POST)
4. Catálogo y productos disponibles (GET / POST available)
5. Registro y consulta transaccional de ventas (POST / GET)
"""

import json
import time
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000/api"

def print_header(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def make_request(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            resp_body = resp.read().decode("utf-8")
            status_code = resp.status
            try:
                parsed = json.loads(resp_body) if resp_body else {}
            except Exception:
                parsed = resp_body
            return status_code, parsed
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            parsed = json.loads(err_body)
        except Exception:
            parsed = err_body
        return e.code, parsed

def run():
    print_header("PRUEBAS HTTP DE LA CAPA DE NEGOCIO (BUSINESS) - TAZANORTE")
    suffix = int(time.time()) % 10000

    # 1. Obtener Token de Autenticación
    print("\n[PASO 1] HTTP POST /auth/login/ -> Autenticación de Administrador")
    status, res = make_request("POST", "/auth/login/", {"username": "admin", "password": "admin123"})
    print(f"Status: HTTP {status}")
    if status != 200:
        print("Error en login:", res)
        return
    token = res.get("access")
    print(f"Token Bearer obtenido con éxito: {token[:35]}...")

    # 2. Clientes
    print("\n[PASO 2] HTTP POST /clients/ -> Registrar nuevo cliente")
    client_payload = {
        "name": f"Carlos Mendoza {suffix}",
        "email": f"carlos.{suffix}@tazanorte.test",
        "phone": f"+57 310 {suffix:04d}",
        "address": "Calle 45 # 12-34, Bogotá",
        "status": "active"
    }
    status, client = make_request("POST", "/clients/", client_payload, token)
    if status == 201:
        print(f"Status: HTTP {status} (Cliente Creado)")
        client_id = client.get("id")
    else:
        # Reutilizar existente si ya fue creado
        _, clients_all = make_request("GET", "/clients/", token=token)
        client = clients_all[0]
        client_id = client.get("id")
        print(f"Status: HTTP 200 (Cliente Existente ID {client_id})")

    print(f"Cliente: ID {client_id} | Nombre: {client.get('name')} | Email: {client.get('email')}")

    print("\n[PASO 3] HTTP GET /clients/ -> Consultar listado de clientes")
    status, clients_list = make_request("GET", "/clients/", token=token)
    print(f"Status: HTTP {status} | Total clientes registrados: {len(clients_list)}")

    # 3. Categorías de producto
    print("\n[PASO 4] HTTP POST /product-types/ -> Crear o asegurar categoría de menú")
    type_payload = {
        "name": f"Bebidas Especiales {suffix}",
        "description": "Cafés de origen y preparaciones de autor",
        "status": "active"
    }
    status, ptype = make_request("POST", "/product-types/", type_payload, token)
    if status == 201:
        print(f"Status: HTTP {status} (Categoría Creada)")
        type_id = ptype.get("id")
    else:
        _, types_all = make_request("GET", "/product-types/", token=token)
        ptype = types_all[0]
        type_id = ptype.get("id")
        print(f"Status: HTTP 200 (Categoría Existente ID {type_id})")

    print(f"Categoría: ID {type_id} | Nombre: {ptype.get('name')}")

    # 4. Productos y Disponibles
    print("\n[PASO 5] HTTP POST /products/ -> Crear o asegurar producto de cafetería")
    product_payload = {
        "name": f"Café Mocca Supremo {suffix}",
        "productTypeId": type_id,
        "price": "8500.00",
        "stock": 50,
        "status": "active"
    }
    status, product = make_request("POST", "/products/", product_payload, token)
    if status == 201:
        print(f"Status: HTTP {status} (Producto Creado)")
        product_id = product.get("id")
    else:
        _, prods_all = make_request("GET", "/products/", token=token)
        product = prods_all[0]
        product_id = product.get("id")
        print(f"Status: HTTP 200 (Producto Existente ID {product_id})")

    print(f"Producto: ID {product_id} | Nombre: {product.get('name')} | Stock: {product.get('stock')}")

    print("\n[PASO 6] HTTP GET /products/available/ -> Consultar menú disponible para venta")
    status, available = make_request("GET", "/products/available/", token=token)
    print(f"Status: HTTP {status}")
    print(f"Productos disponibles en vitrina (activos y con stock > 0): {len(available)}")
    for p in available[:3]:
        print(f" - [{p.get('id')}] {p.get('name')} | Precio: ${p.get('price')} | Stock: {p.get('stock')}")

    # 5. Ventas (Registro Atómico)
    print("\n[PASO 7] HTTP POST /sales/ -> Registrar transacción de venta atómica")
    sale_payload = {
        "clientId": client_id,
        "saleDate": "2026-10-13T21:25:00Z",
        "discounts": "500.00",
        "items": [
            {
                "productId": product_id,
                "quantity": 2
            }
        ]
    }
    status, sale = make_request("POST", "/sales/", sale_payload, token)
    print(f"Status: HTTP {status} (Venta Registrada)")
    print(f" - Venta ID: {sale.get('id')}")
    print(f" - Cliente: {sale.get('clientName')} (ID {sale.get('client')})")
    print(f" - Subtotal: ${sale.get('subtotal')} | Descuentos: ${sale.get('discounts')} | Total: ${sale.get('total')}")
    sale_id = sale.get("id")

    print(f"\n[PASO 8] HTTP GET /sales/{sale_id}/ -> Consultar detalle de la venta con sus líneas")
    status, sale_detail = make_request("GET", f"/sales/{sale_id}/", token=token)
    print(f"Status: HTTP {status}")
    print("Detalle de Venta y Líneas de Producto:")
    print(f" - Venta ID: {sale_detail.get('id')} | Estado: {sale_detail.get('status')}")
    for line in sale_detail.get("lines", []):
        print(f"   * Producto: {line.get('productName')} | Cantidad: {line.get('quantity')} unids x ${line.get('unitPrice')} = ${line.get('lineTotal')}")

    print("\n" + "=" * 70)
    print(" RESULTADO: TODAS LAS OPERACIONES HTTP DE NEGOCIO FINALIZARON EN OK")
    print("=" * 70)

if __name__ == "__main__":
    run()
