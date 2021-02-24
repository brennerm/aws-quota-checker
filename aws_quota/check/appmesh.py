from .quota_check import QuotaCheck, QuotaScope


class MeshCountCheck(QuotaCheck):
    key = "am_mesh_count"
    description = "App Meshes per account"
    scope = QuotaScope.ACCOUNT
    service_code = 'appmesh'
    quota_code = 'L-AC861A39'

    @property
    def current(self):
        return len(self.boto_session.client('appmesh').list_meshes()['meshes'])
