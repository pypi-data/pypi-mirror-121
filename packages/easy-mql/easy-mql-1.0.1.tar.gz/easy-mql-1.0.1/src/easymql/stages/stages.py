from functools import reduce

from pyparsing import ParseException

from easymql.basics import *
from easymql.core import Forward
from easymql.datatypes.composite import Array
from easymql.datatypes.primary import Number, Boolean, String
from easymql.expressions.others import FieldPath
from easymql.keywords import *
from easymql.stages.parts import *
from easymql.utils import DelimitedList


class AddFields(Grammar):

    grammar = Suppress(ADD + FIELDS) + DelimitedList(Alias, min=1) + SEMICOLON

    @classmethod
    def action(cls, tokens):
        fields_dict = {}
        for t in tokens:
            fields_dict.update(t)
        return {"$addFields": fields_dict}


class BucketBy(Grammar):
    class Default(Grammar):
        grammar = DEFAULT + String

        @classmethod
        def action(cls, tokens):
            return {'default': tokens[-1]}

    class Output(Grammar):
        grammar = PROJECT + DelimitedList(ProjectAccumulator, min=1)

        @classmethod
        def action(cls, tokens):
            return {'output': reduce(lambda x, y: {**x, **y}, tokens[1:])}

    grammar = (
        BUCKET
        + BY
        + Expression
        + BOUNDARIES
        + Array
        + Optional(Default)
        + Optional(Output)
        + SEMICOLON
    )

    @classmethod
    def action(cls, tokens):
        doc = {'groupBy': tokens[2], 'boundaries': tokens[4]}
        for t in tokens[5:]:
            doc.update(t)
        return {'$bucket': doc}


class Count(Grammar):

    grammar = Suppress(COUNT + AS) + CollectionName + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$count": tokens[0]}


class GroupBy(Grammar):

    grammar = (
        GROUP
        + BY
        + Expression
        + Optional(PROJECT + DelimitedList(ProjectAccumulator, min=1))
        + SEMICOLON
    )

    @classmethod
    def action(cls, tokens):
        return {
            '$group': reduce(lambda x, y: {**x, **y}, [{'_id': tokens[2]}] + tokens[4:])
        }


class Limit(Grammar):

    grammar = Suppress(LIMIT) + Number + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$limit": tokens[0]}


class Lookup(Grammar):

    grammar = (
        LOOKUP
        + CollectionName
        + ON
        + Field
        + Literal('=')
        + Field
        + Optional(AS + Field)
        + SEMICOLON
    )

    @classmethod
    def action(cls, tokens):
        return {
            '$lookup': {
                'from': tokens[1],
                'localField': tokens[3],
                'foreignField': tokens[5],
                'as': tokens[-1] if len(tokens) == 8 else f'{tokens[1]}_docs',
            }
        }


class Match(Grammar):

    grammar = Suppress(MATCH) + Expression + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$match": {"$expr": tokens[0]}}


class OutputToDb(Grammar):

    grammar = Suppress(OUTPUT + TO) + DbCollectionPath + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$out": tokens[0]}


class Project(Grammar):
    class NewField(Grammar):
        grammar = Expression + AS + Field

        @classmethod
        def action(cls, tokens):
            return {tokens[-1]: tokens[0]}

    class ExcludeOrInclude(Grammar):
        grammar = Literal('+') + Field | Literal('-') + Field | Field

        @classmethod
        def action(cls, tokens):
            if len(tokens) == 1:
                return {tokens[0]: 1}
            else:
                return {tokens[-1]: 1 if tokens[0] == '+' else 0}

    # order matters
    element = NewField | ExcludeOrInclude
    grammar = Suppress(PROJECT) + DelimitedList(element, min=1) + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {'$project': reduce(lambda x, y: {**x, **y}, tokens)}


class Redact(Grammar):

    grammar = Suppress(REDACT) + Expression + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$redact": tokens[0]}


class ReplaceRoot(Grammar):
    grammar = Suppress(REPLACE + ROOT) + Expression + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$replaceRoot": {"newRoot": tokens[0]}}


class ReplaceWith(Grammar):
    grammar = Suppress(REPLACE + WITH) + Expression + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$replaceWith": tokens[0]}


class Sample(Grammar):

    grammar = Suppress(SAMPLE) + Number + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$sample": tokens[0]}


class Set(Grammar):

    grammar = Suppress(SET) + DelimitedList(Alias, min=1) + SEMICOLON

    @classmethod
    def action(cls, tokens):
        fields_dict = {}
        for t in tokens:
            fields_dict.update(t)
        return {"$set": fields_dict}


class Skip(Grammar):

    grammar = Suppress(SKIP | OFFSET) + Number + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$skip": tokens[0]}


class Sort(Grammar):
    class PairBySort(Grammar):
        grammar = Field + (ASC | DESC)

        @classmethod
        def action(cls, tokens):
            if tokens[1] == "ASC":
                tokens[1] = 1
            elif tokens[1] == 'DESC':
                tokens[1] = -1
            return {tokens[0]: tokens[1]}

    grammar = (
        Suppress(SORT | ORDER)
        + Suppress(BY)
        + DelimitedList(PairBySort, min=1)
        + SEMICOLON
    )

    @classmethod
    def action(cls, tokens):
        fields_dict = {}
        for t in tokens:
            fields_dict.update(t)
        return {"$sort": fields_dict}


class SortByCount(Grammar):

    grammar = Suppress(SORT + BY + COUNT) + Expression + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {"$sortByCount": tokens[0]}


class Unset(Grammar):

    grammar = Suppress(UNSET) + DelimitedList(Field, min=1) + SEMICOLON

    @classmethod
    def action(cls, tokens):
        token = []
        for i in tokens:
            token.append(i)
        return {"$unset": token}


class Unwind(Grammar):
    class ArrayIndex(Grammar):
        grammar = ARRAY + INDEX + AS + Field

        @classmethod
        def action(cls, tokens):
            return 'includeArrayIndex', tokens[-1]

    class PreserverNullEmptyArrays(Grammar):
        grammar = PRESERVE + NULL + EMPTY + ARRAYS + Boolean

        @classmethod
        def action(cls, tokens):
            return 'preserveNullAndEmptyArrays', tokens[-1]

    grammar = (
        UNWIND + FieldPath + (ArrayIndex | PreserverNullEmptyArrays)[0, 2] + SEMICOLON
    )

    @classmethod
    def action(cls, loc, tokens):
        # raise error if 2 options are given but both are the same
        if len(tokens) == 4 and tokens[2][0] == tokens[3][0]:
            if tokens[2][0] == 'includeArrayIndex':
                option = 'ARRAY INDEX AS'
            else:
                option = 'PRESERVE NULL EMPTY ARRAYS'
            raise ParseException('', loc=loc, msg=f"Duplicate option '{option}'")
        return {'$unwind': dict([('path', tokens[1])] + tokens[2:])}


class Merge(Grammar):
    class On(Grammar):
        grammar = ON + DelimitedList(Field, min=1)

        @classmethod
        def action(cls, tokens):
            print(tokens.asList())
            return {'on': tokens[1:]}

    class WhenMatched(Grammar):
        grammar = Suppress(WHEN + MATCHED + THEN) + (
            REPLACE
            | KEEP
            | MERGE
            | FAIL
            | LPAREN
            + (AddFields | Set | Project | Unset | ReplaceRoot | ReplaceWith)[1, ...]
            + RPAREN
        )

        @classmethod
        def action(cls, tokens):
            value = tokens.asList()
            if isinstance(tokens[0], str):
                if tokens[0] == 'KEEP':
                    value = 'keepExisting'
                else:
                    value = tokens[0].lower()
            return {'whenMatched': value}

    class WhenNotMatched(Grammar):
        grammar = Suppress(WHEN + NOT + MATCHED + THEN) + (INSERT | DISCARD | FAIL)

        @classmethod
        def action(cls, tokens):
            return {'whenNotMatched': tokens[0].lower()}

    grammar = (
        MERGE
        + INTO
        + DbCollectionPath
        + Optional(On)
        + Optional(WhenMatched)
        + Optional(WhenNotMatched)
        + SEMICOLON
    )

    @classmethod
    def action(cls, tokens):
        return {
            '$merge': reduce(
                lambda x, y: {**x, **y}, [{'into': tokens[2]}] + tokens[3:]
            )
        }


class Facet(Grammar):
    class NewPipeline(Grammar):
        """This should be updated with the new stages whenever get
        added that are supported in FACET"""

        allowed_stages = Forward()
        allowed_stages.set_name('pipeline')

        grammar = LPAREN + allowed_stages[1, ...] + RPAREN + Suppress(AS) + Field

        @classmethod
        def action(cls, tokens):
            print(tokens)
            return {tokens[-1]: tokens[0:-1]}

    grammar = FACET + DelimitedList(NewPipeline, min=1) + SEMICOLON

    @classmethod
    def action(cls, tokens):
        return {'$facet': reduce(lambda x, y: {**x, **y}, tokens[1:])}


class UnionWith(Grammar):
    """This should be updated with the new stages whenever get
    added that are supported in UNION WITH"""

    allowed_stages = Forward()
    allowed_stages.set_name('pipeline')

    grammar = (
        UNION
        + WITH
        + CollectionName
        + Optional(WITH + PIPELINE + LPAREN + allowed_stages[1, ...] + RPAREN)
        + SEMICOLON
    )

    allowed_stages <<= (
        AddFields
        | BucketBy
        | Count
        | Facet
        | GroupBy
        | Limit
        | Lookup
        | Match
        | Project
        | Redact
        | ReplaceRoot
        | ReplaceWith
        | Sample
        | Set
        | Skip
        | Sort
        | SortByCount
        | grammar
        | Unset
        | Unwind
    )

    @classmethod
    def action(cls, tokens):
        print(tokens)
        doc = {'coll': tokens[2]}
        if len(tokens) > 3:
            doc['pipeline'] = tokens[5:]
        return {'$unionWith': doc}


Facet.NewPipeline.allowed_stages <<= (
    AddFields
    | BucketBy
    | Count
    | GroupBy
    | Limit
    | Lookup
    | Match
    | Project
    | Redact
    | ReplaceRoot
    | ReplaceWith
    | Sample
    | Set
    | Skip
    | Sort
    | SortByCount
    | UnionWith
    | Unset
    | Unwind
)


Stages = (
    AddFields
    | BucketBy
    | Count
    | Facet
    | GroupBy
    | Limit
    | Lookup
    | Match
    | Merge
    | Project
    | OutputToDb
    | Redact
    | ReplaceRoot
    | ReplaceWith
    | Sample
    | Set
    | Skip
    | Sort
    | SortByCount
    | UnionWith
    | Unset
    | Unwind
)
