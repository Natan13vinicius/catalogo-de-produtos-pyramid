# mycatalog/views/products.py
from decimal import Decimal, InvalidOperation

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ..models import DBSession, Product


# -----------------------------------------------------------------------------
# Home
# -----------------------------------------------------------------------------
@view_config(route_name="home", renderer="mycatalog:templates/home.jinja2")
def home_view(request):
    return {"message": "Bem-vindo ao Catálogo de Produtos!"}


# -----------------------------------------------------------------------------
# Listagem
#  - expire_all() evita mostrar objetos em cache após um POST/redirect
# -----------------------------------------------------------------------------
@view_config(route_name="list_products", renderer="mycatalog:templates/products/list.jinja2")
def list_products(request):
    DBSession.expire_all()
    produtos = DBSession.query(Product).all()
    return {"products": produtos}


# -----------------------------------------------------------------------------
# Adicionar (GET) – mostra o formulário
# -----------------------------------------------------------------------------
@view_config(
    route_name="add_product",
    renderer="mycatalog:templates/products/add.jinja2",
    request_method="GET",
)
def add_product_form(request):
    return {}


# -----------------------------------------------------------------------------
# Adicionar (POST)
#  - valida campos
#  - converte preço
#  - adiciona no DBSession
#  - NÃO chama commit: pyramid_tm fará o commit ao fim da view
# -----------------------------------------------------------------------------
@view_config(
    route_name="add_product",
    request_method="POST",
    renderer="mycatalog:templates/products/add.jinja2",
)
def add_product(request):
    data = request.POST

    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip()
    price_raw = (data.get("price") or "").strip().replace(",", ".")
    image_path = (data.get("image_path") or "").strip()

    if not name or not description:
        request.response.status_int = 400
        return {
            "error": "Nome e descrição são obrigatórios.",
            "form": {"name": name, "description": description, "price": price_raw, "image_path": image_path},
        }

    try:
        price = Decimal(price_raw) if price_raw else Decimal("0.00")
    except (InvalidOperation, ValueError):
        request.response.status_int = 400
        return {
            "error": "Preço inválido. Use ponto ou vírgula (ex.: 10.50).",
            "form": {"name": name, "description": description, "price": price_raw, "image_path": image_path},
        }

    novo = Product(
        name=name,
        description=description,
        price=price,
        image_path=image_path or None,
    )
    DBSession.add(novo)      # pyramid_tm cuidará do commit
    # DBSession.flush()      # opcional; ajuda a detectar erros cedo

    return HTTPFound(location=request.route_url("list_products"))


# -----------------------------------------------------------------------------
# Editar (GET) – carrega e mostra o formulário
# -----------------------------------------------------------------------------
@view_config(
    route_name="edit_product",
    renderer="mycatalog:templates/products/edit.jinja2",
    request_method="GET",
)
def edit_product_form(request):
    try:
        product_id = int(request.matchdict.get("id"))
    except (TypeError, ValueError):
        product_id = None

    produto = DBSession.get(Product, product_id) if product_id else None
    if not produto:
        request.response.status_int = 404
        return {"error": "Produto não encontrado.", "product": None}

    return {"product": produto}


# -----------------------------------------------------------------------------
# Editar (POST)
#  - busca registro
#  - aplica alterações
#  - NADA de commit manual (pyramid_tm faz)
# -----------------------------------------------------------------------------
@view_config(
    route_name="edit_product",
    request_method="POST",
    renderer="mycatalog:templates/products/edit.jinja2",
)
def edit_product(request):
    try:
        product_id = int(request.matchdict.get("id"))
    except (TypeError, ValueError):
        request.response.status_int = 400
        return {"error": "ID inválido.", "product": None}

    produto = DBSession.get(Product, product_id)
    if not produto:
        request.response.status_int = 404
        return {"error": "Produto não encontrado.", "product": None}

    data = request.POST

    name = (data.get("name") or produto.name or "").strip()
    description = (data.get("description") or produto.description or "").strip()
    price_raw = (data.get("price") or str(produto.price or "")).strip().replace(",", ".")
    image_path = (data.get("image_path") or produto.image_path or "").strip()

    if not name or not description:
        request.response.status_int = 400
        return {"error": "Nome e descrição são obrigatórios.", "product": produto}

    try:
        price = Decimal(price_raw) if price_raw else Decimal("0.00")
    except (InvalidOperation, ValueError):
        request.response.status_int = 400
        return {"error": "Preço inválido. Use ponto ou vírgula.", "product": produto}

    # aplica mudanças; o UPDATE será emitido no commit do pyramid_tm
    produto.name = name
    produto.description = description
    produto.price = price
    produto.image_path = image_path or None
    # DBSession.flush()  # opcional

    return HTTPFound(location=request.route_url("list_products"))


# -----------------------------------------------------------------------------
# Excluir (GET) – confirma
# -----------------------------------------------------------------------------
@view_config(
    route_name="delete_product",
    renderer="mycatalog:templates/products/delete.jinja2",
    request_method="GET",
)
def delete_product_form(request):
    try:
        product_id = int(request.matchdict.get("id"))
    except (TypeError, ValueError):
        product_id = None

    produto = DBSession.get(Product, product_id) if product_id else None
    if not produto:
        request.response.status_int = 404
        return {"error": "Produto não encontrado.", "product": None}

    return {"product": produto}


# -----------------------------------------------------------------------------
# Excluir (POST)
# -----------------------------------------------------------------------------
@view_config(
    route_name="delete_product",
    request_method="POST",
    renderer="mycatalog:templates/products/delete.jinja2",
)
def delete_product(request):
    try:
        product_id = int(request.matchdict.get("id"))
    except (TypeError, ValueError):
        request.response.status_int = 400
        return {"error": "ID inválido.", "product": None}

    produto = DBSession.get(Product, product_id)
    if not produto:
        request.response.status_int = 404
        return {"error": "Produto não encontrado.", "product": None}

    DBSession.delete(produto)  # commit automático pelo pyramid_tm
    # DBSession.flush()        # opcional

    return HTTPFound(location=request.route_url("list_products"))
