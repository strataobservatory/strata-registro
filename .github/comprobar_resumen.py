"""¿Ha sellado hoy el observatorio? Se pregunta desde FUERA de la máquina que sella.

**Contra qué existe.** Con la copia diaria puesta, el riesgo que le queda al proyecto ya no
es perder el archivo: es **enterarse tarde de que la pasada no corrió**. Y eso no lo puede
vigilar la propia máquina — el 2026-09-04 estuvo apagada y se perdió la ejecución del vigía
sin dejar error, ni fichero, ni una línea.

**Por qué mira `resumenes.txt` y no otra cosa.** Es la señal que **ya existe**: la capa C la
empuja al alojamiento cada día como parte de su trabajo, así que este comprobador no añade
nada al camino crítico ni toca el archivo. Y es una señal **del tercero**: lo que se lee es
lo que el alojamiento tiene, no lo que nosotros decimos tener.

**Lo que NO hace, y es deliberado.** No ejecuta la pasada, no escribe en el archivo y no
sabe nada de él. Un suplente que escribiera sería más peligroso que el hueco que tapa: dos
escritores sobre una cadena no dan un conflicto, dan **dos historias incompatibles del mismo
día**, y el producto entero consiste en que haya exactamente una.

**Y lo que no cubre, dicho aquí.** Que un alojamiento tenga la línea de hoy prueba que la
capa C empujó, no que el día se sellara entero ni bien. Es un detector de **silencio**, no un
verificador: para eso están `verificar archivo` y `verificar capas`, que necesitan el archivo
delante.
"""

import datetime
import os
import sys

#: Cuántas horas de gracia desde el final del día UTC antes de dar la voz.
#:
#: La pasada corre a las 07:00 locales (05:00 UTC) y empuja sobre las 05:45 UTC. Con 15 h
#: desde el comienzo del día se avisa a las 15:00 UTC —17:00 locales—, lo que deja **nueve
#: horas de margen** para que una máquina que arrancó tarde haga la pasada y empuje.
#:
#: El margen es ancho a propósito. Un suplente que avisa de mañanas que acaban bien es un
#: suplente que se acaba silenciando, y entonces no avisa del día que importa.
HORAS_DE_GRACIA = 15


def ultimo_dia(texto: str) -> str:
    """La última fecha que aparece en el fichero de resúmenes, o cadena vacía."""
    fechas = []
    for linea in texto.splitlines():
        cacho = linea.strip().split(" ", 1)[0]
        if len(cacho) == 10 and cacho[4] == "-" and cacho[7] == "-":
            fechas.append(cacho)
    return max(fechas) if fechas else ""


def huecos(texto: str) -> list:
    """Los días que faltan en la serie, entre el primero y el último que hay.

    **Por qué hace falta además del veredicto.** El veredicto mira sólo si el último
    resumen es de hoy. Si un día se pierde y ESE día el suplente no llega a correr —el
    alojamiento descarta ejecuciones programadas cuando va cargado, y lo documenta—, al
    día siguiente ya hay resumen nuevo, el veredicto dice «al día», y el día perdido no
    lo denuncia nadie nunca. La serie, en cambio, lo guarda para siempre: un hueco en ella
    es un día que no se selló, y eso no caduca.
    """
    fechas = set()
    for linea in texto.splitlines():
        cacho = linea.strip().split(" ", 1)[0]
        if len(cacho) == 10 and cacho[4] == "-" and cacho[7] == "-":
            try:
                fechas.add(datetime.date.fromisoformat(cacho))
            except ValueError:
                continue
    if not fechas:
        return []
    dia, fin, faltan = min(fechas), max(fechas), []
    while dia < fin:
        dia += datetime.timedelta(days=1)
        if dia not in fechas:
            faltan.append(dia.isoformat())
    return faltan


def veredicto(texto: str, ahora: datetime.datetime,
              horas=HORAS_DE_GRACIA) -> tuple:
    """(¿hay que avisar?, motivo). Función pura: se puede probar sin red y sin repo.

    Está separada del mando a propósito. Una regla metida dentro de algo que habla con
    GitHub no se puede comprobar, y ayer la campaña ya enseñó lo que cuesta eso: cuatro
    reglas declaradas protegidas que no lo estaban.
    """
    ultimo = ultimo_dia(texto)
    if not ultimo:
        return True, ("el fichero de resúmenes no tiene ni una fecha legible: o está "
                      "vacío o no es lo que se espera")

    hoy = ahora.date()
    esperado = hoy if ahora.hour >= horas else hoy - datetime.timedelta(days=1)
    if ultimo >= esperado.isoformat():
        return False, f"al día: el último resumen es del {ultimo}"

    atraso = (hoy - datetime.date.fromisoformat(ultimo)).days
    return True, (
        f"el último resumen del observatorio es del {ultimo} y hoy es {hoy.isoformat()} "
        f"({atraso} día(s) de atraso). La pasada diaria no ha llegado a empujar su "
        "resumen: o no corrió, o corrió y no pudo hablar con el alojamiento. Un día que "
        "no se sella NO se puede sellar después")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    ruta = argv[0] if argv else "resumenes.txt"
    if not os.path.exists(ruta):
        print(f"no existe {ruta}", file=sys.stderr)
        return 1
    with open(ruta, encoding="utf-8") as fichero:
        texto = fichero.read()

    hay_que_avisar, motivo = veredicto(
        texto, datetime.datetime.now(datetime.timezone.utc))
    print(motivo)
    perdidos = huecos(texto)
    if perdidos:
        print(f"días que faltan en la serie: {', '.join(perdidos)}")

    # Se deja el veredicto donde lo lea el paso siguiente del flujo de trabajo.
    salida = os.environ.get("GITHUB_OUTPUT")
    if salida:
        with open(salida, "a", encoding="utf-8") as fichero:
            fichero.write(f"avisar={'si' if hay_que_avisar else 'no'}\n")
            fichero.write(f"motivo={motivo}\n")
            fichero.write(f"huecos={' '.join(perdidos)}\n")
    return 2 if (hay_que_avisar or perdidos) else 0


if __name__ == "__main__":
    raise SystemExit(main())
