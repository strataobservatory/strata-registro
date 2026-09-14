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
- **`.github/`**: the standby watchdog. It runs here, not on the observatory's machine, and
  opens an issue if the day's line has not arrived or if the series has a gap.

## How to check a day

You need that day's header: its line in `registro_publico.jsonl`, which travels inside every
copy of the archive and every deposit.

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

**What it proves:** that the day, with that content, already existed when its line
reached this repository. **What it does not prove on its own:** the date. We set the time
of each commit ourselves; what counts is when GitHub received the push, and GitHub does not
keep that in a form anyone can query again years later. That is why this witness is one of
three layers, not the only one.

## More

- Who we are, how we read and how to stop us: https://github.com/strataobservatory
- The observation method travels in full inside every sealed day. It does not have a
  public address of its own yet.

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
- **`.github/`**: el vigía suplente. Corre aquí, no en la máquina del observatorio, y abre
  una incidencia si la línea del día no ha llegado o si la serie tiene un hueco.

**Cómo comprobar un día.** Hace falta la cabecera de ese día: su línea en
`registro_publico.jsonl`, que viaja dentro de cada copia del archivo y de cada depósito.
Con el código de arriba sale un hash. Tiene que coincidir con la línea de ese día en
`resumenes.txt`, y el `resumen_anterior` de la cabecera tiene que ser la línea del día
anterior.

**Lo que prueba:** que ese día, con ese contenido, ya existía cuando su línea llegó aquí.
**Lo que no prueba por sí solo:** la fecha. La hora de cada commit la ponemos nosotros; la
que cuenta es cuándo lo recibió GitHub, y GitHub no la guarda de forma que se pueda volver
a consultar años después. Por eso este testigo es una de tres capas, no la única.

**Más.** Quiénes somos, cómo leemos y cómo pararnos: https://github.com/strataobservatory.
El método de observación viaja íntegro dentro de cada día sellado. Todavía no tiene una
dirección pública propia.
