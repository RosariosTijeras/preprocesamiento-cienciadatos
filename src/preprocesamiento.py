import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class PreprocesadorDatos:
    def __init__(self):
        self.scaler = None
        self.label_encoders = {}
        
    def cargar_datos(self, ruta_archivo):
        """Carga datos desde diferentes formatos"""
        try:
            if ruta_archivo.endswith('.csv'):
                return pd.read_csv(ruta_archivo)
            elif ruta_archivo.endswith(('.xlsx', '.xls')):
                return pd.read_excel(ruta_archivo)
            else:
                raise ValueError("Formato de archivo no soportado")
        except Exception as e:
            print(f"Error cargando archivo: {e}")
            return None
    
    def explorar_datos(self, df):
        """Exploración básica del dataset"""
        print("=== EXPLORACIÓN DE DATOS ===")
        print(f"Dimensiones: {df.shape}")
        print("\nTipos de datos:")
        print(df.dtypes)
        print("\nValores nulos por columna:")
        print(df.isnull().sum())
        print("\nEstadísticas descriptivas:")
        print(df.describe())
        
        return {
            'filas': df.shape[0],
            'columnas': df.shape[1],
            'valores_nulos': df.isnull().sum().sum(),
            'duplicados': df.duplicated().sum()
        }
    
    def manejar_valores_nulos(self, df, estrategia='eliminar', columnas_especificas=None):
        """Manejo de valores nulos con diferentes estrategias"""
        df_limpio = df.copy()
        
        if columnas_especificas is None:
            columnas_especificas = df.columns
            
        for columna in columnas_especificas:
            if df[columna].isnull().sum() > 0:
                if estrategia == 'eliminar':
                    df_limpio = df_limpio.dropna(subset=[columna])
                elif estrategia == 'media':
                    if df[columna].dtype in ['int64', 'float64']:
                        df_limpio[columna].fillna(df[columna].mean(), inplace=True)
                elif estrategia == 'mediana':
                    if df[columna].dtype in ['int64', 'float64']:
                        df_limpio[columna].fillna(df[columna].median(), inplace=True)
                elif estrategia == 'moda':
                    df_limpio[columna].fillna(df[columna].mode()[0], inplace=True)
                elif estrategia == 'cero':
                    df_limpio[columna].fillna(0, inplace=True)
                    
        print(f"Valores nulos restantes: {df_limpio.isnull().sum().sum()}")
        return df_limpio
    
    def eliminar_duplicados(self, df):
        """Elimina filas duplicadas"""
        filas_originales = df.shape[0]
        df_sin_duplicados = df.drop_duplicates()
        filas_finales = df_sin_duplicados.shape[0]
        
        print(f"Duplicados eliminados: {filas_originales - filas_finales}")
        return df_sin_duplicados
    
    def normalizar_datos(self, df, columnas_numericas, metodo='standard'):
        """Normalización de datos numéricos"""
        if self.scaler is None:
            if metodo == 'standard':
                self.scaler = StandardScaler()
            elif metodo == 'minmax':
                self.scaler = MinMaxScaler()
            else:
                raise ValueError("Método no soportado")
                
        df_normalizado = df.copy()
        df_normalizado[columnas_numericas] = self.scaler.fit_transform(df[columnas_numericas])
        
        print(f"Columnas normalizadas ({metodo}): {columnas_numericas}")
        return df_normalizado
    
    def codificar_categoricas(self, df, columnas_categoricas, metodo='label'):
        """Codificación de variables categóricas"""
        df_codificado = df.copy()
        
        for columna in columnas_categoricas:
            if metodo == 'label':
                if columna not in self.label_encoders:
                    self.label_encoders[columna] = LabelEncoder()
                df_codificado[columna] = self.label_encoders[columna].fit_transform(df[columna])
            elif metodo == 'onehot':
                dummies = pd.get_dummies(df[columna], prefix=columna)
                df_codificado = pd.concat([df_codificado, dummies], axis=1)
                df_codificado.drop(columna, axis=1, inplace=True)
                
        print(f"Columnas codificadas ({metodo}): {columnas_categoricas}")
        return df_codificado
    
    def pipeline_completo(self, ruta_archivo, configuracion):
        """Pipeline completo de preprocesamiento"""
        print("🎯 INICIANDO PIPELINE DE PREPROCESAMIENTO")
        
        # 1. Cargar datos
        df = self.cargar_datos(ruta_archivo)
        if df is None:
            raise Exception("No se pudo cargar el dataset")
        print("✅ Datos cargados correctamente")
        
        # 2. Exploración inicial
        estadisticas = self.explorar_datos(df)
        
        # 3. Manejar valores nulos
        df = self.manejar_valores_nulos(
            df, 
            estrategia=configuracion.get('estrategia_nulos', 'eliminar'),
            columnas_especificas=configuracion.get('columnas_nulos')
        )
        
        # 4. Eliminar duplicados
        df = self.eliminar_duplicados(df)
        
        # 5. Normalizar datos numéricos
        if configuracion.get('columnas_numericas'):
            df = self.normalizar_datos(
                df, 
                configuracion['columnas_numericas'],
                metodo=configuracion.get('metodo_normalizacion', 'standard')
            )
        
        # 6. Codificar categóricas
        if configuracion.get('columnas_categoricas'):
            df = self.codificar_categoricas(
                df,
                configuracion['columnas_categoricas'],
                metodo=configuracion.get('metodo_codificacion', 'label')
            )
        
        print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
        return df

def crear_dataset_ejemplo():
    """Crea un dataset de ejemplo para pruebas"""
    # Asegurar que la carpeta data existe
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    datos_ejemplo = {
        'edad': [25, 30, np.nan, 35, 25, 30, 40, np.nan],
        'salario': [50000, 60000, 70000, np.nan, 50000, 60000, 80000, 55000],
        'departamento': ['Ventas', 'IT', 'Ventas', 'IT', 'Ventas', 'HR', 'IT', 'HR'],
        'experiencia': [2, 5, 3, 7, 2, 4, 10, 3]
    }
    
    df = pd.DataFrame(datos_ejemplo)
    df.to_csv('data/dataset_ejemplo.csv', index=False)
    print("✅ Dataset de ejemplo creado en data/dataset_ejemplo.csv")
    return df

def ejecutar_ejemplo_completo():
    """Ejecuta un ejemplo completo del pipeline"""
    print("🚀 INICIANDO EJEMPLO COMPLETO")
    
    # Crear dataset de ejemplo
    crear_dataset_ejemplo()
    
    # Configuración del preprocesamiento
    config = {
        'estrategia_nulos': 'media',
        'columnas_numericas': ['edad', 'salario', 'experiencia'],
        'columnas_categoricas': ['departamento'],
        'metodo_normalizacion': 'standard',
        'metodo_codificacion': 'label'
    }
    
    # Ejecutar pipeline
    preprocesador = PreprocesadorDatos()
    df_procesado = preprocesador.pipeline_completo('data/dataset_ejemplo.csv', config)
    
    # Guardar resultado
    df_procesado.to_csv('outputs/dataset_procesado.csv', index=False)
    print("✅ Dataset procesado guardado en outputs/dataset_procesado.csv")
    
    print("\n📊 DATASET FINAL PROCESADO:")
    print(df_procesado.head())
    print(f"\n📈 Dimensiones finales: {df_procesado.shape}")
    
    return df_procesado

if __name__ == "__main__":
    resultado = ejecutar_ejemplo_completo()
    print("\n✅ Script ejecutado exitosamente")