# import ipywidgets as widgets
# from IPython.display import display, clear_output
#
#
# def create_semtos_interface(energy_sim, run_simulation_func,
#                             grid_dependency, battery_action, load_control,
#                             solar_curtailment, battery_charging_priority):
#     """
#     تابع لبناء واجهة مستخدم تفاعلية (UI) تعتمد على ipywidgets
#     وتقوم بتحديث الحسابات والرسوم البيانية ديناميكياً عند الضغط على الزر.
#     """
#
#     # 1. إنشاء مؤشرات السحب (Sliders) للمدخلات الخمسة بحسب النطاقات المنطقية
#     solar_slider = widgets.IntSlider(value=75, min=0, max=100, step=1, description='☀️ طاقة الشمس (%):')
#     soc_slider = widgets.IntSlider(value=40, min=0, max=100, step=1, description='🔋 شحن البطارية (%):')
#     grid_slider = widgets.IntSlider(value=100, min=0, max=100, step=1, description='🔌 استقرار الشبكة (%):')
#     consumption_slider = widgets.IntSlider(value=350, min=0, max=1000, step=10, description='📉 عداد تراكمي (ك.و.س):')
#     demand_slider = widgets.IntSlider(value=60, min=0, max=100, step=1, description='🏠 حمل المنزل (%):')
#
#     # تحسين مظهر النصوص في المؤشرات لتظهر بشكل مريح وثابت
#     slider_style = {'description_width': '150px'}
#     for slider in [solar_slider, soc_slider, grid_slider, consumption_slider, demand_slider]:
#         slider.style = slider_style
#         slider.layout.width = '450px'
#
#     # 2. إنشاء زر التشغيل والمحاكاة
#     run_button = widgets.Button(
#         description='🚀 تشغيل محاكاة SEMTOS',
#         disabled=False,
#         button_style='success',  # لون أخضر احترافي
#         tooltip='اضغط لحساب النتائج وتحديث المخططات البيانية',
#         icon='refresh'
#     )
#     run_button.layout.width = '250px'
#     run_button.layout.margin = '20px 0px 20px 150px'
#
#     # 3. صندوق مخصص لعرض المخرجات (الجدول والرسم البياني) بشكل متجدد
#     output_container = widgets.Output()
#
#     # 4. التابع الذي يتم تنفيذه عند الضغط على الزر
#     def on_button_clicked(b):
#         with output_container:
#             # تنظيف المخرجات السابقة حتى لا تتراكم الرسوم تحت بعضها
#             clear_output(wait=True)
#
#             # استدعاء دالة المحاكاة المحدثة وتمرير القيم الحالية من المؤشرات
#             run_simulation_func(
#                 energy_sim=energy_sim,
#                 solar_production=solar_slider.value,
#                 battery_soc=soc_slider.value,
#                 grid_status=grid_slider.value,
#                 cum_consumption=consumption_slider.value,
#                 current_demand=demand_slider.value,
#                 grid_dependency=grid_dependency,
#                 battery_action=battery_action,
#                 load_control=load_control,
#                 solar_curtailment=solar_curtailment,
#                 battery_charging_priority=battery_charging_priority,
#                 scenario_title=f"معطيات المستخدم اللحظية (شمس: {solar_slider.value}%, بطارية: {soc_slider.value}%)"
#             )
#
#     # ربط الزر بالتابع الخاص به
#     run_button.on_click(on_button_clicked)
#
#     # 5. ترتيب عناصر الواجهة بصرياً في صناديق (Layout Containers)
#     ui_layout = widgets.VBox([
#         widgets.HTML("<h2 style='color: #ffaa00; font-family: Segoe UI;'>🎮 لوحة التحكم التفاعلية بنظام SEMTOS</h2>"),
#         widgets.HTML(
#             "<p style='color: #e0e0e0;'>قم بتعديل قيم المدخلات الحالية للمنظومة ثم اضغط على الزر لتحديث القرارات:</p>"),
#         solar_slider,
#         soc_slider,
#         grid_slider,
#         consumption_slider,
#         demand_slider,
#         run_button,
#         output_container
#     ])
#
#     # عرض الواجهة بالكامل داخل النوت بوك
#     display(ui_layout)
#
#     # تشغيل المحاكاة مرة واحدة تلقائياً عند الإقلاع الأول لملء الشاشة بالنتائج الافتراضية
#     on_button_clicked(None)
import ipywidgets as widgets
from IPython.display import display, clear_output


def create_fuzz_interface(energy_sim, run_simulation_func,
                            grid_dependency, battery_action, load_control,
                            solar_curtailment, battery_charging_priority):
    """
    واجهة مستخدم تفاعلية مطورة ومحسنة هندسياً لنظام SEMTOS[cite: 23].
    تتميز بربط المؤشرات بقيم رقمية، تنسيق داكن متناسق، وتنظيم مرئي للمدخلات والمخرجات[cite: 23].
    """

    # تحسين الهيكل والتصميم الثابت للنصوص والمؤشرات
    slider_style = {'description_width': '160px'}

    # دالة مساعدة لإنشاء مؤشر سحب مع صندوق إدخال رقمي متصلين معاً ديناميكياً
    def create_linked_control(label, emoji, val, min_v, max_v, step_v):
        slider = widgets.IntSlider(
            value=val, min=min_v, max=max_v, step=step_v,
            description=f"{emoji} {label}:",
            style=slider_style, continuous_update=True
        )
        slider.layout.width = '380px'

        num_box = widgets.BoundedIntText(
            value=val, min=min_v, max=max_v, step=step_v,
            style={'description_width': '0px'},
            layout=widgets.Layout(width='70px', margin='0px 0px 0px 10px')
        )

        # ربط قيم المؤشر والصندوق الرقمي في اتجاهين
        widgets.link((slider, 'value'), (num_box, 'value'))

        # دمجهم في سطر واحد متناسق
        return slider, num_box, widgets.HBox([slider, num_box],
                                             layout=widgets.Layout(align_items='center', margin='5px 0px'))

    # إنشاء عناصر التحكم المترابطة للمدخلات الخمسة [cite: 9, 32]
    solar_slider, solar_box, solar_row = create_linked_control('طاقة الشمس (%)', '☀️', 75, 0, 100, 1)
    soc_slider, soc_box, soc_row = create_linked_control('شحن البطارية (%)', '🔋', 40, 0, 100, 1)
    grid_status_slider, grid_box, grid_row = create_linked_control('استقرار الشبكة (%)', '🔌', 100, 0, 100, 1)
    consumption_slider, consumption_box, consumption_row = create_linked_control('عداد تراكمي (ك.و.س)', '📉', 350, 0,
                                                                                 1000, 10)
    demand_slider, demand_box, demand_row = create_linked_control('حمل المنزل (%)', '🏠', 60, 0, 100, 1)

    # تجميع صفوف المدخلات في حاوية عمودية منظمة [cite: 9, 32]
    inputs_vbox = widgets.VBox([
        solar_row,
        soc_row,
        grid_row,
        consumption_row,
        demand_row
    ], layout=widgets.Layout(padding='10px', background_color='#1a1a1a', border='1px dashed #444', margin='5px 0px'))

    # وضع المدخلات داخل لوحة أكورديون قابلة للطي لإعطاء طابع برمجي ذكي [cite: 23]
    accordion = widgets.Accordion(children=[inputs_vbox], selected_index=0)
    accordion.set_title(0, '📥 لوحة التحكم وتعديل المعطيات الحالية المنظومية')
    accordion.layout.margin = '10px 0px'

    # 2. إنشاء زر التشغيل والمحاكاة بتصميم عصري عريض وجذاب [cite: 23]
    run_button = widgets.Button(
        description='🚀 تشغيل محاكاة نظام SEMTOS الذكي',
        disabled=False,
        button_style='',  # تفريغ الستايل الافتراضي لإضافة مظهر مخصص وثابت
        tooltip='اضغط هنا لمعالجة القواعد وحساب المخرجات الضبابية ديناميكياً [cite: 17, 23]',
        icon='cogs'
    )
    run_button.layout.width = '100%'
    run_button.layout.height = '45px'
    run_button.layout.margin = '15px 0px'
    run_button.style.button_color = '#00ff66'  # لون أخضر فوسفوري مخصص للمهندسين
    run_button.style.font_weight = 'bold'

    # 3. صندوق مخصص ومستقل تماماً لعرض المخرجات والرسومات البيانية [cite: 12, 23]
    output_container = widgets.Output()

    # 4. دالة معالجة الحدث عند الضغط على الزر لتمرير القيم المحسوبة [cite: 17, 23]
    def on_button_clicked(b):
        with output_container:
            clear_output(wait=True)

            # استدعاء دالة الحساب والرسم الرئيسية وتمرير القيم اللحظية [cite: 12, 17]
            run_simulation_func(
                energy_sim=energy_sim,
                solar_production=solar_slider.value,
                battery_soc=soc_slider.value,
                grid_status=grid_status_slider.value,
                cum_consumption=consumption_slider.value,
                current_demand=demand_slider.value,
                grid_dependency=grid_dependency,
                battery_action=battery_action,
                load_control=load_control,
                solar_curtailment=solar_curtailment,
                battery_charging_priority=battery_charging_priority,
                scenario_title=f"معطيات المستخدم (شمس: {solar_slider.value}%, بطارية: {soc_slider.value}%)"
            )

    # ربط حدث الضغط على الزر بالدالة التنفيذية [cite: 23]
    run_button.on_click(on_button_clicked)

    # 5. تجميع الواجهة بالكامل داخل تصميم متناسق ومحمي بهوامش مناسبة [cite: 23]
    ui_header = widgets.HTML("""
        <div style="font-family: 'Segoe UI', sans-serif; background-color: #111; padding: 15px; border-radius: 8px; border-left: 5px solid #ffaa00; margin-bottom: 10px;">
            <h2 style='color: #ffaa00; margin: 0px; font-size: 22px;'>🎮 لوحة التحكم التفاعلية بنظام SEMTOS الفازي</h2>
            <p style='color: #cccccc; margin: 5px 0px 0px 0px; font-size: 13px;'>مشروع التخرج والتقييم الأكاديمي لأنظمة الذكاء الاصطناعي والخبير الضبابي.</p>
        </div>
    """)

    main_interface_layout = widgets.VBox([
        ui_header,
        accordion,
        run_button,
        output_container
    ], layout=widgets.Layout(max_width='900px', margin='0 auto', padding='10px'))

    # عرض لوحة التحكم المتكاملة للمستخدم داخل الخلية [cite: 23]
    display(main_interface_layout)

    # تشغيل الحسابات تلقائياً للمرة الأولى لعرض الرسوم الافتراضية فوراً [cite: 12, 17]
    on_button_clicked(None)