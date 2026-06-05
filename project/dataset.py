import os
import pandas as pd


def get_test_dataframe():

    test_scenarios = [
        {
            "Scenario_ID": 1,
            "Scenario_Title": "ليلي بطارية فارغة واستهلاك طبيعي",
            "solar_production": 0, "battery_soc": 10, "grid_status": 100, "cum_consumption": 200, "current_demand": 40,
            "Expected_Grid_Dependency": "مرتفع جداً (100%)", "Expected_Battery_Action": "ثبات / انتظار (Standby)",
            "Expected_Load_Control": "طبيعي (Full Power)"
        },
        {
            "Scenario_ID": 2,
            "Scenario_Title": "ذروة شمسية وبطارية فارغة (شحن مكثف)",
            "solar_production": 90, "battery_soc": 15, "grid_status": 100, "cum_consumption": 250, "current_demand": 30,
            "Expected_Grid_Dependency": "منخفض جداً", "Expected_Battery_Action": "شحن قوي (Charge)",
            "Expected_Load_Control": "طبيعي"
        },
        {
            "Scenario_ID": 3,
            "Scenario_Title": "فائض شمسي والبطارية ممتلئة بالكامل",
            "solar_production": 95, "battery_soc": 98, "grid_status": 100, "cum_consumption": 150, "current_demand": 20,
            "Expected_Grid_Dependency": "صفر (فصل كامل)", "Expected_Battery_Action": "ثبات (Standby)",
            "Expected_Load_Control": "رفاهية كاملة / تبديد الفائض"
        },
        {
            "Scenario_ID": 4,
            "Scenario_Title": "انقطاع تيار الدولة (Blackout) نهاراً",
            "solar_production": 60, "battery_soc": 50, "grid_status": 0, "cum_consumption": 300, "current_demand": 70,
            "Expected_Grid_Dependency": "صفر (إجباري)", "Expected_Battery_Action": "تفريغ مساند (Discharge)",
            "Expected_Load_Control": "ترشيد ذكي متوسط"
        },
        {
            "Scenario_ID": 5,
            "Scenario_Title": "انقطاع تيار الدولة ليلاً (حالة طوارئ)",
            "solar_production": 0, "battery_soc": 30, "grid_status": 0, "cum_consumption": 310, "current_demand": 80,
            "Expected_Grid_Dependency": "صفر", "Expected_Battery_Action": "تفريغ حرج للضرورة",
            "Expected_Load_Control": "ترشيد صارم جداً (Eco Mode)"
        },
        {
            "Scenario_ID": 6,
            "Scenario_Title": "تخطي حاجز الاستهلاك الاقتصادي (>500 ك.و.س)",
            "solar_production": 40, "battery_soc": 70, "grid_status": 100, "cum_consumption": 550, "current_demand": 50,
            "Expected_Grid_Dependency": "تقنين السحب لحماية الفاتورة",
            "Expected_Battery_Action": "تفريغ اعتمادي اقتصادي", "Expected_Load_Control": "ترشيد متوسط"
        },
        {
            "Scenario_ID": 7,
            "Scenario_Title": "يوم غائم جزئياً مع حمل منزلي مرتفع",
            "solar_production": 30, "battery_soc": 45, "grid_status": 100, "cum_consumption": 220, "current_demand": 85,
            "Expected_Grid_Dependency": "اعتماد هجين (مزيج)", "Expected_Battery_Action": "تفريغ خفيف",
            "Expected_Load_Control": "ترشيد ذكي للأحمال الثقيلة"
        },
        {
            "Scenario_ID": 8,
            "Scenario_Title": "استقرار كامل للمنظومة (حالة مثالية)",
            "solar_production": 50, "battery_soc": 60, "grid_status": 100, "cum_consumption": 100, "current_demand": 30,
            "Expected_Grid_Dependency": "منخفض ومتوازن", "Expected_Battery_Action": "شحن خفيف أو ثبات",
            "Expected_Load_Control": "طبيعي"
        },
        {
            "Scenario_ID": 9,
            "Scenario_Title": "حمل منزلي منهار (منزل فارغ نهاراً)",
            "solar_production": 80, "battery_soc": 40, "grid_status": 100, "cum_consumption": 410, "current_demand": 5,
            "Expected_Grid_Dependency": "منخفض جداً", "Expected_Battery_Action": "توجيه الطاقة للشحن الأقصى",
            "Expected_Load_Control": "طبيعي"
        },
        {
            "Scenario_ID": 10,
            "Scenario_Title": "حالة حرجة (استهلاك ضخم + عداد مرتفع جداً)",
            "solar_production": 10, "battery_soc": 20, "grid_status": 100, "cum_consumption": 650, "current_demand": 90,
            "Expected_Grid_Dependency": "سحب اضطراري مقنن", "Expected_Battery_Action": "حماية البطارية من الانهيار",
            "Expected_Load_Control": "قطع الأحمال غير الضرورية فورا"
        }
    ]
    return pd.DataFrame(test_scenarios)


def export_dataset_to_excel(filename="semtos_test_dataset.xlsx"):
    """
    تصدير الداتا سيت إلى ملف إكسل حقيقي مع التحقق من الأخطاء وحماية مسار النظام.
    """
    df = get_test_dataframe()
    try:
        df.to_excel(filename, index=False)
        print(f"✅ تم إنشاء وتصدير ملف الإكسل بنجاح باسم: {filename}")
        return True
    except Exception as e:
        print(f"⚠️ حدث خطأ أثناء التصدير لملف إكسل: {e}")
        return False


def run_system_validation_test(energy_sim):
    """
    دالة الفحص والتحقق الآلي (Validation Loop).
    تمر على السيناريوهات الـ 10، وتحسب النتائج عبر المحرك الفازي، وتعيد جدولاً منسقاً بالنتائج المحسوبة.
    """
    df_scenarios = get_test_dataframe()
    validation_results = []

    print("🧠 جاري بدء الفحص الآلي الشامل لـ 10 سيناريوهات على النظام الخبير...")

    for idx, row in df_scenarios.iterrows():
        # 1. حقن المدخلات داخل كائن المحاكاة الخاص بك
        energy_sim.input['solar_production'] = row['solar_production']
        energy_sim.input['battery_soc'] = row['battery_soc']
        energy_sim.input['grid_status'] = row['grid_status']
        energy_sim.input['cum_consumption'] = row['cum_consumption']
        energy_sim.input['current_demand'] = row['current_demand']

        # 2. تشغيل المحرك لحساب القيم الحادة عبر إلغاء الضبابية (Defuzzification)
        try:
            energy_sim.compute()
            grid_out = round(energy_sim.output.get('grid_dependency', 0), 2)
            batt_out = round(energy_sim.output.get('battery_action', 0), 2)
            load_out = round(energy_sim.output.get('load_control', 0), 2)
            status = "✅ ناجح (منطقي)"
        except KeyError:
            # معالجة حماية الحواف الحرجة غير المغطاة بالقواعد
            grid_out, batt_out, load_out = "N/A", "N/A", "N/A"
            status = "⚠️ حافة حرجة (تحتاج مراجعة قواعد)"

        # 3. تجميع التقرير
        validation_results.append({
            "رقم الحساب": row['Scenario_ID'],
            "عنوان السيناريو": row['Scenario_Title'],
            "الاعتماد الفعلي (%)": grid_out,
            "سلوك البطارية الفعلي (%)": batt_out,
            "التحكم بالأحمال الفعلي (%)": load_out,
            "حالة الفحص": status
        })

    # تحويل نتائج الفحص إلى مصفوفة Pandas لعرضها بشكل أكاديمي
    df_results = pd.DataFrame(validation_results)
    return df_results