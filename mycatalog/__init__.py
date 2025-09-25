import os
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
import zope.sqlalchemy

from .models import Base, DBSession

def main(global_config, **settings):
    """Função principal WSGI, chamada pelo Pyramid"""

    # Conexão com banco SQLite (usa engine_from_config para ler do .ini)
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    zope.sqlalchemy.register(DBSession)
    Base.metadata.create_all(engine)

    # Diretório de uploads
    here = os.path.dirname(__file__)
    upload_dir = settings.get("upload_dir", os.path.join(here, "static", "uploads"))
    os.makedirs(upload_dir, exist_ok=True)
    settings["upload_dir"] = upload_dir
    settings["upload_url"] = "/static/uploads"

    # Configuração do Pyramid
    session_factory = SignedCookieSessionFactory("troque-esta-chave")
    config = Configurator(settings=settings, session_factory=session_factory)

    # Segurança CSRF
    config.set_default_csrf_options(require_csrf=True)

    # Suporte a templates Jinja2
    config.include("pyramid_jinja2")

    # Arquivos estáticos (CSS, imagens, etc.)
    config.add_static_view(name="static", path="mycatalog:static", cache_max_age=3600)

    # Rotas da aplicação
    config.add_route("home", "/")
    config.add_route("product_add", "/products/add")
    config.add_route("product_detail", "/products/{id}")
    config.add_route("product_edit", "/products/{id}/edit")
    config.add_route("product_delete", "/products/{id}/delete")

    # Escanear as views (controllers)
    config.scan(".views")

    return config.make_wsgi_app()
