/* Calculator 3.0: shared service questions. No prices or personal data here. */
(() => {
  const S = (ru, ka, en) => ({ru, ka, en});
  const choice = (id, ru, ka, en) => [id, S(ru, ka, en)];
  const field = (id, category, title, options, types) => ({id, category, title, options, types});
  window.BEQSON_CALCULATOR_CONFIG = {
    text: {
      version: S('Конфигуратор проекта · 3.0', 'პროექტის კონფიგურატორი · 3.0', 'Project configurator · 3.0'),
      details: S('Детали проекта', 'პროექტის დეტალები', 'Project details'),
      detailsHint: S('Уточните задачу. Эти ответы помогают оценить объём работ; они не добавляют автоматических наценок.', 'დააზუსტეთ ამოცანა. პასუხები სამუშაოს შეფასებაში გვეხმარება და ფასს ავტომატურად არ ზრდის.', 'Refine your scope. These answers help us prepare a quote; they do not add automatic charges.'),
      choose: S('Пока не определились', 'ჯერ არ გადაგვიწყვეტია', 'Not decided yet'),
      requirements: S('Пожелания и требования', 'სურვილები და მოთხოვნები', 'Goals and requirements'),
      requirementsHint: S('Опишите цели, ограничения и необходимые интеграции. Не указывайте пароли, ключи API или личные контакты: этот текст войдёт в копируемый бриф.', 'აღწერეთ მიზნები, შეზღუდვები და საჭირო ინტეგრაციები. არ მიუთითოთ პაროლები, API გასაღებები ან პირადი კონტაქტები: ეს ტექსტი ბრიეფში მოხვდება.', 'Describe your goals, constraints and integrations. Do not include passwords, API keys or personal contact details: this text is included in the shareable brief.'),
      summary: S('Ваш проект', 'თქვენი პროექტი', 'Your project'),
      category: S('Направление', 'მომსახურების მიმართულება', 'Service category'),
      industry: S('Сфера бизнеса', 'ბიზნესის სფერო', 'Business sector'),
      copy: S('Скопировать бриф', 'ბრიეფის კოპირება', 'Copy project brief'),
      print: S('Печать / сохранить PDF', 'ბეჭდვა / PDF-ად შენახვა', 'Print / save PDF'),
      copied: S('Бриф скопирован.', 'ბრიეფი დაკოპირებულია.', 'Project brief copied.'),
      copyFallback: S('Копирование недоступно. Выделите и скопируйте текст ниже.', 'კოპირება ვერ მოხერხდა. მონიშნეთ და დააკოპირეთ ქვემოთ მოცემული ტექსტი.', 'Clipboard unavailable. Select and copy the text below.'),
      privacy: S('Контакты из формы не включаются в бриф. Просмотрите свои требования перед отправкой брифа другим людям.', 'ფორმაში მითითებული კონტაქტები ბრიეფში არ შედის. გაზიარებამდე გადაამოწმეთ მოთხოვნების ტექსტი.', 'Form contact details are excluded. Review your requirements before sharing the brief.'),
      finalPrice: S('Окончательная стоимость и сроки зависят от согласованного объёма проекта.', 'საბოლოო ფასი და ვადები დამოკიდებულია პროექტის შეთანხმებულ მოცულობაზე.', 'Final pricing and delivery dates depend on the agreed project scope.'),
      timelineHint: S('Укажите приоритет. Сроки подтвердим после обсуждения задачи; автоматической наценки нет.', 'მიუთითეთ პრიორიტეტი. ვადებს ამოცანის განხილვის შემდეგ შევათანხმებთ; ფასი ავტომატურად არ იზრდება.', 'Choose your priority. Dates are agreed after reviewing the scope; no automatic surcharge applies.'),
      standard: S('По согласованному плану', 'შეთანხმებული გეგმით', 'Agreed project schedule'),
      urgent: S('Приоритетный запуск', 'პრიორიტეტული გაშვება', 'Priority delivery'),
      availability: S('После проверки доступности команды', 'გუნდის ხელმისაწვდომობის შემოწმების შემდეგ', 'Subject to team availability'),
      saved: S('Выбор сохраняется при переключении направлений в этой вкладке.', 'ამ ჩანართში მიმართულების შეცვლისას თქვენი არჩევანი შენარჩუნდება.', 'Your selections are kept when switching services in this tab.'),
      languages: S('Язык калькулятора', 'კალკულატორის ენა', 'Calculator language'),
      websiteCategory: S('Сайты и интернет-магазины', 'ვებსაიტები და ონლაინ მაღაზიები', 'Websites & e-commerce'),
      briefTitle: S('BEQSON — бриф проекта', 'BEQSON — პროექტის ბრიეფი', 'BEQSON — project brief'),
    },
    fields: [
      field('platform','website',S('Предпочтительная платформа','სასურველი პლატფორმა','Preferred platform'),[
        choice('wordpress','WordPress','WordPress','WordPress'),choice('webflow','Webflow','Webflow','Webflow'),choice('custom','Индивидуальная разработка','ინდივიდუალური დეველოპმენტი','Custom development')]),
      field('content','website',S('Готовность контента','კონტენტის მზადყოფნა','Content readiness'),[
        choice('ready','Контент готов','კონტენტი მზადაა','Content ready'),choice('partial','Часть контента готова','ნაწილობრივ მზადაა','Partly ready'),choice('needed','Нужна помощь с контентом','გვჭირდება დახმარება კონტენტთან','Content help needed')]),
      field('products','website',S('Размер каталога','კატალოგის მოცულობა','Product catalogue'),[
        choice('small','До 50 товаров','50-მდე პროდუქტი','Up to 50 products'),choice('medium','51–500 товаров','51–500 პროდუქტი','51–500 products'),choice('large','Более 500 товаров','500-ზე მეტი პროდუქტი','Over 500 products')],['store']),
      field('fulfilment','website',S('Доставка и получение','მიწოდება და მიღება','Delivery and fulfilment'),[
        choice('digital','Цифровые товары','ციფრული პროდუქტები','Digital products'),choice('local','Локальная доставка / самовывоз','ადგილობრივი მიწოდება / ადგილზე გატანა','Local delivery / pickup'),choice('international','Международная доставка','საერთაშორისო მიწოდება','International shipping')],['store']),
      field('market','seo',S('Целевой рынок','სამიზნე ბაზარი','Target market'),[
        choice('local','Город или регион','ქალაქი ან რეგიონი','City or region'),choice('national','Вся страна','მთელი ქვეყანა','National'),choice('global','Несколько стран','რამდენიმე ქვეყანა','Multiple countries')]),
      field('seoStage','seo',S('Состояние сайта','ვებსაიტის მდგომარეობა','Website stage'),[
        choice('new','Новый сайт','ახალი ვებსაიტი','New website'),choice('existing','Действующий сайт','მოქმედი ვებსაიტი','Existing website'),choice('migration','Редизайн / перенос','რედიზაინი / გადატანა','Redesign / migration')]),
      field('locations','seo',S('Количество локаций','ლოკაციების რაოდენობა','Business locations'),[
        choice('one','Одна локация','ერთი ლოკაცია','One location'),choice('several','2–5 локаций','2–5 ლოკაცია','2–5 locations'),choice('network','Сеть: 6+ локаций','ქსელი: 6+ ლოკაცია','Network: 6+ locations')],['seo_local']),
      field('aiVisibility','seo',S('Приоритет AI Search','AI ძიების პრიორიტეტი','AI search priority'),[
        choice('baseline','Проверка текущей видимости','არსებული ხილვადობის შემოწმება','Visibility baseline'),choice('content','Структура контента и сущностей','კონტენტისა და ობიექტების სტრუქტურა','Content and entity structure'),choice('monitor','Мониторинг упоминаний','ხსენებების მონიტორინგი','Mention monitoring')],['seo_geo']),
      field('systems','automation',S('Сколько систем нужно связать?','რამდენი სისტემის დაკავშირებაა საჭირო?','How many systems need connecting?'),[
        choice('one','Одна система','ერთი სისტემა','One system'),choice('few','2–3 системы','2–3 სისტემა','2–3 systems'),choice('many','4+ системы','4+ სისტემა','4+ systems')]),
      field('access','automation',S('Доступ к интеграциям','ინტეგრაციებზე წვდომა','Integration access'),[
        choice('ready','API / webhooks доступны','API / webhooks ხელმისაწვდომია','APIs / webhooks available'),choice('review','Нужно проверить возможности','შესაძლებლობები შესამოწმებელია','Access needs review')]),
      field('channel','automation',S('Где будет работать бот?','სად იმუშავებს ბოტი?','Bot channel'),[
        choice('website','На сайте','ვებსაიტზე','Website'),choice('telegram','Telegram','Telegram','Telegram'),choice('whatsapp','WhatsApp','WhatsApp','WhatsApp'),choice('multiple','Несколько каналов','რამდენიმე არხი','Multiple channels')],['auto_bot']),
      field('knowledge','automation',S('База знаний бота','ბოტის ცოდნის ბაზა','Bot knowledge source'),[
        choice('faq','FAQ / страницы сайта','FAQ / ვებსაიტის გვერდები','FAQs / website pages'),choice('docs','Документы компании','კომპანიის დოკუმენტები','Company documents'),choice('prepare','Нужна подготовка базы','ბაზის მომზადებაა საჭირო','Knowledge base needed')],['auto_bot']),
      field('process','automation',S('Основной процесс','ძირითადი პროცესი','Main workflow'),[
        choice('leads','Заявки и продажи','მოთხოვნები და გაყიდვები','Leads and sales'),choice('reporting','Отчёты и синхронизация','ანგარიშები და სინქრონიზაცია','Reporting and data sync'),choice('operations','Внутренние операции','შიდა პროცესები','Internal operations')],['auto_workflow','auto_crm']),
      field('designStage','design',S('Что уже есть?','რა არის უკვე მზად?','Starting point'),[
        choice('new','Новый проект','ახალი პროექტი','New project'),choice('existing','Существующий дизайн','არსებული დიზაინი','Existing design'),choice('brand','Есть бренд-гайд','ბრენდის გზამკვლევი მზადაა','Brand guidelines available')]),
      field('designTarget','design',S('Основной носитель','ძირითადი ფორმატი','Primary format'),[
        choice('website','Веб-сайт','ვებსაიტი','Website'),choice('app','Приложение / SaaS','აპლიკაცია / SaaS','App / SaaS'),choice('campaign','Маркетинговые материалы','მარკეტინგული მასალები','Marketing materials')]),
      field('brandScope','design',S('Состав айдентики','ვიზუალური იდენტობის მოცულობა','Brand identity scope'),[
        choice('refresh','Обновление стиля','სტილის განახლება','Visual refresh'),choice('identity','Логотип, цвета и типографика','ლოგო, ფერები და ტიპოგრაფია','Logo, colours and typography'),choice('guidelines','Система бренда и гайдлайн','ბრენდის სისტემა და გზამკვლევი','Brand system and guidelines')],['design_brand']),
      field('carePlatform','care',S('Платформа сайта','ვებსაიტის პლატფორმა','Website platform'),[
        choice('wordpress','WordPress','WordPress','WordPress'),choice('hosted','Конструктор / SaaS','კონსტრუქტორი / SaaS','Hosted builder / SaaS'),choice('custom','Индивидуальная разработка','ინდივიდუალური დეველოპმენტი','Custom development')]),
      field('frequency','care',S('Формат поддержки','მხარდაჭერის ფორმატი','Support arrangement'),[
        choice('once','Разовая задача','ერთჯერადი ამოცანა','One-off task'),choice('ongoing','Регулярная поддержка','რეგულარული მხარდაჭერა','Ongoing support')]),
      field('impact','care',S('Влияние проблемы','პრობლემის გავლენა','Issue impact'),[
        choice('improvement','Плановые улучшения','დაგეგმილი გაუმჯობესება','Planned improvements'),choice('partial','Часть функций не работает','ზოგი ფუნქცია არ მუშაობს','Some features affected'),choice('outage','Сайт недоступен','ვებსაიტი მიუწვდომელია','Website unavailable')]),
    ]
  };
})();
