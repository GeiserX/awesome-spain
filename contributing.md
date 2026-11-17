# Contribuir a Awesome Spain

Gracias por tu interés en contribuir. Esta selección crece gracias a la comunidad.

## Directrices

### Añadir un proyecto

- Asegúrate de que el proyecto es **open source** y tiene un repositorio público.
- El proyecto debe **dar soporte específico a España** o incluir funcionalidades relevantes para usuarios en España.
- El repositorio debe tener **al menos 5 estrellas y 3 meses de historia**. Las PRs que proponen un repositorio por debajo de ese mínimo se cierran sin revisión; vuelve a proponerlo cuando lo alcance. Tampoco entran los volcados: uno o dos commits del mismo día, o una copia de los datos de otra web sin el código que los genera. El software de organismos oficiales queda exento.
- El proyecto debe **funcionar hoy** y no estar archivado. Si consume un servicio español, que siga funcionando contra él; si no consume ninguno (un validador de DNI, un lector de cuadernos AEB, un dataset), que su lógica o sus datos sigan siendo correctos.
- **Qué se retira**: lo archivado; lo que ya no funciona, tenga la edad que tenga; lo que ya ha sido sustituido por otra entrada mantenida de la lista, aunque tenga reputación (pasa a `DELETED.md` con el enlace a su sucesora); lo que sirve a un sistema retirado, aunque sea oficial; y lo que lleva más de 3 años sin commits en su rama por defecto sin tener reputación (un organismo oficial o una organización conocida detrás, o uso real visible), salvo que se compruebe que sigue funcionando (ejecutándolo, cotejándolo con el servicio que consume o cotejando sus datos con la fuente oficial).
- Cada entrada debe seguir el formato: `- [Nombre](URL) - Descripción breve que empieza en mayúscula y termina con punto.`
- Añade la entrada en **orden alfabético** dentro de la categoría correspondiente.
- Comprueba que no hay **duplicados** ni errores tipográficos.
- Las descripciones deben ser **concisas y objetivas** (una frase).

### Crear una nueva categoría

- Preferiblemente con al menos **3 proyectos** que la justifiquen.
- Añade la nueva categoría al **índice de contenido** en el orden adecuado.

### Formato de entrada

```markdown
- [Nombre](https://github.com/owner/repo) - Descripción que empieza en mayúscula y termina con punto.
```

Las insignias (estrellas, último commit, lenguaje, licencia y etiquetas de servicio) se generan automáticamente con `scripts/transform-readme.py`. No es necesario añadirlas manualmente.

- La descripción **no debe empezar con el nombre** del proyecto (awesome-lint lo rechaza).
- Máximo una línea por entrada.
- Las descripciones deben estar en **español**.
- Valida con `awesome-lint-extra` antes de enviar tu PR para verificar que no hay errores.

### Pull requests

1. Haz fork del repositorio.
2. Crea una rama descriptiva (`add-proyecto-x` o `nueva-categoria-y`).
3. Realiza los cambios siguiendo las directrices anteriores.
4. Envía un pull request usando la plantilla proporcionada.
5. **Incluye en la descripción de la PR la URL del servicio, API o institución española** a la que el software da soporte (p.ej. aeat.es, renfe.com, catastro.meh.es). Esto ayuda a verificar que el proyecto es relevante para España.

### Reportar problemas

Si encuentras enlaces rotos, proyectos archivados, proyectos que han dejado de funcionar o información incorrecta, abre un issue describiendo el problema.

## Insignia

Si tu proyecto está en la lista, puedes añadir una insignia a tu README. El estilo `flat` está en el
[README](https://github.com/GeiserX/awesome-spain#insignia); estos son los otros tres.

Flat square:
```markdown
[![listed on awesome-spain](https://img.shields.io/badge/listed%20on-awesome--spain-c60b1e?style=flat-square&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDIwIDE0Ij48cmVjdCB3aWR0aD0iMjAiIGhlaWdodD0iMTQiIGZpbGw9IiNjNjBiMWUiLz48cmVjdCB5PSIzLjUiIHdpZHRoPSIyMCIgaGVpZ2h0PSI3IiBmaWxsPSIjZmZjNDAwIi8+PC9zdmc+&labelColor=ffc400)](https://github.com/GeiserX/awesome-spain#readme)
```

Plastic:
```markdown
[![listed on awesome-spain](https://img.shields.io/badge/listed%20on-awesome--spain-c60b1e?style=plastic&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDIwIDE0Ij48cmVjdCB3aWR0aD0iMjAiIGhlaWdodD0iMTQiIGZpbGw9IiNjNjBiMWUiLz48cmVjdCB5PSIzLjUiIHdpZHRoPSIyMCIgaGVpZ2h0PSI3IiBmaWxsPSIjZmZjNDAwIi8+PC9zdmc+&labelColor=ffc400)](https://github.com/GeiserX/awesome-spain#readme)
```

Grande (for-the-badge):
```markdown
[![listed on awesome-spain](https://img.shields.io/badge/listed%20on-awesome--spain-c60b1e?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDIwIDE0Ij48cmVjdCB3aWR0aD0iMjAiIGhlaWdodD0iMTQiIGZpbGw9IiNjNjBiMWUiLz48cmVjdCB5PSIzLjUiIHdpZHRoPSIyMCIgaGVpZ2h0PSI3IiBmaWxsPSIjZmZjNDAwIi8+PC9zdmc+&labelColor=ffc400)](https://github.com/GeiserX/awesome-spain#readme)
```

## Código de conducta

Sé respetuoso y constructivo. Las contribuciones deben ser de buena fe y orientadas a mejorar la lista para toda la comunidad.
