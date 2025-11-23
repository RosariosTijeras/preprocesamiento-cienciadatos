import cProfile
import codigo_original
import codigo_optimizado

print("=== PROFILING CÓDIGO ORIGINAL ===")
cProfile.run('codigo_original.main()', 'perfil_original.prof')

print("\n=== PROFILING CÓDIGO OPTIMIZADO ===")
cProfile.run('codigo_optimizado.main()', 'perfil_optimizado.prof')