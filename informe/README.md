# Informe Técnico - Perfil de Vuelo a LEO

## Contenido

- `informe.tex` - Documento LaTeX principal
- `informe.pdf` - PDF generado (4 páginas)
- `logo-utdt.jpg` - Logo de la institución

## Compilación

```bash
cd informe
pdflatex informe.tex
pdflatex informe.tex  # Segunda compilación para referencias
```

## Requisitos

- LaTeX (MiKTeX, TeX Live, o similar)
- Paquetes: babel-spanish, geometry, graphicx, amsmath, booktabs, float, caption, subcaption, setspace, fancyhdr, multicol

## Estructura del Informe

1. **Resumen Ejecutivo** (≤150 palabras)
2. **Hipótesis y Modelo Físico** - Ecuaciones y supuestos
3. **Metodología** - Perfil de vuelo y validación
4. **Resultados** - Gráficos de despegue y estabilidad orbital
5. **Conclusiones** - Viabilidad y recomendaciones

## Gráficos Incluidos

- `12_altura_velocidad_zoom_500s.png` - Evolución primeros 500s
- `03_posicion_radial.png` - Altura orbital largo plazo
- `02_velocidad_radial.png` - Velocidad radial largo plazo

Todos los gráficos se toman de la carpeta `../graficos/`
