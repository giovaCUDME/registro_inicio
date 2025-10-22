from base import create_app

app = create_app()


def _print_routes(application):
    print('Rutas registradas:')
    for r in sorted(application.url_map.iter_rules(), key=lambda x: x.rule):
        methods = ','.join(sorted(r.methods))
        print(f"  {r.rule} -> {methods}")


if __name__ == '__main__':
    # Mostrar rutas al iniciar para diagnóstico
    _print_routes(app)
    app.run(port=5021, debug=True)
