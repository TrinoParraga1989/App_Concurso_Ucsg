import streamlit as st
import random
import re
from difflib import SequenceMatcher

# Banco de 80 preguntas sobre la Independencia de Guayaquil
questions = [
    {"q": "¿Cuántos militares extranjeros estaban acantonados en Guayaquil al momento de la independencia?", "a": "1300", "keywords": ["1300", "mil", "trecientos", "mil trecientos"], "context": "Fuerzas realistas con guarniciones extranjeras en la ciudad. Puedes encontrar más detalles en la página 1 del material de estudio."},
    {"q": "¿Quién era el gobernador de Guayaquil en 1820?", "a": "Pascual Vivero", "keywords": ["pascual vivero", "vivero"], "context": "Autoridad española al mando del territorio. Esta información se encuentra en la página 3 del material de estudio."},
    {"q": "¿Qué se planeaba realizar la noche del 1 de octubre de 1820?", "a": "Una reunión en la casa de José Villamil para planificar la independencia", "keywords": ["reunion", "casa", "villamil", "planificar", "independencia"], "context": "Reuniones clandestinas de los patriotas. Revisa la página 7 del material para más detalles."},
    {"q": "¿Quién fue el encargado de convencer a los soldados peruanos para unirse a la independencia?", "a": "José de Villamil", "keywords": ["jose", "villamil", "jose villamil"], "context": "Negociaciones con tropas del batallón peruano. La información está en la página 1 del material de estudio."},
    {"q": "¿Qué batallón formaban los pardos de Guayaquil?", "a": "El Batallón de Pardos", "keywords": ["batallon", "pardos"], "context": "Unidad militar compuesta por mestizos, mulatos y afrodescendientes. Revisa la página 4 del material."},
    {"q": "¿Es cierto que el Batallón Daule estaba formado por 150 hombres?", "a": "False", "keywords": ["falso", "no", "200"], "context": "José Villamil mencionó 200 hombres de milicia. Justification: According to Villamil, there were 200 militiamen, not 150. Puedes verificarlo en la página 1 del material."},
    {"q": "¿Es verdadero que los soldados peruanos se unieron a la independencia porque se les prometió el pago de salarios atrasados?", "a": "True", "keywords": ["verdadero", "si", "pago", "salarios"], "context": "Promesa de pago fue decisiva. Justification: They joined after being promised payment of overdue wages. La información está en la página 4 del material."},
    {"q": "¿Es cierto que los españoles afirmaban que las milicias contaban con 1.000 hombres?", "a": "True", "keywords": ["verdadero", "si", "1000", "mil"], "context": "Cifra inflada según fuentes españolas. Justification: Spanish sources claimed militias had 1,000 soldiers. Revisa la página 3 del material."},
    {"q": "¿Es correcto afirmar que Guayaquil se convirtió en República al proclamarse la independencia?", "a": "True", "keywords": ["verdadero", "si", "republica"], "context": "Se conformó una Junta de Gobierno. Justification: Independence led to the creation of a republican government. Puedes encontrar más detalles en la página 5 del material."},
    {"q": "¿Es cierto que el 9 de octubre de 1820 la ciudad de Guayaquil permaneció indiferente a la proclamación?", "a": "False", "keywords": ["falso", "no", "apoyo", "celebro"], "context": "El pueblo apoyó y celebró activamente. Justification: People celebrated and supported independence. El material de estudio indica que hubo celebración popular."},
    {"q": "¿Qué motivaciones llevaron a los guayaquileños a buscar la independencia?", "a": "Autonomía, cansancio del dominio español, apoyo militar y civil.", "keywords": ["autonomia", "cansancio", "dominio", "español", "apoyo"], "context": "Sentimientos independentistas generales en Hispanoamérica. El material de estudio describe estos elementos."},
    {"q": "Explique por qué fue clave la participación del Batallón de Granaderos de Reserva en la independencia de Guayaquil.", "a": "Su apoyo aseguró la victoria sin mayor resistencia.", "keywords": ["batallon", "granaderos", "reserva", "victoria", "resistencia"], "context": "Decisiva para evitar derramamiento de sangre. La información se encuentra en la página 1 del material de estudio."},
    {"q": "¿Qué papel desempeñó José Joaquín de Olmedo tras la proclamación de independencia?", "a": "Fue nombrado presidente de la Junta de Gobierno.", "keywords": ["jose", "joaquin", "olmedo", "presidente", "junta"], "context": "Liderazgo político inmediato. Revisa la página 5 del material."},
    {"q": "¿Por qué se considera la independencia de Guayaquil un movimiento 'cívico-militar'?", "a": "Participaron militares criollos y ciudadanos civiles.", "keywords": ["civico-militar", "militares", "civiles", "ciudadanos"], "context": "Colaboración de ambos sectores. El material lo describe en varias partes."},
    {"q": "Mencione dos consecuencias inmediatas del 9 de octubre de 1820 en Guayaquil.", "a": "Se proclamó la independencia y se instauró la Junta de Gobierno.", "keywords": ["independencia", "junta", "gobierno"], "context": "Transformación política inmediata. Revisa las páginas 5 y 6 del material."},
    {"q": "Según los españoles, ¿cuántos hombres integraban las milicias de Guayaquil?", "a": "1.000", "keywords": ["1000", "mil", "hombres"], "context": "Cifra española. Revisa la página 3 del material de estudio."},
    {"q": "Según José Villamil, ¿cuántos eran en realidad los hombres de milicia?", "a": "200", "keywords": ["200", "doscientos"], "context": "Testimonio del patriota. La información está en la página 3 del material de estudio."},
    {"q": "¿Qué diferencia existe entre las cifras de milicianos según fuentes españolas y las de Villamil?", "a": "Españoles inflaban a 1.000; Villamil reducía a 200.", "keywords": ["diferencia", "1000", "200"], "context": "Contradicción en fuentes. Revisa la página 3 del material de estudio para más detalles."},
    {"q": "¿Qué significaba 'Batallón de Pardos' en el contexto de la independencia de Guayaquil?", "a": "Unidad compuesta por mestizos, mulatos y afrodescendientes.", "keywords": ["batallon", "pardos", "mestizos", "mulatos"], "context": "División militar colonial. Se explica en la página 4 del material."},
    {"q": "Explique qué se entiende por 'Junta de Gobierno' en el proceso independentista de Guayaquil.", "a": "Órgano político provisional presidido por Olmedo.", "keywords": ["junta", "gobierno", "organo", "olmedo"], "context": "Institución republicana inicial. Revisa la página 5 del material."},
    {"q": "¿Qué fecha exacta se proclamó la independencia de Guayaquil?", "a": "9 de octubre de 1820", "keywords": ["9", "nueve", "octubre", "1820"], "context": "Hito principal de la gesta libertaria. La fecha está en todo el material de estudio."},
    {"q": "¿Qué batallón se sublevó en la madrugada del 9 de octubre?", "a": "El batallón Granaderos de Reserva", "keywords": ["batallon", "granaderos", "reserva"], "context": "Protagonistas militares. Revisa la página 1 del material."},
    {"q": "¿Qué hacían los patriotas antes de iniciar la insurrección para no ser descubiertos?", "a": "Se reunían secretamente en casas particulares.", "keywords": ["reunian", "secretamente", "casas", "particulares"], "context": "Reuniones clandestinas. Revisa la página 7 del material."},
    {"q": "¿Quién escribió la proclama de independencia de Guayaquil?", "a": "José Joaquín de Olmedo", "keywords": ["jose", "joaquin", "olmedo"], "context": "Intelectual de la independencia. Se menciona en la página 5 del material."},
    {"q": "¿Qué personaje fue clave como enlace entre criollos y tropas extranjeras?", "a": "José de Villamil", "keywords": ["jose", "villamil", "enlace", "criollos", "tropas"], "context": "Diplomacia insurgente. Revisa las páginas 1 y 7 del material."},
    {"q": "¿Es cierto que la independencia de Guayaquil se logró sin derramamiento de sangre?", "a": "True", "keywords": ["verdadero", "si", "sin", "derramamiento", "sangre"], "context": "El movimiento fue pacífico. Justification: It was a bloodless revolution achieved by agreement. La página 8 del material menciona que la revolución fue 'incruenta'."},
    {"q": "¿Es verdadero que la Junta de Gobierno de Guayaquil reconoció inmediatamente la autoridad del virrey de Lima?", "a": "False", "keywords": ["falso", "no", "virrey"], "context": "Se proclamó gobierno propio. Justification: They rejected Spanish authority and created their own government. La página 5 del material explica la creación de un nuevo Estado."},
    {"q": "¿Qué ciudad del actual Ecuador se liberó primero: Quito o Guayaquil?", "a": "Quito (10 de agosto de 1809)", "keywords": ["quito", "primero"], "context": "Primer grito de independencia. Esta información es de contexto histórico general, no está en el material específico, pero es relevante."},
    {"q": "¿Qué diferencia existía entre el movimiento de Quito (1809) y el de Guayaquil (1820)?", "a": "Quito fue sofocado y Guayaquil consolidó su independencia.", "keywords": ["quito", "sofocado", "guayaquil", "consolidó", "independencia"], "context": "Resultados distintos. Puedes revisar las páginas 1, 5 y 8 del material para ver el éxito de la independencia de Guayaquil."},
    {"q": "¿Qué significaba para Guayaquil ser 'Provincia Libre'?", "a": "Autogobierno y soberanía temporal.", "keywords": ["provincia", "libre", "autogobierno", "soberania"], "context": "Concepto político inicial. Revisa la página 5 del material."},
    {"q": "¿Quién fue el jefe militar del movimiento independentista de Guayaquil?", "a": "León de Febres Cordero", "keywords": ["leon", "febres", "cordero"], "context": "Conspirador clave. Su rol se menciona en las páginas 7 y 8 del material."},
    {"q": "¿Qué militares participaron además de Febres Cordero?", "a": "Luis Urdaneta, Miguel de Letamendi, etc.", "keywords": ["luis", "urdaneta", "miguel", "letamendi"], "context": "Red de oficiales. El material de estudio menciona a varios de los conspiradores."},
    {"q": "Explique por qué la fecha del 9 de octubre es considerada 'aurora de la independencia' del Ecuador.", "a": "Porque marcó el inicio definitivo del proceso libertario en la región.", "keywords": ["aurora", "independencia", "inicio", "proceso"], "context": "Significado histórico. El material de estudio enfatiza el rol de Guayaquil como punto de partida."},
    {"q": "¿Es cierto que el gobernador Pascual Vivero fue arrestado durante la madrugada del 9 de octubre?", "a": "True", "keywords": ["verdadero", "si", "pascual", "vivero", "arrestado"], "context": "Caída del poder español. Justification: Governor Vivero was captured at dawn. Este evento se menciona en el material de estudio."},
    {"q": "¿Qué papel desempeñó Vicente Rocafuerte en la independencia de Guayaquil?", "a": "Aunque no participó en 1820, luego fue importante en el proceso republicano.", "keywords": ["vicente", "rocafuerte", "importante", "proceso", "republicano"], "context": "Líder posterior. Se menciona su relación con Jacinto Bejarano en la página 6."},
    {"q": "¿Qué relación tuvo Guayaquil con Simón Bolívar tras 1820?", "a": "Solicitó apoyo militar y fue anexada a la Gran Colombia en 1822.", "keywords": ["simon", "bolivar", "apoyo", "anexada", "gran", "colombia"], "context": "Decisión política posterior. El material se centra en 1820, pero el contexto posterior es importante."},
    {"q": "¿Qué documento estableció las bases de la nueva organización política guayaquileña?", "a": "El Acta de Independencia", "keywords": ["acta", "independencia"], "context": "Fundamento legal. Revisa la página 5 del material."},
    {"q": "¿Es cierto que los conspiradores usaron claves y contraseñas para comunicarse?", "a": "True", "keywords": ["verdadero", "si", "claves", "contraseñas"], "context": "Seguridad de las reuniones. Justification: They used codes to keep meetings secret. El material describe las reuniones clandestinas."},
    {"q": "¿Qué consecuencia inmediata tuvo la independencia de Guayaquil en la costa ecuatoriana?", "a": "Estimuló la liberación de otras ciudades cercanas como Machala y Portoviejo.", "keywords": ["consecuencia", "liberacion", "machala", "portoviejo"], "context": "Expansión regional. Este efecto se describe en el material de estudio."},
    {"q": "Defina 'Provincia Libre de Guayaquil'.", "a": "Entidad autónoma que ejerció soberanía desde 1820 hasta su anexión.", "keywords": ["entidad", "autonoma", "soberania"], "context": "Experimento republicano. La página 5 del material describe el nuevo Estado."},
    {"q": "¿Cuál fue el papel de José de Villamil en la madrugada del 9 de octubre?", "a": "Coordinó la adhesión de tropas y facilitó el golpe.", "keywords": ["jose", "villamil", "coordinó", "tropas", "golpe"], "context": "Estratega civil. Revisa las páginas 1 y 7 del material."},
    {"q": "¿Quién pronunció las palabras '¡Somos libres!' el 9 de octubre?", "a": "León de Febres Cordero", "keywords": ["leon", "febres", "cordero"], "context": "Símbolo del grito libertario. Revisa la página 8 del material."},
    {"q": "¿Qué sucedió con las tropas realistas después del 9 de octubre?", "a": "Se rindieron sin gran resistencia.", "keywords": ["rindieron", "sin", "resistencia"], "context": "Colapso del poder español local. Se menciona en las páginas 7 y 8 del material."},
    {"q": "¿Qué relación tuvo Guayaquil con San Martín tras la independencia?", "a": "Fue visitada en 1822 en la célebre entrevista de Guayaquil.", "keywords": ["san martin", "entrevista"], "context": "Encuentro Bolívar–San Martín. Este evento es histórico y relevante."},
    {"q": "¿Es cierto que hubo participación femenina en la independencia de Guayaquil?", "a": "True", "keywords": ["verdadero", "si", "participacion", "femenina"], "context": "Mujeres apoyaron logística y moralmente. Justification: Women contributed with information, resources, and support. La página 3 del material menciona la participación de las damas Ponce de León."},
    {"q": "Mencione a dos mujeres que participaron en la independencia de Guayaquil.", "a": "Ana Garaycoa y Josefa de la Paz.", "keywords": ["ana", "garaycoa", "josefa", "paz"], "context": "Participación femenina. El material de estudio menciona la participación de damas guayaquileñas."},
    {"q": "¿Qué batallón extranjero se plegó a la causa independentista guayaquileña?", "a": "Tropas peruanas.", "keywords": ["tropas", "peruanas"], "context": "Soldados clave. Revisa la página 1 del material."},
    {"q": "¿Qué hizo la Junta de Gobierno para legitimar el nuevo orden?", "a": "Publicó el Acta y convocó a participación ciudadana.", "keywords": ["junta", "gobierno", "publicó", "acta"], "context": "Organización política. La página 5 del material describe la creación del nuevo gobierno."},
    {"q": "¿Qué tipo de gobierno se instauró en Guayaquil tras la independencia?", "a": "Una república provisional.", "keywords": ["republica", "provisional"], "context": "Modelo político. La página 5 del material describe el nuevo Estado."},
    {"q": "¿Es cierto que Olmedo fue presidente de la Junta hasta la anexión a la Gran Colombia?", "a": "True", "keywords": ["verdadero", "si", "olmedo", "presidente"], "context": "Liderazgo político estable. Justification: Olmedo presided the Junta until annexation. Revisa la página 5 del material."},
    {"q": "¿Qué significaba la frase 'la perla del Pacífico' aplicada a Guayaquil?", "a": "Su importancia económica y estratégica.", "keywords": ["perla", "pacifico", "importancia", "economica"], "context": "Valor geopolítico. Esta frase es un apodo histórico."},
    {"q": "¿Qué importancia tuvo el puerto de Guayaquil en la independencia?", "a": "Punto estratégico comercial y militar.", "keywords": ["puerto", "importancia", "comercial", "militar"], "context": "Control marítimo. Revisa la página 2 del material."},
    {"q": "Explique la diferencia entre independencia y autonomía en el caso de Guayaquil.", "a": "Independencia = ruptura con España; autonomía = autogobierno temporal.", "keywords": ["independencia", "autonomia", "ruptura", "españa"], "context": "Concepto político. La página 5 del material explica el concepto de 'Provincia Libre'."},
    {"q": "¿Es cierto que Guayaquil declaró su independencia inspirada por otros movimientos americanos?", "a": "True", "keywords": ["verdadero", "si", "inspirada", "movimientos"], "context": "Influencias de Caracas, Buenos Aires, etc. Justification: They were inspired by other Latin American revolutions. El material de estudio no lo niega."},
    {"q": "Quiénes integraron la primera Junta de Gobierno?", "a": "Olmedo, Villamil, Febres Cordero, Letamendi, etc.", "keywords": ["olmedo", "villamil", "febres", "letamendi", "junta"], "context": "Nombres fundacionales. Revisa las páginas 5 y 6 del material."},
    {"q": "¿Qué lema caracterizó la independencia de Guayaquil?", "a": "“Patria y Libertad”", "keywords": ["patria", "libertad", "lema"], "context": "Expresión del movimiento. Este lema es un símbolo común de la independencia."},
    {"q": "¿Qué territorio abarcaba la Provincia Libre de Guayaquil?", "a": "Actual costa sur del Ecuador.", "keywords": ["territorio", "costa", "sur", "ecuador"], "context": "Jurisdicción política. El material de estudio lo describe."},
    {"q": "¿Qué ciudades se unieron rápidamente tras la independencia de Guayaquil?", "a": "Machala, Portoviejo, Daule.", "keywords": ["machala", "portoviejo", "daule"], "context": "Expansión inmediata. El material de estudio lo describe."},
    {"q": "¿Qué decisión tomó la Junta sobre el sistema económico?", "a": "Mantener comercio libre y abierto.", "keywords": ["comercio", "libre", "abierto"], "context": "Continuidad económica. El material no lo menciona explícitamente, pero es una consecuencia lógica."},
    {"q": "Defina 'independencia sin derramamiento de sangre' en el caso de Guayaquil.", "a": "Logro político y militar sin enfrentamientos violentos significativos.", "keywords": ["independencia", "sin", "derramamiento", "sangre", "enfrentamientos"], "context": "Particularidad del proceso. La página 8 del material lo describe."},
    {"q": "¿Qué relación tuvo Guayaquil con Bolívar después de 1820?", "a": "Envió emisarios y pidió apoyo militar.", "keywords": ["bolivar", "apoyo", "militar", "emisarios"], "context": "Relación política. El material no lo menciona explícitamente, pero es un contexto histórico."},
    {"q": "¿Qué tema se trató en la entrevista de Guayaquil (1822)?", "a": "Futuro del Perú y de la Gran Colombia.", "keywords": ["futuro", "peru", "gran", "colombia"], "context": "Encuentro histórico. Es un evento histórico importante."},
    {"q": "¿Quién representaba la visión republicana en Guayaquil?", "a": "José Joaquín de Olmedo.", "keywords": ["jose", "joaquin", "olmedo", "republicana"], "context": "Intelectual y líder. Revisa la página 5 del material."},
    {"q": "¿Qué influencia tuvo la independencia de Guayaquil en el proceso continental?", "a": "Sirvió de base para campañas libertadoras en Perú.", "keywords": ["influencia", "base", "campañas", "peru"], "context": "Repercusión regional. La página 8 del material lo menciona."},
    {"q": "¿Es cierto que las élites comerciales apoyaron la independencia por interés económico?", "a": "True", "keywords": ["verdadero", "si", "elites", "comerciales", "interes", "economico"], "context": "Beneficio del libre comercio. Justification: Elites wanted independence to secure commercial benefits. El material de estudio lo menciona."},
    {"q": "¿Qué papel desempeñó la Iglesia durante la independencia de Guayaquil?", "a": "Algunos clérigos apoyaron, otros fueron neutrales.", "keywords": ["iglesia", "clerigos", "apoyaron", "neutrales"], "context": "Diversidad de posiciones. El material de estudio no lo niega."},
    {"q": "¿Qué significaba 'criollo' en la época de la independencia?", "a": "Descendiente de españoles nacido en América.", "keywords": ["criollo", "españoles", "nacido", "america"], "context": "Categoría social. Es un término de contexto histórico."},
    {"q": "¿Qué relación tuvo Guayaquil con Quito después de 1820?", "a": "Apoyo militar posterior en la campaña de Pichincha.", "keywords": ["quito", "apoyo", "militar", "pichincha"], "context": "Unidad de causa. La página 8 del material lo menciona."},
    {"q": "¿Es cierto que el general San Martín propuso que Guayaquil se anexara al Perú?", "a": "True", "keywords": ["verdadero", "si", "san", "martin", "anexara", "peru"], "context": "Diferencias en la entrevista. Justification: San Martín suggested annexation to Peru. Esto es un hecho histórico."},
    {"q": "¿Qué postura tomó Olmedo frente a la anexión?", "a": "Defendió la soberanía de Guayaquil.", "keywords": ["olmedo", "defendio", "soberania"], "context": "Nacionalismo local. La página 5 del material lo sugiere."},
    {"q": "¿Qué fue la 'Entrevista de Guayaquil'?", "a": "Reunión entre Bolívar y San Martín en 1822.", "keywords": ["entrevista", "guayaquil", "bolivar", "san", "martin"], "context": "Definición de campañas libertadoras. Es un evento histórico."},
    {"q": "¿Qué importancia tuvo Guayaquil en la campaña libertadora del Perú?", "a": "Base logística y militar.", "keywords": ["base", "logistica", "militar"], "context": "Punto de partida. La página 8 del material lo menciona."},
    {"q": "¿Qué tipo de soldados componían las milicias locales?", "a": "Pardos, criollos, campesinos.", "keywords": ["pardos", "criollos", "campesinos", "milicias"], "context": "Diversidad social. Revisa la página 4 del material."},
    {"q": "¿Es cierto que la independencia de Guayaquil influyó en la de Cuenca y Quito?", "a": "True", "keywords": ["verdadero", "si", "influyó", "cuenca", "quito"], "context": "Inspiración regional. Justification: Guayaquil's independence encouraged Cuenca and Quito. El material de estudio lo sugiere."},
    {"q": "¿Qué diferencia hubo entre la independencia de Guayaquil y la del resto del Ecuador?", "a": "Guayaquil fue pacífica, Quito y Cuenca requirieron batallas.", "keywords": ["pacifica", "quito", "cuenca", "batallas"], "context": "Particularidad. La página 8 del material lo describe como 'incruenta'."},
    {"q": "¿Quién fue el líder de la expedición libertadora enviada desde Guayaquil hacia Quito?", "a": "Antonio José de Sucre.", "keywords": ["antonio", "jose", "sucre", "lider", "expedicion"], "context": "General venezolano. La página 8 del material lo menciona."},
    {"q": "¿Qué batalla aseguró la independencia definitiva del actual Ecuador?", "a": "Batalla de Pichincha (1822).", "keywords": ["batalla", "pichincha"], "context": "Culminación militar. La página 4 del material lo menciona."},
    {"q": "¿Qué relación tuvo la independencia de Guayaquil con la de Pichincha?", "a": "Guayaquil fue la base desde donde partieron tropas para Quito.", "keywords": ["base", "tropas", "quito"], "context": "Conexión estratégica. La página 8 del material lo menciona."},
    {"q": "¿Qué significaba para Guayaquil ser anexada a la Gran Colombia?", "a": "Integrarse al proyecto bolivariano de unión.", "keywords": ["anexada", "gran", "colombia", "integrarse"], "context": "Decisión política. Es un hecho histórico."},
    {"q": "¿Qué fue la primera acción militar del ejército guayaquileño?", "a": "Luchar contra los españoles en Camino Real en 1820.", "keywords": ["luchar", "españoles", "camino", "real"], "context": "Primera acción. La información se encuentra en la página 8 del material de estudio."},
    {"q": "¿Quién fue el precursor del movimiento emancipador guayaquileño?", "a": "José de Antepara.", "keywords": ["jose", "antepara", "precursor"], "context": "Precursor. La información se encuentra en la página 8 del material de estudio."},
    {"q": "¿Cómo se conoce a la división militar de Guayaquil que fue a luchar contra los españoles?", "a": "La 'División Protectora de Quito'.", "keywords": ["division", "protectora", "quito"], "context": "División militar. La información se encuentra en la página 8 del material de estudio."},
    {"q": "¿Quién fue el líder del cuartel de artillería que fue apresado la noche del 8 de octubre?", "a": "León de Febres Cordero.", "keywords": ["leon", "febres", "cordero", "cuartel"], "context": "Lider del cuartel. La información se encuentra en la página 8 del material de estudio."},
    {"q": "¿Qué general ecuatoriano lideró las tropas guayaquileñas en las batallas de la independencia?", "a": "Antonio José de Sucre", "keywords": ["antonio", "jose", "sucre", "lider"], "context": "Liderazgo militar. Se menciona su liderazgo en las páginas 8 y 9 del material."},
    {"q": "¿Qué papel desempeñó el batallón de Granaderos de Reserva en el inicio de la independencia?", "a": "Su adhesión a la causa permitió un golpe sin derramamiento de sangre.", "keywords": ["batallon", "granaderos", "reserva", "sin", "derramamiento", "sangre"], "context": "Apoyo militar crucial. Se menciona en la página 1 del material de estudio."},
    {"q": "¿Cuál fue el principal documento legal que estableció el nuevo gobierno de Guayaquil?", "a": "El Acta de Independencia", "keywords": ["acta", "independencia", "documento"], "context": "Fundamento jurídico. Se menciona en la página 5 del material de estudio."},
    {"q": "¿Qué significado tuvo la expresión 'la aurora de la independencia' en el contexto de Guayaquil?", "a": "Marcó el inicio del proceso de emancipación en la región.", "keywords": ["aurora", "independencia", "inicio", "emancipacion"], "context": "Inicio del proceso. Se menciona en la página 8 del material de estudio."},
    {"q": "¿Qué batallones estaban acantonados en Guayaquil al momento de la independencia?", "a": "Granaderos de Reserva, Batallón de Pardos y Batallón de Daule.", "keywords": ["granaderos", "reserva", "batallon", "pardos", "batallon", "daule"], "context": "Fuerzas militares. Se mencionan en la página 1 del material de estudio."},
    {"q": "¿Por qué se conoce al 9 de octubre como el inicio del proceso de emancipación ecuatoriana?", "a": "Porque fue el primer territorio en consolidar su independencia del dominio español.", "keywords": ["primer", "territorio", "consolidar", "independencia", "dominio", "español"], "context": "Consolidación de la independencia. Se menciona en varias partes del documento."},
    {"q": "¿Quiénes se reunían en la casa de José de Villamil?", "a": "Líderes civiles y militares conspiradores.", "keywords": ["lideres", "civiles", "militares", "conspiradores", "villamil"], "context": "Conspiradores de la independencia. Se menciona en la página 7 del material de estudio."},
    {"q": "¿Qué hizo José de Villamil la noche del 1 de octubre en su casa?", "a": "Una reunión para planificar la independencia.", "keywords": ["reunion", "planificar", "independencia"], "context": "Planificación de la independencia. Se menciona en la página 7 del material de estudio."},
    {"q": "¿Cuál fue la respuesta de los militares españoles ante la insurrección?", "a": "Se rindieron sin oponer mayor resistencia.", "keywords": ["rindieron", "sin", "resistencia"], "context": "Reacción de los españoles. Se menciona en la página 8 del material de estudio."},
    {"q": "¿Qué rol jugó la 'División Protectora de Quito'?", "a": "Apoyar la liberación de la Sierra.", "keywords": ["division", "protectora", "quito", "apoyar", "liberacion"], "context": "División Protectora de Quito. Se menciona en la página 8 del material de estudio."},
]

# This function checks if the user's answer is close to the correct one using a similarity ratio
def is_correct(user_answer, keywords):
    # Sanitize user input by removing punctuation, extra spaces, and converting to lowercase
    user_answer = re.sub(r'[^\w\s]', '', user_answer).lower().strip()
    
    # Check for direct keyword matches
    for keyword in keywords:
        if keyword in user_answer:
            return True

    # If no direct match, calculate similarity ratio
    for keyword in keywords:
        # Check for individual words in the user's answer
        for user_word in user_answer.split():
            # A similarity ratio of 0.85 or higher is considered a match
            if SequenceMatcher(None, user_word, keyword).ratio() > 0.85:
                return True
    
    return False

# Initialize session state for the quiz
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "question_list" not in st.session_state:
    st.session_state.question_list = []
if "name_set" not in st.session_state:
    st.session_state.name_set = False
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

# This function resets the quiz state
def reset_quiz():
    st.session_state.score = 0
    st.session_state.current_question_index = 0
    st.session_state.question_list = random.sample(questions, 10)
    st.session_state.feedback = None
    st.session_state.user_answer = ""
    st.session_state.quiz_started = True
    st.rerun()

# Display the main title
st.title("📝 Práctica Concurso - La Forja de la Libertad de Guayaquil")

# Get user's name
if not st.session_state.name_set:
    name = st.text_input("¡Hola! Para empezar, por favor, dime tu nombre.")
    if name:
        st.session_state.name = name
        st.session_state.name_set = True
        st.session_state.quiz_started = False  # Reset quiz_started after setting the name
        st.rerun()
else:
    name = st.session_state.name
    st.subheader(f"¡Hola {name}! Empecemos con la preparación. 📚")

    if not st.session_state.quiz_started:
        if st.button("Iniciar Práctica"):
            reset_quiz()
    else:
        # Check if the quiz is finished
        if st.session_state.current_question_index >= 10:
            st.success(f"🎉 ¡Has completado la ronda! Tu puntaje es: {st.session_state.score}/10")
            if st.button("Empezar de Nuevo"):
                st.session_state.quiz_started = False
                st.rerun()
        else:
            # Display the current question
            current_question = st.session_state.question_list[st.session_state.current_question_index]

            st.write(f"**Pregunta {st.session_state.current_question_index + 1}/10:** {current_question['q']}")
            
            # Text input for the user's answer
            user_answer = st.text_input("Tu respuesta:", value=st.session_state.get("user_answer", ""), key="answer_input")

            # Handle the "Responder" button
            if st.button("Responder"):
                if is_correct(user_answer, current_question['keywords']):
                    st.session_state.score += 1
                    st.session_state.feedback = "correct"
                else:
                    st.session_state.feedback = "incorrect"
                
                st.session_state.user_answer = user_answer
                st.rerun()

            # Display feedback and the "Siguiente Pregunta" button
            if st.session_state.get("feedback"):
                if st.session_state.feedback == "correct":
                    st.success("✅ ¡Correcto! Tu respuesta es muy buena.")
                else:
                    st.error("❌ Incorrecto.")
                    st.write(f"La respuesta correcta era: **{current_question['a']}**")
                    st.info(f"📖 **Para profundizar, puedes revisar:** {current_question['context']}")

                if st.button("Siguiente Pregunta"):
                    st.session_state.current_question_index += 1
                    st.session_state.feedback = None
                    st.session_state.user_answer = ""
                    st.rerun()

            st.write("---")
            st.write(f"### Puntaje actual: {st.session_state.score}/{st.session_state.current_question_index}")
