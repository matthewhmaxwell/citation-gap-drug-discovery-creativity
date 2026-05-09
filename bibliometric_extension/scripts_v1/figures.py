"""
Extended figure set, expanded to individual authors for OpenAlex lookup.

The spec defines 26 *figures* — three of these are collaborator groups
(F08 Fauconnier-Turner; F09 Finke-Ward-Smith; F23 Clark-Chalmers).
For OpenAlex author lookup we expand to individuals (33 rows) but tag
each row with a `figure_group` so direct-citation/co-citation/forward
counts can be aggregated back to the 26 named figures.

For each row we provide:
- id: unique row id (e.g. F08a)
- figure_group: the 26-figure name (e.g. "Fauconnier-Turner")
- name: the individual's canonical display name
- search_names: name variants to try in OpenAlex author search
- affiliations: known institutions (used to disambiguate)
- topics: keywords from their work (used to disambiguate / sanity-check)
- known_works: distinctive substrings of major works, used as a fallback
  when authorship lookup is ambiguous.
- group: "original-11" or "extended-15"
"""

FIGURES = [
    # ---- Original eleven ----
    {
        "id": "F01",
        "name": "Geraint Wiggins",
        "search_names": ["Geraint A. Wiggins", "Geraint Wiggins"],
        "affiliations": ["Vrije Universiteit Brussel", "Queen Mary University of London", "Goldsmiths"],
        "topics": ["computational creativity", "music cognition"],
        "known_works": [
            "preliminary framework for description, analysis and comparison of creative systems",
            "searching for computational creativity",
        ],
        "group": "original-11",
    },
    {
        "id": "F02",
        "name": "Margaret Boden",
        "search_names": ["Margaret A. Boden", "Margaret Boden"],
        "affiliations": ["University of Sussex"],
        "topics": ["creativity", "cognitive science", "philosophy of AI"],
        "known_works": [
            "creative mind myths and mechanisms",
            "computer models of mind",
            "creativity and artificial intelligence",
        ],
        "group": "original-11",
    },
    {
        "id": "F03",
        "name": "Douglas Hofstadter",
        "search_names": ["Douglas R. Hofstadter", "Douglas Hofstadter"],
        "affiliations": ["Indiana University"],
        "topics": ["analogy", "fluid concepts", "cognition"],
        "known_works": [
            "fluid concepts and creative analogies",
            "godel escher bach",
            "surfaces and essences",
        ],
        "group": "original-11",
    },
    {
        "id": "F04",
        "name": "Imre Lakatos",
        "search_names": ["Imre Lakatos"],
        "affiliations": ["London School of Economics"],
        "topics": ["philosophy of science", "research programmes"],
        "known_works": [
            "falsification and the methodology of scientific research programmes",
            "proofs and refutations",
        ],
        "group": "original-11",
    },
    {
        "id": "F05",
        "name": "Graham Wallas",
        "search_names": ["Graham Wallas"],
        "affiliations": ["London School of Economics"],
        "topics": ["thought", "creativity stages"],
        "known_works": ["the art of thought"],
        "group": "original-11",
    },
    {
        "id": "F06",
        "name": "Mihaly Csikszentmihalyi",
        "search_names": ["Mihaly Csikszentmihalyi", "Mihály Csíkszentmihályi"],
        "affiliations": ["University of Chicago", "Claremont Graduate University"],
        "topics": ["flow", "creativity", "positive psychology"],
        "known_works": [
            "flow the psychology of optimal experience",
            "creativity flow and the psychology of discovery",
            "society culture and person",
        ],
        "group": "original-11",
    },
    {
        "id": "F07",
        "name": "Dedre Gentner",
        "search_names": ["Dedre Gentner"],
        "affiliations": ["Northwestern University"],
        "topics": ["analogy", "structure mapping"],
        "known_works": [
            "structure mapping a theoretical framework for analogy",
            "the structure mapping engine",
        ],
        "group": "original-11",
    },
    {
        "id": "F08a",
        "name": "Gilles Fauconnier",
        "search_names": ["Gilles Fauconnier"],
        "affiliations": ["University of California San Diego"],
        "topics": ["conceptual blending", "mental spaces"],
        "known_works": [
            "the way we think conceptual blending",
            "conceptual integration networks",
            "mental spaces",
        ],
        "group": "original-11",
    },
    {
        "id": "F08b",
        "name": "Mark Turner",
        "search_names": ["Mark Turner"],
        "affiliations": ["Case Western Reserve University", "University of Maryland"],
        "topics": ["conceptual blending", "cognitive linguistics"],
        "known_works": [
            "the way we think conceptual blending",
            "conceptual integration networks",
            "the literary mind",
        ],
        "group": "original-11",
    },
    {
        "id": "F09a",
        "name": "Ronald Finke",
        "search_names": ["Ronald A. Finke", "Ronald Finke"],
        "affiliations": ["Texas A&M University", "SUNY Stony Brook"],
        "topics": ["creative cognition", "mental imagery"],
        "known_works": ["creative cognition theory research and applications"],
        "group": "original-11",
    },
    {
        "id": "F09b",
        "name": "Thomas Ward",
        "search_names": ["Thomas B. Ward", "Thomas Ward"],
        "affiliations": ["University of Alabama", "Texas A&M University"],
        "topics": ["creative cognition", "conceptual structures"],
        "known_works": ["creative cognition", "structured imagination"],
        "group": "original-11",
    },
    {
        "id": "F09c",
        "name": "Steven Smith",
        "search_names": ["Steven M. Smith", "Steven Smith"],
        "affiliations": ["Texas A&M University"],
        "topics": ["incubation", "creative cognition", "memory"],
        "known_works": ["creative cognition", "incubation effect"],
        "group": "original-11",
    },
    {
        "id": "F10",
        "name": "Arthur Koestler",
        "search_names": ["Arthur Koestler"],
        "affiliations": [],
        "topics": ["bisociation", "creativity"],
        "known_works": ["the act of creation"],
        "group": "original-11",
    },
    {
        "id": "F11",
        "name": "Michael Levin",
        "search_names": ["Michael Levin"],
        "affiliations": ["Tufts University"],
        "topics": ["bioelectricity", "regeneration", "TAME", "morphogenesis"],
        "known_works": [
            "technological approach to mind everywhere",
            "bioelectric signaling",
        ],
        "group": "original-11",
    },
    # ---- Extended fifteen ----
    {
        "id": "F12",
        "name": "Herbert Simon",
        "search_names": ["Herbert A. Simon", "Herbert Simon"],
        "affiliations": ["Carnegie Mellon University"],
        "topics": ["bounded rationality", "problem solving", "artificial intelligence"],
        "known_works": [
            "the sciences of the artificial",
            "human problem solving",
            "a behavioral model of rational choice",
        ],
        "group": "extended-15",
    },
    {
        "id": "F13",
        "name": "Allen Newell",
        "search_names": ["Allen Newell"],
        "affiliations": ["Carnegie Mellon University"],
        "topics": ["problem solving", "cognitive architecture", "soar"],
        "known_works": ["human problem solving", "unified theories of cognition"],
        "group": "extended-15",
    },
    {
        "id": "F14",
        "name": "Teresa Amabile",
        "search_names": ["Teresa M. Amabile", "Teresa Amabile"],
        "affiliations": ["Harvard Business School", "Brandeis University"],
        "topics": ["creativity", "intrinsic motivation", "work environment"],
        "known_works": [
            "a model of creativity and innovation in organizations",
            "the social psychology of creativity",
            "componential theory of creativity",
        ],
        "group": "extended-15",
    },
    {
        "id": "F15",
        "name": "Robert Sternberg",
        "search_names": ["Robert J. Sternberg", "Robert Sternberg"],
        "affiliations": ["Yale University", "Cornell University"],
        "topics": ["creativity", "intelligence", "wisdom"],
        "known_works": [
            "investment theory of creativity",
            "the nature of creativity",
            "handbook of creativity",
            "triarchic theory of intelligence",
        ],
        "group": "extended-15",
    },
    {
        "id": "F16",
        "name": "Donald Campbell",
        "search_names": ["Donald T. Campbell", "Donald Campbell"],
        "affiliations": ["Northwestern University", "Lehigh University"],
        "topics": ["evolutionary epistemology", "blind variation", "selective retention"],
        "known_works": [
            "blind variation and selective retention in creative thought",
            "evolutionary epistemology",
        ],
        "group": "extended-15",
    },
    {
        "id": "F17",
        "name": "Dean Keith Simonton",
        "search_names": ["Dean Keith Simonton", "Dean K. Simonton"],
        "affiliations": ["University of California Davis"],
        "topics": ["creativity", "genius", "scientific productivity"],
        "known_works": [
            "scientific genius",
            "creativity in science",
            "chance configuration theory",
            "origins of genius",
        ],
        "group": "extended-15",
    },
    {
        "id": "F18",
        "name": "Donald Schön",
        "search_names": ["Donald A. Schön", "Donald Schön", "Donald Schon"],
        "affiliations": ["Massachusetts Institute of Technology"],
        "topics": ["reflective practice", "design", "professional knowledge"],
        "known_works": [
            "the reflective practitioner",
            "educating the reflective practitioner",
            "displacement of concepts",
        ],
        "group": "extended-15",
    },
    {
        "id": "F19",
        "name": "Christopher Alexander",
        "search_names": ["Christopher Alexander"],
        "affiliations": ["University of California Berkeley"],
        "topics": ["pattern language", "design", "architecture"],
        "known_works": [
            "a pattern language",
            "notes on the synthesis of form",
            "the timeless way of building",
        ],
        "group": "extended-15",
    },
    {
        "id": "F20",
        "name": "Genrich Altshuller",
        "search_names": ["Genrich Altshuller", "Genrikh Altshuller"],
        "affiliations": [],
        "topics": ["TRIZ", "inventive problem solving"],
        "known_works": [
            "creativity as an exact science",
            "the innovation algorithm",
            "and suddenly the inventor appeared",
        ],
        "group": "extended-15",
    },
    {
        "id": "F21",
        "name": "Donald Stokes",
        "search_names": ["Donald E. Stokes", "Donald Stokes"],
        "affiliations": ["Princeton University"],
        "topics": ["pasteurs quadrant", "use-inspired research"],
        "known_works": ["pasteur's quadrant basic science and technological innovation"],
        "group": "extended-15",
    },
    {
        "id": "F22",
        "name": "Edwin Hutchins",
        "search_names": ["Edwin Hutchins"],
        "affiliations": ["University of California San Diego"],
        "topics": ["distributed cognition", "cognition in the wild"],
        "known_works": ["cognition in the wild", "how a cockpit remembers its speeds"],
        "group": "extended-15",
    },
    {
        "id": "F23a",
        "name": "Andy Clark",
        "search_names": ["Andy Clark"],
        "affiliations": ["University of Edinburgh", "University of Sussex"],
        "topics": ["extended mind", "predictive processing", "philosophy of mind"],
        "known_works": [
            "the extended mind",
            "supersizing the mind",
            "being there putting brain body and world together",
        ],
        "group": "extended-15",
    },
    {
        "id": "F23b",
        "name": "David Chalmers",
        "search_names": ["David J. Chalmers", "David Chalmers"],
        "affiliations": ["New York University", "Australian National University"],
        "topics": ["consciousness", "extended mind", "philosophy of mind"],
        "known_works": [
            "the extended mind",
            "the conscious mind",
            "facing up to the problem of consciousness",
        ],
        "group": "extended-15",
    },
    {
        "id": "F24",
        "name": "Bruno Latour",
        "search_names": ["Bruno Latour"],
        "affiliations": ["Sciences Po", "École des Mines de Paris"],
        "topics": ["actor network theory", "science studies", "STS"],
        "known_works": [
            "laboratory life",
            "science in action",
            "we have never been modern",
            "reassembling the social",
        ],
        "group": "extended-15",
    },
    {
        "id": "F25",
        "name": "Karin Knorr-Cetina",
        "search_names": ["Karin Knorr-Cetina", "Karin Knorr Cetina"],
        "affiliations": ["University of Chicago", "University of Konstanz"],
        "topics": ["epistemic cultures", "science studies", "STS"],
        "known_works": [
            "epistemic cultures",
            "the manufacture of knowledge",
        ],
        "group": "extended-15",
    },
    {
        "id": "F26",
        "name": "Thomas Kuhn",
        "search_names": ["Thomas S. Kuhn", "Thomas Kuhn"],
        "affiliations": ["Massachusetts Institute of Technology", "Princeton University"],
        "topics": ["paradigm", "philosophy of science", "scientific revolutions"],
        "known_works": [
            "the structure of scientific revolutions",
            "the essential tension",
        ],
        "group": "extended-15",
    },
    {
        "id": "F27",
        "name": "Paul Feyerabend",
        "search_names": ["Paul Feyerabend", "Paul K. Feyerabend"],
        "affiliations": ["University of California Berkeley"],
        "topics": ["philosophy of science", "epistemological anarchism"],
        "known_works": ["against method", "science in a free society"],
        "group": "extended-15",
    },
    {
        "id": "F28",
        "name": "Stuart Kauffman",
        "search_names": ["Stuart A. Kauffman", "Stuart Kauffman"],
        "affiliations": ["Santa Fe Institute", "University of Pennsylvania"],
        "topics": ["adjacent possible", "complexity", "self-organization"],
        "known_works": [
            "the origins of order",
            "investigations",
            "at home in the universe",
            "autocatalytic sets",
        ],
        "group": "extended-15",
    },
    {
        "id": "F29",
        "name": "James C. Kaufman",
        "search_names": ["James C. Kaufman"],
        "affiliations": ["University of Connecticut", "California State University San Bernardino"],
        "topics": ["creativity", "four c model", "creativity assessment"],
        "known_works": [
            "beyond big and little the four c model of creativity",
            "the cambridge handbook of creativity",
        ],
        "group": "extended-15",
    },
    {
        "id": "F30",
        "name": "Mark Runco",
        "search_names": ["Mark A. Runco", "Mark Runco"],
        "affiliations": ["University of Georgia", "California State University Fullerton"],
        "topics": ["creativity", "divergent thinking", "creativity research"],
        "known_works": [
            "creativity theories and themes research development and practice",
            "standard definition of creativity",
            "creativity research handbook",
        ],
        "group": "extended-15",
    },
]

# Sanity-check IDs are unique
assert len({f["id"] for f in FIGURES}) == len(FIGURES), "duplicate figure ids"
