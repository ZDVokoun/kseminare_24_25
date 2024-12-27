from krolog_parser import parse
from krolog_tools import Fact, Rule, IndexedFact, Connection, is_var, is_value

TEMPLATE_USED = True # True, pokud jsi použil šablonu; False, pokud ne.

Facts = list[Fact]
Rules = list[Rule]
InFacts = list[IndexedFact]
ConnectNone = Connection | None
Solution = dict[str, str]
Solutions = list[Solution] | bool


def equal_fact_question(fact: IndexedFact, question: IndexedFact,
                        connect: Connection) -> ConnectNone:
    """
        Vyhodnotí, zda je fakt sjednotitelný s danou otázkou. Za předpokladu
        rovností v connect.

        Můžeme-li ho sjednotit, sjednotíme a předáme nové propojení.
        Není-li to možné, předáme None.

        Příklady jsou ve vysvětlující doušce pro prolog_template v zadání.
    """
    if fact.get_name() != question.get_name() or fact.get_len() != question.get_len():
        return None

    new_connection = connect.copy()

    for fact_arg, question_arg in zip(fact.get_args(), question.get_args()):
        if not new_connection.add_equal(fact_arg, question_arg):
            return None

    return new_connection


def apply_rule(rule: Rule, question: IndexedFact, connect: Connection)\
    -> tuple[InFacts, ConnectNone]:
    """
        Vyhodnotí, zda je dané pravidlo použitelné pro danou otázku.

        Pokud ano, předá dvojici (seznam faktů-předpokladů,
            aktualizované connect)
        Pokud ne, předá dvojici ([], None)

        Příklady jsou ve vysvětlující doušce pro prolog_template v zadání.
    """
    unified_connection = equal_fact_question(IndexedFact(rule.truth, question.get_index()), question, connect)
    
    if unified_connection is None:
        return [], None

    preconditions = [IndexedFact(fact, question.get_index()) for fact in rule.when]
    return preconditions, unified_connection

def solve_problem(facts: Facts, rules: Rules, questions: InFacts)\
    -> Solutions:
    """
        Funkce, která vyřeší danou sadu otázek, jako výsledek předá buďto:
          bool - pokud otázky neobsahují proměnnou
              True - jedná se o pravdivé tvrzení
              False - nejedná se o pravdivé tvrzení
          seznam možných řešení - jinak
              řešení jsou ulozena ve slovniku: {promenna: hodnota, ...}
              pokud řešení neexistuje, dany seznam bude prazdny

        Příklady jsou ve vysvětlující doušce pro prolog_template v zadání.
    """
    pass


def solve(facts: Facts, rules: Rules, questions: Facts) -> list[Solutions]:
    """
        Předá řešení všech otázek, podle výskytu .all společné, nebo oddělené.
    """
    pass


if __name__ == "__main__":
    file_name = "test.txt"
    f, r, q = parse(file_name)
    # rule = Rule(Fact("matka", ['X', 'Y']), [Fact('zena', ['X']), Fact('rodic', ['X','Y'])])
    # question = IndexedFact(Fact('matka', ['Z', 'Z']), 0)
    # connect = Connection()
    # connect.add_equal('Z0', 'cecil')
    #
    # print(apply_rule(rule, question, connect)[1].classes)

    print(solve_problem(f, r, [IndexedFact(qu, i) for i, qu in enumerate(q)]))

