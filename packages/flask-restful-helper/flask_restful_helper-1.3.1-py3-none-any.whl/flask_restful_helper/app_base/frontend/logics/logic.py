from flask_restful_helper import Logic

from apps.frontend.managers import manager
from apps.frontend.schemas import schema


class Menu(Logic):
    _manager = manager.Menu
    _schema = schema.Menu

    def list(self, query_args, *args, **kwargs):
        if query_args.format == 'menu':

            data = self.manager.list_root_node()

            if data:
                return True, self.schema.dump(data, many=True), 200
            else:
                return True, [], 204


        else:
            return super(Menu, self).list(query_args, *args, **kwargs)
