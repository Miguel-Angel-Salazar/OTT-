import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.movie_service import listar_peliculas
import urllib.request
import urllib.error


def main():
    pelis = listar_peliculas()
    if not pelis:
        print('No movies returned by listar_peliculas()')
        return

    for i, p in enumerate(pelis[:12], start=1):
        url = p.imagen_url
        print(f"{i:02d} -", url)
        if not url:
            print('   -> MISSING URL')
            continue
        try:
            # If it's a local static path, check file exists on disk
            if url.startswith('/static/'):
                local_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), url.lstrip('/'))
                if os.path.exists(local_path):
                    print('   -> local file found:', local_path)
                else:
                    print('   -> local file MISSING:', local_path)
                continue
            # Use GET because some storage endpoints reject HEAD
            with urllib.request.urlopen(url, timeout=10) as r:
                print('   ->', r.getcode(), r.headers.get('Content-Type'))
        except Exception as e:
            # try to show body for HTTPError
            try:
                import urllib.error
                if isinstance(e, urllib.error.HTTPError):
                    body = e.read().decode('utf-8', errors='ignore')
                    print('   -> ERROR', type(e).__name__, e, '\n   body:', body)
                else:
                    print('   -> ERROR', type(e).__name__, e)
            except Exception:
                print('   -> ERROR', type(e).__name__, e)


if __name__ == '__main__':
    main()
