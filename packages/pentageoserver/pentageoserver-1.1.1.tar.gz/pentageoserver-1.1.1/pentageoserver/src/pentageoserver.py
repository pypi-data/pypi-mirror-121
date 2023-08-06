from Geoserver import _Geoserver


class PentaGeoserver(_Geoserver):

    def __init__(self, service_url="http://localhost:8080/geoserver",
                 username="admin",
                 password="geoserver") -> None:
        _Geoserver.__init__(self, service_url=service_url,
                            username=username, password=password)

    def create_multi_workspaces(self, workspaces: list):
        """
        Create Multi Workspaces
        """
        for workspace in workspaces:
            self.create_workspace(workspace=workspace)

    def publish_style_to_list_layers(self, style_name: str, workspace: str, layers: list):
        '''
        Publish a SLD sytle to one or more Layers in workspace
        '''
        for layer in layers:
            self.publish_style(layer_name=layer,
                               workspace=workspace, style_name=style_name)

    def publish_all_layers(self, tables: list, workspace: str, store_name: str) -> list:
        '''
        Publish All Layers in Postgis pre-created Store
        '''
        status = []
        for table_name in tables:
            m = self.publish_featurestore(store_name=store_name,
                                          workspace=workspace,
                                          pg_table=table_name)
            if m:
                status.append({"tableName": table_name, "error": m})
            else:
                status.append({"tableName": table_name, "error": False})
        return status
