import re
from pathlib import Path

import logipy.logic.properties
from logipy.monitor.monitored_predicate import MonitoredPredicate, add_predicate_to_monitor
from logipy.graphs.timed_property_graph import *
from logipy.graphs.timestamps import RelativeTimestamp, LesserThanRelativeTimestamp


def import_gherkin_path(root_path=""):
    """Imports the rules from all .gherkin files under root_path."""
    for gherkin_file in Path(root_path).rglob("*.gherkin"):
        if gherkin_file.is_file():
            import_gherkin_file(str(gherkin_file))


def import_gherkin_file(path):
    """Imports the rules of given .gherkin file."""
    if not path.endswith(".gherkin"):
        raise Exception("Can only import .gherkin files: " + path)

    with open(path, "r") as file:
        gherkin = file.read()

    properties = convert_gherkin_to_graphs(gherkin)
    for p in properties:
        logipy.logic.properties.add_global_property(p)


def convert_gherkin_to_graphs(gherkin):
    """Converts given gherkin text to a sequence of property graphs."""
    lines = gherkin.split("\n")
    # Remove comment lines.
    lines = [line for line in lines if not line.startswith("#")]
    # Remove preceding and trailing whitespaces.
    lines = [line.strip() for line in lines]
    return convert_gherkin_lines_to_graphs(lines)


def convert_gherkin_lines_to_graphs(lines):
    """Converts given gherkin lines to a sequence of property graphs."""
    graphs = []
    for rule in (" ".join(lines)).split("SCENARIO:"):
        rule = rule.strip()
        if rule:
            graph = convert_specification_to_graph(rule)
            graph.set_property_textual_representation(rule)
            graphs.append(graph)
    return graphs


def convert_specification_to_graph(formula):
    """Converts a specification formula to a specification graph."""
    given_clause, when_clause, then_clause = get_fundamental_clauses(formula)

    when_property = convert_clause_to_graph(when_clause)
    then_property = convert_clause_to_graph(then_clause)

    final_property = when_property
    if given_clause:
        given_property = convert_clause_to_graph(given_clause)
        given_property.set_timestamp(LesserThanRelativeTimestamp(-1))
        final_property.logical_and(given_property)

    final_property.logical_implication(then_property)

    return final_property


def get_fundamental_clauses(formula):
    """Extracts the fundamental step subformulas out of a specification formula."""
    regex = re.compile(
        r"^(GIVEN (?P<given_clause>.*) )?(WHEN (?P<when_clause>.*) )(THEN (?P<then_clause>.*))")

    matches = regex.match(formula).groupdict()
    given_clause = matches['given_clause']
    when_clause = matches['when_clause']
    then_clause = matches['then_clause']

    if when_clause is None or then_clause is None:
        exc_text = "WHEN and THEN clauses are required in specifications syntax.\n"
        exc_text += "The following specifications is invalid:\n"
        exc_text += formula
        raise Exception(exc_text)

    return given_clause, when_clause, then_clause


def convert_clause_to_graph(clause):
    """Converts a fundamental step clause, to property graph.

    A fundamental step clause, is the text tha follows GIVEN, WHEN, THEN steps.

    Steps are allowed to contain SHOULD modifier.
    """
    subclauses = clause.split(" AND ")
    clause_graph = TimedPropertyGraph()

    for subclause in subclauses:
        # TODO: Support PRINT statement
        if subclause.startswith("PRINT "):
            continue

        # Remove any SHOULD modifier and parse the predicate part.
        starts_with_should = subclause.startswith("SHOULD ")
        if starts_with_should:
            subclause = subclause.lstrip("SHOULD ")

        # Remove any preceding negation and parse the positive predicate.
        is_negated = subclause.startswith("NOT ")
        if is_negated:
            subclause = subclause.lstrip("NOT ")

        subclause_graph = convert_predicate_to_graph(subclause)

        if starts_with_should:
            # SHOULD modifier means that a predicate should already have been TRUE.
            subclause_graph.set_timestamp(LesserThanRelativeTimestamp(-1))
        else:
            # Without SHOULD modifier, a predicate becomes TRUE at current time step.
            subclause_graph.set_timestamp(RelativeTimestamp(0))

        # If original subclause was negated, negate the total graph of the subclause.
        if is_negated:
            subclause_graph.logical_not()

        clause_graph.logical_and(subclause_graph)

    return clause_graph


def convert_predicate_to_graph(predicate):
    """Converts a predicate to a graph representation"""
    # Check if predicate is a defined function.
    monitored_predicate = MonitoredPredicate.find_text_matching_monitored_predicate(predicate)

    if monitored_predicate is None:
        predicate_graph = PredicateGraph(predicate, MonitoredVariable("VAR"))
    else:
        predicate_graph = monitored_predicate.convert_to_graph()
        add_predicate_to_monitor(monitored_predicate)

    return predicate_graph
