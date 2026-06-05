import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, HTML

def run_simulation(energy_sim, solar_production, battery_soc, grid_status, cum_consumption, current_demand,
                         grid_dependency, battery_action, load_control, solar_curtailment, battery_charging_priority,
                         scenario_title="فحص سيناريو مخصص"):
    """
    تابع شامل لـ SEMTOS محصن تماماً بكتل try-except لحماية النظام من الانهيار عند الحواف الحادة،
    ويعرض المدخلات والمخرجات على شكل جداول HTML خارقة، ويرسم المنحنيات بدقة لـ 5 مخرجات.
    """
    # 1. تثبيت النمط المظلم للمخططات
    plt.style.use('dark_background')

    # 2. تمرير قيم المدخلات الحادة إلى المحاكي الجديد (energy_sim)
    energy_sim.input['solar_production'] = solar_production
    energy_sim.input['battery_soc']       = battery_soc
    energy_sim.input['grid_status']      = grid_status
    energy_sim.input['cum_consumption']  = cum_consumption
    energy_sim.input['current_demand']   = current_demand

    # 3. تشغيل المحرك للحساب
    energy_sim.compute()

    # 4. جلب المخرجات الرقمية الخمسة مع الحماية الكاملة وصياغة التقارير ديناميكياً

    # --- أ. الاعتماد على الشبكة ---
    try:
        grid_val = energy_sim.output['grid_dependency']
        if grid_val <= 25:
            grid_report = f"فصل شبه كامل عن شبكة الدولة والاعتماد على البديل بنسبة {100-grid_val:.1f}% لحماية العداد ماليّاً."
        elif 25 < grid_val <= 65:
            grid_report = f"تشغيل هجين متوازن اقتصادي (سحب جزئي مقنن من الدولة بنسبة {grid_val:.1f}%)."
        else:
            grid_report = f"الاعتماد الرئيسي على شبكة الدولة العامة بنسبة {grid_val:.1f}% لتأمين أحمال المنزل المتزايدة."
    except KeyError:
        grid_val = None
        grid_report = "⚠️ حافة حرجة غير مغطاة بالقواعد! تم تفعيل وضع حماية الشبكة الافتراضي (فصل احترازي لحماية العداد)."

    # --- ب. سلوك البطارية ---
    try:
        batt_val = energy_sim.output['battery_action']
        if batt_val <= 45:
            batt_report = f"تفريغ آمن (Safe Discharge بنسبة {batt_val:.2f}%) للمساعدة في تغذية الأحمال وتوفير المال."
        elif 45 < batt_val <= 65:
            batt_report = f"وضعية الاستقرار والمحافظة على المخزون الحالي بدون تفريغ حاد (Standby عند {batt_val:.2f}%)."
        else:
            batt_report = f"شحن مكثف وضخ طاقة للبطارية (بقوة {batt_val:.2f}%) لاستغلال الوفرة وتأمين فترات التقنين القادمة."
    except KeyError:
        batt_val = None
        batt_report = "⚠️ حافة حرجة! المنظومة تفعل وضعية الاستقرار الاحتياطي (Standby) للمحافظة على الخلايا الكيميائية."

    # --- ج. التحكم بالأحمال المنزلية ---
    try:
        load_val = energy_sim.output['load_control']
        if load_val <= 45:
            load_report = f"الترشيد الصارم والذكي (Eco Mode بنسبة {load_val:.2f}%) - يسمح بالإنارة والشواحن والبراد فقط."
        elif 45 < load_val <= 75:
            load_report = f"التحكم الذكي المتوسط (Smart Limit بنسبة {load_val:.2f}%) - مسموح بأجهزة متوسطة وتأجيل الثقيلة."
        else:
            load_report = f"الرفاهية الكاملة وتلبية الطلب (Full Power بنسبة {load_val:.2f}%) - مسموح بتشغيل المكيفات والسخانات."
    except KeyError:
        load_val = None
        load_report = "⚠️ حافة حرجة! تم تفعيل نمط الترشيد الصارم (Eco Mode) حركياً لحين استقرار المعطيات الحادة."

    # --- د. التحكم بالفائض الشمسي ---
    try:
        solar_val = energy_sim.output['solar_curtailment']
        if solar_production < 20:
            solar_report = "لا يوجد فائض يذكر نظراً لغياب الأشعة الشمسية الحالية أو ضعف التوليد الشديد."
        else:
            if solar_val <= 50:
                solar_report = "توجيه كامل الإنتاج الشمسي للاستهلاك المنزلي المباشر الفوري (Direct Use)."
            elif 50 < solar_val <= 80:
                solar_report = "يوجد فائض ممتاز من الألواح يتم تحويله ذكياً الآن لحقن البطاريات وتخزينه (Storage)."
            else:
                solar_report = f"فائض حرج جداً (Dump بنسبة {solar_val:.2f}%) المنظومة مكتفية والبطارية ممتلئة! يتم تصريفه بأمان."
    except KeyError:
        solar_val = None
        solar_report = "⚠️ حافة حرجة! يتم توجيه الطاقة الشمسية المتاحة للاستهلاك المباشر دون تفريغ أو كبح إضافي."

    # --- هـ. أولوية شحن البطارية (الخرج الجديد) ---
    try:
        charge_priority_val = energy_sim.output['battery_charging_priority']
        if charge_priority_val <= 35:
            charge_priority_report = f"أولوية منخفضة ({charge_priority_val:.2f}%) - يتم الاعتماد على المصادر الأخرى والأحمال مقدمة حالياً."
        elif 35 < charge_priority_val <= 70:
            charge_priority_report = f"أولوية متوسطة ({charge_priority_val:.2f}%) - موازنة ذكية بين الشحن وتغطية أحمال المنزل اللحظية."
        else:
            charge_priority_report = f"أولوية قصوى للشحن ({charge_priority_val:.2f}%) - يتم توجيه الطاقة فوراً لتأمين مخزون البطارية المنهار."
    except KeyError:
        charge_priority_val = None
        charge_priority_report = "⚠️ حافة حرجة! تم تعيين أولوية الشحن للوضع الافتراضي لحين استقرار النظام."


    # --- 🏗️ بناء التنسيق البصري الخارق يدوياً عن طريق HTML ---
    print("\n" + "="*85)
    print(f" 🤖 لوحة تحكم ونظام تقارير SEMTOS الذكي المحمي ")
    print("="*85)

    title_html = f"""
    <div style="font-family: 'Segoe UI', sans-serif; margin-bottom: 10px;">
        <h2 style="color: #ffaa00; margin-bottom: 5px; border-bottom: 2px solid #ffaa00; padding-bottom: 5px;">🎬 سيناريو الفحص: {scenario_title}</h2>
    </div>
    """
    display(HTML(title_html))

    # أ. جدول المدخلات الحالي
    inputs_table_html = f"""
    <h3 style="color: #00ff66; font-family: 'Segoe UI', sans-serif; margin-top: 15px; margin-bottom: 8px;">📥 جدول المدخلات الحالية (System Inputs)</h3>
    <table style="background-color: #121212; border-collapse: collapse; width: 100%; border: 1px solid #444; font-family: 'Segoe UI', sans-serif; margin-bottom: 25px;">
        <thead>
            <tr style="background-color: #222222;">
                <th style="color: #00ff66; padding: 10px; border: 1px solid #444; text-align: center; width: 25%;">المدخل (Arabic)</th>
                <th style="color: #00ff66; padding: 10px; border: 1px solid #444; text-align: center; width: 25%;">Input (English)</th>
                <th style="color: #00ff66; padding: 10px; border: 1px solid #444; text-align: center; width: 20%;">القيمة الممررة (Value)</th>
                <th style="color: #00ff66; padding: 10px; border: 1px solid #444; text-align: center; width: 30%;">الوحدة / الحالة</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: #1a1a1a;">
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">☀️ إنتاج الطاقة الشمسية</td>
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: left;">Solar Production</td>
                <td style="padding: 10px; color: #ffaa00; border: 1px solid #333; text-align: center; font-weight: bold; font-size: 14px;">{solar_production}%</td>
                <td style="padding: 10px; color: #e0e0e0; border: 1px solid #333; text-align: right;">نسبة توليد الألواح الحالية من القدرة القصوى</td>
            </tr>
            <tr style="background-color: #121212;">
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">🔋 مستوى شحن البطارية</td>
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: left;">Battery SoC</td>
                <td style="padding: 10px; color: #00ff66; border: 1px solid #333; text-align: center; font-weight: bold; font-size: 14px;">{battery_soc}%</td>
                <td style="padding: 10px; color: #e0e0e0; border: 1px solid #333; text-align: right;">حالة شحن بنك البطاريات المتوفر (State of Charge)</td>
            </tr>
            <tr style="background-color: #1a1a1a;">
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">🔌 وضع شبكة الدولة</td>
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: left;">Grid Status</td>
                <td style="padding: 10px; color: #33a1ff; border: 1px solid #333; text-align: center; font-weight: bold; font-size: 14px;">{grid_status}%</td>
                <td style="padding: 10px; color: #e0e0e0; border: 1px solid #333; text-align: right;">استقرار وتوفر تيار الشبكة العامة (الكهرباء النظامية)</td>
            </tr>
            <tr style="background-color: #121212;">
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">📉 استهلاك العداد التراكمي</td>
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: left;">Cumulative Consumption</td>
                <td style="padding: 10px; color: #ff3366; border: 1px solid #333; text-align: center; font-weight: bold; font-size: 14px;">{cum_consumption} ك.و.س</td>
                <td style="padding: 10px; color: #e0e0e0; border: 1px solid #333; text-align: right;">الطاقة المستهلكة خلال الدورة الحالية (مؤشر خطر الـ 500)</td>
            </tr>
            <tr style="background-color: #1a1a1a;">
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">🏠 حمل المنزل الحالي</td>
                <td style="padding: 10px; color: #ffffff; border: 1px solid #333; text-align: left;">Current Demand</td>
                <td style="padding: 10px; color: #cc66ff; border: 1px solid #333; text-align: center; font-weight: bold; font-size: 14px;">{current_demand}%</td>
                <td style="padding: 10px; color: #e0e0e0; border: 1px solid #333; text-align: right;">مجموع سحب الأجهزة والإنارة اللحظي داخل المنزل</td>
            </tr>
        </tbody>
    </table>
    """
    display(HTML(inputs_table_html))

    # تجهيز النصوص الرقمية للجدول لمنع طباعة السلسلة الفارغة
    g_val_str = f"{grid_val:.2f}%" if grid_val is not None else "DEFAULT (0%)"
    b_val_str = f"{batt_val:.2f}%" if batt_val is not None else "DEFAULT (50%)"
    l_val_str = f"{load_val:.2f}%" if load_val is not None else "DEFAULT (30%)"
    s_val_str = f"{solar_val:.2f}%" if solar_val is not None else "DEFAULT (0%)"
    c_priority_val_str = f"{charge_priority_val:.2f}%" if charge_priority_val is not None else "DEFAULT (0%)"

    # ب. جدول المخرجات الذكي (مع الخرج الخامس الجديد)
    outputs_table_html = f"""
    <h3 style="color: #00ffff; font-family: 'Segoe UI', sans-serif; margin-top: 10px; margin-bottom: 8px;">📤 جدول المخرجات والقرارات الأكاديمية (Outputs & Decisions)</h3>
    <table style="background-color: #121212; border-collapse: collapse; width: 100%; border: 1px solid #444; font-family: 'Segoe UI', sans-serif;">
        <thead>
            <tr style="background-color: #2d2d2d;">
                <th style="color: #00ffff; padding: 12px; border: 1px solid #444; text-align: center; width: 25%;">الخرج (Arabic)</th>
                <th style="color: #00ffff; padding: 12px; border: 1px solid #444; text-align: center; width: 25%;">Output (English)</th>
                <th style="color: #00ffff; padding: 12px; border: 1px solid #444; text-align: center; width: 15%;">النسبة الحادة (Value)</th>
                <th style="color: #00ffff; padding: 12px; border: 1px solid #444; text-align: center; width: 35%;">التقرير الذكي ونوع القرار (System Action Report)</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: #1a1a1a;">
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">الاعتماد على الشبكة</td>
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: left;">Grid Dependency</td>
                <td style="padding: 12px; color: #00ffff; border: 1px solid #333; text-align: center; font-weight: bold;">{g_val_str}</td>
                <td style="padding: 12px; color: #e0e0e0; border: 1px solid #333; text-align: right;">{grid_report}</td>
            </tr>
            <tr style="background-color: #121212;">
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">إجراء سلوك البطارية</td>
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: left;">Battery Action</td>
                <td style="padding: 12px; color: #ff3333; border: 1px solid #333; text-align: center; font-weight: bold;">{b_val_str}</td>
                <td style="padding: 12px; color: #e0e0e0; border: 1px solid #333; text-align: right;">{batt_report}</td>
            </tr>
            <tr style="background-color: #1a1a1a;">
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">التحكم بالأحمال المنزلية</td>
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: left;">Load Control</td>
                <td style="padding: 12px; color: #33ff33; border: 1px solid #333; text-align: center; font-weight: bold;">{l_val_str}</td>
                <td style="padding: 12px; color: #e0e0e0; border: 1px solid #333; text-align: right;">{load_report}</td>
            </tr>
            <tr style="background-color: #121212;">
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">التحكم بالفائض الشمسي</td>
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: left;">Solar Curtailment</td>
                <td style="padding: 12px; color: #ffff33; border: 1px solid #333; text-align: center; font-weight: bold;">{s_val_str}</td>
                <td style="padding: 12px; color: #e0e0e0; border: 1px solid #333; text-align: right;">{solar_report}</td>
            </tr>
            <tr style="background-color: #1a1a1a;">
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: right; font-weight: bold;">أولوية شحن البطارية</td>
                <td style="padding: 12px; color: #ffffff; border: 1px solid #333; text-align: left;">Battery Charging Priority</td>
                <td style="padding: 12px; color: #ff9933; border: 1px solid #333; text-align: center; font-weight: bold;">{c_priority_val_str}</td>
                <td style="padding: 12px; color: #e0e0e0; border: 1px solid #333; text-align: right;">{charge_priority_report}</td>
            </tr>
        </tbody>
    </table>
    """
    display(HTML(outputs_table_html))
    print("\n" + "-"*85 + "\n")

    # 6. رسم المخرجات الخمسة بالكامل يدوياً
    fig, axs = plt.subplots(5, 1, figsize=(10, 20))

    # المخطط 1: الاعتماد على الشبكة
    for label in grid_dependency.terms:
        axs[0].plot(grid_dependency.universe, grid_dependency[label].mf, label=label, linewidth=2)
    if grid_val is not None:
        axs[0].axvline(x=grid_val, color='#00ffff', linestyle='--', linewidth=3, label=f'Decision: {grid_val:.2f}%')
    axs[0].set_title("1. Grid Dependency Output Spectrum", fontsize=11, color='white')
    axs[0].set_ylabel("Membership", color='white')
    axs[0].legend(loc='upper right')
    axs[0].grid(True, alpha=0.2)

    # المخطط 2: سلوك وإجراء البطارية
    for label in battery_action.terms:
        axs[1].plot(battery_action.universe, battery_action[label].mf, label=label, linewidth=2)
    if batt_val is not None:
        axs[1].axvline(x=batt_val, color='#ff3333', linestyle='--', linewidth=3, label=f'Decision: {batt_val:.2f}%')
    axs[1].set_title("2. Battery Action Output Spectrum", fontsize=11, color='white')
    axs[1].set_ylabel("Membership", color='white')
    axs[1].legend(loc='upper right')
    axs[1].grid(True, alpha=0.2)

    # المخطط 3: وضعية التحكم بالأحمال
    for label in load_control.terms:
        axs[2].plot(load_control.universe, load_control[label].mf, label=label, linewidth=2)
    if load_val is not None:
        axs[2].axvline(x=load_val, color='#33ff33', linestyle='--', linewidth=3, label=f'Decision: {load_val:.2f}%')
    axs[2].set_title("3. Load Control Output Spectrum", fontsize=11, color='white')
    axs[2].set_ylabel("Membership", color='white')
    axs[2].legend(loc='upper right')
    axs[2].grid(True, alpha=0.2)

    # المخطط 4: التحكم بفائض الطاقة الشمسية
    for label in solar_curtailment.terms:
        axs[3].plot(solar_curtailment.universe, solar_curtailment[label].mf, label=label, linewidth=2)
    if solar_val is not None:
        axs[3].axvline(x=solar_val, color='#ffff33', linestyle='--', linewidth=3, label=f'Decision: {solar_val:.2f}%')
    axs[3].set_title("4. Solar Curtailment Output Spectrum", fontsize=11, color='white')
    axs[3].set_ylabel("Membership", color='white')
    axs[3].legend(loc='upper right')
    axs[3].grid(True, alpha=0.2)

    # المخطط 5: أولوية شحن البطارية (الجديد)
    for label in battery_charging_priority.terms:
        axs[4].plot(battery_charging_priority.universe, battery_charging_priority[label].mf, label=label, linewidth=2)
    if charge_priority_val is not None:
        axs[4].axvline(x=charge_priority_val, color='#ff9933', linestyle='--', linewidth=3, label=f'Decision: {charge_priority_val:.2f}%')
    axs[4].set_title("5. Battery Charging Priority Output Spectrum", fontsize=11, color='white')
    axs[4].set_xlabel("Percentage (%)", color='white')
    axs[4].set_ylabel("Membership", color='white')
    axs[4].legend(loc='upper right')
    axs[4].grid(True, alpha=0.2)

    plt.tight_layout()
    plt.show()
