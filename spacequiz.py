#!/usr/bin/env python3
"""
ESA Space Challenge
A self-contained Tkinter quiz for public outreach events.\n\nEach prize value can contain multiple questions; one is selected randomly\nfrom each value whenever a new game starts.

Run:
    python esa_space_quiz.py

Controls:
    F11     Toggle full screen
    Escape  Leave full screen
    R       Restart quiz

No external images or packages are required.
"""

import math
import random
import tkinter as tk
from tkinter import messagebox

UI_TEXT = {'en': {'subtitle': 'From Earth observation to the outer Solar System',
        'questions': 'QUESTIONS',
        'start': 'START THE MISSION',
        'controls': 'F11: full screen   •   Esc: exit full screen   •   R: restart',
        'ladder': 'PRIZE LADDER',
        'question': 'Question {n} of {total}  •  {prize}',
        'correct_answers': 'Correct answers: {correct}   •   Current score: {score}',
        'correct': 'CORRECT!',
        'wrong': 'NOT THIS TIME',
        'answer_is': 'The answer is {letter}: {answer}',
        'fun_fact': 'FUN FACT',
        'final': 'SEE FINAL RESULT',
        'next': 'NEXT QUESTION',
        'complete': 'MISSION COMPLETE',
        'correct_label': 'CORRECT ANSWERS',
        'score_label': 'QUIZ SCORE',
        'again': 'PLAY AGAIN',
        'exit': 'EXIT',
        'thanks': 'Thank you for exploring Earth and space with ESA!',
        'choose': 'SELECT YOUR LANGUAGE'},
 'it': {'subtitle': 'Dall’osservazione della Terra al Sistema Solare esterno',
        'questions': 'DOMANDE',
        'start': 'INIZIA LA MISSIONE',
        'controls': 'F11: schermo intero   •   Esc: esci dallo schermo intero   •   R: ricomincia',
        'ladder': 'SCALA DEI PREMI',
        'question': 'Domanda {n} di {total}  •  {prize}',
        'correct_answers': 'Risposte corrette: {correct}   •   Punteggio attuale: {score}',
        'correct': 'CORRETTO!',
        'wrong': 'NON QUESTA VOLTA',
        'answer_is': 'La risposta è {letter}: {answer}',
        'fun_fact': 'CURIOSITÀ',
        'final': 'VEDI IL RISULTATO FINALE',
        'next': 'DOMANDA SUCCESSIVA',
        'complete': 'MISSIONE COMPLETATA',
        'correct_label': 'RISPOSTE CORRETTE',
        'score_label': 'PUNTEGGIO QUIZ',
        'again': 'GIOCA ANCORA',
        'exit': 'ESCI',
        'thanks': 'Grazie per aver esplorato la Terra e lo spazio con l’ESA!',
        'choose': 'SELEZIONA LA LINGUA'},
 'de': {'subtitle': 'Von der Erdbeobachtung bis ins äußere Sonnensystem',
        'questions': 'FRAGEN',
        'start': 'MISSION STARTEN',
        'controls': 'F11: Vollbild   •   Esc: Vollbild verlassen   •   R: Neustart',
        'ladder': 'GEWINNLEITER',
        'question': 'Frage {n} von {total}  •  {prize}',
        'correct_answers': 'Richtige Antworten: {correct}   •   Aktueller Punktestand: {score}',
        'correct': 'RICHTIG!',
        'wrong': 'DIESMAL NICHT',
        'answer_is': 'Die Antwort ist {letter}: {answer}',
        'fun_fact': 'WISSENSWERT',
        'final': 'ENDERGEBNIS ANZEIGEN',
        'next': 'NÄCHSTE FRAGE',
        'complete': 'MISSION ABGESCHLOSSEN',
        'correct_label': 'RICHTIGE ANTWORTEN',
        'score_label': 'QUIZ-PUNKTZAHL',
        'again': 'NOCH EINMAL',
        'exit': 'BEENDEN',
        'thanks': 'Danke, dass du mit der ESA Erde und Weltraum erkundet hast!',
        'choose': 'SPRACHE AUSWÄHLEN'},
 'fr': {'subtitle': 'De l’observation de la Terre aux confins du Système solaire',
        'questions': 'QUESTIONS',
        'start': 'LANCER LA MISSION',
        'controls': 'F11 : plein écran   •   Échap : quitter le plein écran   •   R : recommencer',
        'ladder': 'ÉCHELLE DES GAINS',
        'question': 'Question {n} sur {total}  •  {prize}',
        'correct_answers': 'Bonnes réponses : {correct}   •   Score actuel : {score}',
        'correct': 'CORRECT !',
        'wrong': 'PAS CETTE FOIS',
        'answer_is': 'La réponse est {letter} : {answer}',
        'fun_fact': 'LE SAVIEZ-VOUS ?',
        'final': 'VOIR LE RÉSULTAT FINAL',
        'next': 'QUESTION SUIVANTE',
        'complete': 'MISSION ACCOMPLIE',
        'correct_label': 'BONNES RÉPONSES',
        'score_label': 'SCORE DU QUIZ',
        'again': 'REJOUER',
        'exit': 'QUITTER',
        'thanks': 'Merci d’avoir exploré la Terre et l’espace avec l’ESA !',
        'choose': 'CHOISISSEZ LA LANGUE'},
 'es': {'subtitle': 'De la observación de la Tierra al Sistema Solar exterior',
        'questions': 'PREGUNTAS',
        'start': 'INICIAR LA MISIÓN',
        'controls': 'F11: pantalla completa   •   Esc: salir de pantalla completa   •   R: reiniciar',
        'ladder': 'ESCALA DE PREMIOS',
        'question': 'Pregunta {n} de {total}  •  {prize}',
        'correct_answers': 'Respuestas correctas: {correct}   •   Puntuación actual: {score}',
        'correct': '¡CORRECTO!',
        'wrong': 'ESTA VEZ NO',
        'answer_is': 'La respuesta es {letter}: {answer}',
        'fun_fact': 'DATO CURIOSO',
        'final': 'VER RESULTADO FINAL',
        'next': 'SIGUIENTE PREGUNTA',
        'complete': 'MISIÓN COMPLETADA',
        'correct_label': 'RESPUESTAS CORRECTAS',
        'score_label': 'PUNTUACIÓN',
        'again': 'JUGAR DE NUEVO',
        'exit': 'SALIR',
        'thanks': '¡Gracias por explorar la Tierra y el espacio con la ESA!',
        'choose': 'SELECCIONA EL IDIOMA'}}

LOCALIZED_QUESTION_BANKS = {
    'en': {
        "€100": [
            {
                "question": "What does ESA stand for?",
                "answers": ["European Science Alliance", "European Satellite Agency", "European Space Agency", "Europe Space Association"],
                "correct": 2,
                "fact": "ESA brings European countries together to explore space and use space technology for the benefit of people on Earth.",
            },
            {
                "question": "Among other what does ESA primarily study and explore?",
                "answers": ["The oceans", "Space and Earth from space", "Earth's underground", "All of the above"],
                "correct": 3,
                "fact": "ESA develops and operates Space missions that study Earth, including its underground composition and interior strictures, the Solar System and the wider Universe.",
            },
            {
                "question": "What is the main purpose of ESA?",
                "answers": ["To promote Space research, technology and applications", "To build airplanes", "To operate airports", "To provide weather forecasts"],
                "correct": 0,
                "fact": "ESA's purpose shall be to provide for, and to promote, for exclusively peaceful purposes, cooperation among European States in space research and technology",
            },
            {
                "question": "What is ESA?",
                "answers": ["A university", "A European organization", "A private company", "An airline"],
                "correct": 0,
                "fact": "ESA stands for European Space Agency, an international organization dedicated to shape the development of Europe’s Space capability and ensure that investment in space continues to deliver benefits to the citizens of Europe and the world.",
            },
            {
                "question": "Does ESA work with astronauts?",
                "answers": ["Yes, with ESA astronauts", "No, but it works with Pilots", "Yes, but only with NASA astronauts", "No, it works only with Scientists on Earth"],
                "correct": 0,
                "fact": "ESA trains and maintains a Team of Astronauts coming from different European coutries to explore Space.",
            },
            {
                "question": "Which is an area of ESA's work?",
                "answers": ["Space technology", "Fascion design", "Food production", "Road transport"],
                "correct": 0,
                "fact": "ESA's purpose shall be to provide for, and to promote, for exclusively peaceful purposes, cooperation among European States in space research and technology",
            },
        ],
        "€200": [
            {
                "question": "Which planet is known as the ‘Red Planet’?",
                "answers": ["Venus", "Mars", "Jupiter", "Mercury"],
                "correct": 1,
                "fact": "Mars looks reddish because iron minerals in its soil have oxidised, a process rather like rusting.",
            },
            {
                "question": "Which planet is the largest in our Solar System?",
                "answers": ["Earth", "Saturn", "Jupiter", "Neptune"],
                "correct": 2,
                "fact": "Jupiter is the largest planet in the Solar System, with a diameter more than 11 times that of Earth.",
            },
            {
                "question": "Which planet is famous for its prominent ring system?",
                "answers": ["Mars", "Saturn", "Venus", "Mercury"],
                "correct": 1,
                "fact": "Saturn's rings are made mainly of countless pieces of ice and rocky material.",
            },
            {
                "question": "Which planet is closest to the Sun?",
                "answers": ["Venus", "Earth", "Mercury", "Mars"],
                "correct": 2,
                "fact": "Mercury is the innermost planet and completes an orbit around the Sun in about 88 Earth days.",
            },
            {
                "question": "Which planet is sometimes called Earth's sister planet because of its similar size?",
                "answers": ["Jupiter", "Venus", "Mars", "Neptune"],
                "correct": 1,
                "fact": "Venus is similar to Earth in size and composition, although its surface environment is extremely different.",
            },
            {
                "question": "What is the name of the galaxy containing our Solar System?",
                "answers": ["Andromeda", "The Milky Way", "Whirlpool", "Sombrero"],
                "correct": 1,
                "fact": "Our Solar System is located in the Milky Way, a barred spiral galaxy containing hundreds of billions of stars.",
            },
        ],
        "€500": [
            {
                "question": "What are Earth-observation satellites mainly used for?",
                "answers": ["Weather forecasting only", "Monitoring Earth and environmental change", "Broadcasting television only", "Taking holiday photographs"],
                "correct": 1,
                "fact": "Satellite data can help monitor forests, sea ice, air quality, floods, fires, crops and many other changes on our planet.",
            },
            {
                "question": "What can satellites help scientists monitor over large areas?",
                "answers": ["Forest changes", "Only individual houses", "Only underground caves", "Nothing on Earth's surface"],
                "correct": 0,
                "fact": "Earth-observation satellites can repeatedly survey large areas, helping track changes in forests, agriculture and ecosystems.",
            },
            {
                "question": "Why are satellites useful for observing remote parts of Earth?",
                "answers": ["They can observe large areas from orbit", "They never need instruments", "They only work over cities", "They replace all ground measurements"],
                "correct": 0,
                "fact": "Satellites can provide repeated observations of places that are difficult or dangerous to reach from the ground.",
            },
            {
                "question": "Which event can Earth-observation satellites help monitor?",
                "answers": ["Flooding", "Only solar eclipses", "Only meteor showers", "Only spacecraft launches"],
                "correct": 0,
                "fact": "Satellite observations can help map flooded areas and support monitoring before, during and after major floods.",
            },
            {
                "question": "Which of these can satellite observations help monitor in the ocean?",
                "answers": ["Sea-ice extent", "Only fish inside individual nets", "Only ships at harbours", "Nothing"],
                "correct": 0,
                "fact": "Satellite observations can track sea ice and many other large-scale ocean and coastal changes.",
            },
            {
                "question": "What is one advantage of observing Earth from space?",
                "answers": ["Global or regional coverage", "No data processing is needed", "Clouds can never affect observations", "Every satellite sees everything"],
                "correct": 0,
                "fact": "Different satellite instruments provide broad coverage and repeated measurements that complement observations made from the ground.",
            },
        ],
        "€1,200": [
            {
                "question": "What is the name of the European family of Earth-observation missions used by the Copernicus programme?",
                "answers": ["Galileo", "Sentinel", "Voyager", "Kepler"],
                "correct": 1,
                "fact": "The Sentinel missions act like different sets of eyes. Some use radar, while others observe land, oceans or the atmosphere.",
            },
            {
                "question": "Which Copernicus Sentinel mission uses radar to observe Earth?",
                "answers": ["Sentinel-1", "Sentinel-6", "Sentinel-5P", "Sentinel-2"],
                "correct": 0,
                "fact": "Sentinel-1 uses radar, allowing it to observe Earth's surface day and night and through cloud cover.",
            },
            {
                "question": "Which Sentinel mission is particularly associated with detailed land-surface imagery?",
                "answers": ["Sentinel-2", "Sentinel-3", "Sentinel-5P", "Sentinel-6"],
                "correct": 0,
                "fact": "Sentinel-2 provides high-resolution optical imagery useful for studying vegetation, land cover and many other surface features.",
            },
            {
                "question": "What is Copernicus?",
                "answers": ["Europe's Earth-observation programme", "A Mars rover", "A type of rocket engine", "A star catalogue"],
                "correct": 0,
                "fact": "Copernicus is the European Union's Earth-observation programme, using satellites and other sources to provide environmental information.",
            },
            {
                "question": "Why can radar satellites be useful during cloudy weather?",
                "answers": ["Radar can observe through clouds in many situations", "Radar turns clouds into clear skies", "Radar only works indoors", "Radar cannot detect Earth's surface"],
                "correct": 0,
                "fact": "Synthetic-aperture radar can collect useful observations regardless of daylight and can often see through cloud cover.",
            },
            {
                "question": "Which type of information can Sentinel missions provide?",
                "answers": ["Land, ocean and atmosphere observations", "Only photographs of astronauts", "Only radio broadcasts", "Only observations of the Moon"],
                "correct": 0,
                "fact": "Different Sentinel missions are designed for different environmental measurements, covering land, oceans and the atmosphere.",
            },
        ],
        "€2,000": [
            {
                "question": "Which ESA mission placed the Philae lander on a comet in 2014?",
                "answers": ["Gaia", "Rosetta", "Euclid", "Solar Orbiter"],
                "correct": 1,
                "fact": "Philae bounced after its first touchdown on Comet 67P. In the comet’s extremely weak gravity, even a gentle bounce became a dramatic journey.",
            },
            {
                "question": "What was the name of the comet visited by ESA's Rosetta mission?",
                "answers": ["Halley", "67P/Churyumov-Gerasimenko", "Hale-Bopp", "Shoemaker-Levy 9"],
                "correct": 1,
                "fact": "Rosetta travelled to and studied Comet 67P/Churyumov-Gerasimenko, orbiting it for more than two years.",
            },
            {
                "question": "What was Philae?",
                "answers": ["A lander", "A telescope", "A rocket", "A communications satellite"],
                "correct": 0,
                "fact": "Philae was a small robotic lander carried to Comet 67P by ESA's Rosetta spacecraft.",
            },
            {
                "question": "What makes landing on a small comet especially challenging?",
                "answers": ["Very weak gravity", "Too much oxygen", "A thick atmosphere", "Strong ocean currents"],
                "correct": 0,
                "fact": "A small comet has extremely weak gravity, making it difficult for a lander to stay attached to the surface.",
            },
            {
                "question": "How many ESA Astonauts went to Space from September 2021 to September 2026?",
                "answers": ["6", "20", "1", "None"],
                "correct": 0,
                "fact": "From the foundation of ESA, a total of 27 individual astronauts have traveled into space from different European Countries.",
            },
            {
                "question": "What was a major scientific goal of Rosetta?",
                "answers": ["To study a comet in detail", "To land humans on Mars", "To map Earth's oceans", "To observe the Sun's poles"],
                "correct": 0,
                "fact": "Rosetta studied the composition, structure and activity of Comet 67P to improve our understanding of comets and the early Solar System.",
            },
        ],
        "€4,000": [
            {
                "question": "ESA’s Gaia mission was designed to create an extraordinarily precise map of what?",
                "answers": ["Earth’s oceans", "The Moon’s craters", "The Milky Way galaxy", "Mars’s volcanoes"],
                "correct": 2,
                "fact": "By measuring the positions and motions of stars, Gaia helps astronomers investigate the history and structure of our galaxy.",
            },
            {
                "question": "What does Gaia measure very precisely for stars?",
                "answers": ["Positions and motions", "Their smell", "Their surface temperature only", "Their weather forecasts"],
                "correct": 0,
                "fact": "Gaia's astrometric measurements reveal how stars are positioned and moving through the Milky Way.",
            },
            {
                "question": "Which kind of object is Gaia primarily surveying?",
                "answers": ["Stars", "Volcanoes", "Clouds", "Oceans"],
                "correct": 0,
                "fact": "Gaia was designed to survey enormous numbers of stars and build a precise three-dimensional picture of the Milky Way.",
            },
            {
                "question": "Why are stellar motions useful to astronomers?",
                "answers": ["They reveal information about the Milky Way's structure and history", "They predict Earth's weather", "They control spacecraft directly", "They create new stars"],
                "correct": 0,
                "fact": "The positions and motions of stars contain clues about how our galaxy formed and evolved.",
            },
            {
                "question": "Which part of the electromagnetic spectrum does Gaia use for its main astrometric measurements?",
                "answers": ["Visible light", "Radio only", "X-rays only", "Gamma rays only"],
                "correct": 0,
                "fact": "Gaia operates primarily as an optical astrometry mission, measuring stellar positions and motions with extraordinary precision.",
            },
            {
                "question": "What can a detailed map of the Milky Way help scientists investigate?",
                "answers": ["The galaxy's formation and evolution", "The exact weather tomorrow", "Ocean tides on Jupiter", "The colour of Earth's clouds"],
                "correct": 0,
                "fact": "A precise stellar map helps researchers reconstruct the structure, dynamics and history of our galaxy.",
            },
        ],
        "€8,000": [
            {
                "question": "Which ESA-led mission studies the Sun and is designed to observe its polar regions?",
                "answers": ["Solar Orbiter", "JUICE", "Hera", "BepiColombo"],
                "correct": 0,
                "fact": "The Sun’s poles are difficult to see from Earth. Solar Orbiter uses planetary flybys to tilt its orbit and obtain a better view.",
            },
            {
                "question": "What is Solar Orbiter designed to study?",
                "answers": ["The Sun", "Jupiter's moons", "Comets only", "Earth's glaciers only"],
                "correct": 0,
                "fact": "Solar Orbiter studies the Sun and the solar wind, helping scientists understand how our star works.",
            },
            {
                "question": "Why does Solar Orbiter use planetary flybys?",
                "answers": ["To change and tilt its orbit", "To refuel with sunlight", "To land on a planet", "To collect rocks from Earth"],
                "correct": 0,
                "fact": "Gravity assists from planets can change a spacecraft's trajectory and help Solar Orbiter obtain a higher-inclination orbit.",
            },
            {
                "question": "What is the solar wind?",
                "answers": ["A flow of charged particles from the Sun", "Wind in Earth's atmosphere", "A stream of water on Mars", "A ring around Saturn"],
                "correct": 0,
                "fact": "The solar wind is a continuous flow of charged particles escaping from the Sun's outer atmosphere.",
            },
            {
                "question": "Which feature of the Sun is especially important for understanding its magnetic activity?",
                "answers": ["Its magnetic field", "Its rings", "Its oceans", "Its solid surface"],
                "correct": 0,
                "fact": "The Sun's magnetic field drives many forms of solar activity, including sunspots and solar eruptions.",
            },
            {
                "question": "What makes observing the Sun's polar regions from Earth difficult?",
                "answers": ["The viewing geometry", "The Moon blocks them every day", "The Sun has no poles", "They are behind Saturn"],
                "correct": 0,
                "fact": "From Earth's usual viewpoint, the Sun's poles are seen at a very shallow angle, so a spacecraft with a tilted orbit can provide a valuable new perspective.",
            },
        ],
        "€16,000": [
            {
                "question": "What can Copernicus Sentinel satellites detect in Antarctica?",
                "answers": ["Dinosaurs walking under the ice", "Changes in the thickness and movement of ice", "Alien radio messages", "Volcanoes on Mars"],
                "correct": 1,
                "fact": "Radar satellites can observe ice even through clouds and during the long polar night, making them valuable tools for tracking change.",
            },
            {
                "question": "Why is radar particularly useful for observing Antarctica?",
                "answers": ["It can operate without sunlight and through cloud cover", "It melts the ice", "It only works at noon", "It needs clear skies at all times"],
                "correct": 0,
                "fact": "Radar instruments can collect observations in darkness and are much less dependent on cloud-free conditions than optical instruments.",
            },
            {
                "question": "What can satellite observations reveal about glaciers?",
                "answers": ["Changes in their movement", "Their taste", "Their exact age of every snowflake", "Their internal temperature everywhere"],
                "correct": 0,
                "fact": "Repeated satellite observations can show how quickly glaciers and ice streams move and how those patterns change over time.",
            },
            {
                "question": "What is an ice sheet?",
                "answers": ["A vast mass of land ice covering a large area", "A layer of sea water", "A cloud formation", "A volcanic lava flow"],
                "correct": 0,
                "fact": "The Antarctic and Greenland ice sheets are enormous masses of land-based ice that contain most of Earth's freshwater ice.",
            },
            {
                "question": "What kind of change can satellite radar detect on an ice surface?",
                "answers": ["Movement and deformation", "Only colour", "Only air temperature", "Only the age of the ice"],
                "correct": 0,
                "fact": "Radar measurements can be used to detect surface movement and deformation, including changes in glaciers and ice sheets.",
            },
            {
                "question": "Why is monitoring Antarctic ice important to Earth science?",
                "answers": ["It helps track changes in the polar environment", "It determines the number of stars in the Milky Way", "It measures Jupiter's atmosphere", "It replaces all climate models"],
                "correct": 0,
                "fact": "Long-term observations of Antarctic ice help scientists understand changes in the polar environment and their wider effects.",
            },
        ],
        "€24,000": [
            {
                "question": "What does the name JUICE stand for?",
                "answers": ["Jupiter Investigation of Comets and Exploration", "Joint Universe Ice and Climate Explorer", "Jupiter Icy Moons Explorer", "Journey Into Cosmic Evolution"],
                "correct": 2,
                "fact": "JUICE is travelling to the Jupiter system to study the giant planet and its ocean-bearing icy moons.",
            },
            {
                "question": "Which planet is JUICE travelling to study?",
                "answers": ["Mars", "Jupiter", "Saturn", "Venus"],
                "correct": 1,
                "fact": "JUICE is ESA's Jupiter Icy Moons Explorer and is designed to investigate Jupiter and several of its large icy moons.",
            },
            {
                "question": "Which of these is one of the icy moons studied by JUICE?",
                "answers": ["Ganymede", "Phobos", "Titan", "Triton"],
                "correct": 0,
                "fact": "JUICE will study Ganymede in detail and also make observations of Europa and Callisto during its mission.",
            },
            {
                "question": "What is especially interesting about Jupiter's icy moons?",
                "answers": ["Some may contain subsurface oceans", "They all have Earth's atmosphere", "They are hotter than the Sun", "They are made entirely of metal"],
                "correct": 0,
                "fact": "Evidence indicates that some of Jupiter's icy moons contain oceans beneath their frozen surfaces.",
            },
            {
                "question": "Which moon is planned to become the main target of JUICE's orbital mission?",
                "answers": ["Ganymede", "Io", "Europa", "Amalthea"],
                "correct": 0,
                "fact": "JUICE is planned to enter orbit around Ganymede, making it the first spacecraft to orbit a moon other than Earth's Moon.",
            },
            {
                "question": "Why are icy moons interesting in the search for potentially habitable environments?",
                "answers": ["They may have liquid water beneath their ice", "They are all close to the Sun", "They have Earth's continents", "They are made of pure oxygen"],
                "correct": 0,
                "fact": "Liquid water is one of the ingredients scientists consider important when studying environments that might support some form of life.",
            },
        ],
        "€44,000": [
            {
                "question": "Which ESA-JAXA mission uses a complex series of planetary flybys on its journey to Mercury?",
                "answers": ["Euclid", "Sentinel-2", "BepiColombo", "Philae"],
                "correct": 2,
                "fact": "Getting to Mercury is surprisingly difficult. A spacecraft must lose a great deal of orbital energy, so BepiColombo uses flybys as carefully planned cosmic steering manoeuvres.",
            },
            {
                "question": "Which planet is the main destination of BepiColombo?",
                "answers": ["Mercury", "Mars", "Jupiter", "Venus"],
                "correct": 0,
                "fact": "BepiColombo is a joint ESA-JAXA mission designed to study Mercury, the innermost planet of the Solar System.",
            },
            {
                "question": "Why is reaching Mercury particularly challenging for a spacecraft from Earth?",
                "answers": ["It must lose orbital energy to fall closer to the Sun", "Mercury has a thick atmosphere", "Mercury is outside the Solar System", "It has oceans that block spacecraft"],
                "correct": 0,
                "fact": "A spacecraft travelling from Earth has to shed substantial orbital energy to enter an orbit close to the Sun, making Mercury a demanding destination.",
            },
            {
                "question": "When was ESA founded?",
                "answers": ["1975", "1965", "1970", "1985"],
                "correct": 0,
                "fact": "JAXA is Japan's national space agency and research organisation. BepiColombo is a collaboration between JAXA and ESA.",
            },
            {
                "question": "Where are the headquarters of ESA?",
                "answers": ["Paris, France", "Berlin, Germany", "Rome, Italy", "London, UK"],
                "correct": 0,
                "fact": "ESA has 23 member states and seven main estabilishment in Europe, with its headquarters being in the centre of Paris.",
            },
            {
                "question": "What is the biggest estabilishment of ESA?",
                "answers": ["ESRIN, Italy", "ESTEC, the Netherlands", "ESOC, Germany", "ESA Headquarters, France"],
                "correct": 1,
                "fact": "ESTEC is the European Space Research and Technology Centre, ESA's technical heart, where most ESA projects are born and where they are guided through the various phases of development.",
            },
        ],
    },
    'it': {'€100': [{'question': 'Cosa significa ESA?',
                  'answers': ['Alleanza Scientifica Europea',
                              'Agenzia Europea dei Satelliti',
                              'Agenzia Spaziale Europea',
                              'Associazione Spaziale Europea'],
                  'correct': 2,
                  'fact': "L'ESA riunisce i Paesi europei per esplorare lo spazio e usare la tecnologia spaziale a beneficio delle persone sulla "
                          'Terra.'}],
        '€200': [{'question': "Quale pianeta è conosciuto come il 'Pianeta Rosso'?",
                  'answers': ['Venere', 'Marte', 'Giove', 'Mercurio'],
                  'correct': 1,
                  'fact': 'Marte appare rossastro perché i minerali di ferro nel suolo si sono ossidati, in un processo simile alla formazione della '
                          'ruggine.'}],
        '€500': [{'question': "A cosa servono principalmente i satelliti per l'osservazione della Terra?",
                  'answers': ['Solo alle previsioni meteorologiche',
                              'A monitorare la Terra e i cambiamenti ambientali',
                              'Solo a trasmettere la televisione',
                              'A scattare fotografie delle vacanze'],
                  'correct': 1,
                  'fact': "I dati satellitari aiutano a monitorare foreste, ghiaccio marino, qualità dell'aria, alluvioni, incendi, colture e molti "
                          'altri cambiamenti del nostro pianeta.'}],
        '€1,200': [{'question': 'Come si chiama la famiglia europea di missioni di osservazione della Terra utilizzata dal programma Copernicus?',
                    'answers': ['Galileo', 'Sentinel', 'Voyager', 'Kepler'],
                    'correct': 1,
                    'fact': 'Le missioni Sentinel funzionano come diversi tipi di occhi: alcune usano il radar, altre osservano il territorio, gli '
                            "oceani o l'atmosfera."}],
        '€2,000': [{'question': "Quale missione dell'ESA ha portato il lander Philae su una cometa nel 2014?",
                    'answers': ['Gaia', 'Rosetta', 'Euclid', 'Solar Orbiter'],
                    'correct': 1,
                    'fact': 'Philae rimbalzò dopo il primo contatto con la cometa 67P. Nella debolissima gravità della cometa, anche un piccolo '
                            'rimbalzo diventò un viaggio spettacolare.'}],
        '€4,000': [{'question': "La missione Gaia dell'ESA è stata progettata per creare una mappa estremamente precisa di che cosa?",
                    'answers': ['Gli oceani terrestri', 'I crateri lunari', 'La galassia Via Lattea', 'I vulcani di Marte'],
                    'correct': 2,
                    'fact': 'Misurando le posizioni e i movimenti delle stelle, Gaia aiuta gli astronomi a studiare la storia e la struttura della '
                            'nostra galassia.'}],
        '€8,000': [{'question': "Quale missione guidata dall'ESA studia il Sole ed è progettata per osservarne le regioni polari?",
                    'answers': ['Solar Orbiter', 'JUICE', 'Hera', 'BepiColombo'],
                    'correct': 0,
                    'fact': 'I poli del Sole sono difficili da osservare dalla Terra. Solar Orbiter usa sorvoli planetari per inclinare la propria '
                            'orbita e ottenere una vista migliore.'}],
        '€16,000': [{'question': 'Che cosa possono rilevare in Antartide i satelliti Copernicus Sentinel?',
                     'answers': ['Dinosauri che camminano sotto il ghiaccio',
                                 'Cambiamenti nello spessore e nel movimento del ghiaccio',
                                 'Messaggi radio alieni',
                                 'Vulcani su Marte'],
                     'correct': 1,
                     'fact': 'I satelliti radar possono osservare il ghiaccio anche attraverso le nuvole e durante la lunga notte polare, risultando '
                             'preziosi per seguirne i cambiamenti.'}],
        '€24,000': [{'question': 'Che cosa significa il nome JUICE?',
                     'answers': ['Jupiter Investigation of Comets and Exploration',
                                 'Joint Universe Ice and Climate Explorer',
                                 'Jupiter Icy Moons Explorer',
                                 'Journey Into Cosmic Evolution'],
                     'correct': 2,
                     'fact': 'JUICE è in viaggio verso il sistema di Giove per studiare il pianeta gigante e le sue lune ghiacciate che potrebbero '
                             'ospitare oceani.'}],
        '€44,000': [{'question': 'Quale missione ESA-JAXA utilizza una complessa serie di sorvoli planetari nel viaggio verso Mercurio?',
                     'answers': ['Euclid', 'Sentinel-2', 'BepiColombo', 'Philae'],
                     'correct': 2,
                     'fact': 'Raggiungere Mercurio è sorprendentemente difficile. La sonda deve perdere molta energia orbitale, perciò BepiColombo '
                             'usa i sorvoli come manovre cosmiche accuratamente pianificate.'}]},
 'de': {'€100': [{'question': 'Wofür steht ESA?',
                  'answers': ['Europäische Wissenschaftsallianz',
                              'Europäische Satellitenagentur',
                              'Europäische Weltraumorganisation',
                              'Europäischer Weltraumverband'],
                  'correct': 2,
                  'fact': 'Die ESA bringt europäische Länder zusammen, um den Weltraum zu erforschen und Raumfahrttechnologie zum Nutzen der '
                          'Menschen auf der Erde einzusetzen.'}],
        '€200': [{'question': "Welcher Planet ist als der 'Rote Planet' bekannt?",
                  'answers': ['Venus', 'Mars', 'Jupiter', 'Merkur'],
                  'correct': 1,
                  'fact': 'Der Mars erscheint rötlich, weil Eisenminerale in seinem Boden oxidiert sind, ähnlich wie bei der Rostbildung.'}],
        '€500': [{'question': 'Wofür werden Erdbeobachtungssatelliten hauptsächlich eingesetzt?',
                  'answers': ['Nur für Wettervorhersagen',
                              'Zur Beobachtung der Erde und von Umweltveränderungen',
                              'Nur zur Fernsehübertragung',
                              'Für Urlaubsfotos'],
                  'correct': 1,
                  'fact': 'Satellitendaten helfen bei der Beobachtung von Wäldern, Meereis, Luftqualität, Überschwemmungen, Bränden, Nutzpflanzen '
                          'und vielen weiteren Veränderungen unseres Planeten.'}],
        '€1,200': [{'question': 'Wie heißt die europäische Familie von Erdbeobachtungsmissionen des Copernicus-Programms?',
                    'answers': ['Galileo', 'Sentinel', 'Voyager', 'Kepler'],
                    'correct': 1,
                    'fact': 'Die Sentinel-Missionen wirken wie unterschiedliche Augen. Einige nutzen Radar, andere beobachten Land, Ozeane oder die '
                            'Atmosphäre.'}],
        '€2,000': [{'question': 'Welche ESA-Mission setzte 2014 den Lander Philae auf einem Kometen ab?',
                    'answers': ['Gaia', 'Rosetta', 'Euclid', 'Solar Orbiter'],
                    'correct': 1,
                    'fact': 'Philae prallte nach der ersten Landung auf dem Kometen 67P ab. In der extrem schwachen Schwerkraft wurde selbst ein '
                            'sanfter Sprung zu einer eindrucksvollen Reise.'}],
        '€4,000': [{'question': 'Wovon sollte die ESA-Mission Gaia eine außergewöhnlich genaue Karte erstellen?',
                    'answers': ['Von den Ozeanen der Erde', 'Von den Kratern des Mondes', 'Von der Milchstraße', 'Von den Vulkanen des Mars'],
                    'correct': 2,
                    'fact': 'Durch die Messung der Positionen und Bewegungen von Sternen hilft Gaia, Geschichte und Struktur unserer Galaxie zu '
                            'erforschen.'}],
        '€8,000': [{'question': 'Welche von der ESA geleitete Mission untersucht die Sonne und soll ihre Polarregionen beobachten?',
                    'answers': ['Solar Orbiter', 'JUICE', 'Hera', 'BepiColombo'],
                    'correct': 0,
                    'fact': 'Die Pole der Sonne sind von der Erde aus schwer zu sehen. Solar Orbiter nutzt planetare Vorbeiflüge, um seine Bahn zu '
                            'neigen und eine bessere Sicht zu erhalten.'}],
        '€16,000': [{'question': 'Was können Copernicus-Sentinel-Satelliten in der Antarktis erkennen?',
                     'answers': ['Dinosaurier unter dem Eis',
                                 'Veränderungen der Dicke und Bewegung des Eises',
                                 'Außerirdische Funksignale',
                                 'Vulkane auf dem Mars'],
                     'correct': 1,
                     'fact': 'Radarsatelliten können Eis auch durch Wolken und während der langen Polarnacht beobachten und eignen sich daher '
                             'besonders zur Erfassung von Veränderungen.'}],
        '€24,000': [{'question': 'Wofür steht der Name JUICE?',
                     'answers': ['Jupiter Investigation of Comets and Exploration',
                                 'Joint Universe Ice and Climate Explorer',
                                 'Jupiter Icy Moons Explorer',
                                 'Journey Into Cosmic Evolution'],
                     'correct': 2,
                     'fact': 'JUICE ist auf dem Weg zum Jupitersystem, um den Riesenplaneten und seine eisigen Monde mit möglichen Ozeanen zu '
                             'untersuchen.'}],
        '€44,000': [{'question': 'Welche ESA-JAXA-Mission nutzt auf dem Weg zum Merkur eine komplexe Reihe planetarer Vorbeiflüge?',
                     'answers': ['Euclid', 'Sentinel-2', 'BepiColombo', 'Philae'],
                     'correct': 2,
                     'fact': 'Den Merkur zu erreichen ist überraschend schwierig. Ein Raumfahrzeug muss viel Bahnenergie abbauen, daher nutzt '
                             'BepiColombo Vorbeiflüge als präzise geplante kosmische Lenkmanöver.'}]},
 'fr': {'€100': [{'question': 'Que signifie ESA ?',
                  'answers': ['Alliance scientifique européenne',
                              'Agence européenne des satellites',
                              'Agence spatiale européenne',
                              'Association spatiale européenne'],
                  'correct': 2,
                  'fact': "L'ESA rassemble les pays européens pour explorer l'espace et utiliser les technologies spatiales au bénéfice des "
                          'habitants de la Terre.'}],
        '€200': [{'question': "Quelle planète est connue comme la 'planète rouge' ?",
                  'answers': ['Vénus', 'Mars', 'Jupiter', 'Mercure'],
                  'correct': 1,
                  'fact': 'Mars paraît rougeâtre parce que les minéraux de fer de son sol se sont oxydés, selon un processus comparable à la '
                          'formation de rouille.'}],
        '€500': [{'question': "À quoi servent principalement les satellites d'observation de la Terre ?",
                  'answers': ['Uniquement aux prévisions météorologiques',
                              'À surveiller la Terre et les changements environnementaux',
                              'Uniquement à diffuser la télévision',
                              'À prendre des photos de vacances'],
                  'correct': 1,
                  'fact': "Les données satellitaires permettent de surveiller les forêts, la glace de mer, la qualité de l'air, les inondations, les "
                          'incendies, les cultures et de nombreux autres changements de notre planète.'}],
        '€1,200': [{'question': "Comment s'appelle la famille européenne de missions d'observation de la Terre utilisée par le programme Copernicus "
                                '?',
                    'answers': ['Galileo', 'Sentinel', 'Voyager', 'Kepler'],
                    'correct': 1,
                    'fact': "Les missions Sentinel fonctionnent comme différents types d'yeux. Certaines utilisent le radar, tandis que d'autres "
                            "observent les terres, les océans ou l'atmosphère."}],
        '€2,000': [{'question': "Quelle mission de l'ESA a déposé l'atterrisseur Philae sur une comète en 2014 ?",
                    'answers': ['Gaia', 'Rosetta', 'Euclid', 'Solar Orbiter'],
                    'correct': 1,
                    'fact': 'Philae a rebondi après son premier contact avec la comète 67P. Dans la très faible gravité de la comète, même un léger '
                            'rebond est devenu un voyage spectaculaire.'}],
        '€4,000': [{'question': "La mission Gaia de l'ESA a été conçue pour créer une carte extraordinairement précise de quoi ?",
                    'answers': ['Des océans de la Terre', 'Des cratères de la Lune', 'De la Voie lactée', 'Des volcans de Mars'],
                    'correct': 2,
                    'fact': "En mesurant la position et le mouvement des étoiles, Gaia aide les astronomes à étudier l'histoire et la structure de "
                            'notre galaxie.'}],
        '€8,000': [{'question': "Quelle mission dirigée par l'ESA étudie le Soleil et est conçue pour observer ses régions polaires ?",
                    'answers': ['Solar Orbiter', 'JUICE', 'Hera', 'BepiColombo'],
                    'correct': 0,
                    'fact': 'Les pôles du Soleil sont difficiles à voir depuis la Terre. Solar Orbiter utilise des survols planétaires pour incliner '
                            'son orbite et obtenir une meilleure vue.'}],
        '€16,000': [{'question': 'Que peuvent détecter les satellites Copernicus Sentinel en Antarctique ?',
                     'answers': ['Des dinosaures marchant sous la glace',
                                 "Des changements dans l'épaisseur et le mouvement de la glace",
                                 'Des messages radio extraterrestres',
                                 'Des volcans sur Mars'],
                     'correct': 1,
                     'fact': 'Les satellites radar peuvent observer la glace à travers les nuages et pendant la longue nuit polaire, ce qui les rend '
                             'précieux pour suivre les changements.'}],
        '€24,000': [{'question': 'Que signifie le nom JUICE ?',
                     'answers': ['Jupiter Investigation of Comets and Exploration',
                                 'Joint Universe Ice and Climate Explorer',
                                 'Jupiter Icy Moons Explorer',
                                 'Journey Into Cosmic Evolution'],
                     'correct': 2,
                     'fact': "JUICE se dirige vers le système de Jupiter pour étudier la planète géante et ses lunes glacées susceptibles d'abriter "
                             'des océans.'}],
        '€44,000': [{'question': 'Quelle mission ESA-JAXA utilise une série complexe de survols planétaires pendant son voyage vers Mercure ?',
                     'answers': ['Euclid', 'Sentinel-2', 'BepiColombo', 'Philae'],
                     'correct': 2,
                     'fact': "Atteindre Mercure est étonnamment difficile. Un engin spatial doit perdre beaucoup d'énergie orbitale, c'est pourquoi "
                             'BepiColombo utilise des survols comme manœuvres cosmiques soigneusement planifiées.'}]},
 'es': {'€100': [{'question': '¿Qué significan las siglas ESA?',
                  'answers': ['Alianza Científica Europea',
                              'Agencia Europea de Satélites',
                              'Agencia Espacial Europea',
                              'Asociación Espacial Europea'],
                  'correct': 2,
                  'fact': 'La ESA reúne a los países europeos para explorar el espacio y utilizar la tecnología espacial en beneficio de las '
                          'personas en la Tierra.'}],
        '€200': [{'question': "¿Qué planeta se conoce como el 'Planeta Rojo'?",
                  'answers': ['Venus', 'Marte', 'Júpiter', 'Mercurio'],
                  'correct': 1,
                  'fact': 'Marte parece rojizo porque los minerales de hierro de su suelo se han oxidado, en un proceso parecido a la formación de '
                          'óxido.'}],
        '€500': [{'question': '¿Para qué se utilizan principalmente los satélites de observación de la Tierra?',
                  'answers': ['Solo para la predicción meteorológica',
                              'Para vigilar la Tierra y los cambios ambientales',
                              'Solo para emitir televisión',
                              'Para hacer fotos de vacaciones'],
                  'correct': 1,
                  'fact': 'Los datos de satélite ayudan a observar bosques, hielo marino, calidad del aire, inundaciones, incendios, cultivos y '
                          'muchos otros cambios de nuestro planeta.'}],
        '€1,200': [{'question': '¿Cómo se llama la familia europea de misiones de observación de la Tierra utilizada por el programa Copernicus?',
                    'answers': ['Galileo', 'Sentinel', 'Voyager', 'Kepler'],
                    'correct': 1,
                    'fact': 'Las misiones Sentinel funcionan como distintos tipos de ojos. Algunas utilizan radar, mientras que otras observan la '
                            'tierra, los océanos o la atmósfera.'}],
        '€2,000': [{'question': '¿Qué misión de la ESA llevó el módulo Philae a un cometa en 2014?',
                    'answers': ['Gaia', 'Rosetta', 'Euclid', 'Solar Orbiter'],
                    'correct': 1,
                    'fact': 'Philae rebotó tras su primer contacto con el cometa 67P. Con la gravedad extremadamente débil del cometa, incluso un '
                            'pequeño rebote se convirtió en un viaje espectacular.'}],
        '€4,000': [{'question': '¿De qué fue diseñada la misión Gaia de la ESA para crear un mapa extraordinariamente preciso?',
                    'answers': ['De los océanos de la Tierra', 'De los cráteres de la Luna', 'De la Vía Láctea', 'De los volcanes de Marte'],
                    'correct': 2,
                    'fact': 'Al medir las posiciones y los movimientos de las estrellas, Gaia ayuda a investigar la historia y la estructura de '
                            'nuestra galaxia.'}],
        '€8,000': [{'question': '¿Qué misión liderada por la ESA estudia el Sol y está diseñada para observar sus regiones polares?',
                    'answers': ['Solar Orbiter', 'JUICE', 'Hera', 'BepiColombo'],
                    'correct': 0,
                    'fact': 'Los polos del Sol son difíciles de observar desde la Tierra. Solar Orbiter utiliza sobrevuelos planetarios para '
                            'inclinar su órbita y obtener una mejor vista.'}],
        '€16,000': [{'question': '¿Qué pueden detectar los satélites Copernicus Sentinel en la Antártida?',
                     'answers': ['Dinosaurios caminando bajo el hielo',
                                 'Cambios en el grosor y el movimiento del hielo',
                                 'Mensajes de radio alienígenas',
                                 'Volcanes en Marte'],
                     'correct': 1,
                     'fact': 'Los satélites radar pueden observar el hielo a través de las nubes y durante la larga noche polar, por lo que son muy '
                             'útiles para seguir los cambios.'}],
        '€24,000': [{'question': '¿Qué significa el nombre JUICE?',
                     'answers': ['Jupiter Investigation of Comets and Exploration',
                                 'Joint Universe Ice and Climate Explorer',
                                 'Jupiter Icy Moons Explorer',
                                 'Journey Into Cosmic Evolution'],
                     'correct': 2,
                     'fact': 'JUICE viaja hacia el sistema de Júpiter para estudiar el planeta gigante y sus lunas heladas que podrían albergar '
                             'océanos.'}],
        '€44,000': [{'question': '¿Qué misión ESA-JAXA utiliza una compleja serie de sobrevuelos planetarios en su viaje a Mercurio?',
                     'answers': ['Euclid', 'Sentinel-2', 'BepiColombo', 'Philae'],
                     'correct': 2,
                     'fact': 'Llegar a Mercurio es sorprendentemente difícil. Una nave debe perder mucha energía orbital, por lo que BepiColombo '
                             'utiliza sobrevuelos como maniobras cósmicas cuidadosamente planificadas.'}]}}



# The quiz still has one question per prize level, but the question for each
# level is selected randomly when a new game starts.
PRIZE_LADDER = list(LOCALIZED_QUESTION_BANKS['en'].keys())
LADDER_LENGHT = len(PRIZE_LADDER)
LETTERS = ("A", "B", "C", "D")

# Validate the question bank when the program starts.
for language in LOCALIZED_QUESTION_BANKS.keys():
    QUESTION_BANK=LOCALIZED_QUESTION_BANKS[language]
    for prize_value, questions in QUESTION_BANK.items():
        if not questions:
            raise ValueError(f"No questions configured for {prize_value}")
        for question in questions:
            if len(question["answers"]) != 4:
                raise ValueError(f"{prize_value}: every question must have exactly 4 answers")
            if not 0 <= question["correct"] < 4:
                raise ValueError(f"{prize_value}: correct answer must be 0, 1, 2 or 3")

class ESASpaceQuiz(tk.Tk):
    BG = "#030515"
    PANEL = "#090d2c"
    BLUE = "#163c8c"
    BRIGHT_BLUE = "#2474ff"
    CYAN = "#49d9ff"
    GOLD = "#ffc94a"
    ORANGE = "#ff8b27"
    WHITE = "#f7fbff"
    MUTED = "#9eb4d6"
    GREEN = "#1fbd72"
    RED = "#d9445e"

    def __init__(self):
        super().__init__()
        self.title("ESA Space Challenge")
        self.geometry("1280x800")
        self.minsize(960, 650)
        self.configure(bg=self.BG)
        self.fullscreen = False
        self.language = "en"
        self.last_answer_correct = False
        self.current = 0
        self.selected_questions = []
        self.score = 0
        self.correct_count = 0
        self.locked = False
        self.after_id = None

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.leave_fullscreen)
        self.bind("<Key-r>", lambda _e: self.restart())
        self.bind("<Key-R>", lambda _e: self.restart())
        self.bind("<Configure>", self.on_resize)

        self.canvas = tk.Canvas(self, bg=self.BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_background()
        self.show_start_screen()

    def t(self, key, **kwargs):
        text = UI_TEXT[self.language].get(key, UI_TEXT["en"][key])
        return text.format(**kwargs) if kwargs else text

    def set_language(self, language):
        self.language = language
        self.title("ESA Space Challenge")
        self.show_start_screen()

    def toggle_fullscreen(self, _event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def leave_fullscreen(self, _event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)

    def on_resize(self, event):
        if event.widget is self:
            if self.after_id:
                self.after_cancel(self.after_id)
            self.after_id = self.after(80, self.redraw_current_screen)

    def clear(self):
        self.canvas.delete("all")

    def draw_background(self):
        w = max(self.winfo_width(), 960)
        h = max(self.winfo_height(), 650)
        self.canvas.create_rectangle(0, 0, w, h, fill=self.BG, outline="")

        # Game-show inspired radial rings and light beams, drawn without external assets.
        cx, cy = int(w * 0.39), int(h * 0.43)
        for radius, colour, width in [
            (int(h * 0.48), "#08164a", 3),
            (int(h * 0.38), "#0d2870", 2),
            (int(h * 0.29), "#1450a4", 2),
            (int(h * 0.21), "#2474ff", 2),
        ]:
            self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                                    outline=colour, width=width)

        for angle in range(0, 360, 20):
            r1, r2 = int(h * 0.10), int(h * 0.50)
            x1 = cx + math.cos(math.radians(angle)) * r1
            y1 = cy + math.sin(math.radians(angle)) * r1
            x2 = cx + math.cos(math.radians(angle)) * r2
            y2 = cy + math.sin(math.radians(angle)) * r2
            self.canvas.create_line(x1, y1, x2, y2, fill="#0a245f", width=1)

        # Stars
        star_points = [
            (.05,.10),(.12,.28),(.20,.08),(.28,.20),(.35,.06),(.45,.13),
            (.53,.05),(.61,.18),(.70,.09),(.78,.23),(.88,.11),(.95,.30),
            (.08,.72),(.18,.88),(.31,.76),(.47,.91),(.58,.74),(.69,.88),
            (.81,.69),(.91,.86),(.97,.62),(.55,.31),(.24,.55),(.42,.67)
        ]
        for i, (sx, sy) in enumerate(star_points):
            r = 1 + (i % 3 == 0)
            self.canvas.create_oval(w*sx-r, h*sy-r, w*sx+r, h*sy+r,
                                    fill=self.WHITE, outline="")

    def rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1+radius,y1, x2-radius,y1, x2,y1, x2,y1+radius,
            x2,y2-radius, x2,y2, x2-radius,y2, x1+radius,y2,
            x1,y2, x1,y2-radius, x1,y1+radius, x1,y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def text_button(self, x1, y1, x2, y2, text, command,
                    fill=None, outline=None, font_size=18, tag=None):
        tag = tag or f"button_{x1}_{y1}"
        fill = fill or self.BLUE
        outline = outline or self.CYAN
        self.rounded_rect(x1, y1, x2, y2, radius=18, fill=fill,
                          outline=outline, width=2, tags=(tag,))
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=text,
                                fill=self.WHITE, font=("Arial", font_size, "bold"),
                                width=max(100, x2-x1-30), justify="center", tags=(tag,))
        self.canvas.tag_bind(tag, "<Button-1>", lambda _e: command())
        self.canvas.tag_bind(tag, "<Enter>", lambda _e: self.set_button_colour(tag, self.BRIGHT_BLUE))
        self.canvas.tag_bind(tag, "<Leave>", lambda _e: self.set_button_colour(tag, fill))
        return tag

    def set_button_colour(self, tag, colour):
        items = self.canvas.find_withtag(tag)
        if items:
            self.canvas.itemconfigure(items[0], fill=colour)

    def show_start_screen(self):
        self.screen = "start"
        self.clear()
        self.draw_background()
        w, h = self.winfo_width(), self.winfo_height()
        cx = w * 0.42

        self.canvas.create_text(cx, h*0.16, text="ESA", fill=self.CYAN,
                                font=("Arial", max(24, int(h*.055)), "bold"))
        self.canvas.create_text(cx, h*0.24, text="SPACE CHALLENGE", fill=self.WHITE,
                                font=("Arial", max(28, int(h*.065)), "bold"))
        self.canvas.create_text(cx, h*0.33,
                                text=self.t("subtitle"),
                                fill=self.MUTED, font=("Arial", max(14, int(h*.026))),
                                width=w*.66, justify="center")

        r = min(w, h) * .15
        self.canvas.create_oval(cx-r, h*.49-r, cx+r, h*.49+r,
                                fill="#07113a", outline=self.CYAN, width=4)
        self.canvas.create_oval(cx-r*.76, h*.49-r*.76, cx+r*.76, h*.49+r*.76,
                                outline=self.GOLD, width=3)
        self.canvas.create_text(cx, h*.465, text=str(LADDER_LENGHT), fill=self.WHITE,
                                font=("Arial", max(30, int(h*.075)), "bold"))
        self.canvas.create_text(cx, h*.545, text=f"{LADDER_LENGHT} {self.t('questions')}", fill=self.GOLD,
                                font=("Arial", max(14, int(h*.025)), "bold"))

        self.text_button(cx-w*.13, h*.72, cx+w*.13, h*.81,
                         self.t("start"), self.start_quiz,
                         fill="#123d8b", outline=self.GOLD,
                         font_size=max(15, int(h*.026)), tag="start")
        self.canvas.create_text(cx, h*.89,
                                text=self.t("controls"),
                                fill=self.MUTED, font=("Arial", max(10, int(h*.017))))
        # Language selector. Changing language redraws this screen immediately.
        self.canvas.create_text(cx, h*.065, text=self.t("choose"), fill=self.MUTED,
                                font=("Arial", max(10, int(h*.017)), "bold"))
        labels = [("en", "EN"), ("it", "IT"), ("de", "DE"), ("fr", "FR"), ("es", "ES")]
        bw, gap = w*.052, w*.008
        total_w = len(labels)*bw + (len(labels)-1)*gap
        lx = cx-total_w/2
        for i, (code, label) in enumerate(labels):
            x1 = lx+i*(bw+gap)
            self.text_button(x1, h*.085, x1+bw, h*.13, label,
                             lambda c=code: self.set_language(c),
                             fill=self.BRIGHT_BLUE if code == self.language else "#101c45",
                             outline=self.GOLD if code == self.language else self.CYAN,
                             font_size=max(9, int(h*.015)), tag=f"lang_{code}")
        self.draw_ladder(w, h, active=None)

    def randomize_answers(self, question):
        indexed_answers = list(enumerate(question["answers"]))
        random.shuffle(indexed_answers)
        original_correct = question["correct"]
        question["answers"] = [answer for _, answer in indexed_answers]
        question["correct"] = next(
            i for i, (orig_idx, _) in enumerate(indexed_answers)
            if orig_idx == original_correct
        )
        return question

    def start_quiz(self):
        self.current = 0
        self.score = 0
        self.correct_count = 0
        self.locked = False

        # Pick exactly one question at random for each prize level.
        # Shift the answers so it is not always the same correct answer placement.
        # The selected questions remain fixed for the whole game.
        self.selected_questions = [
            self.randomize_answers(__import__("copy").deepcopy(random.choice(LOCALIZED_QUESTION_BANKS[self.language][value])))
            for value in PRIZE_LADDER
        ]

        self.show_question()

    def draw_ladder(self, w, h, active=None):
        x1, x2 = w*.80, w*.97
        y1, y2 = h*.10, h*.90
        self.rounded_rect(x1, y1, x2, y2, 22, fill="#060a22",
                          outline="#2359bd", width=2)
        self.canvas.create_text((x1+x2)/2, y1+h*.045, text=self.t("ladder"),
                                fill=self.CYAN, font=("Arial", max(11, int(h*.019)), "bold"))
        usable = y2-y1-h*.10
        step = usable/LADDER_LENGHT
        for display_i, value in enumerate(reversed(PRIZE_LADDER)):
            question_i = LADDER_LENGHT-1-display_i
            y = y1+h*.085 + display_i*step + step/2
            is_active = active == question_i
            is_passed = active is not None and question_i < active
            if is_active:
                self.rounded_rect(x1+8, y-step*.39, x2-8, y+step*.39, 10,
                                  fill=self.ORANGE, outline=self.GOLD, width=2)
                colour = self.WHITE
            elif is_passed:
                colour = self.GOLD
            else:
                colour = self.MUTED
            self.canvas.create_text(x1+18, y, text=str(question_i+1), anchor="w",
                                    fill=colour, font=("Arial", max(9, int(h*.016)), "bold"))
            self.canvas.create_text(x2-16, y, text=value, anchor="e",
                                    fill=colour, font=("Arial", max(9, int(h*.016)), "bold"))

    def show_question(self):
        self.screen = "question"
        self.locked = False
        self.clear()
        self.draw_background()
        w, h = self.winfo_width(), self.winfo_height()
        q = self.selected_questions[self.current]
        main_right = w*.76

        self.canvas.create_text(w*.03, h*.045, anchor="w",
                                text="ESA SPACE CHALLENGE", fill=self.CYAN,
                                font=("Arial", max(14, int(h*.025)), "bold"))
        self.canvas.create_text(main_right-w*.02, h*.045, anchor="e",
                                text=self.t("question", n=self.current+1, total=LADDER_LENGHT, prize=PRIZE_LADDER[self.current]),
                                fill=self.GOLD, font=("Arial", max(12, int(h*.021)), "bold"))

        # Progress bar
        px1, px2, py = w*.04, main_right-w*.03, h*.09
        self.canvas.create_rectangle(px1, py, px2, py+8, fill="#101c45", outline="")
        self.canvas.create_rectangle(px1, py, px1+(px2-px1)*(self.current+1)/LADDER_LENGHT,
                                     py+8, fill=self.CYAN, outline="")

        self.rounded_rect(w*.04, h*.15, main_right-w*.03, h*.38, 26,
                          fill="#07113a", outline=self.CYAN, width=3)
        self.canvas.create_text((w*.04+main_right-w*.03)/2, h*.265,
                                text=q["question"], fill=self.WHITE,
                                font=("Arial", max(18, int(h*.036)), "bold"),
                                width=main_right-w*.13, justify="center")

        coords = [
            (w*.04, h*.44, w*.38, h*.59),
            (w*.405, h*.44, main_right-w*.03, h*.59),
            (w*.04, h*.63, w*.38, h*.78),
            (w*.405, h*.63, main_right-w*.03, h*.78),
        ]
        for idx, ((x1,y1,x2,y2), answer) in enumerate(zip(coords, q["answers"])):
            tag = f"answer_{idx}"
            self.rounded_rect(x1,y1,x2,y2,20, fill=self.PANEL,
                              outline=self.BRIGHT_BLUE, width=2, tags=(tag,))
            self.canvas.create_text(x1+28, (y1+y2)/2, text=LETTERS[idx]+":",
                                    anchor="w", fill=self.GOLD,
                                    font=("Arial", max(15, int(h*.027)), "bold"), tags=(tag,))
            self.canvas.create_text(x1+70, (y1+y2)/2, text=answer,
                                    anchor="w", fill=self.WHITE,
                                    font=("Arial", max(12, int(h*.021)), "bold"),
                                    width=x2-x1-90, justify="left", tags=(tag,))
            self.canvas.tag_bind(tag, "<Button-1>", lambda _e, i=idx: self.choose_answer(i))
            self.canvas.tag_bind(tag, "<Enter>", lambda _e, t=tag: self.set_answer_colour(t, self.BLUE))
            self.canvas.tag_bind(tag, "<Leave>", lambda _e, t=tag: self.set_answer_colour(t, self.PANEL))

        self.canvas.create_text(w*.04, h*.87, anchor="w",
                                text=self.t("correct_answers", correct=self.correct_count, score=self.print_score()),
                                fill=self.MUTED, font=("Arial", max(11, int(h*.019)), "bold"))
        self.draw_ladder(w, h, active=self.current)

    def set_answer_colour(self, tag, colour):
        if self.locked:
            return
        items = self.canvas.find_withtag(tag)
        if items:
            self.canvas.itemconfigure(items[0], fill=colour)

    def choose_answer(self, selected):
        if self.locked:
            return
        self.locked = True
        q = self.selected_questions[self.current]
        correct = q["correct"]
        is_correct = selected == correct

        for i in range(4):
            items = self.canvas.find_withtag(f"answer_{i}")
            if not items:
                continue
            if i == correct:
                self.canvas.itemconfigure(items[0], fill=self.GREEN, outline="#86ffc1", width=3)
            elif i == selected:
                self.canvas.itemconfigure(items[0], fill=self.RED, outline="#ff9aaa", width=3)
            else:
                self.canvas.itemconfigure(items[0], fill="#0b1029", outline="#263157")

        if is_correct:
            self.correct_count += 1
            self.score = self.score + int(PRIZE_LADDER[self.current][1:].replace(',',''))

        self.last_answer_correct = is_correct
        self.after(850, lambda: self.show_fact(is_correct))

    def show_fact(self, is_correct):
        self.screen = "fact"
        self.clear()
        self.draw_background()
        w, h = self.winfo_width(), self.winfo_height()
        q = self.selected_questions[self.current]
        main_right = w*.76
        colour = self.GREEN if is_correct else self.RED
        headline = self.t("correct") if is_correct else self.t("wrong")

        self.canvas.create_text((main_right)/2, h*.15, text=headline,
                                fill=colour, font=("Arial", max(30, int(h*.065)), "bold"))
        self.canvas.create_text(main_right/2, h*.25,
                                text=self.t("answer_is", letter=LETTERS[q['correct']], answer=q['answers'][q['correct']]),
                                fill=self.WHITE, font=("Arial", max(16, int(h*.031)), "bold"),
                                width=main_right-w*.12, justify="center")

        self.rounded_rect(w*.07, h*.36, main_right-w*.05, h*.66, 28,
                          fill="#08133b", outline=self.GOLD, width=3)
        self.canvas.create_text(w*.11, h*.42, anchor="w", text=self.t("fun_fact"),
                                fill=self.GOLD, font=("Arial", max(14, int(h*.025)), "bold"))
        self.canvas.create_text((w*.07+main_right-w*.05)/2, h*.525,
                                text=q["fact"], fill=self.WHITE,
                                font=("Arial", max(14, int(h*.026))),
                                width=main_right-w*.20, justify="center")

        button_text = self.t("final") if self.current == LADDER_LENGHT-1 else self.t("next")
        self.text_button(main_right/2-w*.12, h*.73, main_right/2+w*.12, h*.82,
                         button_text, self.next_question,
                         fill="#123d8b", outline=self.GOLD,
                         font_size=max(14, int(h*.023)), tag="next")
        self.draw_ladder(w, h, active=self.current)

    def next_question(self):
        if self.current < LADDER_LENGHT-1:
            self.current += 1
            self.show_question()
        else:
            self.show_results()

    def result_title(self):
        titles = {
            "en": [("ESA MISSION DIRECTOR", "A perfect flight through the quiz!"), ("COSMIC EXPERT", "The universe clearly has your attention."), ("ASTRONAUT IN TRAINING", "A strong result and a great launchpad for more discovery."), ("SPACE EXPLORER", "You are well on your way across the Solar System."), ("EARTH OBSERVER", "Every space journey begins by looking up and asking questions.")],
            "it": [("DIRETTORE DI MISSIONE ESA", "Un volo perfetto attraverso il quiz!"), ("ESPERTO COSMICO", "L’universo ha chiaramente la tua attenzione."), ("ASTRONAUTA IN ADDESTRAMENTO", "Un ottimo risultato e una splendida base per nuove scoperte."), ("ESPLORATORE SPAZIALE", "Sei sulla buona strada attraverso il Sistema Solare."), ("OSSERVATORE DELLA TERRA", "Ogni viaggio spaziale inizia guardando in alto e ponendo domande.")],
            "de": [("ESA-MISSIONSDIREKTOR", "Ein perfekter Flug durch das Quiz!"), ("KOSMISCHER EXPERTE", "Das Universum hat eindeutig deine Aufmerksamkeit."), ("ASTRONAUT IM TRAINING", "Ein starkes Ergebnis und eine gute Startrampe für weitere Entdeckungen."), ("WELTRAUMFORSCHER", "Du bist auf einem guten Weg durch das Sonnensystem."), ("ERDBEOBACHTER", "Jede Raumfahrt beginnt mit einem Blick nach oben und mit Fragen.")],
            "fr": [("DIRECTEUR DE MISSION ESA", "Un parcours parfait dans le quiz !"), ("EXPERT COSMIQUE", "L’Univers a clairement toute votre attention."), ("ASTRONAUTE EN FORMATION", "Un excellent résultat et une belle rampe de lancement vers de nouvelles découvertes."), ("EXPLORATEUR SPATIAL", "Vous êtes en bonne voie à travers le Système solaire."), ("OBSERVATEUR DE LA TERRE", "Tout voyage spatial commence en levant les yeux et en posant des questions.")],
            "es": [("DIRECTOR DE MISIÓN DE LA ESA", "¡Un vuelo perfecto a través del concurso!"), ("EXPERTO CÓSMICO", "Está claro que el universo tiene toda tu atención."), ("ASTRONAUTA EN FORMACIÓN", "Un gran resultado y una excelente plataforma para nuevos descubrimientos."), ("EXPLORADOR ESPACIAL", "Vas por buen camino a través del Sistema Solar."), ("OBSERVADOR DE LA TIERRA", "Todo viaje espacial comienza mirando hacia arriba y haciendo preguntas.")]
        }
        if self.correct_count == LADDER_LENGHT: idx = 0
        elif self.correct_count >= 8: idx = 1
        elif self.correct_count >= 6: idx = 2
        elif self.correct_count >= 4: idx = 3
        else: idx = 4
        return titles[self.language][idx]

    def print_score(self):
        return f'€{self.score:,}'
        
    def show_results(self):
        self.screen = "results"
        self.clear()
        self.draw_background()
        w, h = self.winfo_width(), self.winfo_height()
        title, subtitle = self.result_title()
        earned = self.print_score()
        cx = w*.50

        self.canvas.create_text(cx, h*.12, text=self.t("complete"),
                                fill=self.CYAN, font=("Arial", max(22, int(h*.045)), "bold"))
        self.canvas.create_text(cx, h*.22, text=title,
                                fill=self.GOLD, font=("Arial", max(26, int(h*.058)), "bold"))
        self.canvas.create_text(cx, h*.29, text=subtitle,
                                fill=self.MUTED, font=("Arial", max(13, int(h*.024))),
                                width=w*.75, justify="center")

        self.rounded_rect(w*.20, h*.36, w*.80, h*.64, 30,
                          fill="#07113a", outline=self.CYAN, width=3)
        self.canvas.create_text(w*.35, h*.46, text=f"{self.correct_count}/{LADDER_LENGHT}",
                                fill=self.WHITE, font=("Arial", max(32, int(h*.075)), "bold"))
        self.canvas.create_text(w*.35, h*.56, text=self.t("correct_label"),
                                fill=self.MUTED, font=("Arial", max(12, int(h*.021)), "bold"))
        self.canvas.create_line(w*.50, h*.40, w*.50, h*.60, fill="#2850a0", width=2)
        self.canvas.create_text(w*.65, h*.46, text=earned,
                                fill=self.GOLD, font=("Arial", max(32, int(h*.075)), "bold"))
        self.canvas.create_text(w*.65, h*.56, text=self.t("score_label"),
                                fill=self.MUTED, font=("Arial", max(12, int(h*.021)), "bold"))

        self.text_button(w*.31, h*.71, w*.49, h*.81, self.t("again"), self.restart,
                         fill="#123d8b", outline=self.GOLD,
                         font_size=max(14, int(h*.024)), tag="again")
        self.text_button(w*.52, h*.71, w*.70, h*.81, self.t("exit"), self.destroy,
                         fill="#24144d", outline=self.CYAN,
                         font_size=max(14, int(h*.024)), tag="exit")
        self.canvas.create_text(cx, h*.89,
                                text=self.t("thanks"),
                                fill=self.WHITE, font=("Arial", max(12, int(h*.022)), "bold"))

    def restart(self):
        self.current = 0
        self.selected_questions = []
        self.score = 0
        self.correct_count = 0
        self.locked = False
        self.show_start_screen()

    def redraw_current_screen(self):
        self.after_id = None
        screen = getattr(self, "screen", "start")
        if screen == "start":
            self.show_start_screen()
        elif screen == "question":
            self.show_question()
        elif screen == "fact":
            # Preserve the most recent answer state approximately when resizing.
            self.show_fact(self.last_answer_correct)
        elif screen == "results":
            self.show_results()


if __name__ == "__main__":
    app = ESASpaceQuiz()
    app.mainloop()
