# AceCast Namelist Advisor

The AceCast Namelist Advisor is a collection of Python classes designed to validate and provide guidance on configuring namelists for Weather Research and Forecasting (WRF) model simulations. The classes in this repository focus on verifying domain configurations, physics options, dynamics options, and nesting options for use within AceCast's supported options.

## Features

1. **Domain Configuration Validation**: Checks domain coverage, vertical coordinate system, and map projection settings based on the selected region and its characteristics.

2. **Physics Options Validation**: Verifies the choice of microphysics, cumulus parameterization, and planetary boundary layer schemes based on the region's climate characteristics. Additionally, it checks the consistency of radiation and surface-layer schemes with other selected physics options.

3. **Dynamics Options Validation**: Validates the selected advection schemes for horizontal and vertical motions.

4. **Nesting Options Validation**: Verifies the nesting configurations, including one-way or two-way interaction and feedback options. Also checks if the time step ratio and parent grid ratio are consistent for the nested domains.

## Usage

To use the AceCast Namelist Advisor, import the respective validation classes and instantiate them with your namelist as input. Then, call the corresponding validation methods to check your namelist's configuration.

Example:

```python
from helpers.domain_validation import DomainConfigurationValidation
from helpers.physics_consistency_validation import PhysicsConsistencyValidation
from helpers.dynamics_options_validation import DynamicsOptionsValidation
from helpers.nesting_options_validation import NestingOptionsValidation

namelist = {...}  # Your namelist here

domain_validator = DomainConfigurationValidation(namelist)
domain_validator.validate_domain_coverage()

physics_validator = PhysicsConsistencyValidation(namelist)
physics_validator.validate_physics_consistency()

dynamics_validator = DynamicsOptionsValidation(namelist)
dynamics_validator.validate_advection_schemes()

nesting_validator = NestingOptionsValidation(namelist)
nesting_validator.validate_nesting_options()
```

## To do
-Error checking for reading/processing namelist and registry files
-Handle case where physics_suite isn’t set
-Could maybe have a dropdown to choose which version of AceCAST to use eventually
-Have an upload OR copy/paste text from namelist directly into the app 