class Node:

    def __init__(self, text, l_child, r_child, stop=0, make=0):
        self.l_child = l_child
        self.r_child = r_child
        self.text = text
        self.stop = stop
        self.make = make

#'Узел': 'l_child': узел для перехода в случае ответа "нет", 'r_child': узел для перехода в случае ответа "да",
#'text': текст вопроса узла, 'stop': флаг окончания поиска (Если не равен нулю, поиск заканчивается.
# Значение соответствует конечному состоянию на схеме логики.), 'make': флаг расчета (Если выставлен в 1, результат
# должен быть получен внутри программы)
questoins = {'root':
                 {'l_child': '1',
                  'r_child': '2',
                  'text': 'Приобретенный Вами товар имеет недостаток?',
                  'stop':0,
                  'make':0},
             '1':
                 {'l_child': '3',
                  'r_child': '4',
                  'text': 'Товар куплен дистанционным способом? (Это значит, что вы оплатили товар до его получения)',
                  'stop':0,
                  'make':0},
             '2':
                 {'l_child': '6',
                  'r_child': '5',
                  'text': 'Является ли недостаток вашего товара повреждением в ходе эксплуатации?',
                  'stop': 0,
                  'make': 0},
             '3':
                 {'l_child': '7',
                  'r_child': '8',
                  'text': 'Входит ли товар в перечень товаров надлежащего качества, не подлежащих обмену или возврату (ПП55)?',
                  'stop': 0,
                  'make': 1},
             '4':
                 {'l_child': '10',
                  'r_child': '9',
                  'text': 'Сохранен ли товарный вид и потребительские свойства товара? (это значит, что не нарушена целостность упаковки, бирок, ярлыков, на товаре отсутствуют следы эксплуатации и он имеет вид нового товара)',
                  'stop': 0,
                  'make': 0},
             '5':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Отказ на основании п.6 ст.18 ЗоЗПП, поскольку недостаток возник после передачи Вам товара в результате нарушения правил использования, хранения или транспортировки товара, действий третьих лиц или непреодолимой силы.',
                  'stop': 8,
                  'make': 0},
             '6':
                 {'l_child': '11',
                  'r_child': '12',
                  'text': 'На приобретенный Вами товар установлен гарантийный срок?',
                  'stop': 0,
                  'make': 0},
             '7':
                 {'l_child': '14',
                  'r_child': '13',
                  'text': 'С момента покупки (не считая самого дня) прошло 14 дней или более?',
                  'stop': 0,
                  'make': 1},
             '8':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Отказ, поскольку приобретенный Вами товар не подлежит обмену или возврату на основании постановления Правительства РФ №55',
                  'stop': 1,
                  'make': 0},
             '9':
                 {'l_child': '15',
                  'r_child': '16',
                  'text': 'С даты получения товара прошло 7 дней или более?',
                  'stop': 0,
                  'make': 1},
             '10':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Отказ в возврате/обмене на основании абз.3 п.4 ст. 26.1 ЗоЗПП, поскольку товарный вид/потребительские свойства товара не были сохранены',
                  'stop': 2,
                  'make': 0},
             '11':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Потребитель должен быть направлен на экспертизу за свой счет на основании п.6 ст.18 ЗоЗПП',
                  'stop': 9,
                  'make': 0},
             '12':
                 {'l_child': '18',
                  'r_child': '17',
                  'text': 'Гарантийный срок истек на текущий момент?',
                  'stop': 0,
                  'make': 0},
             '13':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Отказ на основании п.1 ст.25 ЗоЗПП, поскольку Вами был пропущен срок, допустимый законом для возврата товара надлежащего качества',
                  'stop': 3,
                  'make': 0},
             '14':
                 {'l_child': '19',
                  'r_child': '20',
                  'text': 'Сохранен ли товарный вид, приобретенного Вами товара? (это значит, что не нарушена целостность упаковки, бирок, ярлыков, на товаре отсутствуют следы эксплуатации и он имеет вид нового товара)имеется ли чек или иное доказательство факта покупки?',
                  'stop': 0,
                  'make': 0},
             '15':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Возможно осуществить возврат на основании ст.26.1, поскольку требование о возврате предъявлено в течение 7 дней с момента покупки, при условии компенсации Вами расходов продавца на доставку',
                  'stop': 4,
                  'make': 0},
             '16':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Отказ в возврате/обмене по причине пропуска 7 дней, предоставленных Законом для возврата товара надлежащего качества, купленного дистанционным способом (на основании п.4 ст.26.1 ЗоЗПП, абз.1)',
                  'stop': 5,
                  'make': 0},
             '17':
                 {'l_child': '22',
                  'r_child': '21',
                  'text': 'Прошло более 2х лет с момента продажи/доставки?',
                  'stop': 0,
                  'make': 1},
             '18':
                 {'l_child': '24',
                  'r_child': '23',
                  'text': 'Имеете ли вы заключение независимой экспертизы или авторизованного сервисного центра, о том, что недостаток Вашего товара является производственным (брак)?',
                  'stop': 0,
                  'make': 0},
             '19':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Отказ, поскольку удовлетворение Вашего требование возможно только если приобретенный Вами товар не был в употреблении, сохранены его товарный вид, потребительские свойства, пломбы, фабричные ярлыки, а также имеется товарный чек или кассовый чек либо иной подтверждающий оплату указанного товара документ. (на основании абз.3 п.1 ст.25 ЗоЗПП)',
                  'stop': 6,
                  'make': 0},
             '20':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Возможен только обмен товара, при условии, что приобретенный не подошел по форме, габаритам, фасону, расцветке и т.д. (ст. 25 ЗоЗПП)',
                  'stop': 7,
                  'make': 0},
             '21':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Отказ, поскольку право на предъявление соответствующего требование ограничено периодом в два года с момента покупки товара. Указанный срок истек. (на основании п.5 ст.19 ЗоЗПП)',
                  'stop': 10,
                  'make': 0},
             '22':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Вам рекомендовано провести независимую экспертизу за свой счет, поскольку по истечении гарантийного срока бремя доказывания причин возникновения недостатка ложится на покупателя. (на основании п.5 ст. 19 ЗоЗПП)',
                  'stop': 11,
                  'make': 0},
             '23':
                 {'l_child': '26',
                  'r_child': '25',
                  'text': 'Товар является сложно техническим? (необходимо руководствоваться Постановлением Правительства №924',
                  'stop': 0,
                  'make': 1},
             '24':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Окончательно решение по Вашему вопросу может быть принято только на основании независимой экспертизы, либо официального заключения Авторизованного сервисного центра производителя.',
                  'stop': 12,
                  'make': 0},
             '25':
                 {'l_child': '27',
                  'r_child': '28',
                  'text': 'Недостаток обнаружен в течение 15 дней?',
                  'stop': 0,
                  'make': 1},
             '26':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Согласован возврат/обмен на основании п.1. ст.18 ЗоЗПП',
                  'stop': 13,
                  'make': 0},
             '27':
                 {'l_child': '29',
                  'r_child': '30',
                  'text': 'Недостаток Вашего товара определен в экспертном заключении или заключении Авторизованного сервисного центра как существенный? (неустранимый недостаток или недостаток, который не может быть устранен без несоразмерных расходов или затрат времени, или выявляется неоднократно, или проявляется вновь после его устранения, или другие подобные недостатки)',
                  'stop': 0,
                  'make': 0},
             '28':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Согласован возврат/обмен на основании п.1. ст.18 ЗоЗПП',
                  'stop': 14,
                  'make': 0},
             '29':
                 {'l_child': '32',
                  'r_child': '31',
                  'text': 'Товар подвергался ремонту?',
                  'stop': 0,
                  'make': 0},
             '30':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Согласован возврат/обмен на основании п.1. ст.18 ЗоЗПП',
                  'stop': 15,
                  'make': 0},
             '31':
                 {'l_child': '34',
                  'r_child': '33',
                  'text': 'Ремонт товара был произведен однократно?',
                  'stop': 0,
                  'make': 0},
             '32':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Вы вправе рассчитывать на бесплатный ремонт Вашего товара силами Авторизованного сервисного центра или продавца. (на основании ст.18 ЗоЗПП)',
                  'stop': 16,
                  'make': 0},
             '33':
                 {'l_child': '36',
                  'r_child': '35',
                  'text': 'Срок ремонта превысил 45 дней?',
                  'stop': 0,
                  'make': 0},
             '34':
                 {'l_child': '38',
                  'r_child': '37',
                  'text': 'Период ремонта за каждый год гарантийного срока превысил 30 дней?',
                  'stop': 0,
                  'make': 0},
             '35':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Согласован возврат/обмен на основании п.1. ст.18 ЗоЗПП',
                  'stop': 17,
                  'make': 0},
             '36':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть следующим: Поскольку недостаток Вашего товара не является существенным, допустимые законом сроки ремонта не нарушены, недостаток не проявляется неоднократно, основания для удовлетворения Вашего требования отсутствуют. Отказ на основании п.1 ст. 20 ЗоЗПП. П.1 ст.18 ЗоЗПП',
                  'stop': 18,
                  'make': 0},
             '37':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть таким: Согласован возврат/обмен на основании п.1. ст.18 ЗоЗПП',
                  'stop': 19,
                  'make': 0},
             '38':
                 {'l_child': None,
                  'r_child': None,
                  'text': 'Ответ на Ваше обращение может быть следующим: Поскольку недостаток Вашего товара не является существенным, , недостаток не проявляется неоднократно, основания для удовлетворения Вашего требования отсутствуют, поскольку не нарушен общий период использования товара в связи с неоднократными ремонтами, но Вы вправе рассчитывать на повторный ремонт товарв. Отказ на основании п.1 ст.18 ЗоЗПП.',
                  'stop': 20,
                  'make': 0}
             }
