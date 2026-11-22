# Servicio de asistencia de Netheret, paso 16: versión final

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

Un ejemplo para enseñar. En dieciséis pasos hemos construido una aplicación web de servicio de asistencia para Netheret, una empresa inventada que da soporte informático a pequeñas empresas. Esta es la aplicación terminada, con su registro de cambios, sus fuentes y su registro de pruebas.

## Qué hace la aplicación

| Rol | Qué puede hacer |
|------|------------------|
| Cliente | Crear solicitudes de soporte, seguir las solicitudes de su empresa en una línea de tiempo, añadir comentarios, leer la base de conocimiento |
| Agente de Tier 1 | Clasificar la cola, asignar y escalar solicitudes, añadir actualizaciones internas o visibles para el cliente, registrar solicitudes por los clientes, usar y escribir la base de conocimiento |
| Técnico de Tier 2 / Tier 3 | Coger y trabajar las solicitudes escaladas, ver su propia agenda, leer las fichas de trabajo y marcar el progreso |
| Responsable | Todo lo que puede hacer el personal, y además asignar a cualquiera, programar trabajos in situ y ver los informes |

Todo el mundo puede elegir texto más grande y alto contraste en Settings.

## Ejecútalo

Necesitas Python 3.10 o una versión más nueva.

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Abre http://127.0.0.1:5000. `python seed.py` borra todo y carga
datos de ejemplo nuevos cada vez que lo ejecutas.

### Cuentas de demostración

Todas usan la contraseña de demostración `password123`, que es solo para estos datos
de ejemplo.

| Rol | Correo |
|------|-------|
| Responsable | `manager@netheret.example` |
| Tier 1 | `tier1@netheret.example` |
| Tier 2 | `tier2@netheret.example` |
| Tier 3 | `tier3@netheret.example` |
| Cliente (Brightwell Bakery) | `customer@brightwell.example` |
| Cliente (Harbour Dental Practice) | `customer@harbour.example` |

### En un servidor real

Pon en `SECRET_KEY` un valor largo y aleatorio y `SESSION_COOKIE_SECURE=1`
detrás de HTTPS, y ejecuta la aplicación con un servidor web de producción en lugar de
`flask run`. Sin `SECRET_KEY`, la aplicación crea una clave aleatoria cada vez que
arranca, lo que está bien en tu propio ordenador.

## Cómo está organizado el código

```
requirements.txt       Flask and Flask-SQLAlchemy, pinned
seed.py                sample data (deletes everything first)
helpdesk/
  __init__.py          create_app(): settings and blueprints
  extensions.py        the db object
  models.py            the six tables and the allowed values
  auth.py              sign in and out, login_required, role_required
  security.py          CSRF token and security headers
  main.py              home, dashboard, privacy, error pages
  tickets.py           raise, queue, detail, assign, escalate, updates
  customer.py          the customer's requests and comments
  jobs.py              scheduling, week view, my schedule, job briefs
  articles.py          the knowledge base
  reports.py           KPIs for managers
  settings.py          accessibility settings
  filters.py           how dates are shown
  templates/           Jinja templates, one folder per feature
  static/css/style.css all the styles
  static/js/charts.js  bar charts drawn from the report tables
docs/
  test-log.md          fifty manual tests and their results
  change-log.md        what each step changed, and why
  sources.md           what came from where, and the use of AI
```

## Una demostración corta, para grabar la pantalla

1. Inicia sesión como el cliente de Brightwell y crea una solicitud.
2. Inicia sesión como Tier 1: búscala en la cola, lee un artículo relacionado y luego
   escálala a Tier 2 con un motivo.
3. Inicia sesión como responsable: asígnala a Sam Okafor y programa una visita.
4. Inicia sesión como Tier 2: abre My schedule, lee la ficha del trabajo y márcalo como hecho.
5. De vuelta como cliente: la línea de tiempo muestra la visita, pero no las notas
   internas.
6. Como responsable, abre Reports. Después activa el texto más grande y el alto contraste.

## En qué fijarse

- `docs/test-log.md`: qué se probó, qué falló y cómo se corrigió.
- `docs/sources.md`: de qué documentación sale cada patrón, y qué
  se cambió después de revisar el código escrito por la IA.
- Ejecuta `git log --oneline` y `git checkout step-07` (cualquier paso) para ver la
  aplicación tal como era en ese momento. `git checkout main` te devuelve al final.

## Aprende este paso

Este es el paso 16 de 16 de **Task 2. Developing the solution**, una serie gratuita de lecciones de T Level Digital Software Development, en inglés, que construye el servicio de asistencia de Netheret en sprints ágiles con Python y Flask. Lee la lección de este paso:
[Registro de cambios, fuentes y la aplicación terminada](https://mitsurutech.co.uk/resources/t-level/dsd-t2-16-final).

- Paso anterior: [paso 15, probar a mano y el registro de pruebas](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [Todas las lecciones gratuitas de T Level Digital](https://mitsurutech.co.uk/resources/t-level)
- [Enseña estas lecciones a tu clase en MitsuruTech](https://mitsurutech.co.uk/es/learning), [mira los precios](https://mitsurutech.co.uk/es/pricing) o
  [empieza un año gratis para tu centro](https://mitsurutech.co.uk/es/signup)

## Acerca de

Escrito por [Mitsuru Technologies](https://mitsurutech.co.uk/es) (MitsuruTech) como ejemplo para enseñar T Level Digital
Software Development. El encargo de Netheret IT Support Solutions procede del material de evaluación de muestra de Pearson; este código
y sus notas son nuestros, y no los publica, respalda ni aprueba Pearson ni el Department for Education.
"T Level" es una marca registrada del Department for Education.
