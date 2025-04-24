# --- START OF FILE populate_all_programs_arabic.py ---

from run import app, db
from models import Program, Course, ProgramCourse
from sqlalchemy import text
import traceback

def add_program_with_courses_arabic(program_name_ar, degree_type, description_ar, courses_data_ar, program_name_en_for_code=None, program_type='Professional'):
    """
    Helper function to add a program and its courses using ARABIC names and descriptions.
    Uses an optional English name base for generating course codes if provided.
    """
    # Use Arabic name for primary lookup and storage
    program_name_main = program_name_ar
    description_main = description_ar

    # Determine the base for course code prefix generation
    code_base = program_name_en_for_code if program_name_en_for_code else program_name_ar

    # Check if program already exists using the main (Arabic) name
    program = Program.query.filter_by(name=program_name_main, degree_type=degree_type).first()

    if not program:
        # Create program if it doesn't exist
        program = Program(
            name=program_name_main, # Store Arabic name in the main 'name' field
            degree_type=degree_type,
            description=description_main, # Store Arabic description in the main 'description' field
            arabic_name=program_name_ar, # Also store in arabic_name field
            arabic_description=description_ar, # Also store in arabic_description field
            type=program_type # Set the program type
        )
        # Add program to database
        db.session.add(program)
        db.session.flush()  # Get program ID before committing
        print(f"Added program: {program_name_main} ({degree_type}) - Type: {program_type}")
    else:
        # Update existing program's type if it's not set or different
        updated = False
        if program.type != program_type:
            print(f"Updating type for existing program: {program_name_main} ({degree_type}) to {program_type}")
            program.type = program_type
            updated = True
        # Ensure Arabic fields are populated if they weren't before
        if not program.arabic_name:
            program.arabic_name = program_name_ar
            updated = True
        if not program.arabic_description:
            program.arabic_description = description_ar
            updated = True
        if updated:
            db.session.flush()


        print(f"Program {program_name_main} ({degree_type}) already exists, checking for courses...")
        # Check if program has courses
        course_count = ProgramCourse.query.filter_by(program_id=program.id).count()
        if course_count > 0:
            print(f"Program {program_name_main} ({degree_type}) already has {course_count} courses. Skipping course addition.")
            # Commit updates if made
            if updated:
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error committing updates for {program_name_main} ({degree_type}): {str(e)}")
            return program

    # Create courses using Arabic titles
    all_courses = []
    for semester, courses_ar in courses_data_ar.items():
        for i, course_title_ar in enumerate(courses_ar):
            # Generate code using the code_base (preferably English name)
            # Using first 3 chars of code_base, or full name if shorter
            program_prefix = ''.join(filter(str.isalnum, code_base)).upper()[:3]
            # Ensure prefix is not empty if code_base was weird
            if not program_prefix:
                program_prefix = "CRS" # Default prefix

            course_code = f"{program_prefix}{degree_type[0]}{semester}{i+1:02d}" # e.g., PRMD101 or إداD101

            # Check if course already exists by ARABIC title
            existing_course = Course.query.filter_by(title=course_title_ar).first()

            if existing_course:
                 if existing_course.semester != semester:
                     print(f"Warning: Course '{course_title_ar}' ({existing_course.code}) exists with different semester ({existing_course.semester}). Using existing.")
                 all_courses.append(existing_course)
                 print(f"  Using existing course: {existing_course.code} - {existing_course.title}")
            else:
                # Check if generated code conflicts, regenerate if needed
                code_exists = Course.query.filter_by(code=course_code).first()
                while code_exists:
                    print(f"  Generated code '{course_code}' conflict for '{course_title_ar}'. Regenerating...")
                    # Simple fallback: append incrementing number or letter
                    if course_code[-1].isdigit():
                       course_code = course_code[:-1] + chr(ord(course_code[-1]) + 1) # Increment last digit char
                    elif course_code[-1].isalpha():
                         course_code = course_code + "1"
                    else: # Failsafe
                        course_code += "X"
                    code_exists = Course.query.filter_by(code=course_code).first()


                course = Course(
                    code=course_code,
                    title=course_title_ar, # Store Arabic title
                    semester=semester,
                    credits=3 if "مشروع" not in course_title_ar else 6 # Example credit logic (check for Arabic word "Project")
                )
                all_courses.append(course)
                db.session.add(course)
                print(f"  Adding course: {course_code} - {course_title_ar} (Semester {semester})")

    db.session.flush() # Get course IDs

    # Associate courses with program
    for course in all_courses:
        # Check if association already exists
        existing_assoc = ProgramCourse.query.filter_by(
            program_id=program.id,
            course_id=course.id
        ).first()

        if not existing_assoc:
            program_course = ProgramCourse(
                program_id=program.id,
                course_id=course.id,
                semester=course.semester
            )
            db.session.add(program_course)
            print(f"  Associated course {course.code} ({course.title}) with program {program.name} (Semester {course.semester})")

    # Commit all changes for this program and its courses
    try:
        db.session.commit()
        print(f"Successfully processed program {program.name} ({degree_type}) and its courses.")
    except Exception as e:
        db.session.rollback()
        print(f"Error processing program {program.name} ({degree_type}): {str(e)}")
        traceback.print_exc()

    return program

def populate_all_programs_arabic():
    with app.app_context():
        try:
            print("--- Starting ARABIC Program Population ---")

            # 1. Project Management (إدارة المشروعات)
            pm_diploma_ar = add_program_with_courses_arabic(
                "إدارة المشروعات", "Diploma", "برنامج دبلوم في إدارة المشروعات",
                {
                    1: ["أساسيات إدارة المشروعات", "تحليل البيانات", "التخطيط والجدولة", "الهيكل التنظيمي والاتصال", "اتخاذ القرار"],
                    2: ["الميزانية والتكلفة", "إدارة الأزمات والمخاطر", "مراقبة المشروع", "إدارة الجودة الشاملة", "مشروع"]
                }, program_name_en_for_code="ProjectManagement"
            )
            pm_master_ar = add_program_with_courses_arabic(
                "إدارة المشروعات", "Master", "برنامج ماجستير في إدارة المشروعات",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "دراسات الجدوى للمشروعات", "موضوعات مختارة في إدارة المشروعات"],
                    2: ["تحليل التكلفة والعائد وتقييم المشروعات", "إدارة المشروعات في الممارسة العملية", "برامج إدارة المشروعات", "مشروع"]
                }, program_name_en_for_code="ProjectManagement"
            )
            pm_phd_ar = add_program_with_courses_arabic(
                "إدارة المشروعات", "PhD", "برنامج دكتوراه في إدارة المشروعات",
                {
                    1: ["إدارة السلوك التنظيمي", "الموارد البشرية الاستراتيجية", "تقييم مشروعات التنمية"],
                    2: ["تحليل القيمة للمشروعات الهندسية", "إدارة المشروعات المتعددة", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="ProjectManagement"
            )

            # 2. Operations Research and Decision Support (بحوث العمليات ودعم القرار)
            ords_diploma_ar = add_program_with_courses_arabic(
                "بحوث العمليات ودعم القرار", "Diploma", "برنامج دبلوم في بحوث العمليات ودعم القرار",
                {
                    1: ["نماذج بحوث العمليات وتطبيقاتها", "نظم دعم القرار", "تحليل إحصائي للأعمال", "إدارة المشروعات والشبكات", "إدارة المخزون"],
                    2: ["إدارة العمليات", "النمذجة والمحاكاة", "مراقبة الجودة", "برمجيات بحوث العمليات", "مشروع"]
                }, program_name_en_for_code="OperationsResearch"
            )
            ords_master_ar = add_program_with_courses_arabic(
                "بحوث العمليات ودعم القرار", "Master", "برنامج ماجستير في بحوث العمليات ودعم القرار",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "موضوعات متقدمة في اتخاذ القرار", "التنبؤ"],
                    2: ["الجدولة", "إدارة سلسلة الإمداد", "برمجيات بحوث العمليات المتقدمة", "مشروع"]
                }, program_name_en_for_code="OperationsResearch"
            )
            ords_phd_ar = add_program_with_courses_arabic(
                "بحوث العمليات ودعم القرار", "PhD", "برنامج دكتوراه في بحوث العمليات ودعم القرار",
                {
                    1: ["موضوعات متقدمة في نظم دعم القرار", "اتخاذ القرارات متعددة المعايير", "النماذج الاحتمالية"],
                    2: ["تطبيقات نظرية الألعاب", "موضوعات متقدمة في بحوث العمليات", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="OperationsResearch"
            )

            # 3. Supply Chain and Operations Management (سلسلة الإمداد وإدارة العمليات)
            scom_diploma_ar = add_program_with_courses_arabic(
                "سلسلة الإمداد وإدارة العمليات", "Diploma", "برنامج دبلوم في سلسلة الإمداد وإدارة العمليات",
                {
                    1: ["إدارة المشروعات: أدوات وتقنيات", "أدوات التحليل الكمي في اتخاذ القرار", "إدارة العمليات", "برمجيات إدارة العمليات", "إدارة سلسلة الإمداد"],
                    2: ["تحليل إحصائي للأعمال", "نظم المعلومات في سلسلة الإمداد", "إدارة الإنتاج", "إدارة الجودة", "مشروع"]
                }, program_name_en_for_code="SupplyChainOpsMgmt"
            )
            scom_master_ar = add_program_with_courses_arabic(
                "سلسلة الإمداد وإدارة العمليات", "Master", "برنامج ماجستير في سلسلة الإمداد وإدارة العمليات",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "النمذجة والمحاكاة", "تحليل وتقييم المخاطر"],
                    2: ["الجدولة", "موضوعات متقدمة في إدارة العمليات", "برمجيات إدارة العمليات", "مشروع"]
                }, program_name_en_for_code="SupplyChainOpsMgmt"
            )
            scom_phd_ar = add_program_with_courses_arabic(
                "سلسلة الإمداد وإدارة العمليات", "PhD", "برنامج دكتوراه في سلسلة الإمداد وإدارة العمليات",
                {
                    1: ["تخطيط وتحديد مواقع المرافق", "نظم العمليات الرشيقة", "تخطيط الإنتاج ومتطلبات المواد"],
                    2: ["التخطيط الإجمالي واستراتيجية العمليات", "الصيانة والموثوقية", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="SupplyChainOpsMgmt"
            )

            # 4. Web Design (تصميم المواقع)
            wd_diploma_ar = add_program_with_courses_arabic(
                "تصميم المواقع", "Diploma", "برنامج دبلوم في تصميم المواقع",
                {
                    1: ["مقدمة في علوم الحاسب", "قواعد بيانات SQL Server", "HTML 5 و CSS 3", "فوتوشوب لتصميم الويب", "ASP.NET, JavaScript و jQuery"],
                    2: ["برمجة الويب باستخدام PHP", "Bootstrap لتصميم الويب المتجاوب", "تطوير الويب لمحركات البحث (SEO)", "البرمجة الشيئية", "مشروع"]
                }, program_name_en_for_code="WebDesign"
            )
            wd_master_ar = add_program_with_courses_arabic(
                "تصميم المواقع", "Master", "برنامج ماجستير في تصميم المواقع",
                {
                    1: ["تصميم وإدارة المواقع المتقدمة", "أمن تطبيقات الويب", "تطوير تطبيقات الويب المتقدمة"],
                    2: ["نظم قواعد البيانات المتقدمة", "تقنيات وممارسات أجايل", "منهجية البحث", "مشروع"]
                }, program_name_en_for_code="WebDesign"
            )
            wd_phd_ar = add_program_with_courses_arabic(
                "تصميم المواقع", "PhD", "برنامج دكتوراه في تصميم المواقع",
                {
                    1: ["تطوير تطبيقات الهواتف المحمولة", "مستجدات في إدارة الويب", "موضوعات مختارة في تكنولوجيا الويب"],
                    2: ["قراءات فردية موجهة (موضوعات متقدمة)", "دراسات موجهة في علوم الويب", "دراسات فردية تحت الإشراف (موضوعات متقدمة)"]
                }, program_name_en_for_code="WebDesign"
            )

            # 5. Software Engineering (هندسة البرمجيات)
            se_diploma_ar = add_program_with_courses_arabic(
                "هندسة البرمجيات", "Diploma", "برنامج دبلوم في هندسة البرمجيات",
                {
                    1: ["مبادئ نظم الحاسب والبرمجة", "نظم قواعد البيانات العلائقية", "عملية تطوير البرمجيات", "تصميم واجهة المستخدم", "تطوير البرمجيات الشيئية باستخدام UML"],
                    2: ["إدارة مشروعات البرمجيات", "تصميم وهيكلة الويب", "تطوير البرمجيات أجايل", "البرمجة على نطاق واسع", "مشروع"]
                }, program_name_en_for_code="SoftwareEngineering"
            )
            se_master_ar = add_program_with_courses_arabic(
                "هندسة البرمجيات", "Master", "برنامج ماجستير في هندسة البرمجيات",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "ضمان جودة البرمجيات", "موضوعات متقدمة في قواعد البيانات"],
                    2: ["موضوعات متقدمة في نظم المعلومات", "أمن المعلومات", "تطوير البرمجيات أجايل المتقدم", "مشروع"]
                }, program_name_en_for_code="SoftwareEngineering"
            )
            se_phd_ar = add_program_with_courses_arabic(
                "هندسة البرمجيات", "PhD", "برنامج دكتوراه في هندسة البرمجيات",
                {
                    1: ["موضوعات مختارة في هندسة البرمجيات", "موضوعات مختارة في نظم المعلومات", "موضوعات مختارة في تكنولوجيا المعلومات"],
                    2: ["تخزين البيانات", "تطوير حلول التجارة الإلكترونية", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="SoftwareEngineering"
            )

            # 6. Population Policies & Data Analysis (السياسات السكانية وتحليل بياناتها)
            ppda_diploma_ar = add_program_with_courses_arabic(
                "السياسات السكانية وتحليل بياناتها", "Diploma", "برنامج دبلوم في السياسات السكانية وتحليل بياناتها",
                {
                    1: ["السياسات والإسقاطات السكانية", "مصادر البيانات السكانية وتقييمها", "السكان والتنمية (البشرية - الفقر - التمكين...)", "استخدام SPSS لتحليل بيانات المسوح", "الإسقاطات السكانية باستخدام برنامج Spectrum"],
                    2: ["إسقاطات القوى العاملة ومؤشرات سوق العمل", "تحليل البيانات متعددة المستويات", "تحليل المسار والمعادلات الهيكلية باستخدام AMOS", "تطبيقات التحليل متعدد المتغيرات", "مشروع"]
                }, program_name_en_for_code="PopulationPoliciesDataAnalysis"
            )

            # 7. Applied Statistics (الإحصاءات التطبيقية)
            as_diploma_ar = add_program_with_courses_arabic(
                "الإحصاءات التطبيقية", "Diploma", "برنامج دبلوم في الإحصاءات التطبيقية",
                {
                    1: ["مقدمة في الإحصاء التطبيقي", "مقدمة في المعاينة", "مقدمة في تحليل البيانات النوعية", "السلاسل الزمنية مع تطبيقات", "تحليل البيانات باستخدام الحزم الإحصائية (1)"],
                    2: ["الأرقام القياسية", "تحليل الانحدار", "مقدمة في تحليل البيانات الكمية", "تحليل البيانات باستخدام الحزم الإحصائية (2)", "مشروع"]
                }, program_name_en_for_code="AppliedStatistics"
            )
            as_master_ar = add_program_with_courses_arabic(
                "الإحصاءات التطبيقية", "Master", "برنامج ماجستير في الإحصاءات التطبيقية",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "تحليل البيانات النوعية", "تحليل البيانات الكمية"],
                    2: ["الاقتصاد القياسي", "مقدمة في التحليل متعدد المستويات", "التحليل متعدد المتغيرات", "مشروع"]
                }, program_name_en_for_code="AppliedStatistics"
            )
            as_phd_ar = add_program_with_courses_arabic(
                "الإحصاءات التطبيقية", "PhD", "برنامج دكتوراه في الإحصاءات التطبيقية",
                {
                    1: ["تنقيب البيانات", "التحليل المتقدم متعدد المستويات", "مقدمة في البيانات الضخمة"],
                    2: ["أدوات تحليل البيانات الضخمة", "التحليل المتقدم متعدد المتغيرات", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="AppliedStatistics"
            )

            # 8. Modern Management for Human Resources (الإدارة الحديثة للموارد البشرية)
            mmhr_diploma_ar = add_program_with_courses_arabic(
                "الإدارة الحديثة للموارد البشرية", "Diploma", "برنامج دبلوم في الإدارة الحديثة للموارد البشرية",
                {
                    1: ["أساسيات ووظائف إدارة الموارد البشرية", "نظام معلومات الموارد البشرية", "تخطيط برامج التدريب", "إدارة الإحلال الوظيفي", "تنمية الموارد البشرية في إطار الجودة الشاملة"],
                    2: ["قوانين العمل في مصر", "تخطيط القوى العاملة", "مقدمة في التحليل الإحصائي", "الموارد البشرية والرضا الوظيفي", "مشروع"]
                }, program_name_en_for_code="ModernMgmtHR"
            )
            mmhr_master_ar = add_program_with_courses_arabic(
                "الإدارة الحديثة للموارد البشرية", "Master", "برنامج ماجستير في الإدارة الحديثة للموارد البشرية",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "التخطيط الاستراتيجي للموارد البشرية", "أخلاقيات الوظيفة"],
                    2: ["السلوك التنظيمي للموارد البشرية", "تخطيط وإدارة المسار الوظيفي", "قراءات فردية", "مشروع"]
                }, program_name_en_for_code="ModernMgmtHR"
            )
            mmhr_phd_ar = add_program_with_courses_arabic(
                "الإدارة الحديثة للموارد البشرية", "PhD", "برنامج دكتوراه في الإدارة الحديثة للموارد البشرية",
                {
                    1: ["التخطيط الاستراتيجي الإداري للموارد البشرية", "إدارة الموارد البشرية الدولية", "الذكاء الاصطناعي والموارد البشرية"],
                    2: ["الاستثمار البشري وإدارة رأس المال الفكري", "الاتجاهات الحديثة في إدارة الموارد البشرية", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="ModernMgmtHR"
            )

            # 9. Econometric Analysis of Time Series (التحليل القياسي للسلاسل الزمنية)
            eats_diploma_ar = add_program_with_courses_arabic(
                "التحليل القياسي للسلاسل الزمنية", "Diploma", "برنامج دبلوم في التحليل القياسي للسلاسل الزمنية",
                {
                    1: ["تحليل إحصائي", "السلاسل الزمنية ونماذج بوكس-جنكنز", "طرق الاقتصاد القياسي", "الطرق الرياضية للسلاسل الزمنية", "الحزم الحاسوبية الإحصائية والاقتصادية القياسية"],
                    2: ["التنبؤ وجودة توافق النموذج", "السلاسل الزمنية القائمة على الاقتصاد القياسي", "تطبيقات السلاسل الزمنية في مجالات مختلفة", "تحليل بيانات البانل", "مشروع"]
                }, program_name_en_for_code="EconometricAnalysisTS"
            )
            eats_master_ar = add_program_with_courses_arabic(
                "التحليل القياسي للسلاسل الزمنية", "Master", "برنامج ماجستير في التحليل القياسي للسلاسل الزمنية",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "الطرق الرياضية المتقدمة للسلاسل الزمنية", "الاحتمالات والإحصاء والعمليات العشوائية"],
                    2: ["طرق الاقتصاد القياسي المتقدمة", "السلاسل الزمنية أحادية المتغير", "السلاسل الزمنية متعددة المتغيرات", "مشروع"]
                }, program_name_en_for_code="EconometricAnalysisTS"
            )

            # 10. Statistical Computing (الحسابات الإحصائية)
            sc_diploma_ar = add_program_with_courses_arabic(
                "الحسابات الإحصائية", "Diploma", "برنامج دبلوم في الحسابات الإحصائية",
                {
                    1: ["تحليل إحصائي", "مقدمة في الإحصاء الرياضي", "الطرق الإحصائية والمحاكاة", "تكنولوجيا الإنترنت وبرمجيات الإنترنت", "الحزم الإحصائية"],
                    2: ["النماذج العشوائية وتطبيقاتها", "الحسابات التطورية والطبيعية", "السلاسل الزمنية والتنبؤ", "النمذجة الرياضية وتحليل القرار", "مشروع"]
                }, program_name_en_for_code="StatisticalComputing"
            )
            sc_master_ar = add_program_with_courses_arabic(
                "الحسابات الإحصائية", "Master", "برنامج ماجستير في الحسابات الإحصائية",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "تحليل عددي", "تحليل الانحدار"],
                    2: ["تقنيات المعاينة", "تحليل السلاسل الزمنية المتقدم", "الحزم الحاسوبية في الإحصاء مع تطبيقات", "مشروع"]
                }, program_name_en_for_code="StatisticalComputing"
            )
            sc_phd_ar = add_program_with_courses_arabic(
                "الحسابات الإحصائية", "PhD", "برنامج دكتوراه في الحسابات الإحصائية",
                {
                    1: ["برمجة SAS الإحصائية", "التقنيات العددية المتقدمة", "الطرق غير المعلمية"],
                    2: ["برمجة Python و R المتقدمة", "الطرق الإحصائية في الموثوقية", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="StatisticalComputing"
            )

            # 11. Statistical Quality Control & Quality Assurance (الضبط الإحصائي وتوكيد الجودة)
            sqcqa_diploma_ar = add_program_with_courses_arabic(
                "الضبط الإحصائي وتوكيد الجودة", "Diploma", "برنامج دبلوم في الضبط الإحصائي وتوكيد الجودة",
                {
                    1: ["أساسيات مراقبة الجودة", "نظم المعلومات وإدارة المعرفة", "خرائط المراقبة", "تحليل البيانات", "نظم الجودة"],
                    2: ["إدارة المشروعات", "معاينة القبول", "الموثوقية والإحلال", "التحسين المستمر", "مشروع"]
                }, program_name_en_for_code="StatQualityControlQA"
            )
            sqcqa_master_ar = add_program_with_courses_arabic(
                "الضبط الإحصائي وتوكيد الجودة", "Master", "برنامج ماجستير في الضبط الإحصائي وتوكيد الجودة",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "خرائط المراقبة المتقدمة", "التنبؤ"],
                    2: ["اتخاذ القرار", "تصميم وتحليل التجارب", "تحليل الكفاءة والإنتاجية", "مشروع"]
                }, program_name_en_for_code="StatQualityControlQA"
            )
            sqcqa_phd_ar = add_program_with_courses_arabic(
                "الضبط الإحصائي وتوكيد الجودة", "PhD", "برنامج دكتوراه في الضبط الإحصائي وتوكيد الجودة",
                {
                    1: ["المحاكاة", "المواصفات والتقييس", "المراجعة الداخلية والخارجية"],
                    2: ["إعادة الهندسة وإدارة التغيير", "التحسين المستمر المتقدم", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="StatQualityControlQA"
            )

            # 12. Risk and Crisis Management (إدارة المخاطر والأزمات)
            rcm_diploma_ar = add_program_with_courses_arabic(
                "إدارة المخاطر والأزمات", "Diploma", "برنامج دبلوم في إدارة المخاطر والأزمات",
                {
                    1: ["إدارة الأزمات والمخاطر (1)", "إدارة المخاطر المالية", "تحليل البيانات الإحصائية وكتابة التقارير", "دور القيادة في إدارة الأزمات", "التخطيط الاستراتيجي لإدارة الأزمات"],
                    2: ["دور الإعلام في إدارة الأزمات", "بحوث العمليات", "إدارة الأزمات والمخاطر (2)", "التحليل العلمي للأزمات", "مشروع"]
                }, program_name_en_for_code="RiskCrisisManagement"
            )
            rcm_master_ar = add_program_with_courses_arabic(
                "إدارة المخاطر والأزمات", "Master", "برنامج ماجستير في إدارة المخاطر والأزمات",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "التنبؤ الوقائي بالأزمات والمخاطر", "التأمين في إدارة الأزمات والمخاطر"],
                    2: ["التحليل الكمي للمخاطر", "دور دعم القرار في إدارة الأزمات والمخاطر", "قراءات فردية", "مشروع"]
                }, program_name_en_for_code="RiskCrisisManagement"
            )
            rcm_phd_ar = add_program_with_courses_arabic(
                "إدارة المخاطر والأزمات", "PhD", "برنامج دكتوراه في إدارة المخاطر والأزمات",
                {
                    1: ["التخطيط الاستراتيجي وسيناريوهات إدارة الأزمات", "دور الحكومة في إدارة الأزمات والمخاطر", "الذكاء الاصطناعي في إدارة الأزمات والمخاطر"],
                    2: ["النظم المقارنة في إدارة الأزمات والمخاطر", "المحاكاة", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="RiskCrisisManagement"
            )

            # 13. Surveys and Reporting (المسوح وإعداد تقاريرها)
            sr_diploma_ar = add_program_with_courses_arabic(
                "المسوح وإعداد تقاريرها", "Diploma", "برنامج دبلوم في المسوح وإعداد تقاريرها",
                {
                    1: ["المسوح وأنواعها", "المعاينة", "إدخال البيانات باستخدام CSPro", "تحليل البيانات الوصفية (Metadata)", "تحليل بيانات الإنجاب"],
                    2: ["تنظيم الأسرة والحاجة غير الملباة (الصحة الإنجابية)", "الوفيات والمراضة", "تطبيقات على البيانات متعددة المتغيرات", "إجراء تقارير المسوح ونشر نتائجها", "مشروع"]
                }, program_name_en_for_code="SurveysReporting"
            )

            # 14. Data Analysis (تحليل البيانات)
            da_diploma_ar = add_program_with_courses_arabic(
                "تحليل البيانات", "Diploma", "برنامج دبلوم في تحليل البيانات",
                {
                    1: ["مقدمة في الإحصاء", "مصادر البيانات وتقييمها", "مقدمة في تقنيات المعاينة", "تحليل الانحدار وتشخيصه", "تحليل البيانات باستخدام SPSS"],
                    2: ["مقدمة في تحليل البيانات النوعية", "مقدمة في تحليل البيانات الكمية", "مقدمة في تحليل البيانات متعددة المستويات", "مقدمة في التحليل متعدد المتغيرات", "مشروع"]
                }, program_name_en_for_code="DataAnalysis"
            )
            da_master_ar = add_program_with_courses_arabic(
                "تحليل البيانات", "Master", "برنامج ماجستير في تحليل البيانات",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "تحليل البيانات النوعية", "تحليل البيانات الكمية"],
                    2: ["تنقيب البيانات مع تطبيقات", "موضوعات متقدمة في تحليل البيانات", "التحليل متعدد المتغيرات", "مشروع"]
                }, program_name_en_for_code="DataAnalysis"
            )
            da_phd_ar = add_program_with_courses_arabic(
                "تحليل البيانات", "PhD", "برنامج دكتوراه في تحليل البيانات",
                {
                    1: ["تحليل البيانات النوعية المتقدم", "تحليل البيانات الكمية المتقدم", "التحليل متعدد المتغيرات المتقدم"],
                    2: ["تنقيب البيانات المتقدم", "التحليل المتقدم متعدد المستويات", "قراءات فردية موجهة (موضوعات متقدمة)"]
                }, program_name_en_for_code="DataAnalysis"
            )

            # 15. Life Testing and Reliability Analysis (اختبارات الحياة وتحليل الصلاحية)
            ltra_diploma_ar = add_program_with_courses_arabic(
                "اختبارات الحياة وتحليل الصلاحية", "Diploma", "برنامج دبلوم في اختبارات الحياة وتحليل الصلاحية",
                {
                    1: ["الإحصاء والاحتمالات", "الإحصاء التطبيقي", "تحليل البقاء", "مقدمة في الموثوقية واختبارات الحياة", "الحزم الإحصائية"],
                    2: ["تحليل الموثوقية الإحصائي", "فترات التنبؤ والتسامح: القياس والموثوقية", "الطرق الإحصائية في الموثوقية", "تطبيقات الموثوقية واختبارات الحياة", "مشروع"]
                }, program_name_en_for_code="LifeTestingReliability"
            )

            # 16. Measuring Public Opinion Polls (قياس استطلاعات الرأى العام)
            mpop_diploma_ar = add_program_with_courses_arabic(
                "قياس استطلاعات الرأى العام", "Diploma", "برنامج دبلوم في قياس استطلاعات الرأي العام",
                {
                    1: ["دليل استطلاعات الرأي العام", "تصميم مسح الرأي العام", "وسائل المسح والقياس، فن المقابلات الشخصية، ميثاق الأخلاق والممارسات المهنية", "تحليل بيانات المسح", "المجالات التي تغطيها استطلاعات الرأي العام"],
                    2: ["استخدام SPSS في تحليل بيانات المسح", "تحليل الاتجاه والمحتوى: تحليل متعمق", "إعداد تقارير المسح ونشر نتائجها", "أمثلة عملية لمسوح الرأي العام، تقييم الأداء وضمان الجودة", "مشروع"]
                }, program_name_en_for_code="MeasuringPublicOpinionPolls"
            )

            # 17. Statistical Research and Development (البحوث الإحصائية والتطوير)
            srd_diploma_ar = add_program_with_courses_arabic(
                "البحوث الإحصائية والتطوير", "Diploma", "برنامج دبلوم في البحوث الإحصائية والتطوير",
                {
                    1: ["أساسيات البحث والتطوير (R & D)", "تنقيب البيانات", "التحسين المستمر", "اتخاذ القرار", "الإبداع والابتكار"],
                    2: ["هندسة القيمة", "إعادة الهندسة وإدارة التغيير", "التنبؤ والإنذار المبكر", "المحاكاة", "مشروع"]
                }, program_name_en_for_code="StatisticalResearchDev"
            )
            srd_master_ar = add_program_with_courses_arabic(
                "البحوث الإحصائية والتطوير", "Master", "برنامج ماجستير في البحوث الإحصائية والتطوير",
                {
                    1: ["مبادئ ومنهجيات البحث العلمي", "إدارة المشروعات", "الذكاء الاصطناعي"],
                    2: ["تحليل الأعمال", "تحليل البيانات الذكي", "تحليل المخاطر", "مشروع"]
                }, program_name_en_for_code="StatisticalResearchDev"
            )

            # 18. Human Development & Resources (التنمية البشرية ومواردها)
            hdr_diploma_ar = add_program_with_courses_arabic(
                "التنمية البشرية ومواردها", "Diploma", "برنامج دبلوم في التنمية البشرية ومواردها",
                {
                    1: ["أساسيات التنمية البشرية", "الصحة والتعليم والقوى العاملة والتنمية البشرية", "تقدير التنمية البشرية", "أساسيات السكان", "الطرق الإحصائية"],
                    2: ["مهارات الإدارة الأساسية", "التنبؤ بالطلب على التنمية البشرية", "اقتصاديات التنمية البشرية", "إسقاطات السكان باستخدام الحزم الحاسوبية", "مشروع"]
                }, program_name_en_for_code="HumanDevelopmentResources"
            )


            print("--- Finished ARABIC Program Population ---")

        except Exception as e:
            db.session.rollback()
            print(f"Error during ARABIC database population: {str(e)}")
            traceback.print_exc()

if __name__ == '__main__':
    populate_all_programs_arabic()

# --- END OF FILE populate_all_programs_arabic.py ---