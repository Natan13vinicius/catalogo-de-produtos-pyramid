from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ..models import DBSession, Product

# 📌 Listar produtos
@view_config(route_name="list_products", renderer="mycatalog:templates/products/list.jinja2")
def list_products(request):
    produtos = DBSession.query(Product).all()
    return {"products": produtos}

# 📌 Exibir formulário de adicionar produto
@view_config(route_name="add_product", renderer="mycatalog:templates/products/add.jinja2", request_method="GET")
def add_product_form(request):
    return {}

# 📌 Processar novo produto
@view_config(route_name="add_product", request_method="POST")
def add_product(request):
    try:
        data = request.POST
        novo_produto = Product(
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            image_path=data.get("image_path"),
        )
        DBSession.add(novo_produto)
        DBSession.commit()
        # 🔄 Redireciona para a lista de produtos
        return HTTPFound(location=request.route_url("list_products"))
    except Exception as e:
        DBSession.rollback()
        return {"status": "error", "message": str(e)}

# 📌 Exibir formulário de edição
@view_config(route_name="edit_product", renderer="mycatalog:templates/products/edit.jinja2", request_method="GET")
def edit_product_form(request):
    product_id = int(request.matchdict["id"])
    produto = DBSession.query(Product).get(product_id)
    return {"product": produto}

# 📌 Processar edição
@view_config(route_name="edit_product", request_method="POST")
def edit_product(request):
    try:
        product_id = int(request.matchdict["id"])
        produto = DBSession.query(Product).get(product_id)

        if not produto:
            return {"status": "error", "message": "Produto não encontrado."}

        data = request.POST
        produto.name = data.get("name", produto.name)
        produto.description = data.get("description", produto.description)
        produto.price = data.get("price", produto.price)
        produto.image_path = data.get("image_path", produto.image_path)

        DBSession.commit()
        # 🔄 Redireciona para a lista de produtos
        return HTTPFound(location=request.route_url("list_products"))
    except Exception as e:
        DBSession.rollback()
        return {"status": "error", "message": str(e)}

# 📌 Exibir confirmação de exclusão
@view_config(route_name="delete_product", renderer="mycatalog:templates/products/delete.jinja2", request_method="GET")
def delete_product_form(request):
    product_id = int(request.matchdict["id"])
    produto = DBSession.query(Product).get(product_id)
    return {"product": produto}

# 📌 Processar exclusão
@view_config(route_name="delete_product", request_method="POST")
def delete_product(request):
    try:
        product_id = int(request.matchdict["id"])
        produto = DBSession.query(Product).get(product_id)

        if not produto:
            return {"status": "error", "message": "Produto não encontrado."}

        DBSession.delete(produto)
        DBSession.commit()
        # 🔄 Redireciona para a lista de produtos
        return HTTPFound(location=request.route_url("list_products"))
    except Exception as e:
        DBSession.rollback()
        return {"status": "error", "message": str(e)}
