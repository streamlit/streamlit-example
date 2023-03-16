import json
import f90nml
from io import StringIO


class NamelistValidator:
    def __init__(self, registry_file, namelist_file):
        self.errors = []

        if isinstance(registry_file, str):
            with open(registry_file, 'r') as f:
                self.registry_file = f.read()
        else:
            self.registry_file = registry_file.read()

        self.namelist_file = namelist_file.read()

        self.nml_cfg = {}
        self.user_nml = None
        self.supported_nml = True
        self.load_registry()
        self.read_namelist()

    def load_registry(self):
        registry = json.loads(self.registry_file)

        for node in registry['Type']:
            if node['name'] == 'domain':
                domain_node = node
                break
        for node in domain_node['fields']:
            RCONFIG_TYPE = 4
            if node['node_kind'] != RCONFIG_TYPE:
                continue
            if node['type'] == 'integer':
                ttype = int
            elif node['type'] == 'real':
                ttype = float
            elif node['type'] == 'logical':
                ttype = bool
            elif 'char' in node['type']:
                ttype = str
            nml_support = node['nml_support']
            if nml_support == '+':
                nml_support = node['dflt']
            section = node['howset'].replace('namelist,', '')
            if section not in self.nml_cfg:
                self.nml_cfg[section] = {}
            self.nml_cfg[section][node['name']] = {
                'nentries': node['nentries'],
                'type': ttype,
                'nml_support': nml_support.lower(),
            }

    def read_namelist(self):
        self.user_nml = f90nml.read(StringIO(self.namelist_file.decode()))


    @staticmethod
    def var_to_list(var, vtype):
        if isinstance(var, list):
            return [vtype(item) for item in var]
        else:
            return [vtype(var)]

    def set_physics_parameters(self, params):
        self.user_nml['physics']['mp_physics'] = self.var_to_list(self.user_nml['physics']['mp_physics'], int)
        for i, v in enumerate(self.user_nml['physics']['mp_physics']):
            if v == -1:
                for var, val in params:
                    self.user_nml['physics'][var] = self.var_to_list(self.user_nml['physics'][var], int)
                    self.user_nml['physics'][var][i] = val

    def apply_physics_suite(self):
        params_conus = [('mp_physics', 8), ('cu_physics', 6), ('ra_lw_physics', 4), ('ra_sw_physics', 4),
                        ('bl_pbl_physics', 2), ('sf_sfclay_physics', 2), ('sf_surface_physics', 2)]

        params_tropical = [('mp_physics', 6), ('cu_physics', 16), ('ra_lw_physics', 4), ('ra_sw_physics', 4),
                           ('bl_pbl_physics', 1), ('sf_sfclay_physics', 91), ('sf_surface_physics', 2)]

        if self.user_nml['physics']['physics_suite'].lower() == 'conus':
            self.set_physics_parameters(params_conus)
                                        
        if self.user_nml['physics']['physics_suite'].lower() == 'tropical':
            self.set_physics_parameters(params_tropical)

    def validate(self):
        self.apply_physics_suite()

        for section in self.user_nml:
            if section not in self.nml_cfg:
                if section == 'namelist_quilt':
                    continue

                self.errors.append({"section": section, "variable": "", "message": f"Unknown section &{section} in namelist.input -- ignoring"})

                continue

            for var in self.user_nml[section]:
                if var not in self.nml_cfg[section]:
                    self.errors.append({"section": section, "variable": var, "message": f"Unknown variable found in &{section} namelist: {var}"})

                    self.supported_nml = False
                    continue

                var_cfg = self.nml_cfg[section][var]
                if var_cfg['nml_support'] == '':
                    continue

                if var_cfg['type'] == bool:
                    soptions = []
                    if 'f' in var_cfg['nml_support'] or '0' in var_cfg['nml_support']:
                        soptions.append(False)
                    if 't' in var_cfg['nml_support'] or '1' in var_cfg['nml_support']:
                        soptions.append(True)
                else:
                    soptions = self.var_to_list(var_cfg['nml_support'].split(','), var_cfg['type'])

                unsupported_found = False
                for option in self.var_to_list(self.user_nml[section][var], var_cfg['type']):
                    if option not in soptions:
                        unsupported_found = True

                if unsupported_found:
                    self.errors.append({"section": section, "variable": var, "message": f"Unsupported option found for variable '{var}' in &{section} namelist: {var} = {self.user_nml[section][var]}"})
                    self.errors.append({"section": section, "variable": var, "message": f"Supported options for {var}: {var_cfg['nml_support']}"})

                    self.supported_nml = False

        return self.errors

