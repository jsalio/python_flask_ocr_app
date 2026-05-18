#!/usr/bin/env python3
import sys
import click
from ocr_service import images_to_searchable_pdf


@click.command()
@click.argument('images', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('--output', '-o', default='output.pdf', show_default=True, help='Output PDF file path')
@click.option('--lang', '-l', default='eng', show_default=True, help='Tesseract language code (eng, spa, fra...)')
def main(images, output, lang):
    """Convert one or more images to a searchable PDF using OCR.

    \b
    Examples:
      python cli.py scan1.jpg scan2.png -o result.pdf
      python cli.py *.jpg --output document.pdf --lang spa
    """
    click.echo(f'Processing {len(images)} image(s) with lang="{lang}"...')
    try:
        pdf_bytes = images_to_searchable_pdf(images, lang=lang)
    except Exception as e:
        click.echo(f'Error: {e}', err=True)
        sys.exit(1)

    with open(output, 'wb') as f:
        f.write(pdf_bytes)

    click.echo(f'Saved: {output}  ({len(pdf_bytes):,} bytes)')


if __name__ == '__main__':
    main()
