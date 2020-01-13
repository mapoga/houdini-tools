import os
import hou
import glob
import nodesearch

PROJECTS_DIR = os.path.abspath(r'Z:\Programming\Python\shed\scene_assembly\filesystem\X\PROJECTS')

class Scene(object):

    @staticmethod
    def path():
        """Returns the path of the current hip file."""

        return os.path.abspath(hou.hipFile.path())

    @staticmethod
    def project():
        """Returns the Project object of the current hip file."""

        current_dir = os.path.dirname(Scene.path())
        return Project.project_from_path(current_dir)

    @staticmethod
    def scene_render_models(network='/obj/'):
        """List render models."""
        
        network = hou.node(network)
        #matcher = nodesearch.All()
        # Find the best way to match against assets correctly.
        # Use hou.nodeType or hou.HDADefinition if necessary
        matcher = nodesearch.NodeType('mga::')
        nodes = matcher.nodes(network)
        print(nodes)
        for n in nodes:
            print(n)
            print(n.type())


class Project(object):

    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return '<Project: {0}>'.format(self.name())


    @staticmethod
    def projects():
        """List projects directly under PROJECTS_DIR."""

        return os.listdir(PROJECTS_DIR)

    @staticmethod
    def project_from_path(path):
        """Return a Project object from a path."""

        dirname = ''
        while os.path.abspath(path) != os.path.abspath(PROJECTS_DIR):
            path, dirname = os.path.split(path)
            if dirname is '':
                break
        else:
            return Project(dirname)


    def name(self):
        return self._name

    def path(self):
        """Root directory of the project."""

        return os.path.join(PROJECTS_DIR, self.name())

    def assets_dir(self):
        """Path to the assets directory."""

        return os.path.join(self.path(), 'prod', 'AST')

    def published_assets(self):
        """List of published Asset objects.

        Any directory under project/prod/AST with a modeling or render_model
        directory under it.
        """

        out_dirs = [Asset.MODELING_OUT, Asset.RENDER_MODEL_OUT]
        assets = []
        for root, dirs, files in os.walk(self.assets_dir()):
            basename = os.path.basename(root)
            for d in dirs:
                if d in out_dirs:
                    assets.append(Asset(path=root))
                    break

        return assets

    def shots_dir(self):
        """Path to the shots directory."""

        return os.path.join(self.path(), 'prod', 'SHT')
    
    def shots(self):
        """List shots directly under project/prod/SHT."""

        # TODO: build a more robust search taking subdirectories into consideration
        return os.listdir(self.shots_dir())


class Asset(object):

    MODELING_OUT = 'mod_out'
    RENDER_MODEL_OUT = 'rdm_out'

    def __init__(self, project=None, name=None, path=None):
        self._project = project
        self._name = name
        self._path = path

    def __repr__(self):
        return '<Asset: {0} {1}>'.format(self.project().name(), self.name())


    def project(self):
        """Project associated with that asset."""

        if self._project:
            return Project(self._project)
        elif self._path:
            return Project.project_from_path(self._path)
        else:
            return

    def name(self):
        """Name of the asset."""

        if self._name:
            return self._name
        elif self._path:
            return os.path.basename(self._path)
        else:
            return
        
    def path(self):
        """Root directory of the asset."""

        if self._path:
            return self._path
        elif self._project and self._name:
            out_dirs = [Asset.MODELING_OUT, Asset.RENDER_MODEL_OUT]
            for root, dirs, files in os.walk(self.project.assets_dir):
                basename = os.path.basename(root)
                for d in dirs:
                    if d in out_dirs:
                        if basename == self._name:
                            return root
        else:
            return

    def model(self):
        """Modeling alembic file."""

        try:
            mod_dir = os.path.join(self.path(), Asset.MODELING_OUT)
            models = glob.glob(os.path.join(mod_dir, '*.abc'))
            return models[-1]
        except:
            return

    def render_model(self):
        """Render model HDA file."""

        try:
            mod_dir = os.path.join(self.path(), Asset.RENDER_MODEL_OUT)
            models = glob.glob(os.path.join(mod_dir, '*.hda'))
            return models[-1]
        except:
            return
