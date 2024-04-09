from .user_route import router as user_router
from .ventas_route import router as ventas_router
from .articulos_route import router as articulos_router
from .VentaMes_route import router as VentaMes_router
from .cliente_route import router as cliente_router
from .ClienteCompra_route import router as cliente_compra_router
from .stock_route import router as stock_router
from .predict_route import router as predict_router

urls = [
    user_router,
    ventas_router,
    articulos_router,
    VentaMes_router,
    cliente_router,
    cliente_compra_router,
    stock_router,
    predict_router,
]