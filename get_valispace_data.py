import valispace

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
TIME_DATA_TRANSMIS = 'Time_Data_Transmission'
PERIOD = 'Period'
NUMBER_GS = 'Number_GS'


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

    def get_comp_mass_info(self):
        mass_budget = [[0.0, 0.0] for _ in LIST_COMP]
        list_mass_comp = [name_comp + '.' + MASS for name_comp in LIST_COMP]

        for vali in self.project_vars:
            if vali['name'] not in list_mass_comp:
                continue
            ind = LIST_COMP.index(vali['name'].split('.')[0])
            mass_budget[ind] = [vali['value'], vali['margin_plus']/100]
        return mass_budget

    def get_propulsion_mass_info(self):
        mass_propulsion_info = [[0.0, 0.0]]

        for vali in self.project_vars:
            if vali['name'] == str(PROPULSION + '.' + MASS_PROPELLANT):
                mass_propulsion_info[0] = [vali['value'], vali['margin_plus']/100]
                return mass_propulsion_info

    def get_comp_price_info(self):
        cost_budget = [[0.0] for _ in LIST_COMP]
        list_price_comp = [name_comp + '.' + PRICE for name_comp in LIST_COMP]

        for vali in self.project_vars:
            if vali['name'] not in list_price_comp:
                continue
            ind = LIST_COMP.index(vali['name'].split('.')[0])
            cost_budget[ind] = [vali['value']]
        return cost_budget

    def get_data_payload_info(self):
        data_payload_budget = [[0.0], [0.0]]

        for vali in self.project_vars:
            if vali['name'] == str(PAYLOAD_PROBE + '.' + DATA_RATE_TRANSMITTED + '.' + OPERATION):
                data_payload_budget[0][0] = vali['value']
            if vali['name'] == str(PAYLOAD_RADIOTOMOGRAPHY + '.' + DATA_RATE_TRANSMITTED + '.' + BEACON_EXPERIMENT):
                data_payload_budget[1][0] = vali['value']

        return data_payload_budget

    def get_downlink_info(self):
        data_downlink_budget = [[0.0]]

        for vali in self.project_vars:
            if vali['name'] == str(COMMUNICATION + '.' + DOWNLINK):
                data_downlink_budget[0][0] = vali['value']
                return data_downlink_budget

    def get_comp_data_info(self):
        data_comp_budget = [[0.0], [0.0]]

        for vali in self.project_vars:
            if vali['name'] == str(ADSC + '.' + DATA_RATE_TRANSMITTED + '.' + OPERATION):
                data_comp_budget[0][0] = vali['value']
            if vali['name'] == str(ON_BOARD_COMPUTER + '.' + DATA_RATE_TRANSMITTED + '.' + OPERATION):
                data_comp_budget[1][0] = vali['value']

        return data_comp_budget

    def get_time_data_transmitted_to_gs(self):
        time_data_transmitted_to_gs = [[0.0]]

        for vali in self.project_vars:
            if vali['name'] == str(ORBITAL + '.' + TIME_DATA_TRANSMIS):
                time_data_transmitted_to_gs[0][0] = vali['value']
                return time_data_transmitted_to_gs

    def get_orbit_period(self):
        orbit_period = [[0.0]]

        for vali in self.project_vars:
            if vali['name'] == str(ORBITAL + '.' + PERIOD):
                orbit_period[0][0] = vali['value']
                return orbit_period

    def get_number_of_gs(self):
        number_of_gs = [[0.0]]

        for vali in self.project_vars:
            if vali['name'] == str(ORBITAL + '.' + NUMBER_GS):
                number_of_gs[0][0] = vali['value']
                return number_of_gs




        # for x in self.project_vars:
        #     print(x)
        # valispace.get_vali_by_name(vali_name='Blade', project_name='Fan)




