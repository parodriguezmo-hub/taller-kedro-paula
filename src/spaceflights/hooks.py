import logging

from kedro.framework.hooks import hook_impl

logger = logging.getLogger(__name__)


class RegistroDeNodos:
    @hook_impl
    def before_node_run(self, node):
        logger.info("Iniciando nodo: %s", node.name)

    @hook_impl
    def after_node_run(self, node):
        logger.info("Nodo completado: %s", node.name)