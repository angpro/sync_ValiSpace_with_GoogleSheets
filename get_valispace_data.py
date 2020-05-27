import valispace


CUBESAT = 'CubeSat1'
# ------------------ COMPONENTS
ADSC = 'ADCS'
COMMUNICATION = 'Communication'
# for COMMUNICATION
DOWNLINK = 'downlink'

EL_POWER = 'ElectricalPower'
MECHANICAL = 'Mechanical'
ON_BOARD_COMPUTER = 'OnBoardComputer'
PAYLOAD_PROBE = 'PayloadProbe'
PAYLOAD_RADIOTOMOGRAPHY = 'PayloadRadiotomography'
PROPULSION = 'Propulsion'
# for PROPULSION
MASS_PROPELLANT = 'mass_propellant'

THERMAL_CONTROL = 'ThermalControl'
LIST_COMP = [ADSC, COMMUNICATION, EL_POWER, MECHANICAL, ON_BOARD_COMPUTER,
             PAYLOAD_PROBE, PAYLOAD_RADIOTOMOGRAPHY, PROPULSION,
             THERMAL_CONTROL]

# ------------------ PROPERTIES
PRICE = 'price'
MASS = 'mass_kg'
POWER_CONSUMPTION = 'power_consumption'
DATA_RATE_TRANSMITTED = 'data_rate_transmitted'

# ------------------ OPERATION MODES CUBE_SAT1
DETUMBLE = 'Detumble'
SAFE = 'Safe'
DATA_TRANSMISSION = 'Data_Transmission'
OPERATION = 'Operation'
BEACON_EXPERIMENT = 'Beacon_Experiment'
MANEUVER = 'Maneuver'
LIST_MODES = [DETUMBLE, SAFE, DATA_TRANSMISSION, OPERATION, BEACON_EXPERIMENT,
              MANEUVER]

# ------------------ ORBITAL
ORBITAL = 'Orbital'
PERIOD = 'Period'
NUMBER_GS = 'Number_GS'
NUMBER_BEACON_GS = 'Number_Beacon_GS'

# ------------------ TIME MODES
TIME_DETUMBLE = 'Time_Detumble'
TIME_SAFE = 'Time_Safe'
TIME_DATA_TRANSMIS = 'Time_Data_Transmission'
TIME_OPERATION = 'Time_Operation'
TIME_BEACON_EXPERIMENT = 'Time_Beacon_Experiment'
TIME_MANEUVER = 'Time_Maneuver'


class GetValiData:
    def __init__(self, url, username, password, project_name):
        self.valispace = valispace
        self.username = username
        self.password = password
        self.url = url
        self.project_name = project_name
        self.valispace_api = valispace.API(url=url,
                                           username=self.username,
                                           password=self.password)

        self.project_comps = self.valispace_api.get_component_list(
            project_name=project_name)
        self.project_vars = self.valispace_api.get_vali_list(
            project_name=project_name)

    @staticmethod
    def check_name(vali_name, first, second=None, third=None):
        if third:
            if vali_name == first + '.' + second + '.' + third or vali_name == CUBESAT + '.' + first +'.'+ second +'.'+ third:
                return True
        if second:
            if vali_name == first + '.' + second or vali_name == CUBESAT + '.' + first + '.' + second:
                return True
        if vali_name == first or vali_name == CUBESAT + '.' + first:
            return True
        return False

    def get_comp_mass_info(self):
        mass_budget = [[0.0, 0.0] for _ in LIST_COMP]
        list_mass_comp = [name_comp + '.' + MASS for name_comp in LIST_COMP]
        list_price_comp1 = [CUBESAT + '.' + name_comp + '.' + MASS for name_comp in LIST_COMP]

        for vali in self.project_vars:
            if vali['name'] not in list_mass_comp and vali['name'] not in list_price_comp1:
                continue
            if vali['name'].split('.')[0] in LIST_COMP:
                ind = LIST_COMP.index(vali['name'].split('.')[0])
            if vali['name'].split('.')[1] in LIST_COMP:
                ind = LIST_COMP.index(vali['name'].split('.')[1])
            mass_budget[ind] = [vali['value'], vali['margin_plus']/100]
        return mass_budget

    def get_propulsion_mass_info(self):
        mass_propulsion_info = [[0.0, 0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], PROPULSION, MASS_PROPELLANT):
                mass_propulsion_info[0] = [vali['value'], vali['margin_plus']/100]
                return mass_propulsion_info

    def get_comp_price_info(self):
        cost_budget = [[0.0] for _ in LIST_COMP]
        list_price_comp = [name_comp + '.' + PRICE for name_comp in LIST_COMP]
        list_price_comp1 = [CUBESAT + '.' + name_comp + '.' + PRICE for name_comp in LIST_COMP]

        for vali in self.project_vars:
            if vali['name'] not in list_price_comp and vali['name'] not in list_price_comp1:
                continue
            if vali['name'].split('.')[0] in LIST_COMP:
                ind = LIST_COMP.index(vali['name'].split('.')[0])
            if vali['name'].split('.')[1] in LIST_COMP:
                ind = LIST_COMP.index(vali['name'].split('.')[1])
            cost_budget[ind] = [vali['value']]
        return cost_budget

    def get_data_payload_info(self):
        data_payload_budget = [[0.0], [0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], PAYLOAD_PROBE, DATA_RATE_TRANSMITTED, OPERATION):
                data_payload_budget[0][0] = vali['value']
            if self.check_name(vali['name'], PAYLOAD_RADIOTOMOGRAPHY, DATA_RATE_TRANSMITTED, BEACON_EXPERIMENT):
                data_payload_budget[1][0] = vali['value']

        return data_payload_budget

    def get_downlink_info(self):
        data_downlink_budget = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], COMMUNICATION, DOWNLINK):
                data_downlink_budget[0][0] = vali['value']
                return data_downlink_budget

    def get_comp_data_info(self):
        data_comp_budget = [[0.0], [0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ADSC, DATA_RATE_TRANSMITTED, OPERATION):
                data_comp_budget[0][0] = vali['value']
            if self.check_name(vali['name'], ON_BOARD_COMPUTER, DATA_RATE_TRANSMITTED, OPERATION):
                data_comp_budget[1][0] = vali['value']

        return data_comp_budget

    def get_orbit_period(self):
        orbit_period = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ORBITAL, PERIOD):
                orbit_period[0][0] = vali['value']
                return orbit_period

    def get_number_of_gs(self):
        number_of_gs = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ORBITAL, NUMBER_GS):
                number_of_gs[0][0] = vali['value']
                return number_of_gs

    def get_number_of_beacon_gs(self):
        number_of_beacon_gs = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ORBITAL, NUMBER_BEACON_GS):
                number_of_beacon_gs[0][0] = vali['value']
                return number_of_beacon_gs

    def _get_power_for_mode(self, MODE):
        power_for_mode = [[0.0] for _ in LIST_COMP]
        list_power_for_mode_comp = [name_comp + '.' + POWER_CONSUMPTION + '.' + MODE for name_comp in LIST_COMP]
        list_power_for_mode_comp1 = [CUBESAT + '.' + name_comp + '.' + POWER_CONSUMPTION + '.' + MODE for name_comp in LIST_COMP]
        print(MODE)

        for vali in self.project_vars:
            if vali['name'] not in list_power_for_mode_comp and vali['name'] not in list_power_for_mode_comp1:
                continue
            if vali['name'].split('.')[0] in LIST_COMP:
                ind = LIST_COMP.index(vali['name'].split('.')[0])
            if vali['name'].split('.')[1] in LIST_COMP:
                ind = LIST_COMP.index(vali['name'].split('.')[1])
            power_for_mode[ind] = [vali['value']]
        print(power_for_mode)

        return power_for_mode

    def get_power_for_detumble_mode(self):
        return self._get_power_for_mode(DETUMBLE)

    def get_power_for_safe_mode(self):
        return self._get_power_for_mode(SAFE)

    def get_power_data_transm_mode(self):
        return self._get_power_for_mode(DATA_TRANSMISSION)

    def get_power_for_operation_mode(self):
        return self._get_power_for_mode(OPERATION)

    def get_power_for_beacon_experiment_mode(self):
        return self._get_power_for_mode(BEACON_EXPERIMENT)

    def get_power_for_maneuver_mode(self):
        return self._get_power_for_mode(MANEUVER)

    def get_time_detumble(self):
        time_detumble = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ADSC, TIME_DETUMBLE):
                time_detumble[0][0] = vali['value']
                return time_detumble

    def get_time_safe(self):
        time_safe = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ORBITAL, TIME_SAFE):
                time_safe[0][0] = vali['value']
                return time_safe

    def get_time_data_transmitted_to_gs(self):
        time_data_transmitted_to_gs = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ORBITAL, TIME_DATA_TRANSMIS):
                time_data_transmitted_to_gs[0][0] = vali['value']
                return time_data_transmitted_to_gs

    def get_time_operation(self):
        time_operation = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ORBITAL, TIME_OPERATION):
                time_operation[0][0] = vali['value']
                return time_operation

    def get_time_beacon_experiment(self):
        time_beacon_experiment = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ORBITAL, TIME_BEACON_EXPERIMENT):
                time_beacon_experiment[0][0] = vali['value']
                return time_beacon_experiment

    def get_time_maneuver(self):
        time_maneuver = [[0.0]]

        for vali in self.project_vars:
            if self.check_name(vali['name'], ORBITAL, TIME_MANEUVER):
                time_maneuver[0][0] = vali['value']
                return time_maneuver


        # for x in self.project_vars:
        #     print(x)
        # valispace_api.get_vali_by_name(vali_name='Blade', project_name='Fan)
