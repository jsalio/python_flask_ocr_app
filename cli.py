#!/usr/bin/env python3
import sys
import subprocess
import click
from ocr_service import images_to_searchable_pdf

__version__ = '1.0.0'


def get_tesseract_langs():
    try:
        result = subprocess.run(
            ['tesseract', '--list-langs'],
            capture_output=True, text=True
        )
        lines = (result.stdout + result.stderr).strip().splitlines()
        return [l.strip() for l in lines if l.strip() and not l.startswith('List')]
    except FileNotFoundError:
        return []


@click.group()
@click.version_option(version=__version__, prog_name='ocr-cli')
def cli():
    """OCR CLI — convierte imágenes a PDF con texto buscable usando Tesseract.

    \b
    Comandos disponibles:
      convert     Convierte imágenes a PDF buscable
      langs       Lista los idiomas instalados en Tesseract
      info        Muestra información del entorno

    \b
    Uso rápido:
      ocr-cli convert scan1.jpg scan2.png -o resultado.pdf
      ocr-cli convert *.jpg --lang spa
      ocr-cli langs
    """
    pass


@cli.command()
@click.argument('images', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('--output', '-o', default='output.pdf', show_default=True,
              help='Ruta del archivo PDF de salida.')
@click.option('--lang', '-l', default='eng', show_default=True,
              help='Código de idioma Tesseract (eng, spa, fra, deu, por...).')
def convert(images, output, lang):
    """Convierte una o más imágenes a un PDF con texto buscable.

    IMAGES puede ser uno o varios archivos de imagen (JPG, PNG, TIFF, BMP).

    \b
    Ejemplos:
      ocr-cli convert scan.jpg -o documento.pdf
      ocr-cli convert img1.png img2.png -o multi.pdf --lang spa
      ocr-cli convert *.tiff --output batch.pdf --lang fra
    """
    click.echo(f'Procesando {len(images)} imagen(es) con idioma="{lang}"...')
    try:
        pdf_bytes = images_to_searchable_pdf(images, lang=lang)
    except Exception as e:
        click.echo(f'Error: {e}', err=True)
        sys.exit(1)

    with open(output, 'wb') as f:
        f.write(pdf_bytes)

    click.echo(f'Guardado: {output}  ({len(pdf_bytes):,} bytes)')


@cli.command()
def langs():
    """Lista los idiomas de Tesseract disponibles en este sistema.

    \b
    Idiomas comunes:
      eng   Inglés
      spa   Español
      fra   Francés
      deu   Alemán
      por   Portugués
      ita   Italiano
      chi_sim  Chino simplificado
      jpn   Japonés
    """
    available = get_tesseract_langs()
    if not available:
        click.echo(
            'No se encontró Tesseract o no hay idiomas instalados.\n'
            'Descarga Tesseract desde: https://github.com/tesseract-ocr/tesseract',
            err=True
        )
        sys.exit(1)

    click.echo(f'Idiomas instalados ({len(available)}):')
    for lang in available:
        click.echo(f'  {lang}')


@cli.command()
def info():
    """Muestra la versión de Tesseract y la configuración del entorno."""
    import pytesseract
    from PIL import Image

    click.echo(f'ocr-cli v{__version__}')

    try:
        tess_ver = pytesseract.get_tesseract_version()
        click.echo(f'Tesseract:  {tess_ver}')
    except Exception as e:
        click.echo(f'Tesseract:  no encontrado ({e})', err=True)

    try:
        pil_ver = Image.__version__
        click.echo(f'Pillow:     {pil_ver}')
    except Exception:
        click.echo('Pillow:     instalado')

    langs = get_tesseract_langs()
    click.echo(f'Idiomas:    {len(langs)} disponibles  (usa "ocr-cli langs" para verlos)')


if __name__ == '__main__':
    cli()
