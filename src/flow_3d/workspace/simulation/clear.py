import os
import shutil


class WorkspaceSimulationClear:
    """
    Workspace class clearing files in simulation folder for say a failed run.
    """

    def simulation_clear(
        self,
        name,
        keep_files=["simulation.yml", "simulation.pkl", "prepin.simulation"],
        **kwargs,
    ):
        """
        Clears everything in a simulation folder except for:
        - simulation.yml
        - simulation.pkl
        - prepin.simulation
        """
        simulation_folder = os.path.join(self.workspace_path, name)

        if not os.path.isdir(simulation_folder):
            raise FileNotFoundError(f"{simulation_folder} does not exist.")

        for entry in os.listdir(simulation_folder):
            entry_path = os.path.join(simulation_folder, entry)
            if entry in keep_files:
                continue
            if os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
            else:
                os.remove(entry_path)
