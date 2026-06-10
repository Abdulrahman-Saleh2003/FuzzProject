import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_semtos_control_surfaces(energy_sim, resolution=20):
    """
    تابع مخصص لرسم أسطح القرار ثلاثية الأبعاد (3D Control Surfaces) لنظام SEMTOS.
    يقوم بحساب العلاقات المستمرة بين المدخلات والمخرجات وتوليد مجسمات ثلاثية الأبعاد احترافية.
    """
    # 1. تفعيل الثيم المظلم للرسومات ليتوافق مع لوحة تحكم المشروع بالكامل
    plt.style.use('dark_background')

    print("⏳ جاري توليد نقاط السطح ثلاثي الأبعاد (قد يستغرق بضع ثوانٍ)...")

    # ==========================================
    # 🏗️ السطح الأول: [شمس + بطارية] ---> [التحكم بالأحمال]
    # ==========================================

    solar_range = np.linspace(0, 100, resolution)
    battery_range = np.linspace(0, 100, resolution)
    Solar_Mesh, Battery_Mesh = np.meshgrid(solar_range, battery_range)

    Load_Control_Surface = np.zeros_like(Solar_Mesh)

    # قيم المدخلات الأخرى تثبت عند منتصف النطاقات المنطقية
    fixed_grid_status = 100
    fixed_cum_cons = 350
    fixed_current_demand = 50

    for i in range(resolution):
        for j in range(resolution):
            energy_sim.input['solar_production'] = Solar_Mesh[i, j]
            energy_sim.input['battery_soc']       = Battery_Mesh[i, j]
            energy_sim.input['grid_status']      = fixed_grid_status
            energy_sim.input['cum_consumption']  = fixed_cum_cons
            energy_sim.input['current_demand']   = fixed_current_demand

            try:
                energy_sim.compute()
                Load_Control_Surface[i, j] = energy_sim.output['load_control']
            except KeyError:
                Load_Control_Surface[i, j] = 50.0  # قيمة احتياطية آمنة في حال الحواف غير المغطاة

    # ==========================================
    # 🏗️ السطح الثاني: [تراكمي العداد + وضع الشبكة] ---> [الاعتماد على الشبكة]
    # ==========================================

    cum_cons_range = np.linspace(0, 1000, resolution)
    grid_status_range = np.linspace(0, 100, resolution)
    Cum_Cons_Mesh, Grid_Status_Mesh = np.meshgrid(cum_cons_range, grid_status_range)

    Grid_Dependency_Surface = np.zeros_like(Cum_Cons_Mesh)

    # قيم المدخلات الأخرى تثبت عند قيم اعتيادية
    fixed_solar_prod = 50
    fixed_battery_soc = 50
    fixed_current_demand = 60

    for i in range(resolution):
        for j in range(resolution):
            energy_sim.input['cum_consumption']  = Cum_Cons_Mesh[i, j]
            energy_sim.input['grid_status']      = Grid_Status_Mesh[i, j]
            energy_sim.input['solar_production'] = fixed_solar_prod
            energy_sim.input['battery_soc']       = fixed_battery_soc
            energy_sim.input['current_demand']   = fixed_current_demand

            try:
                energy_sim.compute()
                Grid_Dependency_Surface[i, j] = energy_sim.output['grid_dependency']
            except KeyError:
                Grid_Dependency_Surface[i, j] = 50.0

    # ==========================================
    # 🎨 إعداد ساحة الرسم وإظهار المجسمات ثلاثية الأبعاد
    # ==========================================
    fig = plt.figure(figsize=(16, 7))

    # الرسم الأول: مجسم التحكم بالأحمال
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    surf1 = ax1.plot_surface(Solar_Mesh, Battery_Mesh, Load_Control_Surface,
                             cmap='viridis', edgecolor='none', alpha=0.9)
    ax1.set_title('1. Load Control Decision Surface', fontsize=14, color='#00ff66', pad=15)
    ax1.set_xlabel('Solar Production (%)', color='white', labelpad=10)
    ax1.set_ylabel('Battery SoC (%)', color='white', labelpad=10)
    ax1.set_zlabel('Load Control (%)', color='white', labelpad=10)
    fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10, label='Load Luxury Level')
    ax1.view_init(elev=30, azim=135)

    # الرسم الثاني: مجسم الاعتماد على الشبكة واجتناب شريحة الـ 500
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    surf2 = ax2.plot_surface(Cum_Cons_Mesh, Grid_Status_Mesh, Grid_Dependency_Surface,
                             cmap='plasma', edgecolor='none', alpha=0.9)
    ax2.set_title('2. Grid Dependency Decision Surface', fontsize=14, color='#00ffff', pad=15)
    ax2.set_xlabel('Cumulative Consumption (kWh)', color='white', labelpad=10)
    ax2.set_ylabel('Grid Status (%)', color='white', labelpad=10)
    ax2.set_zlabel('Grid Dependency (%)', color='white', labelpad=10)
    fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10, label='Grid Use Level')
    ax2.view_init(elev=30, azim=45)

    plt.tight_layout()
    plt.show()