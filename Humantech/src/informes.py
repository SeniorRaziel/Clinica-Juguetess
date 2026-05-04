class EstrategiaInforme:
    def generar(self, datos, ruta):
        raise NotImplementedError

class InformeExcel(EstrategiaInforme):
    def generar(self, datos, ruta):
        import pandas as pd
        with pd.ExcelWriter(ruta, engine='xlsxwriter') as writer:
            pd.DataFrame(datos).to_excel(writer, index=False, sheet_name='Donaciones')

class InformeCSV(EstrategiaInforme):
    def generar(self, datos, ruta):
        import pandas as pd
        pd.DataFrame(datos).to_csv(ruta, index=False)

class GeneradorInforme:
    def __init__(self, estrategia: EstrategiaInforme):
        self.estrategia = estrategia

    def generar(self, datos, ruta):
        self.estrategia.generar(datos, ruta)