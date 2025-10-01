import streamlit as st
import random
import re
from difflib import SequenceMatcher

# Banco de 80 preguntas sobre la Independencia de GuayaquiL
# NOTA: Se ha ajustado la lista de preguntas para que coincida con el material de estudio
# y se han incluido las palabras clave para una evaluación más flexible.
questions = [
    {"q": "¿Cuántos militares extranjeros estaban acantonados en Guayaquil al momento de la independencia?", "a": "1300", "keywords": ["1300", "mil", "trecientos", "mil trecientos"], "context": "Fuerzas realistas con guarniciones extranjeras en la ciudad. Puedes encontrar más detalles en la página 1 del material de estudio."},
    {"q": "¿Quién era el gobernador de Guayaquil en 1820?", "a": "Pascual Vivero", "keywords": ["pascual vivero", "vivero"], "context": "Autoridad española al mando del territorio. Esta información se encuentra en la página 3 del material de estudio."},
    {"q": "¿Qué se planeaba realizar la noche del 1 de octubre de 1820?", "a": "Una reunión en la casa de José Villamil para planificar la independencia", "keywords": ["reunion", "casa", "villamil", "planificar", "independencia"], "context": "Reuniones clandestinas de los patriotas. Revisa la página 7 del material para más detalles."},
    {"q": "¿Quién fue el encargado de convencer a los soldados peruanos para unirse a la independencia?", "a": "José de Villamil", "keywords": ["jose", "villamil", "jose villamil"], "context": "Negociaciones con tropas del batallón peruano. La información está en la página 1 del material de estudio."},
    {"q": "¿Qué batallón formaban los pardos de Guayaquil?", "a": "El Batallón de Pardos", "keywords": ["batallon", "pardos", "pardos de guayaquil"], "context": "Unidad militar compuesta por mestizos, mulatos y afrodescendientes. Revisa la página 4 del material."},
    {"q": "¿Es cierto que el Batallón Daule estaba formado por 150 hombres?", "a": "True", "keywords": ["verdadero", "si", "150", "ciento cincuenta"], "context": "José Villamil mencionó 150 hombres de milicia en el escuadrón de caballería de Daule. Puedes verificarlo en la página 1 del material."},
    {"q": "¿Es verdadero que los soldados peruanos se unieron a la independencia porque se les prometió el pago de salarios atrasados?", "a": "True", "keywords": ["verdadero", "si", "pago", "salarios", "atrasados"], "context": "Promesa de pago fue decisiva. La información está en la página 4 del material."},
    {"q": "¿Es cierto que los españoles afirmaban que las milicias contaban con 1.000 hombres?", "a": "True", "keywords": ["verdadero", "si", "1000", "mil"], "context": "Cifra inflada según fuentes españolas. Revisa la página 3 del material."},
    {"q": "¿Es correcto afirmar que Guayaquil se convirtió en República al proclamarse la independencia?", "a": "True", "keywords": ["verdadero", "si", "republica", "provincia libre"], "context": "Se conformó una Junta de Gobierno, estableciendo un gobierno republicano provisional. Puedes encontrar más detalles en la página 5 del material."},
    {"q": "¿Es cierto que el 9 de octubre de 1820 la ciudad de Guayaquil permaneció indiferente a la proclamación?", "a": "False", "keywords": ["falso", "no", "apoyo", "celebro"], "context": "El pueblo apoyó y celebró activamente. El material de estudio indica que hubo celebración popular."},
    {"q": "¿Qué motivaciones llevaron a los guayaquileños a buscar la independencia?", "a": "Autonomía, cansancio del dominio español, apoyo militar y civil.", "keywords": ["autonomia", "cansancio", "dominio", "español", "apoyo"], "context": "Sentimientos independentistas generales en Hispanoamérica. El material de estudio describe estos elementos."},
    {"q": "Explique por qué fue clave la participación del Batallón de Granaderos de Reserva en la independencia de Guayaquil.", "a": "Su apoyo aseguró la victoria sin mayor resistencia.", "keywords": ["batallon", "granaderos", "reserva", "victoria", "resistencia"], "context": "Decisiva para evitar derramamiento de sangre. La información se encuentra en la página 1 del material de estudio."},
    {"q": "¿Qué papel desempeñó José Joaquín de Olmedo tras la proclamación de independencia?", "a": "Fue nombrado presidente de la Junta de Gobierno.", "keywords": ["jose joaquin", "olmedo", "presidente", "junta"], "context": "Liderazgo político inmediato. Revisa la página 5 del material."},
    {"q": "¿Por qué se considera la independencia de Guayaquil un movimiento 'cívico-militar'?", "a": "Participaron militares criollos y ciudadanos civiles.", "keywords": ["civico", "militar", "militares", "civiles"], "context": "Colaboración de ambos sectores. El material lo describe en varias partes."},
    {"q": "Mencione dos consecuencias inmediatas del 9 de octubre de 1820 en Guayaquil.", "a": "Se proclamó la independencia y se instauró la Junta de Gobierno.", "keywords": ["proclamó", "independencia", "instauró", "junta", "gobierno"], "context": "Transformación política inmediata. Revisa las páginas 5 y 6 del material."},
    {"q": "Según los españoles, ¿cuántos hombres integraban las milicias de Guayaquil?", "a": "1.000", "keywords": ["1000", "mil", "hombres"], "context": "Cifra española. Revisa la página 3 del material de estudio."},
    {"q": "Según José Villamil, ¿cuántos eran en realidad los hombres de milicia?", "a": "200", "keywords": ["200", "doscientos"], "context": "Testimonio del patriota. La información está en la página 3 del material de estudio."},
    {"q": "¿Qué diferencia existe entre las cifras de milicianos según fuentes españolas y las de Villamil?", "a": "Españoles inflaban a 1.000; Villamil reducía a 200.", "keywords": ["diferencia", "1000", "200"], "context": "Contradicción en fuentes. Revisa la página 3 del material de estudio para más detalles."},
    {"q": "¿Qué significaba 'Batallón de Pardos' en el contexto de la independencia de Guayaquil?", "a": "Unidad compuesta por mestizos, mulatos y afrodescendientes.", "keywords": ["batallon", "pardos", "mestizos", "mulatos"], "context": "División militar colonial. Se explica en la página 4 del material."},
    {"q": "Explique qué se entiende por 'Junta de Gobierno' en el proceso independentista de Guayaquil.", "a": "Órgano político provisional presidido por Olmedo.", "keywords": ["junta", "gobierno", "organo", "olmedo", "provisional"], "context": "Institución republicana inicial. Revisa la página 5 del material."},
    {"q": "¿Qué fecha exacta se proclamó la independencia de Guayaquil?", "a": "9 de octubre de 1820", "keywords": ["9", "nueve", "octubre", "1820"], "context": "Hito principal de la gesta libertaria. La fecha está en todo el material de estudio."},
    {"q": "¿Qué batallón se sublevó en la madrugada del 9 de octubre?", "a": "El batallón Granaderos de Reserva", "keywords": ["batallon", "granaderos", "reserva"], "context": "Protagonistas militares. Revisa la página 1 del material."},
    {"q": "¿Qué hacían los patriotas antes de iniciar la insurrección para no ser descubiertos?", "a": "Se reunían secretamente en casas particulares.", "keywords": ["reunian", "secretamente", "casas", "particulares"], "context": "Reuniones clandestinas. Revisa la página 7 del material."},
    {"q": "¿Quién escribió la proclama de independencia de Guayaquil?", "a": "José Joaquín de Olmedo", "keywords": ["jose joaquin", "olmedo", "proclama"], "context": "Intelectual de la independencia. Se menciona en la página 5 del material."},
    {"q": "¿Qué personaje fue clave como enlace entre criollos y tropas extranjeras?", "a": "José de Villamil", "keywords": ["jose", "villamil", "enlace", "criollos", "tropas"], "context": "Diplomacia insurgente. Revisa las páginas 1 y 7 del material."},
    {"q": "¿Es cierto que la independencia de Guayaquil se logró sin derramamiento de sangre?", "a": "True", "keywords": ["verdadero", "no", "hubo", "tantas", "victimas"], "context": "Según el material (p. 8), sí hubo derramamiento de sangre, pero no tantas como pudieron darse. El concepto de 'incruenta' se usa, aunque el material indica que sí hubo víctimas."},
    {"q": "¿Es verdadero que la Junta de Gobierno de Guayaquil reconoció inmediatamente la autoridad del virrey de Lima?", "a": "False", "keywords": ["falso", "no", "virrey"], "context": "Se proclamó gobierno propio. La página 5 del material explica la creación de un nuevo Estado."},
    {"q": "¿Qué diferencia existía entre el movimiento de Quito (1809) y el de Guayaquil (1820)?", "a": "Quito fue sofocado y Guayaquil consolidó su independencia.", "keywords": ["quito", "sofocado", "guayaquil", "consolidó", "independencia"], "context": "Resultados distintos. Puedes revisar las páginas 1, 5 y 8 del material para ver el éxito de la independencia de Guayaquil."},
    {"q": "¿Qué significaba para Guayaquil ser 'Provincia Libre'?", "a": "Autogobierno y soberanía temporal.", "keywords": ["provincia", "libre", "autogobierno", "soberania"], "context": "Concepto político inicial. Revisa la página 5 del material."},
    {"q": "¿Quién fue el jefe militar del movimiento independentista de Guayaquil?", "a": "León de Febres Cordero", "keywords": ["leon", "febres", "cordero"], "context": "Conspirador clave. Su rol se menciona en las páginas 7 y 8 del material."},
    {"q": "¿Qué militares participaron además de Febres Cordero?", "a": "Luis Urdaneta, Miguel de Letamendi.", "keywords": ["luis", "urdaneta", "miguel", "letamendi"], "context": "Red de oficiales. El material de estudio menciona a varios de los conspiradores."},
    {"q": "Explique por qué la fecha del 9 de octubre es considerada 'aurora de la independencia' del Ecuador.", "a": "Porque marcó el inicio definitivo del proceso libertario en la región.", "keywords": ["aurora", "independencia", "inicio", "proceso", "definitivo"], "context": "Significado histórico. El material de estudio enfatiza el rol de Guayaquil como punto de partida."},
    {"q": "¿Es cierto que el gobernador Pascual Vivero fue arrestado durante la madrugada del 9 de octubre?", "a": "True", "keywords": ["verdadero", "si", "pascual", "vivero", "arrestado"], "context": "Caída del poder español. Este evento se menciona en el material de estudio."},
    {"q": "¿Qué documento estableció las bases de la nueva organización política guayaquileña?", "a": "El Acta de Independencia", "keywords": ["acta", "independencia"], "context": "Fundamento legal. Revisa la página 5 del material."},
    {"q": "¿Qué batallón extranjero se plegó a la causa independentista guayaquileña?", "a": "Tropas peruanas (Batallón Granaderos de Reserva, compuesto mayormente por peruanos)", "keywords": ["tropas", "peruanas", "granaderos", "reserva"], "context": "Soldados clave. Revisa la página 1 del material."},
    {"q": "¿Qué hizo la Junta de Gobierno para legitimar el nuevo orden?", "a": "Publicó el Acta y convocó a participación ciudadana.", "keywords": ["junta", "gobierno", "publicó", "acta", "convocó"], "context": "Organización política. La página 5 del material describe la creación del nuevo gobierno."},
    {"q": "¿Qué tipo de gobierno se instauró en Guayaquil tras la independencia?", "a": "Una república provisional.", "keywords": ["republica", "provisional"], "context": "Modelo político. La página 5 del material describe el nuevo Estado."},
    {"q": "¿Quiénes integraron la primera Junta de Gobierno?", "a": "Olmedo, Villamil, Febres Cordero, Letamendi (y otros vocales).", "keywords": ["olmedo", "villamil", "febres", "letamendi", "junta"], "context": "Nombres fundacionales. Revisa las páginas 5 y 6 del material."},
    {"q": "¿Qué ciudades se unieron rápidamente tras la independencia de Guayaquil?", "a": "Machala, Portoviejo, Daule.", "keywords": ["machala", "portoviejo", "daule"], "context": "Expansión inmediata. El material de estudio lo describe."},
    {"q": "¿Qué tipo de soldados componían las milicias locales?", "a": "Pardos, criollos, campesinos (principalmente mestizos, mulatos y afrodescendientes en el Batallón de Pardos).", "keywords": ["pardos", "criollos", "campesinos", "milicias", "mestizos", "mulatos"], "context": "Diversidad social. Revisa la página 4 del material."},
    {"q": "¿Es cierto que la independencia de Guayaquil influyó en la de Cuenca y Quito?", "a": "True", "keywords": ["verdadero", "si", "influyó", "cuenca", "quito"], "context": "Inspiración regional. El material de estudio lo sugiere."},
    {"q": "¿Qué fue la primera acción militar del ejército guayaquileño?", "a": "Luchar contra los españoles que estaban acantonados en un punto llamado \"Camino Real\" en el mes de noviembre de 1820.", "keywords": ["luchar", "españoles", "camino", "real", "noviembre", "1820"], "context": "Primera acción. La información se encuentra en la página 8 del material de estudio."},
    {"q": "¿A qué prócer de la independencia se le conoce como el precursor del movimiento emancipador guayaquileño?", "a": "Al prócer José de Antepara.", "keywords": ["jose", "antepara", "precursor"], "context": "Precursor. La información se encuentra en la página 8 del material de estudio."},
    {"q": "¿Cómo se conoce a la división militar de Guayaquil que fue a luchar contra los españoles?", "a": "La 'División Protectora de Quito'.", "keywords": ["division", "protectora", "quito"], "context": "División militar. La información se encuentra en la página 8 del material de estudio."},
    {"q": "¿Qué batalla aseguró la independencia definitiva del actual Ecuador?", "a": "Batalla de Pichincha (1822).", "keywords": ["batalla", "pichincha"], "context": "Culminación militar. La página 4 del material lo menciona."},
    {"q": "¿Qué relación tuvo la independencia de Guayaquil con la de Pichincha?", "a": "Guayaquil fue la base desde donde partieron tropas para Quito.", "keywords": ["base", "tropas", "quito"], "context": "Conexión estratégica. La página 8 del material lo menciona."},
    {"q": "¿Quiénes se reunían en la casa de José de Villamil?", "a": "Líderes civiles y militares conspiradores.", "keywords": ["lideres", "civiles", "militares", "conspiradores", "villamil"], "context": "Conspiradores de la independencia. Se menciona en la página 7 del material de estudio."},
    {"q": "¿Cuál fue la respuesta de los militares españoles ante la insurrección?", "a": "Se rindieron sin oponer mayor resistencia.", "keywords": ["rindieron", "sin", "resistencia"], "context": "Reacción de los españoles. Se menciona en la página 8 del material de estudio."},
    {"q": "¿Qué dio a conocer Gregorio Escobedo la tarde del 8 de octubre en la casa de Villamil?", "a": "Que la revolución sería incruenta y que todo estaba conversado para que no hubiera víctimas.", "keywords": ["gregorio", "escobedo", "incruenta", "conversado", "victimas"], "context": "Plan de insurrección. Se menciona en la página 8 del material de estudio."},
    {"q": "¿Cuándo y a qué hora cayó el primer cuartel tomado por los patriotas?", "a": "A las 11 de la noche del 8 de octubre y fue la brigada de artillería.", "keywords": ["11", "noche", "8", "octubre", "artilleria"], "context": "Primer cuartel tomado. Se menciona en la página 8 del material de estudio."},
    {"q": "¿Qué batallones estaban acantonados en Guayaquil al momento de la independencia?", "a": "Granaderos de Reserva, Batallón de Pardos y Escuadrón de Caballería de Daule.", "keywords": ["granaderos", "reserva", "pardos", "caballeria", "daule"], "context": "Fuerzas militares. Se mencionan en la página 1 del material de estudio."},
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
    # Aseguramos que haya al menos 10 preguntas en el banco. Si hay más, toma 10 al azar.
    num_questions = min(10, len(questions))
    st.session_state.question_list = random.sample(questions, num_questions)
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
        total_questions = len(st.session_state.question_list)
        if st.session_state.current_question_index >= total_questions:
            st.success(f"🎉 ¡Has completado la ronda! Tu puntaje es: {st.session_state.score}/{total_questions}")
            if st.button("Empezar de Nuevo"):
                st.session_state.quiz_started = False
                st.rerun()
        else:
            # Display the current question
            current_question = st.session_state.question_list[st.session_state.current_question_index]

            st.write(f"**Pregunta {st.session_state.current_question_index + 1}/{total_questions}:** {current_question['q']}")
            
            # Text input for the user's answer
            # Use a unique key based on the index to ensure proper reset on "Siguiente"
            user_answer = st.text_input("Tu respuesta:", value=st.session_state.get("user_answer", ""), key=f"answer_input_{st.session_state.current_question_index}")

            # Handle the "Responder" button
            if st.button("Responder", key=f"btn_respond_{st.session_state.current_question_index}"):
                if user_answer.strip() == "":
                    st.warning("Por favor, ingresa una respuesta antes de continuar.")
                else:
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

                if st.button("Siguiente Pregunta", key=f"btn_next_{st.session_state.current_question_index}"):
                    st.session_state.current_question_index += 1
                    st.session_state.feedback = None
                    # Clear the user answer state for the next question
                    st.session_state.user_answer = "" 
                    st.rerun()

            st.write("---")
            st.write(f"### Puntaje actual: {st.session_state.score}/{st.session_state.current_question_index}")

