# OCR INE Reverse

Script para extraer el número CIC de una credencial INE utilizando Tesseract OCR y Docker.

## Requisitos

* Docker instalado
* Imagen frontal o reversa de una credencial INE

## Estructura del proyecto

```text
ocr_ine/
├── Dockerfile
├── requirements.txt
├── main.py
├── ine-frontal.jpg
├── ine-reverse.jpg
└── images/
```

## Construir la imagen Docker

```bash
docker build -t ine-ocr .
```

## Ejecutar OCR

### Imagen frontal

```bash
docker run --rm \
-v $(pwd):/data \
ine-ocr \
/data/ine-frontal.jpg
```

### Imagen reversa

```bash
docker run --rm \
-v $(pwd):/data \
ine-ocr \
/data/ine-reverse.jpg
```

## Resultado esperado

```json
{
  "message": "ok",
  "data": {
    "ocr_cic": "1234567890123"
  }
}
```

## Verificar Tesseract dentro del contenedor

Abrir una terminal dentro del contenedor:

```bash
docker run --rm -it \
--entrypoint sh \
-v $(pwd):/data \
ine-ocr
```

Verificar versión:

```bash
tesseract --version
```

## Ejecutar manualmente dentro del contenedor

```bash
python main.py /data/ine-reverse.jpg
```

## Solución de problemas

### El archivo no existe

Verificar que la imagen esté montada:

```bash
ls -la /data
```

### No se encontró CIC válido

El OCR pudo leer la imagen, pero no encontró un patrón válido:

* MEX##########
* #############

Revisar el texto detectado mostrado en consola.

### Error al abrir la imagen

Verificar que la ruta exista:

```bash
ls -la /data
```

## Tecnologías

* Python 3.12
* Tesseract OCR
* Pillow
* NumPy
* Docker

## Autor

Héctor G
