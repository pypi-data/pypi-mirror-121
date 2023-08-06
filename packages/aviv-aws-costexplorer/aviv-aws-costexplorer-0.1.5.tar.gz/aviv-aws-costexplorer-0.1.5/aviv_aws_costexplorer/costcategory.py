import logging
import typing
import pydantic
import boto3
from . import base

class CostCategoryRuleDefinition(pydantic.BaseModel):
    """
    For type == 'Dimensions':
    Key: typing.Literal["LINKED_ACCOUNT", "INSTANCE_TYPE", "REGION", "SERVICE"]="LINKED_ACCOUNT"
    """
    Key: str="LINKED_ACCOUNT"
    Values: typing.List[str]
    MatchOptions: typing.List[typing.Literal["EQUALS", "ABSENT", "STARTS_WITH", "ENDS_WITH", "CONTAINS", "CASE_SENSITIVE", "CASE_INSENSITIVE"]]=["EQUALS"]

class CostCategoryRule(pydantic.BaseModel):
    Value: str
    Rule: typing.Dict[typing.Literal["Dimensions", "Tags", "CostCategories"], CostCategoryRuleDefinition]
    Type: typing.Literal["REGULAR", "INHERITED_VALUE"]=None
    InheritedValue: dict=None

class CostCategoryRules(pydantic.BaseModel):
    __root__: typing.List[CostCategoryRule]=[]

    def append(self, value) -> None:
        self.__root__.append(value)
        super().__init__(__root__=self.__root__)

    def __getitem__(self, item: int) -> int:
        return self.__root__[item]

    def __setitem__(self, item: int, value) -> None:
        self.__root__[item] = value
        super().__init__(__root__=self.__root__)

    def names(self) -> list:
        return list(r.Value for r in self.__root__)

    def get(self, name) -> CostCategoryRule:
        return next(filter(lambda r: r.Value == name, self.__root__), None)

    def find(self, value) -> CostCategoryRule:
        for rule in self.__root__:
            rk = list(rule.Rule.keys())[0]
            if value in rule.Rule[rk].Values:
                return rule
        return None

class CostCategory(pydantic.BaseModel):
    class Config:
        extra = 'allow'
        validate_assignment = True

    Name: str
    CostCategoryArn: str=None
    EffectiveStart: str=None
    RuleVersion: str='CostCategoryExpression.v1'
    Rules: CostCategoryRules=CostCategoryRules()
    _cli: boto3.Session.client=boto3.client('ce')

    def __init__(self, _cli: boto3.Session.client=None, role_arn: str=None, **data) -> None:
        if role_arn:
            _cli = base.AWSClient.client('ce', role_arn=role_arn)
        super().__init__(**data)
        if _cli:
            self._cli = _cli

    def dict(self, **attr: dict) -> dict:
        attr['exclude_none'] = True
        attr['exclude'] = {"_cli"}
        return super().dict(**attr)

    def get_arn(self):
        refs = self._cli.list_cost_category_definitions()['CostCategoryReferences']
        cat = next(filter(lambda r: r['Name'] == self.Name, refs), None)
        return cat['CostCategoryArn'] if cat else None

    def sync(self):
        # If no CostCategoryArn, first check if we don't have one with the same Name
        if not self.CostCategoryArn:
            self.CostCategoryArn = self.get_arn()
        if self.CostCategoryArn:
            attr = self.dict(include={'CostCategoryArn', 'RuleVersion', 'Rules'})
            return self._cli.update_cost_category_definition(**attr)
        attr = self.dict(include={'Name', 'RuleVersion', 'Rules'})
        return self._cli.create_cost_category_definition(**attr)

    def describe(self):
        definition = self._cli.describe_cost_category_definition(CostCategoryArn=self.CostCategoryArn)['CostCategory']
        super().__init__(_cli=self._cli, **definition)

class CostCategories(pydantic.BaseModel):
    class Config:
        extra = 'allow'

    __root__: typing.List[CostCategory]=[]
    _cli: boto3.Session.client=boto3.client('ce')

    def __init__(self, _cli: boto3.Session.client=None, role_arn: str=None, **data) -> None:
        if role_arn:
            _cli = base.AWSClient.client('ce', role_arn=role_arn)
        # Ensure cli is passed on to CostCategory
        if '__root__' in data and _cli:
            for c in data['__root__']:
                c['_cli'] = _cli
        super().__init__(**data)
        if _cli:
            self._cli = _cli

    def list(self) -> None:
        definitions = self._cli.list_cost_category_definitions()['CostCategoryReferences']
        self.__init__(_cli=self._cli, __root__=definitions)

    def get(self, name) -> CostCategory:
        return next(filter(lambda r: r.Name == name, self.__root__), None)


def diff_CostCategoryRules(cc1: CostCategoryRules, cc2: CostCategoryRules):
    diffs = dict(
        added = list(set(cc1.names()) - set(cc2.names())),
        removed = list(set(cc2.names()) - set(cc1.names())),
        changed = {}
    )
    for rule in list(set(cc1.names()) & set(cc2.names())):
        r1k = list(cc1.get(rule).Rule.keys())[0]
        r2k = list(cc2.get(rule).Rule.keys())[0]
        r1 = cc1.get(rule).Rule[r1k]
        r2 = cc2.get(rule).Rule[r2k]
        if r1k != r2k or set(r1.Values) != set(r2.Values):
            diffs['changed'][rule] = dict(
                added = list(set(r1.Values) - set(r2.Values)),
                removed = list(set(r2.Values) - set(r1.Values))
            )
            if r1k != r2k:
                diffs['changed'][rule]['type'] = f"{r2k} -> {r1k}"

    return diffs
