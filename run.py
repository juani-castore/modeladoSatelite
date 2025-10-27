"""
Script de ayuda para ejecutar todas las funcionalidades del proyecto
"""
import sys
import subprocess

def mostrar_menu():
    print("="*70)
    print("🚀 SIMULADOR DE COHETE A ÓRBITA LEO")
    print("="*70)
    print("\nOpciones:")
    print("  1. Ejecutar simulación principal (simulacion.py)")
    print("  2. Ejecutar test de mortero (tiro parabólico)")
    print("  3. Ejecutar test de velocidad de escape")
    print("  4. Ejecutar test de órbitas LEO/GEO")
    print("  5. Ejecutar TODOS los tests")
    print("  0. Salir")
    print("="*70)

def ejecutar_comando(cmd, descripcion):
    print(f"\n▶ {descripcion}...")
    print("-"*70)
    result = subprocess.run(cmd, shell=True)
    print("-"*70)
    if result.returncode == 0:
        print(f"✓ {descripcion} completado exitosamente\n")
    else:
        print(f"✗ Error al ejecutar {descripcion}\n")
    return result.returncode

def main():
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "0":
            print("\n¡Hasta luego! 🚀")
            break
        elif opcion == "1":
            ejecutar_comando("python simulacion.py", "Simulación principal")
        elif opcion == "2":
            ejecutar_comando("python tests/test_mortero.py", "Test de mortero")
        elif opcion == "3":
            ejecutar_comando("python tests/test_velocidad_escape.py", "Test de velocidad de escape")
        elif opcion == "4":
            ejecutar_comando("python tests/test_orbitas.py", "Test de órbitas LEO/GEO")
        elif opcion == "5":
            print("\n" + "="*70)
            print("EJECUTANDO TODOS LOS TESTS")
            print("="*70)
            ejecutar_comando("python tests/test_mortero.py", "Test 1/3: Mortero")
            ejecutar_comando("python tests/test_velocidad_escape.py", "Test 2/3: Velocidad de escape")
            ejecutar_comando("python tests/test_orbitas.py", "Test 3/3: Órbitas LEO/GEO")
            print("\n" + "="*70)
            print("✓ TODOS LOS TESTS COMPLETADOS")
            print("="*70)
        else:
            print("\n⚠ Opción inválida. Por favor selecciona 0-5.")
        
        if opcion != "0":
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
