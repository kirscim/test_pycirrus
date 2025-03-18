# Test Pycirrus

A collaborative project repository for working with pycontrails.

## Installation

### Prerequisites
- Miniforge3 (recommended) or Anaconda
- Git

### Installation Steps

1. Clone the repository:
```bash
git clone git@github.com:kirscim/test_pycirrus.git
cd test_pycirrus
```

2. Install the environment:
```bash
cd install
./install_pycontrails.sh install default
```

3. Activate the environment:
```bash
conda activate $HOME/miniforge3/envs/pycontrails_env
```

### Environment Management

#### Install in different locations
```bash
# Testing environment
./install_pycontrails.sh install testing

# Production environment
./install_pycontrails.sh install ps
```

#### Remove environments
```bash
# Remove default environment
./install_pycontrails.sh remove default

# Remove testing environment
./install_pycontrails.sh remove testing

# Remove production environment
./install_pycontrails.sh remove ps
```

## Project Structure
- `environment.yml`: Conda environment specification
- `install/`: Installation scripts
  - `install_pycontrails.sh`: Main installation script
