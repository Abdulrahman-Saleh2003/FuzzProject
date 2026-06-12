import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, HTML

import os

import matplotlib.pyplot as plt
import warnings
from bidi.algorithm import get_display
import arabic_reshaper
from IPython.display import display, HTML

# دالة مساولة لمعالجة وتصحيح الكلمات العربية داخل الجداول والمخططات
def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text



def run_simulation(energy_sim, solar_production, battery_soc, grid_status, cum_consumption, current_demand,
                   grid_dependency, battery_dependency, load_control, scenario_title="فحص سيناريو مخصص"):
    """
    تابع شامل ومحصن تماماً بكتل try-except لحماية النظام من الانهيار عند الحواف الحادة،
    ويعرض المدخلات والمخرجات على شكل جداول HTML مدمجة وأنيقة، ويرسم المنحنيات بجانب بعضها للمخرجات الثلاثة.
    """
    # إخفاء التنبيهات التجميلية
    warnings.filterwarnings("ignore", category=UserWarning)

    # تثبيت النمط المظلم الاحترافي للمخططات البيانية
    plt.style.use('dark_background')

    # تمرير قيم المدخلات الحادة إلى المحاكي الجديد (energy_sim)
    energy_sim.input['solar_production'] = solar_production
    energy_sim.input['battery_soc'] = battery_soc
    energy_sim.input['grid_status'] = grid_status
    energy_sim.input['cum_consumption'] = cum_consumption
    energy_sim.input['house_demand'] = current_demand

    # تشغيل المحرك للحساب واستخلاص النتائج ضبابياً
    energy_sim.compute()

    # --- أ. الاعتماد على الشبكة الحكومية ---
    try:
        grid_val = energy_sim.output['grid_dependency']
        if grid_val <= 25:
            grid_report = f"فصل شبه كامل عن شبكة الدولة والاعتماد على البديل بنسبة {100 - grid_val:.1f}% لحماية العداد ماليّاً."
        elif 25 < grid_val <= 65:
            grid_report = f"تشغيل هجين متوازن اقتصادي (سحب جزئي مقنن من الدولة بنسبة {grid_val:.1f}%)."
        else:
            grid_report = f"الاعتماد الرئيسي على شبكة الدولة العامة بنسبة {grid_val:.1f}% لتأمين أحمال المنزل المتزايدة."
    except KeyError:
        grid_val = None
        grid_report = "⚠️ حافة حرجة غير مغطاة بالقواعد! تم تفعيل وضع حماية الشبكة الافتراضي."

    # --- ب. سلوك الاعتماد على البطارية ---
    try:
        batt_val = energy_sim.output['battery_dependency']
        if batt_val <= 25:
            batt_report = f"تفريغ أدنى لحماية خلايا البطارية أو الاعتماد الكامل على مصادر التغذية الأخرى المتوفرة."
        elif 25 < batt_val <= 65:
            batt_report = f"تفريغ آمن ومتوازن بنسبة {batt_val:.2f}% للمساعدة في تلبية الأحمال دون التسبب بإجهاد كيميائي."
        else:
            batt_report = f"اعتماد عالي وقصوى على تفريغ البطارية بنسبة {batt_val:.2f}% لتغطية انقطاع الطاقة وحظر السحب المالي."
    except KeyError:
        batt_val = None
        batt_report = "⚠️ حافة حرجة! المنظومة تفعل وضعية الاستقرار الاحتياطي (Standby) للمحافظة على الخلايا الكيميائية."

    # --- ج. التحكم بالأحمال المنزلية المسموحة ---
    try:
        load_val = energy_sim.output['load_control']
        if load_val <= 45:
            load_report = f"الترشيد الصارم والذكي (Eco Mode بنسبة {load_val:.2f}%) - يسمح بالإنارة والشواحن والبراد فقط."
        elif 45 < load_val <= 75:
            load_report = f"التحكم الذكي المتوسط (Smart Limit بنسبة {load_val:.2f}%) - مسموح بأجهزة متوسطة وتأجيل الثقيلة."
        else:
            load_report = f"الRefahiah الكاملة وتلبية الطلب (Full Power بنسبة {load_val:.2f}%) - مسموح بتشغيل المكيفات والسخانات."
    except KeyError:
        load_val = None
        load_report = "⚠️ حافة حرجة! تم تفعيل نمط الترشيد الصارم (Eco Mode) حركياً لحين استقرار المعطيات الحادة."

    # --- 🏗️ بناء التنسيق البصري يدوياً عن طريق لوحة HTML مخصصة ---
    header_html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e1e2f 0%, #111119 100%);
                border-left: 5px solid #00ffaa;
                padding: 15px 20px;
                margin: 20px auto;
                border-radius: 6px;
                max-width: 80%;
                box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
        <div style="font-size: 11px; color: #00ffaa; letter-spacing: 2px; font-weight: bold; text-transform: uppercase;">
            Fuzzy Logic Inference System Backend
        </div>
        <h2 style="color: #ffffff; margin: 5px 0; font-size: 20px; font-weight: 600; letter-spacing: 0.5px;">
            SEMTOS: Intelligent Energy Management & Diagnostics Control System
        </h2>
        <div style="color: #a0a0b0; font-size: 13px; margin-top: 8px;">
            <strong style="color: #ffaa00;">Active Test Scenario:</strong> {scenario_title}
        </div>
    </div>
    """
    display(HTML(header_html))

    # أ. جدول المدخلات الحالي (عرض 80%)
    inputs_table_html = f"""
    <div style="max-width: 80%; margin: 0 auto 20px auto; font-family: 'Segoe UI', sans-serif;">
        <h4 style="color: #00ff66; margin-bottom: 6px; font-size: 13px; letter-spacing: 0.5px;">📥 SYSTEM INPUT PARAMETERS (CRISP METRICS)</h4>
        <table style="background-color: #121212; border-collapse: collapse; width: 100%; border: 1px solid #333; font-size: 12px;">
            <thead>
                <tr style="background-color: #1a1a24; border-bottom: 2px solid #333;">
                    <th style="color: #00ff66; padding: 6px 10px; text-align: right; width: 25%;">المدخل لغوياً</th>
                    <th style="color: #00ff66; padding: 6px 10px; text-align: left; width: 25%;">Fuzzy Input Variable</th>
                    <th style="color: #00ff66; padding: 6px 10px; text-align: center; width: 15%;">Value</th>
                    <th style="color: #00ff66; padding: 6px 10px; text-align: right; width: 35%;">Operational Status / Context</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: #161616; border-bottom: 1px solid #222;">
                    <td style="padding: 6px 10px; color: #ffffff; text-align: right; font-weight: 500;">☀️ إنتاج الطاقة الشمسية</td>
                    <td style="padding: 6px 10px; color: #aaa; text-align: left;">Solar Production</td>
                    <td style="padding: 6px 10px; color: #ffaa00; text-align: center; font-weight: bold;">{solar_production}%</td>
                    <td style="padding: 6px 10px; color: #888; text-align: right;">نسبة توليد الألواح الحالية من القدرة القصوى</td>
                </tr>
                <tr style="background-color: #121212; border-bottom: 1px solid #222;">
                    <td style="padding: 6px 10px; color: #ffffff; text-align: right; font-weight: 500;">🔋 مستوى شحن البطارية</td>
                    <td style="padding: 6px 10px; color: #00ff66; text-align: center; font-weight: bold;">{battery_soc}%</td>
                    <td style="padding: 6px 10px; color: #aaa; text-align: left;">Battery SoC</td>
                    <td style="padding: 6px 10px; color: #888; text-align: right;">حالة شحن بنك البطاريات المتوفر (State of Charge)</td>
                </tr>
                <tr style="background-color: #161616; border-bottom: 1px solid #222;">
                    <td style="padding: 6px 10px; color: #ffffff; text-align: right; font-weight: 500;">🔌 وضع شبكة الدولة</td>
                    <td style="padding: 6px 10px; color: #aaa; text-align: left;">Grid Status</td>
                    <td style="padding: 6px 10px; color: #33a1ff; text-align: center; font-weight: bold;">{grid_status}%</td>
                    <td style="padding: 6px 10px; color: #888; text-align: right;">استقرار وتوفر تيار الشبكة العامة (الكهرباء النظامية)</td>
                </tr>
                <tr style="background-color: #121212; border-bottom: 1px solid #222;">
                    <td style="padding: 6px 10px; color: #ffffff; text-align: right; font-weight: 500;">📉 استهلاك العداد التراكمي</td>
                    <td style="padding: 6px 10px; color: #aaa; text-align: left;">Cumulative Consumption</td>
                    <td style="padding: 6px 10px; color: #ff3366; text-align: center; font-weight: bold;">{cum_consumption} kWh</td>
                    <td style="padding: 6px 10px; color: #888; text-align: right;">الطاقة المستهلكة خلال الدورة الحالية (مؤشر خطر الـ 500)</td>
                </tr>
                <tr style="background-color: #161616;">
                    <td style="padding: 6px 10px; color: #ffffff; text-align: right; font-weight: 500;">🏠 حمل المنزل الحالي</td>
                    <td style="padding: 6px 10px; color: #aaa; text-align: left;">Current Demand</td>
                    <td style="padding: 6px 10px; color: #cc66ff; text-align: center; font-weight: bold;">{current_demand}%</td>
                    <td style="padding: 6px 10px; color: #888; text-align: right;">مجموع سحب الأجهزة والإنارة اللحظي داخل المنزل</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    display(HTML(inputs_table_html))

    # تجهيز النصوص الرقمية للجدول لمنع طباعة السلسلة الفارغة
    g_val_str = f"{grid_val:.2f}%" if grid_val is not None else "DEFAULT (0%)"
    b_val_str = f"{batt_val:.2f}%" if batt_val is not None else "DEFAULT (0%)"
    l_val_str = f"{load_val:.2f}%" if load_val is not None else "DEFAULT (0%)"

    # ب. جدول المخرجات الثلاثة الذكي
    outputs_table_html = f"""
    <div style="max-width: 80%; margin: 0 auto 25px auto; font-family: 'Segoe UI', sans-serif;">
        <h4 style="color: #00ffff; margin-bottom: 6px; font-size: 13px; letter-spacing: 0.5px;">📤 DEFUZZIFIED SYSTEM OUTPUTS & DECISION LOGIC</h4>
        <table style="background-color: #121212; border-collapse: collapse; width: 100%; border: 1px solid #444; font-size: 12px;">
            <thead>
                <tr style="background-color: #1e252b; border-bottom: 2px solid #444;">
                    <th style="color: #00ffff; padding: 7px 10px; text-align: right; width: 22%;">الخرج المتحكم به</th>
                    <th style="color: #00ffff; padding: 7px 10px; text-align: left; width: 23%;">Fuzzy Output Variable</th>
                    <th style="color: #00ffff; padding: 7px 10px; text-align: center; width: 15%;">Crisp Output</th>
                    <th style="color: #00ffff; padding: 7px 10px; text-align: right; width: 40%;">System Action Report (القرار الذكي)</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: #161616; border-bottom: 1px solid #2d2d2d;">
                    <td style="padding: 7px 10px; color: #ffffff; text-align: right; font-weight: 500;">الاعتماد على الشبكة</td>
                    <td style="padding: 7px 10px; color: #aaa; text-align: left;">Grid Dependency</td>
                    <td style="padding: 7px 10px; color: #00ffff; text-align: center; font-weight: bold;">{g_val_str}</td>
                    <td style="padding: 7px 10px; color: #e0e0e0; text-align: right; font-size: 11.5px;">{grid_report}</td>
                </tr>
                <tr style="background-color: #121212; border-bottom: 1px solid #2d2d2d;">
                    <td style="padding: 7px 10px; color: #ffffff; text-align: right; font-weight: 500;">إجراء سلوك البطارية</td>
                    <td style="padding: 7px 10px; color: #aaa; text-align: left;">Battery Dependency</td>
                    <td style="padding: 7px 10px; color: #ff3333; text-align: center; font-weight: bold;">{b_val_str}</td>
                    <td style="padding: 7px 10px; color: #e0e0e0; text-align: right; font-size: 11.5px;">{batt_report}</td>
                </tr>
                <tr style="background-color: #161616;">
                    <td style="padding: 7px 10px; color: #ffffff; text-align: right; font-weight: 500;">التحكم بالأحمال المنزلية</td>
                    <td style="padding: 7px 10px; color: #aaa; text-align: left;">Load Control</td>
                    <td style="padding: 7px 10px; color: #33ff33; text-align: center; font-weight: bold;">{l_val_str}</td>
                    <td style="padding: 7px 10px; color: #e0e0e0; text-align: right; font-size: 11.5px;">{load_report}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    display(HTML(outputs_table_html))

    # --- 📊 3. رسم المخرجات الثلاثة الأساسية في سطر واحد متناسق وممتاز للتقرير ---
    outputs_list = [
        (grid_dependency, "1. Grid Dependency Spectrum", grid_val, '#00ffff'),
        (battery_dependency, "2. Battery Dependency Spectrum", batt_val, '#ff3333'),
        (load_control, "3. Load Control Spectrum", load_val, '#33ff33')
    ]

    # شكل مجمع من سطر واحد يحتوي على 3 مخططات متناسقة
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    axes = axes.flatten()

    for i, (var, title, val, color) in enumerate(outputs_list):
        ax = axes[i]

        for label in var.terms:
            ax.plot(var.universe, var[label].mf, label=label, linewidth=2)

        if val is not None:
            ax.axvline(x=val, color=color, linestyle='--', linewidth=3, label=f'Decision: {val:.2f}%')

        ax.set_title(title, fontsize=11, color='white', fontweight='bold')
        ax.set_xlim([var.universe.min(), var.universe.max()])
        ax.set_ylim([0, 1.05])
        ax.set_ylabel("Membership", color='white', fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.2)
        ax.legend(loc='upper right', fontsize=8)

    plt.tight_layout()

    # safe_title = scenario_title.replace(" ", "_").replace(":", "")

    folder_path = r"E:\PyCharmProjects\FuzzProject\project\images"

    # 2. بناء اسم الصورة الديناميكي الشامل
    image_name = f"Dashboard_S{solar_production}_B{battery_soc}.png"

    # 3. دمج المسار مع اسم الصورة الكامل
    full_save_path = os.path.join(folder_path, image_name)

    plt.tight_layout()

    # 4. تعليمة الحفظ بالمسار الكامل الجديد
    plt.savefig(full_save_path, dpi=300, bbox_inches='tight')
    plt.show()

    print(f"✔️ [SUCCESS] Combined Dashboard saved successfully to:\n--> {full_save_path}")

    # # plt.savefig('SEMTOS_Simulation_Dashboard.png', dpi=300, bbox_inches='tight')
    # plt.savefig(f"Simulation_Dashboard{ solar_production}{battery_soc}.png", dpi=300, bbox_inches='tight')
    #
    # plt.show()
    # print(f"Simulation_Dashboard{ solar_production}{battery_soc}.png")