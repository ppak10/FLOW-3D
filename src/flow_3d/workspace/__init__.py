from .base import WorkspaceBase
from .huggingface import WorkspaceHuggingFace
from .simulation.base import WorkspaceSimulationBase
from .simulation.clear import WorkspaceSimulationClear
from .simulation.build import WorkspaceSimulationBuild
from .simulation.huggingface import WorkspaceSimulationHuggingFace
from .simulation.measure import WorkspaceSimulationMeasure
from .simulation.post import WorkspaceSimulationPost
from .simulation.run import WorkspaceSimulationRun
from .simulation.view import WorkspaceSimulationView
from .simulation.visualize import WorkspaceSimulationVisualize
from .utils import WorkspaceUtils

class Workspace(
    WorkspaceBase,
    WorkspaceHuggingFace,
    WorkspaceSimulationBase,
    WorkspaceSimulationClear,
    WorkspaceSimulationBuild,
    WorkspaceSimulationHuggingFace,
    WorkspaceSimulationMeasure,
    WorkspaceSimulationPost,
    WorkspaceSimulationRun,
    WorkspaceSimulationView,
    WorkspaceSimulationVisualize,
    WorkspaceUtils,
):
    def __init__(
            self,
            name: str = None,
            filename: str = None,
            workspace_path: str = None,
            verbose = False,
            **kwargs,
        ):
        super().__init__(
            name = name,
            filename = filename,
            verbose = verbose,
            workspace_path = workspace_path,
            **kwargs,
        )
