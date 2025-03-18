#!/bin/bash

# Define environment paths
declare -A ENV_PATHS
ENV_PATHS[default]="$HOME/miniforge3/envs/pycontrails_env"
ENV_PATHS[testing]="$HOME/miniforge3/envs/pycontrails_env_testing"
ENV_PATHS[ps]="$HOME/miniforge3/envs/pycontrails_env_ps"

# Function to check if conda is installed
check_conda() {
    if ! command -v conda &> /dev/null; then
        echo "Error: Conda is not installed. Please install Miniforge3 first."
        exit 1
    fi
    
    # Check if it's Miniforge3
    conda info | grep -q "miniforge3"
    if [ $? -ne 0 ]; then
        echo "Error: This script requires Miniforge3. Found different Conda installation."
        exit 1
    fi
}

# Function to check if environment.yml exists
check_environment_file() {
    if [ ! -f "../environment.yml" ]; then
        echo "Error: environment.yml not found in parent directory"
        exit 1
    fi
}

# Function to create environment
create_environment() {
    local env_path="$1"
    local env_name="pycontrails_env"
    
    # Check if environment.yml exists
    check_environment_file
    
    # Create environment
    conda env create -f ../environment.yml -p "$env_path"
    
    if [ $? -eq 0 ]; then
        echo "Environment created successfully at $env_path"
        echo "Activate with: conda activate $env_path"
    else
        echo "Error creating environment"
        exit 1
    fi
}

# Function to remove environment
remove_environment() {
    local env_path="$1"
    
    # Check if environment exists
    if conda env list | grep -q "$env_path"; then
        conda env remove -p "$env_path"
        if [ $? -eq 0 ]; then
            echo "Environment removed successfully from $env_path"
        else
            echo "Error removing environment"
            exit 1
        fi
    else
        echo "Environment does not exist at $env_path"
        exit 1
    fi
}

# Main script
main() {
    if [ $# -ne 2 ]; then
        echo "Usage: $0 <install/remove> <default/testing/ps>"
        echo "Example: $0 install default"
        echo "Example: $0 remove testing"
        exit 1
    fi

    local action="$1"
    local location="$2"
    
    check_conda
    
    # Get environment path from location key
    if [[ -z "${ENV_PATHS[$location]}" ]]; then
        echo "Error: Invalid location. Must be one of: default, testing, ps"
        exit 1
    fi
    env_path="${ENV_PATHS[$location]}"

    case $action in
        install)
            create_environment "$env_path"
            ;;
        remove)
            remove_environment "$env_path"
            ;;
        *)
            echo "Error: Invalid action. Must be one of: install, remove"
            exit 1
            ;;
    esac
}

# Make script executable
chmod +x "$0"

# Run main function
main "$@"
