"""
Script de prueba para validar la firma y verificación asimétrica (RSA/RS256)
entre el backend PHP de DIRPOLES_4 y el microservicio Python DIRPOLES_IA.
"""

import os
import time
import jwt

# Rutas a las llaves (acceso directo para pruebas de integración local)
PRIVATE_KEY_PATH = r"C:\xampp\htdocs\DIRPOLES_4\app\Config\Keys\jwt_private.pem"
PUBLIC_KEY_PATH = r"C:\xampp\htdocs\DIRPOLES_IA\certs\jwt_public.pem"

def ejecutar_prueba():
    print("=" * 60)
    print("INICIANDO PRUEBA DE AUTENTICACIÓN RSA (RS256)")
    print("=" * 60)
    
    # 1. Verificar existencia de las llaves
    if not os.path.exists(PRIVATE_KEY_PATH):
        print(f"[-] ERROR: No se encontró la llave privada en {PRIVATE_KEY_PATH}")
        print("Asegúrate de tener el backend de DIRPOLES_4 en la misma máquina local.")
        return
        
    if not os.path.exists(PUBLIC_KEY_PATH):
        print(f"[-] ERROR: No se encontró la llave pública en {PUBLIC_KEY_PATH}")
        return
        
    print("[+] Llaves encontradas correctamente.")
    
    # 2. Simular generación de JWT en PHP (Firmado con Llave Privada)
    print("\n[1] Generando JWT simulación PHP (firmado con llave privada)...")
    try:
        with open(PRIVATE_KEY_PATH, "r") as f:
            private_key_pem = f.read()
            
        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600, # 1 hora de validez
            "data": {
                "id_usuario": 42,
                "nombre": "Administrador de DIRPOLES_4",
                "correo": "admin@dirpoles.gob.ve",
                "rol": "coordinador"
            }
        }
        
        # Codificamos usando RS256 y la llave privada
        token = jwt.encode(payload, private_key_pem, algorithm="RS256")
        print(f"[+] Token JWT generado con éxito:")
        print(f"    {token[:40]}...{token[-40:]}")
        
    except Exception as e:
        print(f"[-] ERROR al simular generación de token: {e}")
        return

    # 3. Simular validación en Python (Verificado con Llave Pública)
    print("\n[2] Validando JWT en Python (verificado con llave pública)...")
    try:
        with open(PUBLIC_KEY_PATH, "r") as f:
            public_key_pem = f.read()
            
        # Decodificamos usando la llave pública
        decoded_payload = jwt.decode(token, public_key_pem, algorithms=["RS256"])
        print("[+] ¡CONEXIÓN SEGURA EXITOSA! El token es 100% legítimo.")
        print("[+] Payload decodificado correctamente:")
        for k, v in decoded_payload.items():
            print(f"    - {k}: {v}")
            
    except jwt.ExpiredSignatureError:
        print("[-] ERROR: El token ha expirado.")
    except jwt.InvalidSignatureError:
        print("[-] ERROR: Firma inválida. El token fue alterado o firmado con otra llave.")
    except Exception as e:
        print(f"[-] ERROR al validar el token: {e}")

    print("=" * 60)

if __name__ == "__main__":
    ejecutar_prueba()
