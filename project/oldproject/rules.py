from skfuzzy import control as ctrl


def get_rules(solar_production, battery_soc, grid_status, cum_consumption, current_demand,
                     grid_dependency, battery_action, load_control, solar_curtailment, battery_charging_priority):
    """
    تابع لتجميع وحزم كافة القواعد الـ 54 لنظام SEMTOS الضبابي،
    بحيث يتم استدعاؤه ديناميكياً من النوت بوك دون تضارب المتغيرات.
    """

    rules = [
        # ---------- 2 Inputs ----------
        ctrl.Rule(battery_soc['empty'] & grid_status['excellent'],
                  (battery_charging_priority['urgent'], battery_action['fast_charge'], grid_dependency['full'])),
        ctrl.Rule(battery_soc['full'] & solar_production['high'], (grid_dependency['islanded'], load_control['full'])),
        ctrl.Rule(battery_soc['good'] & solar_production['medium'], (grid_dependency['low'], load_control['normal'])),
        ctrl.Rule(battery_soc['empty'] & solar_production['low'],
                  (battery_charging_priority['high'], grid_dependency['high'])),
        ctrl.Rule(grid_status['weak'] & current_demand['high'], (load_control['eco'], grid_dependency['medium'])),
        ctrl.Rule(current_demand['low'] & solar_production['high'],
                  (battery_action['charge'], battery_charging_priority['medium'])),
        ctrl.Rule(battery_soc['full'] & current_demand['high'],
                  (battery_action['full_discharge'], load_control['full'])),
        ctrl.Rule(battery_soc['good'] & grid_status['stable'], (load_control['normal'], battery_action['idle'])),
        ctrl.Rule(solar_production['high'] & current_demand['high'], (load_control['full'], grid_dependency['low'])),
        ctrl.Rule(solar_production['none'] & grid_status['off'], (load_control['critical'])),

        # ---------- 3 Inputs ----------
        ctrl.Rule(battery_soc['low'] & solar_production['none'] & grid_status['off'],
                  (load_control['critical'], battery_action['idle'])),
        ctrl.Rule(battery_soc['medium'] & solar_production['high'] & current_demand['medium'],
                  (load_control['normal'], grid_dependency['low'])),
        ctrl.Rule(battery_soc['full'] & solar_production['high'] & current_demand['low'],
                  (battery_action['idle'], solar_curtailment['high'])),
        ctrl.Rule(battery_soc['empty'] & grid_status['stable'] & solar_production['low'],
                  (battery_action['fast_charge'], battery_charging_priority['urgent'])),
        ctrl.Rule(battery_soc['good'] & current_demand['high'] & solar_production['medium'],
                  (battery_action['eco_discharge'])),
        ctrl.Rule(cum_consumption['border'] & solar_production['high'] & battery_soc['good'],
                  (grid_dependency['low'], load_control['eco'])),
        ctrl.Rule(cum_consumption['critical'] & grid_status['excellent'] & solar_production['high'],
                  (grid_dependency['islanded'])),
        ctrl.Rule(battery_soc['medium'] & current_demand['high'] & grid_status['weak'], (load_control['eco'])),
        ctrl.Rule(battery_soc['full'] & solar_production['medium'] & grid_status['off'],
                  (battery_action['eco_discharge'])),
        ctrl.Rule(solar_production['none'] & current_demand['high'] & grid_status['stable'], (grid_dependency['high'])),

        # ---------- 4 Inputs ----------
        ctrl.Rule(battery_soc['good'] & solar_production['high'] & grid_status['stable'] & current_demand['medium'],
                  (load_control['full'], grid_dependency['low'])),
        ctrl.Rule(battery_soc['empty'] & solar_production['none'] & current_demand['high'] & grid_status['off'],
                  (load_control['critical'], battery_action['idle'])),
        ctrl.Rule(battery_soc['full'] & solar_production['high'] & current_demand['high'] & cum_consumption['safe'],
                  (load_control['full'], grid_dependency['islanded'])),
        ctrl.Rule(
            battery_soc['medium'] & solar_production['medium'] & grid_status['stable'] & cum_consumption['warning'],
            (load_control['normal'])),
        ctrl.Rule(battery_soc['good'] & solar_production['high'] & grid_status['excellent'] & current_demand['low'],
                  (solar_curtailment['full'])),

        # ---------- 5 Inputs ----------
        ctrl.Rule(battery_soc['full'] & solar_production['high'] & grid_status['excellent'] & current_demand['high'] &
                  cum_consumption['safe'],
                  (load_control['full'], grid_dependency['islanded'], battery_action['full_discharge'])),
        ctrl.Rule(battery_soc['empty'] & solar_production['none'] & grid_status['off'] & current_demand['high'] &
                  cum_consumption['critical'], (load_control['critical'], battery_action['idle'])),
        ctrl.Rule(battery_soc['low'] & solar_production['low'] & grid_status['stable'] & current_demand['medium'] &
                  cum_consumption['warning'], (battery_charging_priority['high'], grid_dependency['high'])),
        ctrl.Rule(battery_soc['good'] & solar_production['medium'] & grid_status['stable'] & current_demand['medium'] &
                  cum_consumption['safe'], (load_control['normal'], battery_action['eco_discharge'])),
        ctrl.Rule(battery_soc['full'] & solar_production['high'] & grid_status['off'] & current_demand['low'] &
                  cum_consumption['safe'], (solar_curtailment['high'], battery_action['idle'])),

        # ---------- Single Input / Base Rules ----------
        ctrl.Rule(battery_soc['medium'], battery_action['idle']),
        ctrl.Rule(battery_soc['good'], battery_action['eco_discharge']),
        ctrl.Rule(battery_soc['full'], battery_action['full_discharge']),
        ctrl.Rule(battery_soc['empty'], battery_action['fast_charge']),
        ctrl.Rule(battery_soc['low'], battery_action['charge']),

        ctrl.Rule(battery_soc['empty'], battery_charging_priority['urgent']),
        ctrl.Rule(battery_soc['low'], battery_charging_priority['high']),
        ctrl.Rule(battery_soc['medium'], battery_charging_priority['medium']),
        ctrl.Rule(battery_soc['good'], battery_charging_priority['low']),
        ctrl.Rule(battery_soc['full'], battery_charging_priority['none']),

        ctrl.Rule(solar_production['none'], solar_curtailment['none']),
        ctrl.Rule(solar_production['low'], solar_curtailment['low']),
        ctrl.Rule(solar_production['medium'], solar_curtailment['medium']),
        ctrl.Rule(solar_production['high'] & battery_soc['full'], solar_curtailment['full']),
        ctrl.Rule(solar_production['high'] & battery_soc['good'], solar_curtailment['high']),

        ctrl.Rule(cum_consumption['safe'], load_control['full']),
        ctrl.Rule(cum_consumption['warning'], load_control['normal']),
        ctrl.Rule(cum_consumption['border'], load_control['eco']),
        ctrl.Rule(cum_consumption['critical'], load_control['critical']),

        # ---------- Multi-Output Rule & Safe Guards ----------
        ctrl.Rule(battery_soc['full'] & solar_production['high'] & grid_status['excellent'] & cum_consumption['safe'] &
                  current_demand['low'],
                  (grid_dependency['islanded'], load_control['full'], battery_action['idle'], solar_curtailment['full'],
                   battery_charging_priority['none'])),

        ctrl.Rule(solar_production['high'] & battery_soc['empty'], solar_curtailment['low']),
        ctrl.Rule(solar_production['high'] & battery_soc['low'], solar_curtailment['medium']),
        ctrl.Rule(solar_production['high'] & battery_soc['medium'], solar_curtailment['high']),
        ctrl.Rule(solar_production['high'], solar_curtailment['medium'])
    ]

    return rules