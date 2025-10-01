from decimal import Decimal
import transaction

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ..models import DBSession, Product


# 📌 Página inicial
@view_config(route_name="home", renderer="mycatalog:templates/home.jinja2")
def home_view(request):
    return {"message": "Bem-vindo ao Catálogo de Produtos!"}


# 📌 Listar produtos
@view_config(route_name="list_products", renderer="mycatalog:templates/products/list.jinja2")
def list_products(request):
    produtos = DBSession.query(Product).all()
    return {"products": produtos}


# 📌 Exibir formulário de adicionar produto
@view_config(route_name="add_product", renderer="mycatalog:templates/products/add.jinja2", request_method="GET")
def add_product_form(request):
    return {}


# 📌 Processar novo produto (usa transaction manager)
@view_config(route_name="add_product", request_method="POST",
             renderer="mycatalog:templates/products/add.jinja2")
def add_product(request):
    try:
        data = request.POST

        name = (data.get("name") or "").strip()
        description = (data.get("description") or "").strip()
        price_raw = (data.get("price") or "0").strip().replace(",", ".")
        image_path = (data.get("image_path") or "").strip()

        if not name or not description:
            raise ValueError("Nome e descrição são obrigatórios.")

        price = Decimal(price_raw)

        novo_produto = Product(
            name=name,
            description=description,
            price=price,
            image_path=image_path or None,
        )

        # 👉 Commit via transaction manager
        with transaction.manager:
            DBSession.add(novo_produto)

        # Sucesso: redireciona
        return HTTPFound(location=request.route_url("list_products"))

    except Exception as e:
        # Falha: re-renderiza o formulário com erro e valores preenchidos
        request.response.status_int = 400
        return {
            "error": str(e),
            "form": {
                "name": request.POST.get("name", ""),
                "description": request.POST.get("description", ""),
                "price": request.POST.get("price", ""),
                "image_path": request.POST.get("image_path", ""),
            },
        }


# 📌 Exibir formulário de edição
@view_config(route_name="edit_product", renderer="mycatalog:templates/products/edit.jinja2", request_method="GET")
def edit_product_form(request):
    product_id = int(request.matchdict["id"])
    produto = DBSession.query(Product).get(product_id)
    return {"product": produto}


# 📌 Processar edição (usa transaction manager)
@view_config(route_name="edit_product", request_method="POST",
             renderer="mycatalog:templates/products/edit.jinja2")
def edit_product(request):
    product_id = int(request.matchdict["id"])
    produto = DBSession.query(Product).get(product_id)

    if not produto:
        request.response.status_int = 404
        return {"error": "Produto não encontrado.", "product": None}

    try:
        data = request.POST

        name = (data.get("name") or produto.name).strip()
        description = (data.get("description") or produto.description).strip()
        price_raw = (data.get("price") or str(produto.price)).strip().replace(",", ".")
        image_path = (data.get("image_path") or produto.image_path or "").strip()

        price = Decimal(price_raw)

        with transaction.manager:
            produto.name = name
            produto.description = description
            produto.price = price
            produto.image_path = image_path or None

        return HTTPFound(location=request.route_url("list_products"))

    except Exception as e:
        request.response.status_int = 400
        return {"error": str(e), "product": produto}


# 📌 Exibir confirmação de exclusão
@view_config(route_name="delete_product", renderer="mycatalog:templates/products/delete.jinja2", request_method="GET")
def delete_product_form(request):
    product_id = int(request.matchdict["id"])
    produto = DBSession.query(Product).get(product_id)
    return {"product": produto}


# 📌 Processar exclusão (usa transaction manager)
@view_config(route_name="delete_product", request_method="POST",
             renderer="mycatalog:templates/products/delete.jinja2")
def delete_product(request):
    product_id = int(request.matchdict["id"])
    produto = DBSession.query(Product).get(product_id)

    if not produto:
        request.response.status_int = 404
        return {"error": "Produto não encontrado.", "product": None}

    try:
        with transaction.manager:
            DBSession.delete(produto)

        return HTTPFound(location=request.route_url("list_products"))

    except Exception as e:
        request.response.status_int = 400
        return {"error": str(e), "product": produto}
