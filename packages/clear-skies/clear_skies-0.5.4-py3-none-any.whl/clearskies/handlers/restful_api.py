from .routing import Routing
from .create import Create
from .update import Update
from .delete import Delete
from .read import Read
from .. import autodoc


class InvalidUrl(Exception):
    pass

class RestfulAPI(Routing):
    _configuration_defaults = {
        'base_url': '',
        'allow_create': True,
        'allow_read': True,
        'allow_update': True,
        'allow_delete': True,
        'allow_search': True,
        'read_only': False,
        'create_handler': Create,
        'read_handler': Read,
        'update_handler': Update,
        'delete_handler': Delete,
        'create_request_method': 'POST',
        'update_request_method': 'PUT',
        'delete_request_method': 'DELETE',
    }

    _resource_id = None
    _is_search = False

    def __init__(self, di):
        super().__init__(di)

    def handler_classes(self, configuration):
        classes = []
        for action in ['create', 'read', 'update', 'delete']:
            allow_key = f'allow_{action}'
            handler_key = f'{action}_handler'
            if allow_key in configuration and not configuration[allow_key]:
                continue
            classes.append(configuration[handler_key] if handler_key in configuration else self._configuration_defaults[handler_key])
        return classes

    def configure(self, configuration):
        # if we have read only set then we can't allow any write methods
        if configuration.get('read_only'):
            for action in ['update', 'delete', 'create']:
                if configuration.get(f'allow_{action}'):
                    raise ValueError(
                        f"Contradictory configuration for handler '{self.__class__.__name__}': " + \
                        f"'read_only' and 'allow_{action} are both set to True"
                    )
                configuration[f'allow_{action}'] = False

        super().configure(configuration)

    def _parse_url(self, input_output):
        self._resource_id = None
        full_path = input_output.get_full_path().strip('/')
        base_url = self.configuration('base_url').strip('/')
        if base_url and full_path[:len(base_url)] != base_url:
            raise InvalidUrl()
        url = full_path[len(base_url):].strip('/')
        if url:
            if not url.isnumeric():
                if url == 'search' and self.configuration('allow_search'):
                    self._is_search = True
                else:
                    raise InvalidUrl()
            else:
                self._resource_id = int(url)

    def handle(self, input_output):
        handler_class = self._get_handler_class_for_route(input_output)
        if handler_class is None:
            return self.error(input_output, 'Not Found', 404)
        handler = self.build_handler(handler_class)
        return handler(input_output)

    def _get_handler_class_for_route(self, input_output):
        try:
            self._parse_url(input_output)
        except InvalidUrl:
            return None
        if self._is_search:
            return self.configuration('read_handler') if (self.configuration('allow_search') and self.configuration('allow_read')) else None
        request_method = input_output.get_request_method()
        if self._resource_id:
            if request_method == self.configuration('update_request_method'):
                return self.configuration('update_handler') if self.configuration('allow_update') else None
            elif request_method == self.configuration('delete_request_method'):
                return self.configuration('delete_handler') if self.configuration('allow_delete') else None
            if request_method != 'GET':
                return None
            return self.configuration('read_handler') if self.configuration('allow_read') else None
        if request_method == self.configuration('create_request_method'):
            return self.configuration('create_handler') if self.configuration('allow_create') else None
        if request_method == 'GET':
            return self.configuration('read_handler') if self.configuration('allow_read') else None
        return None

    def _finalize_configuration_for_sub_handler(self, configuration, handler_class):
        if self._resource_id:
            if handler_class == self.configuration('read_handler'):
                configuration['single_record'] = True
                if not 'where' in configuration:
                    configuration['where'] = []
                id_column = self.configuration('id_column')
                configuration['where'].append(f'{id_column}={self._resource_id}')
            else:
                configuration['resource_id'] = self._resource_id
        return configuration

    def documentation(self):
        self.configuration('read_handler') if self.configuration('allow_read') else None,
        docs = []
        # read handler is slightly different so handle that individually....
        if self.configuration('allow_read'):
            read_handler = self.build_handler(self.configuration('read_handler'))
            for doc in read_handler.documentation(include_search=self.configuration('allow_search')):
                docs.append(doc)

        for name in ['create', 'update', 'delete']:
            if not self.configuration(f'allow_{name}'):
                continue
            handler = self.build_handler(self.configuration(f'{name}_handler'))
            action_docs = handler.documentation()
            for doc in action_docs:
                doc.set_request_methods([self.configuration(f'{name}_request_method')])

                # the restful API adjusts the routing behavior of delete and update, so we want to clobber
                # the parameters
                if name != 'create':
                    doc.add_parameter(
                        autodoc.request.URLPath(
                            autodoc.schema.Integer('id'),
                            description=f'The id of the record to {name}',
                            required=True,
                        )
                    )

                docs.append(doc)

        return docs

    def documentation_models(self):
        # read and write use the same model, so we just need one
        read_handler = self.build_handler(self.configuration('read_handler'))
        return read_handler.documentation_models()
