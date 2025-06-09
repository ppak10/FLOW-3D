![pytest](https://github.com/ppak10/FLOW-3D/workflows/pytest/badge.svg)

# FLOW-3D
Python wrapper for running and managing simulations in FLOW-3D

## Getting Started
### 1. Installation
```bash
pip install flow-3d
```

### 2. In the environment with `FLOW-3D` create a new `Workspace`:
```bash
flow-3d workspace_init example
```
  - This command can also create a huggingface dataset:
    #### 2.1 Create Workspace HuggingFace Dataset
    ```bash
    flow3d-manage workspace_init example upload=True
    ```
    #### Which runs runs the following command to initialize a dataset for the workspace (defaults to HuggingFace)
    ```bash
    python manage.py workspace_dataset_init
    ```

### 3. Navigate to created workspace directory and use package with `manage.py` file.
```bash
cd out/example
```

## Usage for individual simulations
### 1. Initialize Simulation folders and `simulation.yml` file.
```bash
python manage.py simulation_init example_simulation
```

### 2. Edit generated `simulation.yml` file to your specific configurations
```yaml
# If using scientific notation, make sure to format like 1.0e+4 or 3.5e-3
# https://stackoverflow.com/a/77563328/10521456

# Global
simulation_finish_time: 0.001    # 0.001 Seconds
velocity: 0.0

# Units here are in (m)
mesh:
  size: 1.0e-5      # 10 µm resolution
  x_start: 0      # 0 µm
  x_end: 1.0e-3     # 1000 µm
  y_start: 0      # 0 µm
  y_end: 1.0e-3     # 1000 µm
  z_start: 0      # 0 µm
  z_end: 3.0e-3     # 3000 µm

fluid_region:
  x_start: 0      # 0 µm
  x_end: 1.0e-3     # 1000 µm
  y_start: 0      # 0 µm
  y_end: 1.0e-3     # 1000 µm
  z_start: 0      # 0 µm
  z_end: 2.8e-3     # 2800 µm

beam:
  diameter: 1.0e-4  # 100 µm (not explicity in prepin file)
  x: 5.0e-4         # Starting Location of Laser Beam 500 µm (0.05 cm)
  y: 5.0e-4         # Starting Location of Laser Beam 500 µm (0.05 cm)
  z: 0.01         # Starting Location of Laser Beam 10,000 µm (1.00 cm)

```

### 3. Generate prepin file from `simulation.yml`
```bash
python manage.py simulation_generate_prepin example_simulation
```

### 4. Run Simulation (and all other postprocessing and visualization steps)
```bash
python manage.py simulation_run example_simulation
```
  - This also runs the following with default arguments:

    #### 4.1. (`postprocess = True`) Postprocess Simulations
    ```bash
    python manage.py simulation_postprocess example_simulation
    ```

  - Following arguments only work if `postprocess` is set to `True`.
    #### 4.2. (`visualize = True`)Visualize Simulations
    ```bash
    python manage.py simulation_visualize example_simulation num_proc=4
    ```

    #### 4.3. (`upload = True`) Generate Simulation Dataset
    ```bash
    python manage.py simulation_generate_dataset example_simulation
    ```
    #### 4.4. (`upload = True`) Upload Simulation and source files. (defaults to HuggingFace)
    ```bash
    python manage.py simulation_upload_dataset example_simulation
    ```

## Usage for batch simulations
### 1. Create an initialization script (`initialize.py`) within the workspace directory.
```python
import os

from flow3d import Workspace

# Sets current directory path of `manage.py` to the workspace.
workspace_path = os.path.dirname(__file__)

workspace_filename = os.path.basename(workspace_path)

workspace = Workspace(
    workspace_path=workspace_path,
    filename=workspace_filename,
)

step = 100
start = 100
end = 1000

config = {
    "simulation_finish_time": 0.001,
    "power": 100,
    "velocity": 0.0,
    "temperature_initial": 299.15,
    "evaporation": 0,
    "lens_radius": 5.0e-5,
    "spot_radius": 5.0e-5,
    "mesh": {
        "size": 2.0e-5,
        "x_start": 0,
        "x_end": 5.0e-4,
        "y_start": 0,
        "y_end": 5.0e-4,
        "z_start": 0,
        "z_end": 1.0e-3
    },
    "fluid_region": {
        "x_start": 0,
        "x_end": 5.0e-4,
        "y_start": 0,
        "y_end": 5.0e-4,
        "z_start": 0,
        "z_end": 8.0e-4
    },
    "beam": {
        "diameter": 1.0e-4,
        "x": 2.5e-4,
        "y": 2.5e-4,
        "z": 0.01
    }
}

for power in range(start, end + step, step):
    config["power"] = power
    simulation_folder_string = f"{power}".zfill(4)
    simulation_name = f"{simulation_folder_string}_watts"
    workspace.simulation_initialize(simulation_name, config)
```

### 2. Run script to initialize simulations
```bash
python initialize.py
```

### 3. Build all simulations
```bash
python manage.py simulation_build_all
```

### 4. Run all simulation
```bash
python manage.py simulation_run_all upload=True num_proc=4
```
