

import ipywidgets as widgets
from IPython.display import display, clear_output


def create_fuzz_interface(energy_sim, run_simulation_func,
                          grid_dependency, battery_dependency, load_control):


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

        # ربط قيم المؤشر والصندوق الرقمي في اتجاهين بشكل متزامن
        widgets.link((slider, 'value'), (num_box, 'value'))

        # دمجهم في سطر واحد متناسق
        return slider, num_box, widgets.HBox([slider, num_box],
                                             layout=widgets.Layout(align_items='center', margin='5px 0px'))

    # إنشاء عناصر التحكم المترابطة للمدخلات الخمسة الشاملة للنظام
    solar_slider, solar_box, solar_row = create_linked_control('طاقة الشمس (%)', '☀️', 75, 0, 100, 1)
    soc_slider, soc_box, soc_row = create_linked_control('شحن البطارية (%)', '🔋', 40, 0, 100, 1)
    grid_status_slider, grid_box, grid_row = create_linked_control('استقرار الشبكة (%)', '🔌', 100, 0, 100, 1)
    consumption_slider, consumption_box, consumption_row = create_linked_control('عداد تراكمي (ك.و.س)', '📉', 350, 0, 1000, 10)
    demand_slider, demand_box, demand_row = create_linked_control('حمل المنزل (%)', '🏠', 60, 0, 100, 1)

    # تجميع صفوف المدخلات في حاوية عمودية منظمة ذات ستايل داكن فخم
    inputs_vbox = widgets.VBox([
        solar_row,
        soc_row,
        grid_row,
        consumption_row,
        demand_row
    ], layout=widgets.Layout(padding='10px', background_color='#1a1a1a', border='1px dashed #444', margin='5px 0px'))

    # وضع المدخلات داخل لوحة أكورديون قابلة للطي لإعطاء طابع برمجي ذكي ونظيف
    accordion = widgets.Accordion(children=[inputs_vbox], selected_index=0)
    accordion.set_title(0, '📥 لوحة التحكم وتعديل المعطيات الحالية المنظومية')
    accordion.layout.margin = '10px 0px'

    # إنشاء زر التشغيل والمحاكاة بتصميم عصري عريض وجذاب باللون الأخضر الفوسفوري
    run_button = widgets.Button(
        description='🚀 تشغيل محاكاة نظام SEMTOS الذكي',
        disabled=False,
        button_style='',
        tooltip='اضغط هنا لمعالجة القواعد وحساب المخرجات الضبابية ديناميكياً',
        icon='cogs'
    )
    run_button.layout.width = '100%'
    run_button.layout.height = '45px'
    run_button.layout.margin = '15px 0px'
    run_button.style.button_color = '#00ff66'
    run_button.style.font_weight = 'bold'

    # صندوق مخصص ومستقل تماماً لعرض المخرجات والرسومات البيانية دون تشويه خلية العمل
    output_container = widgets.Output()

    # دالة معالجة الحدث اللحظي عند الضغط على الزر لتمرير القيم إلى محرك الاستدلال
    def on_button_clicked(b):
        with output_container:
            # تنظيف المخرجات السابقة فوراً لتحديث اللوحة في نفس المكان
            clear_output(wait=True)

            # استدعاء دالة الحساب والرسم المحدثة لـ 3 مخرجات
            run_simulation_func(
                energy_sim=energy_sim,
                solar_production=solar_slider.value,
                battery_soc=soc_slider.value,
                grid_status=grid_status_slider.value,
                cum_consumption=consumption_slider.value,
                current_demand=demand_slider.value,
                grid_dependency=grid_dependency,
                battery_dependency=battery_dependency,  # التمرير بالاسم الجديد الصحيح
                load_control=load_control,
                scenario_title=f"User_Interactive_S{solar_slider.value}_B{soc_slider.value}"
            )

    # ربط حدث الضغط على الزر بالدالة التنفيذية
    run_button.on_click(on_button_clicked)

    # تجميع الواجهة بالكامل داخل تصميم مرئي متناسق ومحمي بهوامش مناسبة
    ui_header = widgets.HTML("""
        <div style="font-family: 'Segoe UI', sans-serif; background-color: #111; padding: 15px; border-radius: 8px; border-left: 5px solid #ffaa00; margin-bottom: 10px;">
            <h2 style='color: #ffaa00; margin: 0px; font-size: 22px;'>🎮 لوحة التحكم التفاعلية بنظام SEMTOS الفازي</h2>
            <p style='color: #cccccc; margin: 5px 0px 0px 0px; font-size: 13px;'>مشروع التخرج والتقييم الأكاديمي لأنظمة الذكاء الاصطناعي والخبير الضبابي المحسن.</p>
        </div>
    """)

    main_interface_layout = widgets.VBox([
        ui_header,
        accordion,
        run_button,
        output_container
    ], layout=widgets.Layout(max_width='900px', margin='0 auto', padding='10px'))

    # عرض لوحة التحكم المتكاملة للمستخدم داخل الخلية
    display(main_interface_layout)

    # تشغيل الحسابات تلقائياً للمرة الأولى لعرض الرسوم الافتراضية فوراً عند ظهور الواجهة
    on_button_clicked(None)