# strata-registro — the daily witness of Strata Observatory

*Español más abajo.*

This repository is the **daily witness** of the Strata Observatory archive. Every morning,
after the day is sealed, the observatory appends one line here and pushes it. It holds no
observation from the archive, only its fingerprint.

## What is in it

- **`resumenes.txt`**: one line per day since 2026-09-02, `<day> <resumen_dia>`.
  `resumen_dia` is a SHA-256 in lowercase hex: the fingerprint of that day's header, which
  in turn chains the previous day's fingerprint and the root of the tree of every entry of
  the day. A line is never rewritten, and a missing day would show as a gap.
- **`registro_publico.jsonl`**: one line per day, the day's header exactly as it was
  sealed. It has six fields and no others: `version`, `dia`, `raiz_lote`, `dia_anterior`,
  `resumen_anterior` and `resumen_dia`. None of them is a measurement: no counts, no
  absences, not even how many entries the day had.
- **`.github/`**: the standby watchdog. It runs here, not on the observatory's machine, and
  opens an issue if the day's line has not arrived or if the series has a gap.

## How to check a day

Take that day's line in `registro_publico.jsonl`, in this same repository:

```python
import hashlib, json
header = json.loads(line)                 # the day's line in registro_publico.jsonl
header.pop("resumen_dia", None)
canonical = json.dumps(header, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
print(hashlib.sha256(b"\x02" + canonical.encode("utf-8")).hexdigest())
```

The result must be that day's line in `resumenes.txt`, and the header's `resumen_anterior`
must be the previous day's line. This serialisation is valid for the header, which holds
only strings and `null`. The full canonical rules are in the sealing specification that
comes with the archive.

**What anyone can check with this repository alone:** every summary, recomputed from its
header, and the whole chain, day by day, with no gap and no rewritten link.

**What it does not prove on its own.**
- **That the root corresponds to real observations.** `raiz_lote` is opaque without the
  day's entries, which are not published. Given any one entry of a day, a proof of
  inclusion ties it to that root; without entries, the root is only a commitment.
- **The date.** We set the time of each commit ourselves; what counts is when GitHub
  received the push, and GitHub does not keep that in a form anyone can query again years
  later. That is why this witness is one of three layers, not the only one.

## More

- Who we are, how we read and how to stop us: https://github.com/strataobservatory
- The observation method, every version, with the days each one governs:
  https://github.com/strataobservatory/strata-metodo

---

## En español

Este repositorio es el **testigo diario** del archivo de Strata Observatory. Cada mañana,
después de sellar el día, el observatorio añade aquí una línea y la empuja. No contiene
ninguna observación del archivo, sólo su huella.

**Qué contiene.**
- **`resumenes.txt`**: una línea por día desde el 2026-09-02, `<día> <resumen_dia>`.
  `resumen_dia` es un SHA-256 en hexadecimal: la huella de la cabecera de ese día, que a
  su vez encadena la huella del día anterior y la raíz del árbol de todas las entradas del
  día. Una línea no se reescribe nunca, y si faltara un día quedaría el hueco a la vista.
- **`registro_publico.jsonl`**: una línea por día, la cabecera del día tal como se selló.
  Tiene seis campos y ninguno más: `version`, `dia`, `raiz_lote`, `dia_anterior`,
  `resumen_anterior` y `resumen_dia`. Ninguno es una medida: ni cifras, ni ausencias, ni
  siquiera cuántas entradas tuvo el día.
- **`.github/`**: el vigía suplente. Corre aquí, no en la máquina del observatorio, y abre
  una incidencia si la línea del día no ha llegado o si la serie tiene un hueco.

**Cómo comprobar un día.** Se toma su línea en `registro_publico.jsonl`, en este mismo
repositorio. Con el código de arriba sale un hash. Tiene que coincidir con la línea de ese día en
`resumenes.txt`, y el `resumen_anterior` de la cabecera tiene que ser la línea del día
anterior.

**Lo que cualquiera comprueba sólo con este repositorio:** cada resumen, rehecho desde su
cabecera, y la cadena entera, día a día, sin huecos ni eslabones reescritos.

**Lo que no prueba por sí solo.**
- **Que la raíz corresponda a observaciones reales.** `raiz_lote` es opaca sin las entradas
  del día, que no se publican. Dada cualquier entrada de un día, una prueba de inclusión la
  ata a esa raíz; sin entradas, la raíz es sólo un compromiso.
- **La fecha.** La hora de cada commit la ponemos nosotros; la que cuenta es cuándo lo
  recibió GitHub, y GitHub no la guarda de forma que se pueda volver a consultar años
  después. Por eso este testigo es una de tres capas, no la única.

**Más.** Quiénes somos, cómo leemos y cómo pararnos: https://github.com/strataobservatory.
El método de observación, todas sus versiones y los días que gobierna cada una:
https://github.com/strataobservatory/strata-metodo.
